#!/usr/bin/env python3
"""
Progress Lock - Atomic progress.json updates with file locking.

Provides safe, atomic updates to progress.json files across all stages
(discovery, prototype, productspecs, solarch, implementation) to prevent
corruption from concurrent updates or interrupted writes.

Usage:
    from progress_lock import ProgressLock

    # Context manager (recommended)
    with ProgressLock('prototype') as progress:
        progress['phases']['qa']['status'] = 'complete'
        progress['phases']['qa']['completed_at'] = '2025-01-03T15:30:00Z'
        # Automatically saved and lock released on exit

    # Direct API
    lock = ProgressLock('discovery')
    lock.acquire()
    try:
        lock.update_phase('analyze', status='in_progress')
        lock.save()
    finally:
        lock.release()

Exit Codes:
    0 - Success
    1 - Lock acquisition failed (timeout or conflict)
    2 - File corruption detected
    3 - Invalid operation
"""

import argparse
import json
import os
import sys
import fcntl
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from contextlib import contextmanager
import shutil


# Configuration
LOCK_TIMEOUT_SECONDS = 30
LOCK_RETRY_INTERVAL = 0.5
STATE_DIR = "_state"


class ProgressLockError(Exception):
    """Base exception for progress lock errors."""
    pass


class LockTimeoutError(ProgressLockError):
    """Raised when lock acquisition times out."""
    pass


class FileCorruptionError(ProgressLockError):
    """Raised when progress file is corrupted."""
    pass


class ProgressLock:
    """
    Thread-safe and process-safe progress file updater.

    Uses file locking (fcntl) to ensure atomic updates across processes.
    Includes rollback capability and corruption detection.
    """

    VALID_STAGES = ['discovery', 'prototype', 'productspecs', 'solarch', 'implementation']

    def __init__(self, stage: str, timeout_seconds: int = LOCK_TIMEOUT_SECONDS):
        """
        Initialize progress lock for a specific stage.

        Args:
            stage: Stage name (discovery, prototype, productspecs, solarch, implementation)
            timeout_seconds: Maximum time to wait for lock acquisition
        """
        if stage not in self.VALID_STAGES:
            raise ValueError(f"Invalid stage '{stage}'. Must be one of: {self.VALID_STAGES}")

        self.stage = stage
        self.timeout_seconds = timeout_seconds
        self.state_dir = Path(STATE_DIR)
        self.state_dir.mkdir(exist_ok=True)

        # Progress file paths
        self.progress_file = self.state_dir / f"{stage}_progress.json"
        self.lock_file = self.state_dir / f".{stage}_progress.lock"
        self.backup_file = self.state_dir / f".{stage}_progress.backup"

        # State
        self.lock_fd = None
        self.progress_data = None
        self.original_data = None

    def __enter__(self):
        """Context manager entry - acquire lock and load progress."""
        self.acquire()
        return self.progress_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - save and release lock."""
        if exc_type is None:
            # No exception - save changes
            self.save()
        else:
            # Exception occurred - rollback
            print(f"⚠️  Exception during update, rolling back: {exc_val}", file=sys.stderr)
            self.rollback()

        self.release()
        return False  # Don't suppress exceptions

    def acquire(self) -> None:
        """
        Acquire exclusive lock on progress file.

        Raises:
            LockTimeoutError: If lock cannot be acquired within timeout
        """
        # Create lock file if it doesn't exist
        self.lock_file.touch(exist_ok=True)

        start_time = time.time()
        while True:
            try:
                # Open lock file
                self.lock_fd = open(self.lock_file, 'r+')

                # Try to acquire exclusive lock (non-blocking)
                fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)

                # Lock acquired - load progress data
                self.progress_data = self._load_progress()
                self.original_data = json.dumps(self.progress_data, indent=2)

                return

            except (IOError, OSError) as e:
                # Lock is held by another process
                if time.time() - start_time > self.timeout_seconds:
                    if self.lock_fd:
                        self.lock_fd.close()
                        self.lock_fd = None
                    raise LockTimeoutError(
                        f"Failed to acquire lock on {self.progress_file} after {self.timeout_seconds}s. "
                        f"Another process may be updating progress."
                    )

                # Wait and retry
                time.sleep(LOCK_RETRY_INTERVAL)

    def release(self) -> None:
        """Release lock on progress file."""
        if self.lock_fd:
            try:
                fcntl.flock(self.lock_fd.fileno(), fcntl.LOCK_UN)
                self.lock_fd.close()
            except Exception as e:
                print(f"⚠️  Error releasing lock: {e}", file=sys.stderr)
            finally:
                self.lock_fd = None

    def _load_progress(self) -> Dict[str, Any]:
        """
        Load progress data from file.

        Returns:
            Progress data dictionary

        Raises:
            FileCorruptionError: If file is corrupted
        """
        if not self.progress_file.exists():
            # Create new progress file with template
            return self._create_template()

        try:
            with open(self.progress_file, 'r') as f:
                data = json.load(f)

            # Validate structure
            if not isinstance(data, dict):
                raise FileCorruptionError(f"{self.progress_file} is not a JSON object")

            if 'checkpoint' not in data or 'phases' not in data:
                raise FileCorruptionError(f"{self.progress_file} missing required fields")

            return data

        except json.JSONDecodeError as e:
            # Try to restore from backup
            if self.backup_file.exists():
                print(f"⚠️  Progress file corrupted, restoring from backup", file=sys.stderr)
                shutil.copy(self.backup_file, self.progress_file)
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            else:
                raise FileCorruptionError(f"Progress file corrupted and no backup available: {e}")

    def _create_template(self) -> Dict[str, Any]:
        """Create template progress structure for new file."""
        return {
            "checkpoint": 0,
            "current_phase": None,
            "started_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "phases": {},
            "validation": {
                "status": "pending",
                "issues": []
            }
        }

    def save(self) -> None:
        """
        Save progress data to file atomically.

        Creates backup before writing to allow rollback on corruption.
        """
        if self.progress_data is None:
            raise ProgressLockError("No progress data loaded. Call acquire() first.")

        # Update timestamp
        self.progress_data['updated_at'] = datetime.now().isoformat()

        # Create backup of current file
        if self.progress_file.exists():
            shutil.copy(self.progress_file, self.backup_file)

        # Write to temporary file first
        temp_file = self.progress_file.with_suffix('.tmp')
        with open(temp_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())

        # Atomic rename
        temp_file.replace(self.progress_file)

    def rollback(self) -> None:
        """Rollback changes - restore from backup or original data."""
        if self.backup_file.exists():
            shutil.copy(self.backup_file, self.progress_file)
            print(f"✓ Rolled back to backup", file=sys.stderr)

    def update_phase(self, phase_name: str, **kwargs) -> None:
        """
        Update a specific phase in progress data.

        Args:
            phase_name: Name of the phase to update
            **kwargs: Fields to update (status, completed_at, outputs, etc.)

        Example:
            lock.update_phase('qa', status='complete', completed_at='2025-01-03T15:30:00Z')
        """
        if self.progress_data is None:
            raise ProgressLockError("No progress data loaded. Call acquire() first.")

        if 'phases' not in self.progress_data:
            self.progress_data['phases'] = {}

        if phase_name not in self.progress_data['phases']:
            self.progress_data['phases'][phase_name] = {}

        # Update fields
        for key, value in kwargs.items():
            self.progress_data['phases'][phase_name][key] = value

    def update_checkpoint(self, checkpoint: int) -> None:
        """Update checkpoint number."""
        if self.progress_data is None:
            raise ProgressLockError("No progress data loaded. Call acquire() first.")

        self.progress_data['checkpoint'] = checkpoint
        self.progress_data['updated_at'] = datetime.now().isoformat()

    def set_current_phase(self, phase_name: str) -> None:
        """Set current phase being executed."""
        if self.progress_data is None:
            raise ProgressLockError("No progress data loaded. Call acquire() first.")

        self.progress_data['current_phase'] = phase_name
        self.progress_data['updated_at'] = datetime.now().isoformat()

    def get_phase(self, phase_name: str) -> Optional[Dict[str, Any]]:
        """Get phase data by name."""
        if self.progress_data is None:
            raise ProgressLockError("No progress data loaded. Call acquire() first.")

        return self.progress_data.get('phases', {}).get(phase_name)


@contextmanager
def safe_progress_update(stage: str):
    """
    Context manager for safe progress updates.

    Usage:
        with safe_progress_update('prototype') as progress:
            progress['checkpoint'] = 12
            progress['phases']['build']['status'] = 'complete'

    Args:
        stage: Stage name (discovery, prototype, productspecs, solarch, implementation)

    Yields:
        Progress data dictionary (automatically saved on exit)
    """
    lock = ProgressLock(stage)
    with lock as progress:
        yield progress


def main():
    """CLI interface for progress lock operations."""
    parser = argparse.ArgumentParser(description='Atomic progress.json updates')
    parser.add_argument('stage', choices=ProgressLock.VALID_STAGES, help='Stage name')
    parser.add_argument('--update-phase', metavar='PHASE', help='Phase name to update')
    parser.add_argument('--status', help='Phase status value')
    parser.add_argument('--checkpoint', type=int, help='Update checkpoint number')
    parser.add_argument('--field', action='append', help='Additional field in format key=value')
    parser.add_argument('--show', action='store_true', help='Show current progress')

    args = parser.parse_args()

    try:
        if args.show:
            # Show current progress
            lock = ProgressLock(args.stage)
            with lock as progress:
                print(json.dumps(progress, indent=2))
            return 0

        if args.checkpoint is not None:
            # Update checkpoint
            lock = ProgressLock(args.stage)
            with lock:
                lock.update_checkpoint(args.checkpoint)
                print(f"✓ Updated {args.stage} checkpoint to {args.checkpoint}")
            return 0

        if args.update_phase:
            # Update phase
            lock = ProgressLock(args.stage)
            fields = {}

            if args.status:
                fields['status'] = args.status

            if args.field:
                for field_str in args.field:
                    key, value = field_str.split('=', 1)
                    # Try to parse as JSON
                    try:
                        fields[key] = json.loads(value)
                    except json.JSONDecodeError:
                        fields[key] = value

            with lock:
                lock.update_phase(args.update_phase, **fields)
                print(f"✓ Updated {args.stage} phase '{args.update_phase}'")

            return 0

        parser.print_help()
        return 0

    except LockTimeoutError as e:
        print(f"❌ Lock timeout: {e}", file=sys.stderr)
        return 1
    except FileCorruptionError as e:
        print(f"❌ File corruption: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 3


if __name__ == '__main__':
    sys.exit(main())
