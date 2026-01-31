# ProductSpecs Entry Points - Usage Guide

**Version**: 1.0.0
**Date**: 2026-01-27
**Phase**: 4 - Entry Points

---

## Quick Reference

### Command Syntax

```bash
/productspecs <SystemName> [OPTIONS]
```

### Available Entry Points (7 Types)

| Entry Point | Flag | Time Savings | Example |
|-------------|------|--------------|---------|
| **System** | (default) | 0% | `/productspecs InventorySystem` |
| **Module** | `--module` | 80% | `/productspecs INV --module MOD-INV-SEARCH-01` |
| **Feature** | `--feature` | 60-70% | `/productspecs INV --feature SEARCH` |
| **Screen** | `--screen` | 50-60% | `/productspecs INV --screen SCR-003` |
| **Persona** | `--persona` | 40-50% | `/productspecs INV --persona admin` |
| **Subsystem** | `--subsystem` | 30-40% | `/productspecs INV --subsystem middleware` |
| **Layer** | `--layer` | 40-50% | `/productspecs INV --layer frontend` |

### Quality Flag

```bash
--quality critical    # Enable VP review for ALL modules (P0, P1, P2)
```

---

## Common Use Cases

### 1. Initial Generation (System-Level)

**Scenario**: First-time generation, need all modules

```bash
/productspecs InventorySystem
```

**Output**: All modules generated with default quality checks (P0 modules get VP review)

**Time**: Baseline (e.g., 16 minutes for 20 modules)

---

### 2. Single Module Update (Module-Level)

**Scenario**: Feedback on one module, need to regenerate quickly

```bash
/productspecs InventorySystem --module MOD-INV-SEARCH-01
```

**Output**: Only `MOD-INV-SEARCH-01` regenerated

**Time**: 80% savings (e.g., 3 min vs 16 min)

**Use Case**: Post-review updates, bug fixes, iterative improvements

---

### 3. Feature Iteration (Feature-Level)

**Scenario**: Redesigning search feature, need all search-related modules

```bash
# Exact match
/productspecs InventorySystem --feature SEARCH

# Fuzzy match (tolerates typos)
/productspecs InventorySystem --feature srch
```

**Output**: All modules with "SEARCH" in feature part (e.g., `MOD-INV-SEARCH-01`, `MOD-INV-SEARCH-02`)

**Time**: 60-70% savings

**Use Case**: Feature refactoring, A/B testing, feature-specific updates

---

### 4. Screen Updates (Screen-Level)

**Scenario**: Redesigning login screen, need all linked modules

```bash
/productspecs InventorySystem --screen SCR-003
```

**Output**: All modules linked to `SCR-003` in their `sources.screens` field

**Time**: 50-60% savings

**Use Case**: UI redesigns, screen refactoring, UX improvements

---

### 5. Persona-Specific Features (Persona-Level)

**Scenario**: Adding admin-only features, need all admin modules

```bash
/productspecs InventorySystem --persona admin
```

**Output**: All modules with "admin" in their `personas` field

**Time**: 40-50% savings

**Use Case**: Role-based features, permission changes, persona-specific enhancements

---

### 6. Subsystem Refactoring (Subsystem-Level)

**Scenario**: Refactoring middleware layer, need all middleware modules

```bash
/productspecs InventorySystem --subsystem middleware
```

**Output**: All modules with `subsystem: "middleware"`

**Time**: 30-40% savings

**Use Case**: Subsystem isolation, refactoring, architectural changes

---

### 7. Layer Separation (Layer-Level)

**Scenario**: Splitting frontend from backend, need all frontend modules

```bash
/productspecs InventorySystem --layer frontend
```

**Output**: All modules with `layer: "frontend"`

**Valid Layers**: `frontend`, `backend`, `middleware`, `database`

**Time**: 40-50% savings

**Use Case**: Microservices migration, layer separation, frontend/backend split

---

### 8. High-Stakes Release (Quality Critical)

**Scenario**: Production release, need maximum quality

```bash
/productspecs InventorySystem --quality critical
```

**Output**: ALL modules (P0, P1, P2) get per-module VP review

**Time**: +119% (e.g., 35 min vs 16 min for 20 modules)

**Cost**: +126%

**Quality**: +28% (score 75 → 96)

**Use Case**: Production releases, high-visibility launches, critical updates

---

## Fuzzy Matching Examples

### Exact Match (Preferred)

```bash
/productspecs InventorySystem --feature SEARCH
# Output: MOD-INV-SEARCH-01, MOD-INV-SEARCH-02
```

### Fuzzy Match (Typo Tolerant)

```bash
/productspecs InventorySystem --feature srch
# Output: ⚠️ Fuzzy match: 'srch' matched features: SEARCH
#         MOD-INV-SEARCH-01, MOD-INV-SEARCH-02

/productspecs InventorySystem --feature Seach
# Output: ⚠️ Fuzzy match: 'Seach' matched features: SEARCH (80% similarity)
#         MOD-INV-SEARCH-01, MOD-INV-SEARCH-02
```

### No Match (Helpful Error)

```bash
/productspecs InventorySystem --feature xyz
# Output: ❌ No modules found for feature 'xyz'
#         Try: SEARCH, REPORT, EXPORT, ADMIN, DASHBOARD
```

**Threshold**: 60% similarity (configurable in `.claude/hooks/productspecs_scope_filter.py`)

---

## Validation Examples

### Valid Module

```bash
/productspecs InventorySystem --module MOD-INV-SEARCH-01
# ✅ Scope filtered: 1 module (module-level)
```

### Invalid Module

```bash
/productspecs InventorySystem --module MOD-XXX-YYY-01
# ❌ Module 'MOD-XXX-YYY-01' not found
#    Available modules: MOD-INV-SEARCH-01, MOD-INV-SEARCH-02, ...
```

### Valid Layer

```bash
/productspecs InventorySystem --layer frontend
# ✅ Scope filtered: 8 modules (layer-level)
```

### Invalid Layer

```bash
/productspecs InventorySystem --layer api
# ❌ Invalid layer 'api'
#    Valid layers: frontend, backend, middleware, database
```

---

## Workflow Integration

### Standard Workflow

```bash
# 1. Initial generation (system-level)
/productspecs InventorySystem

# 2. Review and feedback on specific modules

# 3. Regenerate only affected modules (module-level)
/productspecs InventorySystem --module MOD-INV-SEARCH-01
/productspecs InventorySystem --module MOD-INV-REPORT-01

# 4. Validate traceability
/productspecs-validate InventorySystem

# 5. Export JIRA
/productspecs-jira InventorySystem
```

### Iterative Feature Development

```bash
# 1. Generate all modules
/productspecs InventorySystem

# 2. Iterate on search feature
/productspecs InventorySystem --feature SEARCH

# 3. Iterate on UI screens
/productspecs InventorySystem --screen SCR-001

# 4. Final quality check (critical mode)
/productspecs InventorySystem --quality critical

# 5. Export
/productspecs-export InventorySystem
```

---

## Testing

### Run Test Suite

```bash
# Run all tests (14 test cases)
bash .claude/hooks/test_productspecs_scope_filter.sh
```

**Test Cases**:
1. System-level (all modules)
2. Module-level (exact match)
3. Feature-level (exact match)
4. Feature-level (fuzzy match)
5. Screen-level
6. Persona-level
7. Subsystem-level
8. Layer-level (frontend)
9. Invalid module (validation)
10. Invalid feature (validation)
11. Invalid layer (validation)
12. Empty screen result (validation)
13. Quality critical mode (all VP reviews)
14. Standard mode (P0 only VP reviews)

**Expected Output**:

```
════════════════════════════════════════════════════════════════
  TEST RESULTS
════════════════════════════════════════════════════════════════

  Tests Run:    14
  Tests Passed: 14
  Tests Failed: 0

  ✅ ALL TESTS PASSED

════════════════════════════════════════════════════════════════
```

---

## Direct Script Usage

### Using the Python Utility Directly

```bash
# Module-level
python3 .claude/hooks/productspecs_scope_filter.py \
  InventorySystem \
  --module MOD-INV-SEARCH-01 \
  --output _state/filtered_scope.json

# Feature-level with fuzzy match
python3 .claude/hooks/productspecs_scope_filter.py \
  InventorySystem \
  --feature srch \
  --output _state/filtered_scope.json

# Quality critical mode
python3 .claude/hooks/productspecs_scope_filter.py \
  InventorySystem \
  --quality critical \
  --output _state/filtered_scope.json
```

### Inspect Filtered Scope

```bash
# View filtered scope
cat _state/filtered_scope.json | jq .

# Count modules
cat _state/filtered_scope.json | jq -r '.total_modules'

# List module IDs
cat _state/filtered_scope.json | jq -r '.modules[].id'

# Check VP review flags
cat _state/filtered_scope.json | jq -r '.modules[] | select(.needs_vp_review == true) | .id'
```

---

## Troubleshooting

### Issue: "Module registry is empty"

**Cause**: No modules generated yet

**Solution**: Run system-level first to generate all modules
```bash
/productspecs InventorySystem
```

### Issue: "No modules found for feature 'X'"

**Cause**: Feature name doesn't match any modules (even with fuzzy matching)

**Solution**: Check available features
```bash
cat traceability/module_registry.json | jq -r '.[].id' | cut -d'-' -f3 | sort -u
```

### Issue: "Invalid layer"

**Cause**: Layer name not in valid list

**Solution**: Use one of: `frontend`, `backend`, `middleware`, `database`

### Issue: Fuzzy match too permissive

**Cause**: 60% threshold matching unintended features

**Solution**: Adjust threshold in `.claude/hooks/productspecs_scope_filter.py` (line ~48):
```python
def fuzzy_match_feature(feature_input: str, module_ids: List[str], threshold: float = 0.6):
    # Change to 0.7 for stricter matching, 0.5 for more permissive
```

---

## Performance Comparison

### Baseline: 20 Modules (5 P0, 10 P1, 5 P2)

| Entry Point | Modules | Time | Cost | Quality | Use Case |
|-------------|---------|------|------|---------|----------|
| **System** | 20 | 16 min | $53 | 85 | Initial generation |
| **Module** | 1 | 3 min | $10 | 85 | Single module update |
| **Feature** (3 modules) | 3 | 5 min | $16 | 85 | Feature iteration |
| **Screen** (4 modules) | 4 | 6 min | $21 | 85 | Screen updates |
| **Persona** (10 modules) | 10 | 8 min | $27 | 85 | Persona features |
| **Subsystem** (12 modules) | 12 | 10 min | $32 | 85 | Subsystem refactoring |
| **Layer** (10 modules) | 10 | 8 min | $27 | 85 | Layer separation |
| **Quality Critical** | 20 | 35 min | $120 | 96 | Production release |

**Assumptions**: 20 modules, standard mode (P0 VP review only), except quality critical

---

## Best Practices

1. **Start System-Level**: Always run system-level first to generate all modules and registries

2. **Use Module-Level for Iterations**: For quick updates, use module-level for 80% time savings

3. **Fuzzy Match Feature Names**: Don't worry about exact feature names, fuzzy matching tolerates typos

4. **Quality Critical for Production**: Use `--quality critical` for final releases

5. **Test Before Production**: Run test suite to validate scope filter works correctly

6. **Check Filtered Scope**: Review `_state/filtered_scope.json` before long operations

---

## Related Commands

| Command | Description |
|---------|-------------|
| `/productspecs` | Full generation with entry points |
| `/productspecs-status` | Show current progress |
| `/productspecs-resume` | Resume from checkpoint |
| `/productspecs-validate` | Validate traceability |
| `/productspecs-export` | Export JIRA files |

---

## Related Documentation

- **Implementation Plan**: `.claude/architecture/Workflows/Solution Specification Phase/SolutionSpecs_Implementation_Plan_FINAL.md`
- **Phase 4 Completion**: `.claude/architecture/Workflows/Solution Specification Phase/Phase_4_Entry_Points_COMPLETED.md`
- **Command Reference**: `.claude/commands/productspecs.md`
- **Agent Registry**: `.claude/skills/PRODUCTSPECS_AGENT_REGISTRY.json`

---

## Support

For issues or questions:
1. Check this guide for common use cases
2. Review error messages (they include suggestions)
3. Run test suite to validate installation
4. Check troubleshooting section above

---

**Last Updated**: 2026-01-27
**Version**: 1.0.0
**Phase**: 4 - Entry Points
