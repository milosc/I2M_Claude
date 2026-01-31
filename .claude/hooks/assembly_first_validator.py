#!/usr/bin/env python3
"""
Assembly-First Validator - Component Library Compliance

Validates that prototype React components follow Assembly-First principles:
- No raw HTML interactive elements
- Component library imports present
- No manual ARIA attributes (except approved cases)
- Tailwind theme tokens usage

Usage:
    python3 assembly_first_validator.py --file <path>
    python3 assembly_first_validator.py --dir <path>
    python3 assembly_first_validator.py --list-violations <path>
    python3 assembly_first_validator.py --validate-prototype <prototype_dir>

Exit Codes:
    0 - All validations passed
    1 - Warnings only (non-blocking)
    2 - Critical violations found (blocking)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ValidationResult:
    """Represents a validation result."""

    def __init__(self, severity: str, message: str, line: Optional[int] = None, suggestion: Optional[str] = None,
                 code_context: Optional[str] = None, file_path: Optional[str] = None):
        self.severity = severity  # CRITICAL, HIGH, MEDIUM, LOW
        self.message = message
        self.line = line
        self.suggestion = suggestion
        self.code_context = code_context  # Code snippet showing context
        self.file_path = file_path  # File where violation occurred

    def to_dict(self) -> dict:
        return {
            'severity': self.severity,
            'message': self.message,
            'line': self.line,
            'suggestion': self.suggestion,
            'code_context': self.code_context,
            'file_path': self.file_path
        }


class AssemblyFirstValidator:
    """Validates Assembly-First compliance for React components."""

    # Forbidden raw HTML elements
    FORBIDDEN_ELEMENTS = [
        '<button', '<input', '<select', '<textarea',
        '<a href', 'role="button"', 'role="textbox"',
        'role="combobox"', 'role="listbox"', 'role="radio"',
        'role="checkbox"', 'role="tab"', 'role="dialog"'
    ]

    # Component library import patterns
    VALID_IMPORT_PATTERNS = [
        r"from\s+['\"]@/component-library['\"]",            # Absolute alias
        r"from\s+['\"]@/components['\"]",                   # Absolute alias (alt)
        r"from\s+['\"]\.\./component-library['\"]",        # Relative path (FIX: Phase 3 false positives)
        r"import\s+\{[^}]+\}\s+from\s+['\"]@/component-library['\"]",           # Absolute alias with named imports
        r"import\s+\{[^}]+\}\s+from\s+['\"]\.\./component-library['\"]",       # Relative path with named imports
    ]

    # Manual ARIA attributes (should be handled by components)
    MANUAL_ARIA_ATTRIBUTES = [
        'aria-label=', 'aria-labelledby=', 'aria-describedby=',
        'aria-expanded=', 'aria-controls=', 'aria-pressed=',
        'aria-checked=', 'aria-selected=', 'aria-hidden=',
        'aria-live=', 'aria-atomic=', 'aria-relevant='
    ]

    # Arbitrary color values (should use theme tokens)
    ARBITRARY_VALUES = [
        r'bg-\[#', r'text-\[#', r'border-\[#',
        r'bg-gray-\d', r'text-gray-\d', r'border-gray-\d',
        r'bg-blue-\d', r'text-blue-\d', r'border-blue-\d'
    ]

    # Theme token recommendations
    THEME_TOKEN_RECOMMENDATIONS = {
        'bg-[#': 'bg-canvas, bg-surface-1, bg-surface-2, bg-accent-default',
        'text-[#': 'text-primary, text-secondary, text-accent, text-link',
        'border-[#': 'border-default, border-subtle, border-emphasis',
        'bg-gray-': 'bg-surface-1, bg-surface-2, bg-canvas',
        'text-gray-': 'text-primary, text-secondary, text-tertiary',
        'bg-blue-': 'bg-accent-default, bg-accent-hover, bg-accent-active',
        'text-blue-': 'text-accent, text-link'
    }

    # Component replacements
    COMPONENT_REPLACEMENTS = {
        '<button': 'Button',
        '<input': 'TextField, Input, SearchField',
        '<select': 'Select, ComboBox',
        '<textarea': 'TextArea',
        '<a href': 'Link',
        'role="button"': 'Button',
        'role="textbox"': 'TextField',
        'role="combobox"': 'ComboBox',
        'role="listbox"': 'ListBox',
        'role="radio"': 'RadioGroup',
        'role="checkbox"': 'Checkbox',
        'role="tab"': 'Tabs',
        'role="dialog"': 'Dialog, Modal'
    }

    def __init__(self):
        self.results: List[ValidationResult] = []

    def _get_code_context(self, content: str, line_num: int, context_lines: int = 2) -> str:
        """
        Extract code context around a specific line with syntax highlighting.

        Args:
            content: Full file content
            line_num: Line number where violation occurred (1-indexed)
            context_lines: Number of lines to show before and after (default: 2)

        Returns:
            Formatted code snippet with line numbers and marker
        """
        lines = content.split('\n')
        start_line = max(0, line_num - 1 - context_lines)
        end_line = min(len(lines), line_num + context_lines)

        context = []
        for i in range(start_line, end_line):
            line_number = i + 1
            line_content = lines[i]

            # Add line with number
            context.append(f"   {line_number:3d} │ {line_content}")

            # Add marker line if this is the violation line
            if line_number == line_num:
                # Find the position of the violation in the line
                # Add marker pointing to it
                indent = len(line_content) - len(line_content.lstrip())
                marker = ' ' * (indent + 8) + '^' * min(7, len(line_content.strip()))
                context.append(f"       │ {marker}")

        return '\n'.join(context)

    def validate_file(self, file_path: Path) -> Tuple[bool, List[ValidationResult]]:
        """
        Validate a single React component file.

        Returns:
            (is_valid, results) tuple where is_valid is True if no critical violations
        """
        self.results = []

        if not file_path.exists():
            self.results.append(ValidationResult(
                'CRITICAL',
                f'File not found: {file_path}'
            ))
            return False, self.results

        if not str(file_path).endswith(('.tsx', '.jsx')):
            # Not a React component file, skip validation
            return True, []

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self.results.append(ValidationResult(
                'CRITICAL',
                f'Failed to read file: {e}'
            ))
            return False, self.results

        # Run all validation checks
        self._check_forbidden_elements(content, file_path)
        self._check_component_imports(content, file_path)
        self._check_manual_aria(content, file_path)
        self._check_theme_tokens(content, file_path)

        # Determine if validation passed (no CRITICAL violations)
        has_critical = any(r.severity == 'CRITICAL' for r in self.results)

        return not has_critical, self.results

    def _check_forbidden_elements(self, content: str, file_path: Path):
        """Check for raw HTML interactive elements."""
        for element in self.FORBIDDEN_ELEMENTS:
            if element in content:
                # Find line number
                lines = content.split('\n')
                line_num = next((i + 1 for i, line in enumerate(lines) if element in line), None)

                replacement = self.COMPONENT_REPLACEMENTS.get(element, 'component library')

                # Generate code context
                code_context = self._get_code_context(content, line_num) if line_num else None

                self.results.append(ValidationResult(
                    'CRITICAL',
                    f'Raw HTML element detected: {element}',
                    line=line_num,
                    suggestion=f'Replace with {replacement} from @/component-library',
                    code_context=code_context,
                    file_path=str(file_path.name)
                ))

    def _check_component_imports(self, content: str, file_path: Path):
        """Check that component library imports are present."""
        # Skip if file doesn't export a component
        if 'export function' not in content and 'export const' not in content:
            return

        # Skip if it's just a type/interface file
        if 'export type' in content or 'export interface' in content:
            return

        # Check for valid import patterns
        has_import = any(
            re.search(pattern, content)
            for pattern in self.VALID_IMPORT_PATTERNS
        )

        if not has_import:
            # Only flag if file uses JSX (has < and >)
            if '<' in content and '>' in content:
                # Show top of file (lines 1-5) as context for where imports should be added
                lines = content.split('\n')
                context_lines = []
                for i in range(min(5, len(lines))):
                    context_lines.append(f"   {i+1:3d} │ {lines[i]}")
                context_lines.append(f"       │ ^^^ Add imports here")
                code_context = '\n'.join(context_lines)

                self.results.append(ValidationResult(
                    'CRITICAL',
                    'No component library imports detected',
                    line=1,
                    suggestion='Add: import { Button, TextField, ... } from \'@/component-library\'',
                    code_context=code_context,
                    file_path=str(file_path.name)
                ))

    def _check_manual_aria(self, content: str, file_path: Path):
        """Check for manual ARIA attributes."""
        for attr in self.MANUAL_ARIA_ATTRIBUTES:
            if attr in content:
                # Exception: aria-label on icon-only buttons
                if attr == 'aria-label=' and '<Button' in content and 'Icon' in content:
                    continue

                # Exception: aria-label on custom components for accessibility
                if attr == 'aria-label=' and any(x in content for x in ['aria-label="', "aria-label='"]):
                    # Check if it's on a component library component (acceptable) or raw HTML (not acceptable)
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if attr in line:
                            # If line has component library import or uppercase component, it's acceptable
                            if re.search(r'<[A-Z]\w+', line):
                                continue

                            line_num = i + 1
                            code_context = self._get_code_context(content, line_num) if line_num else None

                            self.results.append(ValidationResult(
                                'HIGH',
                                f'Manual ARIA attribute: {attr}',
                                line=line_num,
                                suggestion='React Aria components handle ARIA automatically. Remove unless icon-only button.',
                                code_context=code_context,
                                file_path=str(file_path.name)
                            ))
                            break
                else:
                    lines = content.split('\n')
                    line_num = next((i + 1 for i, line in enumerate(lines) if attr in line), None)
                    code_context = self._get_code_context(content, line_num) if line_num else None

                    self.results.append(ValidationResult(
                        'HIGH',
                        f'Manual ARIA attribute: {attr}',
                        line=line_num,
                        suggestion='React Aria components handle ARIA automatically',
                        code_context=code_context,
                        file_path=str(file_path.name)
                    ))

    def _check_theme_tokens(self, content: str, file_path: Path):
        """Check for arbitrary values instead of theme tokens."""
        for pattern in self.ARBITRARY_VALUES:
            matches = re.finditer(pattern, content)
            for match in matches:
                # Get line number
                line_num = content[:match.start()].count('\n') + 1

                # Get recommendation
                pattern_key = pattern.replace(r'\d', '').replace(r'\[', '[').strip()
                recommendation = self.THEME_TOKEN_RECOMMENDATIONS.get(pattern_key, 'Use theme tokens')

                # Generate code context
                code_context = self._get_code_context(content, line_num) if line_num else None

                self.results.append(ValidationResult(
                    'MEDIUM',
                    f'Arbitrary value instead of theme token: {match.group()}',
                    line=line_num,
                    suggestion=f'Use: {recommendation}',
                    code_context=code_context,
                    file_path=str(file_path.name)
                ))

    def generate_fix(self, violation: ValidationResult, file_content: str) -> Optional[str]:
        """
        Generate a corrected code snippet for the violation.

        Args:
            violation: The validation result with violation details
            file_content: Full file content

        Returns:
            Corrected code snippet or None if auto-fix not possible
        """
        # Only auto-fix CRITICAL violations (raw HTML elements)
        if violation.severity != 'CRITICAL':
            return None

        if not violation.line or not file_content:
            return None

        lines = file_content.split('\n')
        if violation.line > len(lines):
            return None

        original_line = lines[violation.line - 1]

        # Detect element type and generate fix
        if '<button' in original_line:
            return self._fix_button_element(original_line)
        elif '<input' in original_line:
            return self._fix_input_element(original_line)
        elif '<select' in original_line:
            return self._fix_select_element(original_line)
        elif '<textarea' in original_line:
            return self._fix_textarea_element(original_line)
        elif '<a href' in original_line:
            return self._fix_anchor_element(original_line)

        return None

    def _fix_button_element(self, line: str) -> str:
        """Generate Button component replacement for <button> element."""
        import re

        # Extract onClick handler
        onclick_match = re.search(r'onClick=\{([^}]+)\}', line)
        onclick = onclick_match.group(1) if onclick_match else None

        # Extract disabled attribute
        disabled = 'isDisabled' in line or 'disabled' in line

        # Extract type attribute
        type_match = re.search(r'type=["\']([^"\']+)["\']', line)
        button_type = type_match.group(1) if type_match else None

        # Extract button text content
        text_match = re.search(r'>([^<]+)</button>', line)
        text = text_match.group(1) if text_match else 'Button'

        # Build replacement
        props = []
        if onclick:
            props.append(f'onPress={{{onclick}}}')
        if disabled:
            props.append('isDisabled')
        if button_type:
            props.append(f'type="{button_type}"')

        props_str = ' ' + ' '.join(props) if props else ''
        indent = len(line) - len(line.lstrip())

        return f"{' ' * indent}<Button{props_str}>{text}</Button>"

    def _fix_input_element(self, line: str) -> str:
        """Generate TextField/Input component replacement for <input> element."""
        import re

        # Extract type attribute
        type_match = re.search(r'type=["\']([^"\']+)["\']', line)
        input_type = type_match.group(1) if type_match else 'text'

        # Extract value binding
        value_match = re.search(r'value=\{([^}]+)\}', line)
        value = value_match.group(1) if value_match else None

        # Extract onChange handler
        onchange_match = re.search(r'onChange=\{([^}]+)\}', line)
        onchange = onchange_match.group(1) if onchange_match else None

        # Extract placeholder
        placeholder_match = re.search(r'placeholder=["\']([^"\']+)["\']', line)
        placeholder = placeholder_match.group(1) if placeholder_match else None

        # Build replacement
        props = []
        if input_type and input_type != 'text':
            props.append(f'type="{input_type}"')
        if value:
            props.append(f'value={{{value}}}')
        if onchange:
            props.append(f'onChange={{{onchange}}}')
        if placeholder:
            props.append(f'placeholder="{placeholder}"')

        props_str = ' ' + ' '.join(props) if props else ''
        indent = len(line) - len(line.lstrip())

        # Use TextField for text/email/password/search, Input for others
        if input_type in ['text', 'email', 'password', 'search']:
            return f"{' ' * indent}<TextField{props_str} />"
        else:
            return f"{' ' * indent}<Input{props_str} />"

    def _fix_select_element(self, line: str) -> str:
        """Generate Select component replacement for <select> element."""
        import re

        # Extract value binding
        value_match = re.search(r'value=\{([^}]+)\}', line)
        value = value_match.group(1) if value_match else None

        # Extract onChange handler
        onchange_match = re.search(r'onChange=\{([^}]+)\}', line)
        onchange = onchange_match.group(1) if onchange_match else None

        # Build replacement
        props = []
        if value:
            props.append(f'selectedKey={{{value}}}')
        if onchange:
            props.append(f'onSelectionChange={{{onchange}}}')

        props_str = ' ' + ' '.join(props) if props else ''
        indent = len(line) - len(line.lstrip())

        return f"{' ' * indent}<Select{props_str}>\n{' ' * (indent + 2)}{{/* Add <Item> elements here */}}\n{' ' * indent}</Select>"

    def _fix_textarea_element(self, line: str) -> str:
        """Generate TextArea component replacement for <textarea> element."""
        import re

        # Extract value binding
        value_match = re.search(r'value=\{([^}]+)\}', line)
        value = value_match.group(1) if value_match else None

        # Extract onChange handler
        onchange_match = re.search(r'onChange=\{([^}]+)\}', line)
        onchange = onchange_match.group(1) if onchange_match else None

        # Extract placeholder
        placeholder_match = re.search(r'placeholder=["\']([^"\']+)["\']', line)
        placeholder = placeholder_match.group(1) if placeholder_match else None

        # Build replacement
        props = []
        if value:
            props.append(f'value={{{value}}}')
        if onchange:
            props.append(f'onChange={{{onchange}}}')
        if placeholder:
            props.append(f'placeholder="{placeholder}"')

        props_str = ' ' + ' '.join(props) if props else ''
        indent = len(line) - len(line.lstrip())

        return f"{' ' * indent}<TextArea{props_str} />"

    def _fix_anchor_element(self, line: str) -> str:
        """Generate Link component replacement for <a href> element."""
        import re

        # Extract href attribute
        href_match = re.search(r'href=["\']([^"\']+)["\']', line)
        href = href_match.group(1) if href_match else '#'

        # Extract link text content
        text_match = re.search(r'>([^<]+)</a>', line)
        text = text_match.group(1) if text_match else 'Link'

        # Build replacement
        indent = len(line) - len(line.lstrip())

        return f"{' ' * indent}<Link href=\"{href}\">{text}</Link>"

    def validate_directory(self, dir_path: Path, recursive: bool = True) -> Dict[str, Tuple[bool, List[ValidationResult]]]:
        """
        Validate all React component files in a directory.

        Returns:
            Dictionary mapping file paths to (is_valid, results) tuples
        """
        results = {}

        pattern = '**/*.tsx' if recursive else '*.tsx'

        for file_path in dir_path.glob(pattern):
            # Skip node_modules, dist, build
            if any(part in file_path.parts for part in ['node_modules', 'dist', 'build', '.next']):
                continue

            is_valid, file_results = self.validate_file(file_path)
            if file_results:  # Only include files with violations
                results[str(file_path.relative_to(dir_path))] = (is_valid, file_results)

        return results


def _detect_required_imports(fixed_code: str) -> List[str]:
    """
    Detect which component library imports are required based on the fixed code.

    Args:
        fixed_code: The suggested fix code snippet

    Returns:
        List of component names that need to be imported
    """
    import re

    # Common component library elements
    components = [
        'Button', 'TextField', 'Input', 'Select', 'TextArea', 'Link',
        'Checkbox', 'RadioGroup', 'Switch', 'ComboBox', 'Autocomplete',
        'NumberField', 'DatePicker', 'DateField', 'TimeField',
        'Table', 'TableHeader', 'TableBody', 'Column', 'Row', 'Cell',
        'ListBox', 'GridList', 'Menu', 'MenuItem', 'MenuTrigger',
        'Tabs', 'TabList', 'TabPanel', 'Breadcrumbs',
        'Dialog', 'Modal', 'Tooltip', 'Popover',
        'ProgressBar', 'Badge', 'Meter',
        'Form', 'Label', 'Item'
    ]

    required = []
    for component in components:
        # Look for component usage: <Component or </Component
        pattern = rf'</?{component}[\s>]'
        if re.search(pattern, fixed_code):
            required.append(component)

    return required


def print_validation_report(results: Dict[str, Tuple[bool, List[ValidationResult]]],
                           verbose: bool = False,
                           suggest_fixes: bool = False,
                           validator: Optional['AssemblyFirstValidator'] = None,
                           file_contents: Optional[Dict[str, str]] = None):
    """
    Print a formatted validation report.

    Args:
        results: Validation results by file path
        verbose: Show warnings in addition to critical violations
        suggest_fixes: Generate and display suggested fixes (Phase 4 enhancement)
        validator: Validator instance for generating fixes
        file_contents: Dict of file_path -> content for fix generation
    """
    total_files = len(results)
    files_with_critical = sum(1 for is_valid, _ in results.values() if not is_valid)
    files_with_warnings = sum(1 for is_valid, res in results.values() if is_valid and any(r.severity in ['HIGH', 'MEDIUM'] for r in res))

    print("\n" + "═" * 70)
    print("ASSEMBLY-FIRST VALIDATION REPORT")
    print("═" * 70)
    print(f"\nFiles Validated: {total_files}")
    print(f"Critical Violations: {files_with_critical}")
    print(f"Warnings: {files_with_warnings}")

    if files_with_critical == 0:
        print("\n✅ VALIDATION PASSED - All files comply with Assembly-First principles")
    else:
        print("\n❌ VALIDATION FAILED - Critical violations found")

    print("\n" + "─" * 70)

    # Group results by severity
    critical_files = []
    warning_files = []

    for file_path, (is_valid, file_results) in sorted(results.items()):
        if not is_valid:
            critical_files.append((file_path, file_results))
        elif any(r.severity in ['HIGH', 'MEDIUM'] for r in file_results):
            warning_files.append((file_path, file_results))

    # Print critical violations
    if critical_files:
        print("\n🚫 CRITICAL VIOLATIONS (BLOCKING):\n")
        for file_path, file_results in critical_files:
            print(f"  📄 {file_path}")
            for result in file_results:
                if result.severity == 'CRITICAL':
                    line_info = f" (line {result.line})" if result.line else ""
                    print(f"     ❌ {result.message}{line_info}")

                    # Show code context if available
                    if result.code_context:
                        print(f"\n     📄 Context ({result.file_path}):")
                        for line in result.code_context.split('\n'):
                            print(f"     {line}")
                        print()

                    if result.suggestion:
                        print(f"        💡 {result.suggestion}")

                    # Phase 4 Enhancement: Show suggested fix
                    if suggest_fixes and validator and file_contents:
                        content = file_contents.get(file_path, '')
                        if content:
                            suggested_fix = validator.generate_fix(result, content)
                            if suggested_fix:
                                print(f"\n     🔧 SUGGESTED FIX:")
                                # Show fixed line with same formatting
                                if result.line:
                                    print(f"        {result.line:3d} │ {suggested_fix}")
                                else:
                                    print(f"        {suggested_fix}")

                                # Detect required imports
                                required_imports = _detect_required_imports(suggested_fix)
                                if required_imports:
                                    print(f"\n     📦 Required import:")
                                    print(f"        import {{ {', '.join(required_imports)} }} from '@/component-library';")
                                print()
            print()

    # Print warnings
    if warning_files and verbose:
        print("\n⚠️  WARNINGS (NON-BLOCKING):\n")
        for file_path, file_results in warning_files:
            print(f"  📄 {file_path}")
            for result in file_results:
                if result.severity in ['HIGH', 'MEDIUM']:
                    line_info = f" (line {result.line})" if result.line else ""
                    icon = "⚠️ " if result.severity == 'HIGH' else "ℹ️ "
                    print(f"     {icon}{result.message}{line_info}")

                    # Show code context if available
                    if result.code_context:
                        print(f"\n     📄 Context ({result.file_path}):")
                        for line in result.code_context.split('\n'):
                            print(f"     {line}")
                        print()

                    if result.suggestion:
                        print(f"        💡 {result.suggestion}")
            print()

    print("═" * 70)


def validate_prototype(prototype_dir: Path, suggest_fixes: bool = False) -> int:
    """
    Validate all screens in a prototype directory.

    Args:
        prototype_dir: Path to prototype root directory
        suggest_fixes: Generate suggested fixes for violations (Phase 4 enhancement)
    """
    screens_dir = prototype_dir / 'prototype' / 'src' / 'screens'

    if not screens_dir.exists():
        print(f"❌ Screens directory not found: {screens_dir}")
        return 2

    validator = AssemblyFirstValidator()
    results = validator.validate_directory(screens_dir, recursive=False)

    if not results:
        print("\n✅ No React component files found or all files are compliant")
        return 0

    # Read file contents if fixes are requested
    file_contents = {}
    if suggest_fixes:
        for file_path in results.keys():
            try:
                full_path = screens_dir / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    file_contents[file_path] = f.read()
            except Exception as e:
                print(f"⚠️  Could not read {file_path} for fix generation: {e}")

    print_validation_report(
        results,
        verbose=True,
        suggest_fixes=suggest_fixes,
        validator=validator if suggest_fixes else None,
        file_contents=file_contents if suggest_fixes else None
    )

    # Exit code: 0 if passed, 2 if critical violations, 1 if only warnings
    has_critical = any(not is_valid for is_valid, _ in results.values())
    has_warnings = any(is_valid and res for is_valid, res in results.values())

    if has_critical:
        return 2
    elif has_warnings:
        return 1
    else:
        return 0


def list_violations(prototype_dir: Path) -> int:
    """List all violations in JSON format for programmatic consumption."""
    screens_dir = prototype_dir / 'prototype' / 'src' / 'screens'

    if not screens_dir.exists():
        print(json.dumps({'error': f'Screens directory not found: {screens_dir}'}))
        return 2

    validator = AssemblyFirstValidator()
    results = validator.validate_directory(screens_dir, recursive=False)

    # Convert to JSON-serializable format
    output = {
        'total_files': len(results),
        'files_with_violations': len([r for r in results.values() if not r[0] or r[1]]),
        'files': {}
    }

    for file_path, (is_valid, file_results) in results.items():
        output['files'][file_path] = {
            'is_valid': is_valid,
            'violations': [r.to_dict() for r in file_results]
        }

    print(json.dumps(output, indent=2))
    return 0


def main():
    parser = argparse.ArgumentParser(description='Assembly-First Validator')
    parser.add_argument('--file', type=str, help='Validate a single file')
    parser.add_argument('--dir', type=str, help='Validate all files in directory')
    parser.add_argument('--validate-prototype', type=str, help='Validate screens in prototype directory')
    parser.add_argument('--list-violations', type=str, help='List violations in JSON format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show warnings in addition to critical violations')
    parser.add_argument('--suggest-fixes', action='store_true', help='Generate suggested fixes for violations (Phase 4 enhancement)')
    parser.add_argument('--interactive-fix', action='store_true', help='Interactive mode to apply fixes (Phase 4 enhancement)')

    args = parser.parse_args()

    if args.file:
        validator = AssemblyFirstValidator()
        is_valid, results = validator.validate_file(Path(args.file))

        if results:
            # Read file contents if fixes are requested
            file_contents = {}
            if args.suggest_fixes or args.interactive_fix:
                try:
                    with open(args.file, 'r', encoding='utf-8') as f:
                        file_contents[args.file] = f.read()
                except Exception as e:
                    print(f"⚠️  Could not read file for fix generation: {e}")

            print_validation_report(
                {args.file: (is_valid, results)},
                verbose=args.verbose,
                suggest_fixes=args.suggest_fixes or args.interactive_fix,
                validator=validator,
                file_contents=file_contents
            )
            return 2 if not is_valid else 1
        else:
            print("✅ File is compliant")
            return 0

    elif args.dir:
        validator = AssemblyFirstValidator()
        results = validator.validate_directory(Path(args.dir))

        if results:
            # Read file contents if fixes are requested
            file_contents = {}
            if args.suggest_fixes or args.interactive_fix:
                for file_path in results.keys():
                    try:
                        full_path = Path(args.dir) / file_path
                        with open(full_path, 'r', encoding='utf-8') as f:
                            file_contents[file_path] = f.read()
                    except Exception as e:
                        print(f"⚠️  Could not read {file_path} for fix generation: {e}")

            print_validation_report(
                results,
                verbose=args.verbose,
                suggest_fixes=args.suggest_fixes or args.interactive_fix,
                validator=validator,
                file_contents=file_contents
            )
            has_critical = any(not is_valid for is_valid, _ in results.values())
            return 2 if has_critical else 1
        else:
            print("✅ All files are compliant")
            return 0

    elif args.validate_prototype:
        return validate_prototype(Path(args.validate_prototype), suggest_fixes=args.suggest_fixes or args.interactive_fix)

    elif args.list_violations:
        return list_violations(Path(args.list_violations))

    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
