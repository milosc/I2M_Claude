"""
HTEC Framework Validators Library

Self-validating hooks that enforce quality gates deterministically.
Exit codes:
- 0: Validation passed, continue
- 1: Validation failed, block Claude from stopping
- 2: Critical error/security violation, force Claude to address
"""

__version__ = "1.0.0"
