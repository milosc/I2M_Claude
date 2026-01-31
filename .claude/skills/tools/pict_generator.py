#!/usr/bin/env python3
"""
PICT Generator - Pairwise Independent Combinatorial Testing

Generates efficient test case combinations using pairwise (2-wise) or
n-wise combinatorial testing methodology without requiring Microsoft PICT.

Usage:
    # Parse model and generate combinations
    python pict_generator.py --model model.pict --output combinations.md

    # With specific coverage strength
    python pict_generator.py --model model.pict --coverage 3 --output results.md

    # Analyze multiple models
    python pict_generator.py --analyze ./models/ --report coverage.md

    # Generate from JSON definition
    python pict_generator.py --json params.json --output combinations.md

Author: Claude Code Accelerators
Version: 1.0.0
"""

import argparse
import json
import itertools
import random
from pathlib import Path
from typing import Dict, List, Tuple, Set, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Parameter:
    """Represents a test parameter with its possible values."""
    name: str
    values: List[str]
    is_negative: Dict[str, bool] = field(default_factory=dict)  # value -> is_negative

    def __post_init__(self):
        # Mark values starting with ~ as negative
        clean_values = []
        for v in self.values:
            if v.startswith('~'):
                clean_v = v[1:]
                self.is_negative[clean_v] = True
                clean_values.append(clean_v)
            else:
                self.is_negative[v] = False
                clean_values.append(v)
        self.values = clean_values


@dataclass
class Constraint:
    """Represents a constraint on parameter combinations."""
    condition_param: str
    condition_value: str
    condition_op: str  # '=' or '<>'
    result_param: str
    result_values: List[str]
    result_op: str  # '=' '<>' 'IN' 'NOT IN'


@dataclass
class PICTModel:
    """Represents a complete PICT model."""
    name: str
    parameters: List[Parameter]
    constraints: List[Constraint]
    sub_models: Dict[Tuple[str, ...], int] = field(default_factory=dict)  # params -> strength
    seeded_cases: List[Dict[str, str]] = field(default_factory=list)


class PICTParser:
    """Parses PICT model files."""

    @staticmethod
    def parse_file(filepath: Path) -> PICTModel:
        """Parse a .pict model file."""
        model = PICTModel(name=filepath.stem, parameters=[], constraints=[])

        with open(filepath, 'r') as f:
            lines = f.readlines()

        current_section = 'parameters'

        for line in lines:
            line = line.strip()

            # Skip comments and empty lines
            if not line or line.startswith('#'):
                # Check for section markers in comments
                if 'Constraints' in line:
                    current_section = 'constraints'
                elif 'Sub-models' in line:
                    current_section = 'submodels'
                elif 'Seeding' in line:
                    current_section = 'seeding'
                continue

            if current_section == 'parameters':
                if ':' in line and 'IF' not in line:
                    PICTParser._parse_parameter(line, model)

            elif current_section == 'constraints':
                if line.startswith('IF'):
                    PICTParser._parse_constraint(line, model)

            elif current_section == 'submodels':
                if line.startswith('{'):
                    PICTParser._parse_submodel(line, model)

            elif current_section == 'seeding':
                if ',' in line and not line.startswith('{'):
                    PICTParser._parse_seeded_case(line, model)

        return model

    @staticmethod
    def _parse_parameter(line: str, model: PICTModel):
        """Parse a parameter definition line."""
        if ':' not in line:
            return

        name, values_str = line.split(':', 1)
        name = name.strip()
        values = [v.strip() for v in values_str.split(',')]
        model.parameters.append(Parameter(name=name, values=values))

    @staticmethod
    def _parse_constraint(line: str, model: PICTModel):
        """Parse a constraint line (simplified parser)."""
        # Example: IF [Param1] = "Value1" THEN [Param2] <> "Value2";
        try:
            parts = line.replace(';', '').split('THEN')
            if len(parts) != 2:
                return

            condition = parts[0].replace('IF', '').strip()
            result = parts[1].strip()

            # Parse condition
            cond_param = condition.split('[')[1].split(']')[0]
            if '=' in condition and '<>' not in condition:
                cond_op = '='
                cond_value = condition.split('=')[1].strip().strip('"').strip("'")
            elif '<>' in condition:
                cond_op = '<>'
                cond_value = condition.split('<>')[1].strip().strip('"').strip("'")
            else:
                return

            # Parse result
            res_param = result.split('[')[1].split(']')[0]
            if 'IN' in result:
                res_op = 'IN' if 'NOT IN' not in result else 'NOT IN'
                values_part = result.split('{')[1].split('}')[0]
                res_values = [v.strip().strip('"').strip("'") for v in values_part.split(',')]
            elif '<>' in result:
                res_op = '<>'
                res_values = [result.split('<>')[1].strip().strip('"').strip("'").strip(';')]
            elif '=' in result:
                res_op = '='
                res_values = [result.split('=')[1].strip().strip('"').strip("'").strip(';')]
            else:
                return

            model.constraints.append(Constraint(
                condition_param=cond_param,
                condition_value=cond_value,
                condition_op=cond_op,
                result_param=res_param,
                result_values=res_values,
                result_op=res_op
            ))
        except (IndexError, ValueError):
            pass  # Skip malformed constraints

    @staticmethod
    def _parse_submodel(line: str, model: PICTModel):
        """Parse a sub-model definition."""
        try:
            params_part = line.split('}')[0].replace('{', '')
            params = tuple(p.strip() for p in params_part.split(','))
            strength = int(line.split('@')[1].strip()) if '@' in line else 2
            model.sub_models[params] = strength
        except (IndexError, ValueError):
            pass

    @staticmethod
    def _parse_seeded_case(line: str, model: PICTModel):
        """Parse a seeded test case."""
        values = [v.strip() for v in line.split(',')]
        if len(values) == len(model.parameters):
            case = {p.name: v for p, v in zip(model.parameters, values)}
            model.seeded_cases.append(case)

    @staticmethod
    def parse_json(filepath: Path) -> PICTModel:
        """Parse a JSON model definition."""
        with open(filepath, 'r') as f:
            data = json.load(f)

        model = PICTModel(
            name=data.get('name', filepath.stem),
            parameters=[],
            constraints=[]
        )

        for param_data in data.get('parameters', []):
            model.parameters.append(Parameter(
                name=param_data['name'],
                values=param_data['values']
            ))

        # Constraints from JSON would need a different format
        # This is a simplified version

        return model


class PairwiseGenerator:
    """Generates pairwise (n-wise) test combinations."""

    def __init__(self, model: PICTModel, coverage_strength: int = 2):
        self.model = model
        self.strength = coverage_strength
        self.test_cases: List[Dict[str, str]] = []
        self.uncovered_pairs: Set[Tuple] = set()

    def generate(self) -> List[Dict[str, str]]:
        """Generate test combinations."""
        if not self.model.parameters:
            return []

        # Start with seeded cases
        self.test_cases = list(self.model.seeded_cases)

        # Generate all n-wise combinations that need coverage
        pairs_to_cover = self._generate_pairs_to_cover()

        # Remove pairs already covered by seeded cases
        for case in self.test_cases:
            pairs_to_cover -= self._get_covered_pairs(case)

        # Greedy algorithm to cover remaining pairs
        while pairs_to_cover:
            best_case = self._find_best_case(pairs_to_cover)
            if best_case is None:
                break

            # Check constraints
            if self._satisfies_constraints(best_case):
                self.test_cases.append(best_case)
                pairs_to_cover -= self._get_covered_pairs(best_case)
            else:
                # Try to fix the case
                fixed_case = self._fix_constraint_violations(best_case)
                if fixed_case and self._satisfies_constraints(fixed_case):
                    self.test_cases.append(fixed_case)
                    pairs_to_cover -= self._get_covered_pairs(fixed_case)
                else:
                    # Skip this pair combination
                    pairs_to_cover -= self._get_covered_pairs(best_case)

        self.uncovered_pairs = pairs_to_cover
        return self.test_cases

    def _generate_pairs_to_cover(self) -> Set[Tuple]:
        """Generate all n-wise parameter combinations to cover."""
        pairs = set()
        param_indices = list(range(len(self.model.parameters)))

        for combo in itertools.combinations(param_indices, self.strength):
            params = [self.model.parameters[i] for i in combo]
            for values in itertools.product(*[p.values for p in params]):
                pair = tuple(zip([p.name for p in params], values))
                pairs.add(pair)

        return pairs

    def _get_covered_pairs(self, case: Dict[str, str]) -> Set[Tuple]:
        """Get all n-wise pairs covered by a test case."""
        pairs = set()
        param_names = list(case.keys())

        for combo in itertools.combinations(param_names, self.strength):
            pair = tuple((name, case[name]) for name in combo)
            pairs.add(pair)

        return pairs

    def _find_best_case(self, pairs_to_cover: Set[Tuple]) -> Optional[Dict[str, str]]:
        """Find a test case that covers the most uncovered pairs."""
        if not pairs_to_cover:
            return None

        # Get a random uncovered pair to start
        target_pair = random.choice(list(pairs_to_cover))

        # Build a case that includes this pair
        case = {}
        for param_name, value in target_pair:
            case[param_name] = value

        # Fill in remaining parameters
        for param in self.model.parameters:
            if param.name not in case:
                # Choose value that covers most additional pairs
                best_value = None
                best_count = -1

                for value in param.values:
                    test_case = {**case, param.name: value}
                    count = len(self._get_covered_pairs(test_case) & pairs_to_cover)
                    if count > best_count:
                        best_count = count
                        best_value = value

                case[param.name] = best_value or param.values[0]

        return case

    def _satisfies_constraints(self, case: Dict[str, str]) -> bool:
        """Check if a test case satisfies all constraints."""
        for constraint in self.model.constraints:
            # Check if condition applies
            if constraint.condition_param not in case:
                continue

            condition_met = False
            if constraint.condition_op == '=':
                condition_met = case[constraint.condition_param] == constraint.condition_value
            elif constraint.condition_op == '<>':
                condition_met = case[constraint.condition_param] != constraint.condition_value

            if not condition_met:
                continue

            # Check result
            if constraint.result_param not in case:
                continue

            result_value = case[constraint.result_param]

            if constraint.result_op == '=':
                if result_value not in constraint.result_values:
                    return False
            elif constraint.result_op == '<>':
                if result_value in constraint.result_values:
                    return False
            elif constraint.result_op == 'IN':
                if result_value not in constraint.result_values:
                    return False
            elif constraint.result_op == 'NOT IN':
                if result_value in constraint.result_values:
                    return False

        return True

    def _fix_constraint_violations(self, case: Dict[str, str]) -> Optional[Dict[str, str]]:
        """Try to fix constraint violations in a test case."""
        fixed = dict(case)

        for constraint in self.model.constraints:
            if constraint.condition_param not in fixed:
                continue

            condition_met = False
            if constraint.condition_op == '=':
                condition_met = fixed[constraint.condition_param] == constraint.condition_value
            elif constraint.condition_op == '<>':
                condition_met = fixed[constraint.condition_param] != constraint.condition_value

            if not condition_met:
                continue

            # Need to fix result
            if constraint.result_param not in fixed:
                continue

            result_value = fixed[constraint.result_param]
            param = next((p for p in self.model.parameters if p.name == constraint.result_param), None)
            if not param:
                continue

            if constraint.result_op == '=' and result_value not in constraint.result_values:
                # Use first allowed value
                fixed[constraint.result_param] = constraint.result_values[0]
            elif constraint.result_op == '<>' and result_value in constraint.result_values:
                # Use first value not in forbidden list
                for v in param.values:
                    if v not in constraint.result_values:
                        fixed[constraint.result_param] = v
                        break
            elif constraint.result_op == 'IN' and result_value not in constraint.result_values:
                fixed[constraint.result_param] = constraint.result_values[0]
            elif constraint.result_op == 'NOT IN' and result_value in constraint.result_values:
                for v in param.values:
                    if v not in constraint.result_values:
                        fixed[constraint.result_param] = v
                        break

        return fixed if self._satisfies_constraints(fixed) else None

    def get_coverage_stats(self) -> Dict[str, Any]:
        """Calculate coverage statistics."""
        total_pairs = len(self._generate_pairs_to_cover())
        covered_pairs = set()
        for case in self.test_cases:
            covered_pairs |= self._get_covered_pairs(case)

        covered_count = len(covered_pairs)

        # Calculate exhaustive count
        exhaustive = 1
        for param in self.model.parameters:
            exhaustive *= len(param.values)

        return {
            'total_pairs': total_pairs,
            'covered_pairs': covered_count,
            'coverage_percentage': (covered_count / total_pairs * 100) if total_pairs > 0 else 100,
            'test_count': len(self.test_cases),
            'exhaustive_count': exhaustive,
            'reduction_percentage': ((exhaustive - len(self.test_cases)) / exhaustive * 100) if exhaustive > 0 else 0,
            'uncovered_pairs': list(self.uncovered_pairs)[:10]  # First 10 uncovered
        }


class ReportGenerator:
    """Generates coverage reports in Markdown format."""

    @staticmethod
    def generate_report(
        model: PICTModel,
        test_cases: List[Dict[str, str]],
        stats: Dict[str, Any],
        output_path: Path
    ):
        """Generate a Markdown report."""
        report = []
        report.append(f"# PICT Test Combinations: {model.name}")
        report.append(f"\n*Generated: {datetime.now().isoformat()}*\n")

        # Summary
        report.append("## Summary\n")
        report.append("| Metric | Value |")
        report.append("|--------|-------|")
        report.append(f"| Parameters | {len(model.parameters)} |")
        report.append(f"| Total Values | {sum(len(p.values) for p in model.parameters)} |")
        report.append(f"| Exhaustive Count | {stats['exhaustive_count']:,} |")
        report.append(f"| PICT Test Count | {stats['test_count']} |")
        report.append(f"| Reduction | {stats['reduction_percentage']:.1f}% |")
        report.append(f"| Pair Coverage | {stats['coverage_percentage']:.1f}% |")

        # Parameters
        report.append("\n## Parameters\n")
        report.append("| Parameter | Values | Count |")
        report.append("|-----------|--------|-------|")
        for param in model.parameters:
            values_str = ', '.join(param.values[:5])
            if len(param.values) > 5:
                values_str += f', ... (+{len(param.values) - 5} more)'
            report.append(f"| {param.name} | {values_str} | {len(param.values)} |")

        # Constraints
        if model.constraints:
            report.append("\n## Constraints\n")
            report.append("```")
            for c in model.constraints:
                report.append(
                    f"IF [{c.condition_param}] {c.condition_op} \"{c.condition_value}\" "
                    f"THEN [{c.result_param}] {c.result_op} {c.result_values}"
                )
            report.append("```")

        # Test Cases
        report.append("\n## Generated Test Cases\n")

        if test_cases:
            # Header
            headers = [p.name for p in model.parameters]
            report.append("| TC | " + " | ".join(headers) + " |")
            report.append("|" + "|".join(["---"] * (len(headers) + 1)) + "|")

            # Rows
            for i, case in enumerate(test_cases, 1):
                values = [case.get(h, '-') for h in headers]
                report.append(f"| {i} | " + " | ".join(values) + " |")

        # Uncovered pairs
        if stats.get('uncovered_pairs'):
            report.append("\n## Uncovered Pairs\n")
            report.append("The following pairs could not be covered due to constraints:\n")
            for pair in stats['uncovered_pairs']:
                report.append(f"- {pair}")

        # Write report
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write('\n'.join(report))

        print(f"Report generated: {output_path}")

    @staticmethod
    def generate_json_output(
        test_cases: List[Dict[str, str]],
        stats: Dict[str, Any],
        output_path: Path
    ):
        """Generate JSON output."""
        output = {
            'generated': datetime.now().isoformat(),
            'statistics': stats,
            'test_cases': test_cases
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"JSON output: {output_path}")


def analyze_directory(dir_path: Path, report_path: Path):
    """Analyze all PICT models in a directory."""
    models = list(dir_path.glob('*.pict'))

    if not models:
        print(f"No .pict files found in {dir_path}")
        return

    report = []
    report.append("# PICT Coverage Analysis Report")
    report.append(f"\n*Generated: {datetime.now().isoformat()}*\n")
    report.append(f"*Directory: {dir_path}*\n")

    total_tests = 0
    total_exhaustive = 0

    report.append("## Summary\n")
    report.append("| Model | Parameters | Exhaustive | PICT | Reduction | Coverage |")
    report.append("|-------|------------|------------|------|-----------|----------|")

    for model_path in models:
        model = PICTParser.parse_file(model_path)
        generator = PairwiseGenerator(model)
        test_cases = generator.generate()
        stats = generator.get_coverage_stats()

        total_tests += stats['test_count']
        total_exhaustive += stats['exhaustive_count']

        report.append(
            f"| {model.name} | {len(model.parameters)} | "
            f"{stats['exhaustive_count']:,} | {stats['test_count']} | "
            f"{stats['reduction_percentage']:.1f}% | {stats['coverage_percentage']:.1f}% |"
        )

    report.append("")
    report.append(f"**Total Tests**: {total_tests}")
    report.append(f"**Total Exhaustive**: {total_exhaustive:,}")
    if total_exhaustive > 0:
        report.append(f"**Overall Reduction**: {((total_exhaustive - total_tests) / total_exhaustive * 100):.1f}%")

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))

    print(f"Analysis report: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description='PICT Generator - Pairwise Independent Combinatorial Testing'
    )
    parser.add_argument('--model', type=Path, help='Path to .pict model file')
    parser.add_argument('--json', type=Path, help='Path to JSON model file')
    parser.add_argument('--output', type=Path, help='Output path for results')
    parser.add_argument('--coverage', type=int, default=2, help='Coverage strength (2=pairwise)')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown')
    parser.add_argument('--analyze', type=Path, help='Analyze all models in directory')
    parser.add_argument('--report', type=Path, help='Path for analysis report')

    args = parser.parse_args()

    if args.analyze:
        if not args.report:
            args.report = args.analyze / 'coverage-report.md'
        analyze_directory(args.analyze, args.report)
        return

    if args.model:
        model = PICTParser.parse_file(args.model)
    elif args.json:
        model = PICTParser.parse_json(args.json)
    else:
        parser.print_help()
        return

    generator = PairwiseGenerator(model, coverage_strength=args.coverage)
    test_cases = generator.generate()
    stats = generator.get_coverage_stats()

    if not args.output:
        args.output = Path(f'{model.name}-combinations.md')

    if args.format == 'json':
        ReportGenerator.generate_json_output(test_cases, stats, args.output)
    else:
        ReportGenerator.generate_report(model, test_cases, stats, args.output)

    print(f"\nGenerated {len(test_cases)} test cases with {stats['coverage_percentage']:.1f}% pair coverage")
    print(f"Reduction: {stats['reduction_percentage']:.1f}% vs exhaustive ({stats['exhaustive_count']:,} cases)")


if __name__ == '__main__':
    main()
