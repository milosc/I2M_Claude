#!/usr/bin/env python3
"""
Registry Merger - Consolidates outputs from parallel Discovery agents.

This utility merges client facts, pain points, and other registry entries
from multiple agents into unified registries while maintaining traceability.

Usage:
    python registry_merger.py merge <agent_outputs_dir> <target_registry>
    python registry_merger.py deduplicate <registry_file> --threshold 0.8
    python registry_merger.py validate <registry_file>

Version: 1.0.0
"""

import json
import os
import sys
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from difflib import SequenceMatcher
from pathlib import Path


class RegistryMerger:
    """Handles merging of parallel agent outputs into unified registries."""

    # ID namespace allocation by agent
    ID_NAMESPACES = {
        "pdf-analyst": {"CF": (100, 199)},
        "interview-analyst": {"CF": (200, 299), "PP": (1, 20)},
        "design-analyst": {"CF": (300, 399)},
        "data-analyst": {"CF": (400, 499)},
        "persona-generator": {"UT": (1, 99)},
        "jtbd-extractor": {"JTBD": (1, 99)},
    }

    def __init__(self, similarity_threshold: float = 0.8):
        """
        Initialize the merger.

        Args:
            similarity_threshold: Threshold for content similarity (0-1).
                                  Items above this are considered duplicates.
        """
        self.similarity_threshold = similarity_threshold
        self.merge_log: List[Dict[str, Any]] = []

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity ratio between two text strings.

        Args:
            text1: First text to compare
            text2: Second text to compare

        Returns:
            Similarity ratio between 0.0 and 1.0
        """
        if not text1 or not text2:
            return 0.0
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def detect_duplicates(
        self, items: List[Dict[str, Any]], content_key: str = "content"
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Detect and separate duplicate items based on content similarity.

        Args:
            items: List of registry items to check
            content_key: Key in item dict that contains the content to compare

        Returns:
            Tuple of (unique_items, duplicate_items)
        """
        if not items:
            return [], []

        unique_items = []
        duplicate_items = []
        seen_contents: List[str] = []

        for item in items:
            content = item.get(content_key, "")
            is_duplicate = False

            for seen in seen_contents:
                if self.calculate_similarity(content, seen) >= self.similarity_threshold:
                    is_duplicate = True
                    duplicate_items.append(item)
                    self.merge_log.append({
                        "action": "duplicate_detected",
                        "item_id": item.get("id", "unknown"),
                        "similar_to": seen[:50] + "...",
                        "similarity": self.calculate_similarity(content, seen)
                    })
                    break

            if not is_duplicate:
                unique_items.append(item)
                seen_contents.append(content)

        return unique_items, duplicate_items

    def merge_client_facts(
        self, agent_outputs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Merge client facts from multiple agents.

        Args:
            agent_outputs: List of agent output dictionaries containing client_facts

        Returns:
            Merged client facts registry
        """
        all_facts = []
        source_agents = []

        for output in agent_outputs:
            agent_id = output.get("agent_id", "unknown")
            source_agents.append(agent_id)

            facts = output.get("client_facts", output.get("facts", []))
            for fact in facts:
                fact["source_agent"] = agent_id
                all_facts.append(fact)

        # Deduplicate
        unique_facts, duplicates = self.detect_duplicates(all_facts, "content")

        # Sort by ID for consistency
        unique_facts.sort(key=lambda x: x.get("id", "ZZ-999"))

        return {
            "schema_version": "1.0.0",
            "stage": "Discovery",
            "merged_at": datetime.now().isoformat(),
            "merged_from": source_agents,
            "facts": unique_facts,
            "duplicates_removed": len(duplicates),
            "summary": {
                "total_facts": len(unique_facts),
                "by_source_agent": self._count_by_field(unique_facts, "source_agent"),
                "by_type": self._count_by_field(unique_facts, "type"),
                "by_category": self._count_by_field(unique_facts, "category"),
            }
        }

    def merge_pain_points(
        self, agent_outputs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Merge pain points from multiple agents.

        Args:
            agent_outputs: List of agent output dictionaries containing pain_points

        Returns:
            Merged pain point registry
        """
        all_pain_points = []
        source_agents = []

        for output in agent_outputs:
            agent_id = output.get("agent_id", "unknown")
            source_agents.append(agent_id)

            pain_points = output.get("pain_points", output.get("items", []))
            for pp in pain_points:
                pp["source_agent"] = agent_id
                all_pain_points.append(pp)

        # Deduplicate based on title + description
        def get_pp_content(pp):
            return f"{pp.get('title', '')} {pp.get('description', '')}"

        for pp in all_pain_points:
            pp["_merge_content"] = get_pp_content(pp)

        unique_pps, duplicates = self.detect_duplicates(all_pain_points, "_merge_content")

        # Clean up merge key
        for pp in unique_pps:
            del pp["_merge_content"]

        # Sort by ID
        unique_pps.sort(key=lambda x: self._parse_pp_id(x.get("id", "PP-99.99")))

        return {
            "schema_version": "1.0.0",
            "stage": "Discovery",
            "merged_at": datetime.now().isoformat(),
            "merged_from": source_agents,
            "items": unique_pps,
            "duplicates_removed": len(duplicates),
            "summary": {
                "total_pain_points": len(unique_pps),
                "by_severity": self._count_by_field(unique_pps, "severity"),
                "by_category": self._count_by_field(unique_pps, "category"),
            }
        }

    def merge_user_types(
        self, agent_outputs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Merge user types from persona generator agents.

        Args:
            agent_outputs: List of agent output dictionaries containing user_types

        Returns:
            Merged user type registry
        """
        all_user_types = []
        source_agents = []

        for output in agent_outputs:
            agent_id = output.get("agent_id", "unknown")
            source_agents.append(agent_id)

            user_types = output.get("user_types", output.get("items", []))
            for ut in user_types:
                ut["source_agent"] = agent_id
                all_user_types.append(ut)

        # Deduplicate based on role name
        unique_uts, duplicates = self.detect_duplicates(all_user_types, "role")

        # Sort by ID
        unique_uts.sort(key=lambda x: x.get("id", "UT-999"))

        return {
            "schema_version": "1.0.0",
            "stage": "Discovery",
            "merged_at": datetime.now().isoformat(),
            "merged_from": source_agents,
            "items": unique_uts,
            "duplicates_removed": len(duplicates),
            "summary": {
                "total_user_types": len(unique_uts),
                "by_category": self._count_by_field(unique_uts, "category"),
            }
        }

    def merge_jtbd(
        self, agent_outputs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Merge JTBD from extractor agents.

        Args:
            agent_outputs: List of agent output dictionaries containing jtbd

        Returns:
            Merged JTBD registry
        """
        all_jtbd = []
        source_agents = []

        for output in agent_outputs:
            agent_id = output.get("agent_id", "unknown")
            source_agents.append(agent_id)

            jtbd_items = output.get("jtbd", output.get("items", []))
            for jtbd in jtbd_items:
                jtbd["source_agent"] = agent_id
                all_jtbd.append(jtbd)

        # Deduplicate based on job statement
        def get_jtbd_content(jtbd):
            return f"{jtbd.get('when', '')} {jtbd.get('i_want_to', '')} {jtbd.get('so_that', '')}"

        for jtbd in all_jtbd:
            jtbd["_merge_content"] = get_jtbd_content(jtbd)

        unique_jtbd, duplicates = self.detect_duplicates(all_jtbd, "_merge_content")

        # Clean up merge key
        for jtbd in unique_jtbd:
            del jtbd["_merge_content"]

        # Sort by ID
        unique_jtbd.sort(key=lambda x: self._parse_jtbd_id(x.get("id", "JTBD-99.99")))

        return {
            "schema_version": "1.0.0",
            "stage": "Discovery",
            "merged_at": datetime.now().isoformat(),
            "merged_from": source_agents,
            "items": unique_jtbd,
            "duplicates_removed": len(duplicates),
            "summary": {
                "total_jtbd": len(unique_jtbd),
                "by_priority": self._count_by_field(unique_jtbd, "priority"),
                "by_category": self._count_by_field(unique_jtbd, "category"),
            }
        }

    def validate_cross_references(
        self, registries: Dict[str, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate cross-references between merged registries.

        Args:
            registries: Dict mapping registry name to registry content

        Returns:
            Validation report
        """
        issues = []

        # Get all IDs by type
        ids = {
            "CF": set(),
            "PP": set(),
            "UT": set(),
            "JTBD": set(),
        }

        if "client_facts" in registries:
            for fact in registries["client_facts"].get("facts", []):
                ids["CF"].add(fact.get("id"))

        if "pain_points" in registries:
            for pp in registries["pain_points"].get("items", []):
                ids["PP"].add(pp.get("id"))

        if "user_types" in registries:
            for ut in registries["user_types"].get("items", []):
                ids["UT"].add(ut.get("id"))

        if "jtbd" in registries:
            for jtbd in registries["jtbd"].get("items", []):
                ids["JTBD"].add(jtbd.get("id"))

        # Check pain point references to client facts
        if "pain_points" in registries:
            for pp in registries["pain_points"].get("items", []):
                for ref in pp.get("client_fact_refs", []):
                    if ref not in ids["CF"]:
                        issues.append({
                            "type": "broken_reference",
                            "source": pp.get("id"),
                            "target": ref,
                            "registry": "client_facts"
                        })

        # Check JTBD references to pain points
        if "jtbd" in registries:
            for jtbd in registries["jtbd"].get("items", []):
                for ref in jtbd.get("pain_point_refs", []):
                    if ref not in ids["PP"]:
                        issues.append({
                            "type": "broken_reference",
                            "source": jtbd.get("id"),
                            "target": ref,
                            "registry": "pain_points"
                        })

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "counts": {k: len(v) for k, v in ids.items()},
            "validated_at": datetime.now().isoformat()
        }

    def _count_by_field(
        self, items: List[Dict[str, Any]], field: str
    ) -> Dict[str, int]:
        """Count items by a specific field value."""
        counts: Dict[str, int] = {}
        for item in items:
            value = item.get(field, "unknown")
            counts[value] = counts.get(value, 0) + 1
        return counts

    def _parse_pp_id(self, pp_id: str) -> Tuple[int, int]:
        """Parse PP-X.Y into (X, Y) for sorting."""
        match = re.match(r"PP-(\d+)\.(\d+)", pp_id)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return (99, 99)

    def _parse_jtbd_id(self, jtbd_id: str) -> Tuple[int, int]:
        """Parse JTBD-X.Y into (X, Y) for sorting."""
        match = re.match(r"JTBD-(\d+)\.(\d+)", jtbd_id)
        if match:
            return (int(match.group(1)), int(match.group(2)))
        return (99, 99)

    def get_merge_log(self) -> List[Dict[str, Any]]:
        """Get the merge operation log."""
        return self.merge_log


def load_agent_outputs(directory: str) -> List[Dict[str, Any]]:
    """
    Load all agent output JSON files from a directory.

    Args:
        directory: Path to directory containing agent output files

    Returns:
        List of parsed agent output dictionaries
    """
    outputs = []
    dir_path = Path(directory)

    for json_file in dir_path.glob("*.json"):
        try:
            with open(json_file, "r") as f:
                data = json.load(f)
                # Add filename as agent_id if not present
                if "agent_id" not in data:
                    data["agent_id"] = json_file.stem
                outputs.append(data)
        except Exception as e:
            print(f"Warning: Could not load {json_file}: {e}")

    return outputs


def write_registry(registry: Dict[str, Any], output_path: str) -> None:
    """
    Write a registry to a JSON file.

    Args:
        registry: Registry dictionary to write
        output_path: Path to output file
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(registry, f, indent=2)
    print(f"Wrote registry to {output_path}")


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "merge":
        if len(sys.argv) < 4:
            print("Usage: registry_merger.py merge <agent_outputs_dir> <output_dir>")
            sys.exit(1)

        inputs_dir = sys.argv[2]
        output_dir = sys.argv[3]

        merger = RegistryMerger()
        outputs = load_agent_outputs(inputs_dir)

        if not outputs:
            print(f"No agent outputs found in {inputs_dir}")
            sys.exit(1)

        print(f"Loaded {len(outputs)} agent outputs")

        # Merge each registry type
        cf_registry = merger.merge_client_facts(outputs)
        write_registry(cf_registry, f"{output_dir}/client_facts_registry.json")

        pp_registry = merger.merge_pain_points(outputs)
        write_registry(pp_registry, f"{output_dir}/pain_point_registry.json")

        # Validate cross-references
        validation = merger.validate_cross_references({
            "client_facts": cf_registry,
            "pain_points": pp_registry,
        })

        write_registry(validation, f"{output_dir}/merge_validation.json")

        print(f"\nMerge complete:")
        print(f"  - Client facts: {cf_registry['summary']['total_facts']}")
        print(f"  - Pain points: {pp_registry['summary']['total_pain_points']}")
        print(f"  - Cross-reference issues: {len(validation['issues'])}")

    elif command == "deduplicate":
        if len(sys.argv) < 3:
            print("Usage: registry_merger.py deduplicate <registry_file> [--threshold 0.8]")
            sys.exit(1)

        registry_file = sys.argv[2]
        threshold = 0.8

        if "--threshold" in sys.argv:
            idx = sys.argv.index("--threshold")
            threshold = float(sys.argv[idx + 1])

        with open(registry_file, "r") as f:
            registry = json.load(f)

        merger = RegistryMerger(similarity_threshold=threshold)

        # Detect type and deduplicate
        if "facts" in registry:
            unique, dupes = merger.detect_duplicates(registry["facts"], "content")
            registry["facts"] = unique
        elif "items" in registry:
            unique, dupes = merger.detect_duplicates(registry["items"], "title")
            registry["items"] = unique

        output_file = registry_file.replace(".json", "_deduplicated.json")
        write_registry(registry, output_file)
        print(f"Removed {len(dupes)} duplicates (threshold: {threshold})")

    elif command == "validate":
        if len(sys.argv) < 3:
            print("Usage: registry_merger.py validate <traceability_dir>")
            sys.exit(1)

        trace_dir = sys.argv[2]
        registries = {}

        for name in ["client_facts", "pain_points", "user_types", "jtbd"]:
            path = f"{trace_dir}/{name}_registry.json"
            if os.path.exists(path):
                with open(path, "r") as f:
                    registries[name] = json.load(f)

        merger = RegistryMerger()
        validation = merger.validate_cross_references(registries)

        if validation["valid"]:
            print("All cross-references valid")
        else:
            print(f"Found {len(validation['issues'])} issues:")
            for issue in validation["issues"][:10]:
                print(f"  - {issue['source']} -> {issue['target']} (missing in {issue['registry']})")

        sys.exit(0 if validation["valid"] else 1)

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
