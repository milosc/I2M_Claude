# GDPR Data Flow Diagram Skill

Generate comprehensive GDPR-compliant data flow diagrams using Mermaid notation.

## Quick Start

Invoke the skill:
```
/gdpr-data-flow-diagram
```

Or describe your need:
- "Create a data flow diagram for our customer data processing"
- "Map our personal data flows for GDPR compliance"
- "Generate DFDs for our DPIA"

## What It Does

1. **Collects Data Inventory** - Gathers info about data subjects, data types, processing activities, and recipients
2. **Generates Multi-Level DFDs** - Creates Context (L0), Decomposition (L1), and Detail (L2) diagrams
3. **Maps GDPR Requirements** - Shows legal bases, cross-border transfers, special category data handling
4. **Provides Compliance Checklist** - Validates against GDPR articles

## Diagram Types Generated

| Type | Purpose |
|------|---------|
| Context (Level 0) | System overview with external entities |
| Decomposition (Level 1) | Major processing areas |
| Detail (Level 2) | Granular process views |
| Cross-Border | International data transfers |
| Special Category | Sensitive data flows |
| DSR Flow | Data subject rights handling |

## File Structure

```
GDPR_DataFlow_Mapper/
├── SKILL.md                    # Main skill definition
├── README.md                   # This file
└── references/
    ├── mermaid-patterns.md     # Mermaid syntax reference
    ├── gdpr-requirements.md    # GDPR compliance requirements
    └── examples.md             # Complete examples
```

## Output

The skill generates:
- Mermaid diagram code blocks (copy-paste ready)
- `.mmd` files for each diagram level
- Compliance checklist in markdown
- Data inventory summary

## Color Coding

| Color | Meaning |
|-------|---------|
| 🔵 Blue | Your organization's processing |
| 🟣 Purple | Third-party processors |
| 🟢 Green | Data stores |
| ⚪ Gray | External entities/data subjects |
| 🔴 Red | Special category data |
| 🟡 Amber | Cross-border / attention needed |

## Version

- **Version**: 1.0.0
- **Created**: 2025-02-02
- **Sources**:
  - Information Governance Services - Data Flow Mapping Guide
  - IBM Think - Data Flow Diagram Concepts
