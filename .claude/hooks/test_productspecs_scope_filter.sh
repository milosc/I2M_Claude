#!/bin/bash
#
# Test Script for ProductSpecs Scope Filter (Phase 4)
# Tests all 7 entry points + fuzzy matching + validation
#

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
FILTER_SCRIPT="$SCRIPT_DIR/productspecs_scope_filter.py"

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "  PRODUCTSPECS SCOPE FILTER - TEST SUITE"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Setup: Create test registry
echo "⏳ Setting up test environment..."
mkdir -p "$PROJECT_ROOT/traceability"

cat > "$PROJECT_ROOT/traceability/TestSystem_module_registry.json" <<'EOF'
[
  {
    "id": "MOD-TEST-SEARCH-01",
    "priority": "P0",
    "layer": "frontend",
    "subsystem": "ui",
    "personas": ["admin", "user"],
    "sources": {
      "screens": ["SCR-001", "SCR-002"]
    }
  },
  {
    "id": "MOD-TEST-SEARCH-02",
    "priority": "P1",
    "layer": "backend",
    "subsystem": "api",
    "personas": ["admin"],
    "sources": {
      "screens": ["SCR-001"]
    }
  },
  {
    "id": "MOD-TEST-REPORT-01",
    "priority": "P0",
    "layer": "frontend",
    "subsystem": "ui",
    "personas": ["admin"],
    "sources": {
      "screens": ["SCR-003"]
    }
  },
  {
    "id": "MOD-TEST-REPORT-02",
    "priority": "P2",
    "layer": "backend",
    "subsystem": "api",
    "personas": ["user"],
    "sources": {
      "screens": ["SCR-003", "SCR-004"]
    }
  },
  {
    "id": "MOD-TEST-EXPORT-01",
    "priority": "P1",
    "layer": "middleware",
    "subsystem": "integration",
    "personas": ["admin", "user"],
    "sources": {
      "screens": ["SCR-005"]
    }
  }
]
EOF

echo "✅ Test registry created: 5 modules"
echo ""

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
  local test_name="$1"
  local expected_modules="$2"
  shift 2
  local args=("$@")

  TESTS_RUN=$((TESTS_RUN + 1))
  echo "────────────────────────────────────────────────────────────────"
  echo "Test $TESTS_RUN: $test_name"
  echo "────────────────────────────────────────────────────────────────"

  # Run filter
  if python3 "$FILTER_SCRIPT" TestSystem "${args[@]}" > /dev/null 2>&1; then
    # Check result
    local actual_modules=$(jq -r '.total_modules' "$PROJECT_ROOT/_state/filtered_scope.json")

    if [ "$actual_modules" -eq "$expected_modules" ]; then
      echo "✅ PASS - Expected: $expected_modules modules, Got: $actual_modules"
      TESTS_PASSED=$((TESTS_PASSED + 1))
    else
      echo "❌ FAIL - Expected: $expected_modules modules, Got: $actual_modules"
      TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
  else
    if [ "$expected_modules" -eq "-1" ]; then
      # Expected to fail
      echo "✅ PASS - Expected failure (validation error)"
      TESTS_PASSED=$((TESTS_PASSED + 1))
    else
      echo "❌ FAIL - Command failed unexpectedly"
      TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
  fi

  echo ""
}

# Test Suite

echo "═══════════════════════════════════════════════════════════════"
echo "  TEST SUITE: 7 ENTRY POINTS"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Test 1: System-level (all modules)
run_test "System-level (default)" 5

# Test 2: Module-level (exact match)
run_test "Module-level (exact match)" 1 --module MOD-TEST-SEARCH-01

# Test 3: Feature-level (exact match)
run_test "Feature-level (exact match)" 2 --feature SEARCH

# Test 4: Feature-level (fuzzy match)
run_test "Feature-level (fuzzy match 'srch')" 2 --feature srch

# Test 5: Screen-level
run_test "Screen-level (SCR-001)" 2 --screen SCR-001

# Test 6: Persona-level
run_test "Persona-level (admin)" 4 --persona admin

# Test 7: Subsystem-level
run_test "Subsystem-level (ui)" 2 --subsystem ui

# Test 8: Layer-level (frontend)
run_test "Layer-level (frontend)" 2 --layer frontend

echo "═══════════════════════════════════════════════════════════════"
echo "  TEST SUITE: VALIDATION"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Test 9: Invalid module
run_test "Invalid module (should fail)" -1 --module MOD-XXX-YYY-01

# Test 10: Invalid feature
run_test "Invalid feature (should fail)" -1 --feature XYZ

# Test 11: Invalid layer
run_test "Invalid layer (should fail)" -1 --layer invalid

# Test 12: Empty screen result
run_test "Empty screen result (should fail)" -1 --screen SCR-999

echo "═══════════════════════════════════════════════════════════════"
echo "  TEST SUITE: QUALITY CRITICAL FLAG"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Test 13: Quality critical mode
run_test "Quality critical mode" 5 --quality critical

# Verify all modules have needs_vp_review=true
if python3 "$FILTER_SCRIPT" TestSystem --quality critical > /dev/null 2>&1; then
  VP_COUNT=$(jq -r '[.modules[] | select(.needs_vp_review == true)] | length' "$PROJECT_ROOT/_state/filtered_scope.json")
  TOTAL_COUNT=$(jq -r '.total_modules' "$PROJECT_ROOT/_state/filtered_scope.json")

  if [ "$VP_COUNT" -eq "$TOTAL_COUNT" ]; then
    echo "✅ All modules flagged for VP review in quality critical mode"
  else
    echo "❌ Not all modules flagged for VP review: $VP_COUNT/$TOTAL_COUNT"
  fi
fi

echo ""

# Test 14: Standard mode (only P0)
run_test "Standard mode (P0 only)" 5

# Verify only P0 modules have needs_vp_review=true
if python3 "$FILTER_SCRIPT" TestSystem > /dev/null 2>&1; then
  P0_COUNT=$(jq -r '[.modules[] | select(.priority == "P0")] | length' "$PROJECT_ROOT/_state/filtered_scope.json")
  VP_COUNT=$(jq -r '[.modules[] | select(.needs_vp_review == true)] | length' "$PROJECT_ROOT/_state/filtered_scope.json")

  if [ "$VP_COUNT" -eq "$P0_COUNT" ]; then
    echo "✅ Only P0 modules flagged for VP review in standard mode ($VP_COUNT/$P0_COUNT)"
  else
    echo "❌ VP review mismatch: Expected $P0_COUNT (P0 count), Got $VP_COUNT"
  fi
fi

echo ""

# Summary
echo "════════════════════════════════════════════════════════════════"
echo "  TEST RESULTS"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "  Tests Run:    $TESTS_RUN"
echo "  Tests Passed: $TESTS_PASSED"
echo "  Tests Failed: $TESTS_FAILED"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
  echo "  ✅ ALL TESTS PASSED"
  echo ""
  echo "════════════════════════════════════════════════════════════════"
  echo ""
  exit 0
else
  echo "  ❌ SOME TESTS FAILED"
  echo ""
  echo "════════════════════════════════════════════════════════════════"
  echo ""
  exit 1
fi
