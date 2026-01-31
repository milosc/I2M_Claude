---
document_id: SKL-VC-STANDARD-001
version: 1.1.0
created_at: 2025-12-19
updated_at: 2025-12-29
generated_by: human
source_files: []
change_history:
  - version: 1.0.0
    date: 2025-12-19
    author: human
    changes: Initial version
  - version: 1.1.0
    date: 2025-12-29
    author: System
    changes: Added global version state registry logic and /version-bump command
---

---
document_id: SKL-VC-STANDARD-001
version: 1.2.0
created_at: 2025-12-19
updated_at: 2025-12-29
generated_by: human
source_files: []
change_history:
  - version: 1.0.0
    date: 2025-12-19
    author: human
    changes: Initial version
  - version: 1.1.0
    date: 2025-12-29
    author: System
    changes: Added global version state registry logic and /version-bump command
  - version: 1.2.0
    date: 2025-12-29
    author: System
    changes: Added Global Traceability Version History logging requirement
---

# Version Control Standard for Skill Outputs

---

## Overview

All skills that produce or modify `.md`, `.json`, or code files MUST include version control metadata and log their changes to the Global Traceability Version History.

---

## Global Traceability Version History

Every change (creation, modification, deletion) MUST be logged into a central JSON file: `traceability/{system_name}_version_history.json`.

### JSON Structure
```json
{
  "system_name": "{SystemName}",
  "history": [
    {
      "timestamp": "2025-12-29T14:30:00Z",
      "stage": "discovery",
      "author": "Claude",
      "version": "1.0.1",
      "action": "modification",
      "file": "ClientAnalysis_X/01-analysis/ANALYSIS_SUMMARY.md",
      "reason": "Updated analysis with new interview data from Michael.",
      "references": ["CF-001", "PP-1.2", "JTBD-3"]
    }
  ]
}
```

---

## Markdown File Header Standard
... content ...

---

## Regeneration & Modification Behavior

When a skill creates, modifies, or deletes a file:

### 1. Read Existing Metadata (for existing files)
... content ...

### 2. Read Version State Registry
... content ...

### 3. Determine Version Bump
... content ...

### 4. Append to Change History (Local File)
... content ...

### 5. Update Metadata (Local File)
... content ...

### 6. Log to Global Traceability History (MANDATORY)
```
EXECUTE: python3 .claude/hooks/version_history_logger.py \
  "traceability/" \
  "{system_name}" \
  "{current_stage}" \
  "{author}" \
  "{new_version}" \
  "{reason_single_sentence}" \
  "{references_comma_separated}" \
  "{file_path}" \
  "{action}"
```
- **Reason**: MUST be a single concise sentence.
- **References**: MUST include IDs (e.g., CF-, JTBD-, PP-, US-, E-, T-).

---

## Footer Standard (Optional but Recommended)
... content ...

---

**Standard Version**: 1.2.0
**Updated**: 2025-12-29
