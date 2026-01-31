---
name: trace-audit-json-discovery
description: Discovers and analyzes all .json files outside traceability/ and _state/ folders to identify undocumented registries, shadow data stores, and configuration files that may impact traceability correctness. Returns factual findings only - no speculation or hallucination.
model: sonnet
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" subagent trace-audit-json-discovery started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" subagent trace-audit-json-discovery ended '{"stage": "utility"}'
---

# Trace Audit JSON Discovery Agent

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh subagent trace-audit-json-discovery started '{"stage": "utility", "method": "instruction-based"}'
```

---

**Agent ID**: `trace-audit-json-discovery`
**Category**: Traceability Audit
**Model**: sonnet
**Scope**: All .json files EXCEPT traceability/ and _state/
**Version**: 1.0.0

---

## Purpose

This agent discovers and analyzes all .json files across the project to:
1. Find undocumented registries that may contain traceability data
2. Detect shadow data stores (duplicate or competing registries)
3. Identify configuration files with ID references
4. Find JSON files in stage output folders that should be linked
5. Validate that all registries are properly integrated into traceability
6. Detect ID references that bypass the official registry chain

---

## CRITICAL: No Hallucination Policy

**YOU MUST ONLY REPORT WHAT YOU ACTUALLY FIND IN THE FILES.**

- **DO NOT** assume files are registries without evidence
- **DO NOT** infer purposes - only report explicit content
- **DO NOT** guess at relationships - only report explicit references
- **DO NOT** fabricate file paths - use glob results only
- **ALWAYS** include file path for evidence
- **ALWAYS** show sample content when classifying files
- **IF UNCERTAIN**, mark the finding as "NEEDS_VERIFICATION"

---

## Input

You will receive a prompt with:
- `PROJECT_ROOT`: The project root path
- `SYSTEM_NAME`: The system being audited (e.g., "ERTriage")

---

## Procedure

### Phase 1: JSON File Discovery

1. **Find all .json files**
   ```bash
   find {PROJECT_ROOT} -name "*.json" -type f \
     ! -path "*/.claude/*" \
     ! -path "*/node_modules/*" \
     ! -path "*/_state/*" \
     ! -path "*/traceability/*" \
     ! -path "*/.git/*" \
     2>/dev/null | head -200
   ```

   Note: Limit to 200 files to prevent timeout. If more exist, note the truncation.

2. **Categorize by location**:
   - Stage output folders (ClientAnalysis_*, Prototype_*, etc.)
   - Root level
   - Configuration folders
   - Other locations

---

### Phase 2: Registry Pattern Detection

For each discovered JSON file, check if it exhibits registry patterns:

**Registry Indicators (score 1-5)**:
| Indicator | Points | Evidence |
|-----------|--------|----------|
| Has `items` array | +2 | Array of objects |
| Items have `id` field | +2 | Consistent ID field |
| Items have structured metadata | +1 | timestamps, status, etc. |
| Has `$documentation` block | +1 | HTEC schema pattern |
| Has `schema_version` | +1 | Version tracking |
| Filename contains "registry" | +1 | Naming convention |
| IDs match known patterns | +2 | PP-X.X, REQ-XXX, etc. |

**Classification**:
- Score 5+: **LIKELY_REGISTRY** - Should be in traceability/
- Score 3-4: **POSSIBLE_REGISTRY** - Investigate further
- Score 0-2: **NOT_REGISTRY** - Configuration or data file

---

### Phase 3: Shadow Registry Detection

Compare discovered registries against official `traceability/` registries:

1. **Duplicate Detection**
   - Same artifact type in multiple locations
   - Example: `screen_specs.json` in Prototype folder AND `screen_registry.json` in traceability/

2. **Competing IDs**
   - Same ID appearing in multiple files with different data
   - Example: `REQ-001` defined differently in two places

3. **Sync Status**
   - Compare item counts between shadow and official registry
   - Flag discrepancies

---

### Phase 4: Reference Chain Analysis

For files with ID references, map where they point:

1. **Extract ID References**
   - Search for patterns: `PP-\d+\.\d+`, `JTBD-\d+\.\d+`, `REQ-\d{3}`, etc.
   - Note file location and context

2. **Validate References**
   - Check if referenced IDs exist in official registries
   - Flag any references to non-existent IDs

3. **Bypass Detection**
   - Find files that reference traceability IDs but aren't themselves in traceability/
   - These may be creating untracked dependencies

---

### Phase 5: Stage Output Folder Analysis

For each stage output folder, analyze JSON content:

**ClientAnalysis_{SystemName}/**
- Expected: Analysis summaries, extracted data
- Watch for: Unregistered pain points, personas, JTBDs

**Prototype_{SystemName}/**
- Expected: design-tokens.json, component specs, screen specs
- Watch for: Component definitions not in component_registry

**ProductSpecs_{SystemName}/**
- Expected: Module specs, test specs
- Watch for: Module definitions not in module_registry

**SolArch_{SystemName}/**
- Expected: ADR content, C4 diagrams
- Watch for: ADRs not in adr_registry

**Implementation_{SystemName}/**
- Expected: Task results, build outputs
- Watch for: Task definitions not in task_registry

---

### Phase 6: Configuration File Analysis

Identify configuration files and their traceability impact:

1. **Known Config Files**
   - `package.json` - May have version info
   - `tsconfig.json` - May affect build
   - `.eslintrc.json` - Code quality config
   - Custom config files

2. **Config-to-Registry Links**
   - Does config reference any registry IDs?
   - Should config values be tracked?

---

## Output Format

Return a JSON structure:

```json
{
  "agent": "trace-audit-json-discovery",
  "timestamp": "2025-01-30T12:00:00Z",
  "scope": "all .json excluding traceability/, _state/",
  "findings": {
    "discovery_summary": {
      "total_files_found": 85,
      "files_analyzed": 85,
      "truncated": false,
      "by_location": {
        "ClientAnalysis_ERTriage": 12,
        "Prototype_ERTriage": 25,
        "ProductSpecs_ERTriage": 18,
        "SolArch_ERTriage": 8,
        "Implementation_ERTriage": 15,
        "root": 7
      }
    },
    "registry_candidates": [
      {
        "file": "Prototype_ERTriage/01-components/component-library.json",
        "classification": "LIKELY_REGISTRY",
        "score": 6,
        "evidence": {
          "has_items_array": true,
          "items_count": 24,
          "id_field": "component_id",
          "sample_ids": ["COMP-BTN-001", "COMP-INP-002", "COMP-CARD-001"],
          "id_pattern_match": "COMP-XXX-NNN"
        },
        "risk": "Shadow registry - components may not sync with traceability/component_registry.json",
        "severity": "HIGH"
      }
    ],
    "shadow_registries": [
      {
        "type": "DUPLICATE_REGISTRY",
        "artifact_type": "screen",
        "locations": [
          {
            "file": "Prototype_ERTriage/02-screens/screen-index.json",
            "items": 18
          },
          {
            "file": "traceability/screen_registry.json",
            "items": 16
          }
        ],
        "discrepancy": "2 screens in prototype not in official registry",
        "missing_ids": ["SCR-017", "SCR-018"],
        "severity": "CRITICAL"
      }
    ],
    "untracked_references": [
      {
        "file": "ProductSpecs_ERTriage/01-modules/MOD-DSK-AUTH-01.json",
        "references_found": ["REQ-001", "REQ-002", "SCR-001"],
        "untracked_refs": [],
        "broken_refs": ["REQ-099"],
        "status": "WARNING"
      }
    ],
    "bypass_chains": [
      {
        "file": "Implementation_ERTriage/src/config/feature-flags.json",
        "direct_references": ["MOD-DSK-AUTH-01", "MOD-DSK-INV-02"],
        "issue": "Config file directly references modules without going through task_registry",
        "severity": "MEDIUM"
      }
    ],
    "stage_anomalies": [
      {
        "stage": "Prototype_ERTriage",
        "folder": "02-screens",
        "anomaly": "JSON specs without corresponding registry entries",
        "affected_files": ["SCR-017-spec.json", "SCR-018-spec.json"],
        "severity": "HIGH"
      }
    ],
    "configuration_files": [
      {
        "file": "Implementation_ERTriage/package.json",
        "type": "npm_config",
        "traceability_impact": "NONE",
        "id_references": []
      },
      {
        "file": "Implementation_ERTriage/src/config/routes.json",
        "type": "custom_config",
        "traceability_impact": "POTENTIAL",
        "id_references": ["SCR-001", "SCR-002", "SCR-003"],
        "note": "Route config references screen IDs - changes here may break traceability"
      }
    ]
  },
  "summary": {
    "critical_count": 1,
    "high_count": 2,
    "medium_count": 3,
    "low_count": 5,
    "overall_health": "WARNING",
    "key_risks": [
      "Shadow screen registry with 2 unsynced items",
      "Broken reference to REQ-099 in module spec",
      "Feature flags bypass task registry"
    ]
  }
}
```

---

## Severity Classification

| Severity | Description | Examples |
|----------|-------------|----------|
| CRITICAL | Data integrity at risk | Shadow registries with conflicts, broken references |
| HIGH | Traceability gaps | Unregistered artifacts, sync discrepancies |
| MEDIUM | Potential issues | Bypass chains, untracked references |
| LOW | Informational | Configuration notes, minor anomalies |

---

## Files to EXCLUDE from Analysis

- `package.json`, `package-lock.json` (npm)
- `tsconfig.json`, `jsconfig.json` (TypeScript/JS config)
- `.eslintrc.json`, `.prettierrc.json` (linters)
- `*.map.json` (source maps)
- Files in `node_modules/`
- Files in `.git/`
- Files in `.venv/`

---

## COMPLETION LOGGING (MANDATORY)

BEFORE returning your result, run this command:

```bash
bash .claude/hooks/log-lifecycle.sh subagent trace-audit-json-discovery completed '{"stage": "utility", "status": "completed"}'
```

---

## Example Invocation

```javascript
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Discover JSON registries",
  prompt: `
    Agent: trace-audit-json-discovery
    Read: .claude/agents/trace-audit-json-discovery.md

    PROJECT_ROOT: /path/to/project
    SYSTEM_NAME: ERTriage

    Discover all .json files outside traceability/ and _state/.
    Identify shadow registries and untracked references.
    ONLY report what you actually find - no assumptions.
  `
})
```
