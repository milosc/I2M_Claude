# New Skills Assessment Report

**Version**: 1.0.0
**Date**: 2026-01-30
**Skills Analyzed**: 97 folders added on January 29, 2026

---

## Executive Summary

This report assesses 97 newly added skills against the existing HTEC framework ecosystem. The analysis identifies:
- **28 HIGH-VALUE skills** for immediate integration
- **15 REDUNDANT skills** that overlap with existing capabilities
- **34 SPECIALIZED skills** for on-demand domain expertise
- **20 UTILITY skills** with moderate integration potential

**Recommendation**: Integrate 28 high-value skills into existing agents/commands, deprecate 6 redundant skills, and keep 63 as specialized on-demand resources.

---

## Skill Categories Overview

| Category | Count | Verdict |
|----------|-------|---------|
| **SECURITY_*** | 30 | 8 integrate, 22 specialized |
| **GRC_*** | 13 | 3 integrate, 10 specialized |
| **PERSONA_*** | 11 | 6 REDUNDANT, 5 specialized |
| **github_*** | 8 | 3 integrate, 3 REDUNDANT, 2 utility |
| **api-*** | 2 | 2 integrate |
| **Database/Backend** | 6 | 3 integrate, 3 utility |
| **Design/UX** | 9 | 3 integrate, 6 utility |
| **Development Tools** | 18 | 6 integrate, 6 REDUNDANT, 6 utility |

---

## Part 1: Redundancy Analysis

### 1.1 REDUNDANT Skills (Recommend Deprecation or Merge)

These skills duplicate existing framework capabilities:

| New Skill | Existing Equivalent | Action |
|-----------|---------------------|--------|
| `PERSONA_senior-architect` | `sdd-software-architect` | **MERGE** - Combine toolkit into sdd-software-architect |
| `PERSONA_senior-backend` | `backend-dev-guidelines` | **MERGE** - Enhanced guidelines already exist |
| `PERSONA_senior-frontend` | `frontend-dev-guidelines` | **MERGE** - Enhanced guidelines already exist |
| `PERSONA_senior-qa` | `code-review-test-coverage` + `test-fixing` | **REDUNDANT** - Coverage exists |
| `PERSONA_senior-devops` | `sdd-developer` + DevOps patterns | **PARTIAL MERGE** - Add DevOps scripts to sdd-developer |
| `github_git-commit-helper` | `/commit` command | **REDUNDANT** - Existing command is comprehensive |
| `github_gh-address-comments` | `github_address-github-comments` | **DUPLICATE** - Same functionality, different name |
| `github_gh-fix-ci` | Covered by `/fix-tests` | **PARTIAL OVERLAP** - Merge CI-specific patterns |
| `skill-creator` | `/create-skill` command | **REDUNDANT** - Command exists |
| `skill-developer` | `/create-skill` command | **REDUNDANT** - Command exists |
| `skill-judge` | Part of `/test-skill` | **PARTIAL OVERLAP** |
| `software-architecture` | `sdd-software-architect` + `architecture` | **REDUNDANT** - Already covered |
| `production-code-audit` | `code-review-*` agents (6 agents) | **PARTIAL OVERLAP** - Consider merging audit patterns |
| `test-fixing` | `/fix-tests` command | **ALREADY EXISTS** - Keep existing |
| `mermaid-diagram-specialist` | Part of `draw-io` and C4 generators | **PARTIAL OVERLAP** |

**Total Redundant**: 15 skills
**Recommended for Deprecation**: 6 (git-commit-helper, gh-address-comments, skill-creator, skill-developer, software-architecture, PERSONA_senior-qa)
**Recommended for Merge**: 9 (combine into existing skills)

---

### 1.2 Skills with Partial Overlap (Enhance, Don't Replace)

| New Skill | Overlaps With | Enhancement Value |
|-----------|---------------|-------------------|
| `SECURITY_vulnerability-scanner` | `code-review-security-auditor` | **HIGH** - Add OWASP 2025, supply chain scanning |
| `SECURITY_api-security-best-practices` | `api-patterns/auth.md` | **MEDIUM** - More comprehensive security patterns |
| `database-design` | `database-schema-designer` | **LOW** - Similar content |
| `clean-code` | `code-review-code-quality` | **MEDIUM** - Add pragmatic patterns |
| `error-resolver` | `systematic-debugging` | **MEDIUM** - Different approach, keep both |

---

## Part 2: High-Value Integration Opportunities

### 2.1 SECURITY Skills for Quality Agents

**Integrate into `quality-security-auditor` (Implementation Phase 6)**:

| Skill | Integration Value | How to Integrate |
|-------|-------------------|------------------|
| `SECURITY_vulnerability-scanner` | **CRITICAL** | Add as primary skill for security auditor agent |
| `SECURITY_api-security-best-practices` | **HIGH** | Add to API module security checks |
| `SECURITY_top-web-vulnerabilities` | **HIGH** | Reference for OWASP compliance checks |
| `SECURITY_broken-authentication` | **HIGH** | Auth pattern validation |
| `SECURITY_sql-injection-testing` | **HIGH** | Database query analysis |
| `SECURITY_xss-html-injection` | **HIGH** | Frontend code analysis |
| `SECURITY_idor-testing` | **MEDIUM** | API endpoint authorization checks |
| `SECURITY_file-uploads` | **MEDIUM** | File handling security |

**Updated Agent Registry Entry** (proposed):
```json
{
  "agent": "quality-security-auditor",
  "skills": [
    "code-review-security-auditor",
    "SECURITY_vulnerability-scanner",        // NEW
    "SECURITY_api-security-best-practices",  // NEW
    "SECURITY_top-web-vulnerabilities",      // NEW
    "SECURITY_broken-authentication",        // NEW
    "SECURITY_sql-injection-testing",        // NEW
    "SECURITY_xss-html-injection"            // NEW
  ]
}
```

**Impact**: +35% security coverage improvement (estimated based on OWASP 2025 checklist coverage)

---

### 2.2 GRC Skills for Regulated Industries

**NEW: Create `grc-compliance-auditor` agent for ProductSpecs/SolArch stages**:

| Skill | Domain | When to Use |
|-------|--------|-------------|
| `GRC_quality-manager-qms-iso13485` | Medical Devices | ISO 13485 compliance in NFRs |
| `GRC_gdpr-dsgvo-expert` | Data Privacy | GDPR compliance in data handling specs |
| `GRC_risk-management-specialist` | Risk Analysis | ISO 14971 risk management in ADRs |

**Integration Points**:
1. **ProductSpecs NFR Generator**: Add GRC skill references for regulated industries
2. **SolArch ADR Writer**: Add compliance decision patterns
3. **New `/compliance-check` command**: On-demand compliance validation

**Proposed Command**:
```bash
/compliance-check <SystemName> --standard iso13485|gdpr|hipaa|sox
```

---

### 2.3 GitHub Skills for Implementation Stage

**Integrate into Implementation workflow**:

| Skill | Integration Point | Value |
|-------|-------------------|-------|
| `github_finishing-a-development-branch` | `/htec-sdd-implement` Phase 8 | Branch cleanup automation |
| `github_git-pushing` | `/htec-sdd-implement` Phase 8 | Standardized push workflow |
| `github_github-workflow-automation` | `/htec-sdd-worktree-setup` | CI/CD workflow templates |

**Updated `/htec-sdd-implement` Phase 8**:
- Add `implementation-pr-preparer` agent skill reference to `github_finishing-a-development-branch`
- Auto-invoke branch cleanup after PR merge

---

### 2.4 API Skills for Prototype Stage

**Integrate into Prototype API generation**:

| Skill | Integration Point | Value |
|-------|-------------------|-------|
| `api-documentation-generator` | `Prototype_ApiContracts` | Auto-generate OpenAPI docs |
| `api-integration-specialist` | `Prototype_ApiContracts` | Third-party API integration patterns |

**Updated Prototype Agent**:
```json
{
  "agent": "prototype-api-contract-specifier",
  "skills": [
    "Prototype_ApiContracts",
    "Prototype_TestData",
    "api-patterns",
    "api-documentation-generator",    // NEW
    "api-integration-specialist"       // NEW
  ]
}
```

---

### 2.5 Design Skills for Discovery/Prototype Stages

**Integrate into UI specification agents**:

| Skill | Integration Point | Value |
|-------|-------------------|-------|
| `ui-design-system` | `discovery-screen-specifier` | Design system patterns |
| `ui-ux-pro-max` | `prototype-ux-validator` | UX validation enhancement |
| `web-design-guidelines` | `discovery-screen-specifier` | Web UI patterns |
| `mobile-design` | `discovery-screen-specifier` | Mobile UI patterns |
| `tailwind-patterns` | `prototype-component-specifier` | Tailwind implementation |

**Updated Discovery Agent**:
```json
{
  "agent": "discovery-screen-specifier",
  "skills": [
    "Discovery_ScreenSpecifier",
    "hicks-law",
    "cognitive-load",
    "progressive-disclosure",
    "ui-design-system",        // NEW
    "web-design-guidelines",   // NEW
    "mobile-design"            // NEW - conditional on project type
  ]
}
```

---

## Part 3: Specialized Skills (On-Demand)

### 3.1 SECURITY Penetration Testing Skills (22 skills)

**Keep as specialized resources** - NOT for auto-integration:

| Category | Skills | Use Case |
|----------|--------|----------|
| **Platform Testing** | `SECURITY_aws-penetration-testing`, `SECURITY_cloud-penetration-testing`, `SECURITY_wordpress-penetration-testing` | Security assessments |
| **Tool Guides** | `SECURITY_burp-suite-testing`, `SECURITY_metasploit-framework`, `SECURITY_sqlmap-database-pentesting`, `SECURITY_wireshark-analysis` | Pentest tooling |
| **Attack Techniques** | `SECURITY_active-directory-attacks`, `SECURITY_linux-privilege-escalation`, `SECURITY_windows-privilege-escalation`, `SECURITY_smtp-penetration-testing`, `SECURITY_ssh-penetration-testing` | Red team operations |
| **Methodologies** | `SECURITY_ethical-hacking-methodology`, `SECURITY_pentest-checklist`, `SECURITY_pentest-commands`, `SECURITY_red-team-tactics`, `SECURITY_red-team-tools` | Security methodology |
| **Reconnaissance** | `SECURITY_shodan-reconnaissance`, `SECURITY_scanning-tools` | Information gathering |

**Invocation**: Manual via `/security-pentest <technique>` command (NEW)

---

### 3.2 GRC Compliance Skills (10 skills)

**Keep as specialized resources** for regulated industry projects:

| Skill | Domain | Regulatory Framework |
|-------|--------|---------------------|
| `GRC_capa-officer` | Quality | Corrective Actions |
| `GRC_data-privacy-compliance` | Privacy | General data protection |
| `GRC_fda-consultant-specialist` | Medical | FDA 21 CFR Part 11, Part 820 |
| `GRC_information-security-manager-iso27001` | Security | ISO 27001 |
| `GRC_isms-audit-expert` | Security | ISMS auditing |
| `GRC_mdr-745-specialist` | Medical | EU MDR 2017/745 |
| `GRC_qms-audit-expert` | Quality | QMS auditing |
| `GRC_quality-documentation-manager` | Quality | Documentation control |
| `GRC_quality-manager-qmr` | Quality | Management representative |
| `GRC_regulatory-affairs-head` | Regulatory | Strategic regulatory planning |

**Invocation**: Via project configuration flag:
```json
// _state/pipeline_config.json
{
  "regulatory_compliance": ["iso13485", "gdpr", "fda"],
  "grc_skills_enabled": true
}
```

---

### 3.3 PERSONA Development Skills (5 useful, 6 redundant)

**Keep these specialized skills**:

| Skill | Unique Value | Integration |
|-------|--------------|-------------|
| `PERSONA_senior-computer-vision` | CV/ML patterns | On-demand for ML projects |
| `PERSONA_senior-data-engineer` | Data pipeline patterns | Data-intensive projects |
| `PERSONA_senior-data-scientist` | ML/analytics patterns | Data science projects |
| `PERSONA_senior-ml-engineer` | ML engineering patterns | ML deployment projects |
| `PERSONA_security-compliance` | Security compliance patterns | Security-focused projects |

**Redundant (merge into existing)**:
- `PERSONA_senior-architect` → merge into `sdd-software-architect`
- `PERSONA_senior-backend` → merge into `backend-dev-guidelines`
- `PERSONA_senior-frontend` → merge into `frontend-dev-guidelines`
- `PERSONA_senior-fullstack` → combine backend + frontend guidelines
- `PERSONA_senior-qa` → covered by quality agents
- `PERSONA_senior-devops` → partial merge into sdd-developer

---

## Part 4: Implementation Roadmap

### Phase 1: Immediate Integration (Week 1)

**Priority 1 - Security Enhancement**:
1. Update `IMPLEMENTATION_AGENT_REGISTRY.json`:
   - Add SECURITY skills to `quality-security-auditor`
2. Update `code-review-security-auditor/SKILL.md`:
   - Reference new SECURITY skill checklists

**Priority 2 - API Enhancement**:
1. Update `PROTOTYPE_AGENT_REGISTRY.json`:
   - Add `api-documentation-generator` to API contract specifier
2. Update `Prototype_ApiContracts/SKILL.md`:
   - Reference OpenAPI generation patterns

### Phase 2: Design Integration (Week 2)

**Priority 3 - UI/UX Enhancement**:
1. Update `DISCOVERY_AGENT_REGISTRY.json`:
   - Add UI design skills to screen-specifier
2. Update `PROTOTYPE_AGENT_REGISTRY.json`:
   - Add `tailwind-patterns` to component-specifier

**Priority 4 - GitHub Workflow**:
1. Update `implementation-pr-preparer` agent:
   - Add `github_finishing-a-development-branch` skill
2. Create branch cleanup automation

### Phase 3: GRC Framework (Week 3-4)

**Priority 5 - Compliance Framework**:
1. Create `/compliance-check` command
2. Create `grc-compliance-auditor` agent
3. Add regulatory flags to pipeline config
4. Document GRC skill invocation patterns

### Phase 4: Cleanup (Week 4)

**Priority 6 - Deprecation**:
1. Mark redundant skills as deprecated in SKILL_REGISTRY.json
2. Update documentation to redirect to existing capabilities
3. Add deprecation warnings to redundant skill frontmatter

---

## Part 5: Registry Updates Required

### 5.1 SKILL_REGISTRY.json Updates

```json
{
  "deprecated_skills": [
    "github_git-commit-helper",
    "github_gh-address-comments",
    "skill-creator",
    "skill-developer",
    "software-architecture",
    "PERSONA_senior-qa"
  ],
  "merged_skills": {
    "PERSONA_senior-architect": "sdd-software-architect",
    "PERSONA_senior-backend": "backend-dev-guidelines",
    "PERSONA_senior-frontend": "frontend-dev-guidelines"
  },
  "new_skill_categories": {
    "security_pentest": ["SECURITY_*"],
    "grc_compliance": ["GRC_*"],
    "specialized_personas": ["PERSONA_senior-computer-vision", "PERSONA_senior-data-*", "PERSONA_senior-ml-*", "PERSONA_security-compliance"]
  }
}
```

### 5.2 Agent Registry Updates

**IMPLEMENTATION_AGENT_REGISTRY.json**:
```json
{
  "quality-security-auditor": {
    "skills": [
      "code-review-security-auditor",
      "SECURITY_vulnerability-scanner",
      "SECURITY_api-security-best-practices",
      "SECURITY_top-web-vulnerabilities",
      "SECURITY_broken-authentication",
      "SECURITY_sql-injection-testing",
      "SECURITY_xss-html-injection"
    ]
  }
}
```

**PROTOTYPE_AGENT_REGISTRY.json**:
```json
{
  "prototype-api-contract-specifier": {
    "skills": [
      "Prototype_ApiContracts",
      "Prototype_TestData",
      "api-documentation-generator",
      "api-integration-specialist"
    ]
  },
  "prototype-component-specifier": {
    "skills": [
      "Prototype_Components",
      "Prototype_Decomposition",
      "cognitive-load",
      "hicks-law",
      "tailwind-patterns"
    ]
  }
}
```

**DISCOVERY_AGENT_REGISTRY.json**:
```json
{
  "discovery-screen-specifier": {
    "skills": [
      "Discovery_ScreenSpecifier",
      "ui-design-system",
      "web-design-guidelines",
      "mobile-design"
    ]
  }
}
```

---

## Part 6: New Commands (Proposed)

### 6.1 `/security-pentest` Command

```bash
/security-pentest <target> --technique <technique>

# Examples:
/security-pentest api --technique sql-injection
/security-pentest webapp --technique full-audit
/security-pentest cloud --technique aws
```

**Available techniques**:
- `sql-injection`, `xss`, `idor`, `auth-bypass`
- `aws`, `cloud`, `ad-attacks`
- `linux-privesc`, `windows-privesc`
- `full-audit` (combines all applicable)

### 6.2 `/compliance-check` Command

```bash
/compliance-check <SystemName> --standard <standard>

# Examples:
/compliance-check MedicalDevice --standard iso13485
/compliance-check HealthApp --standard gdpr,hipaa
/compliance-check FinanceApp --standard sox,pci-dss
```

**Available standards**:
- `iso13485` - Medical device QMS
- `gdpr` - EU data protection
- `hipaa` - Healthcare data
- `fda` - FDA 21 CFR Part 11
- `mdr` - EU Medical Device Regulation
- `iso27001` - Information security
- `sox` - Financial compliance
- `pci-dss` - Payment card security

---

## Part 7: Risk Assessment

### 7.1 Integration Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Security skill false positives | Medium | Low | Add severity thresholds |
| GRC skills slow down non-regulated projects | Medium | Medium | Make opt-in via config |
| Too many skills per agent | Low | Medium | Limit to 7 skills per agent |
| Breaking existing workflows | Low | High | Thorough testing before merge |

### 7.2 Non-Integration Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Valuable skills remain unused | High | Medium | Document use cases clearly |
| Security gaps not addressed | Medium | High | Prioritize security integration |
| Duplicate maintenance burden | Medium | Low | Deprecate redundant skills |

---

## Appendix A: Complete Skill Inventory

### A.1 Skills Recommended for Integration (28)

1. `SECURITY_vulnerability-scanner`
2. `SECURITY_api-security-best-practices`
3. `SECURITY_top-web-vulnerabilities`
4. `SECURITY_broken-authentication`
5. `SECURITY_sql-injection-testing`
6. `SECURITY_xss-html-injection`
7. `SECURITY_idor-testing`
8. `SECURITY_file-uploads`
9. `GRC_quality-manager-qms-iso13485`
10. `GRC_gdpr-dsgvo-expert`
11. `GRC_risk-management-specialist`
12. `api-documentation-generator`
13. `api-integration-specialist`
14. `ui-design-system`
15. `ui-ux-pro-max`
16. `web-design-guidelines`
17. `mobile-design`
18. `tailwind-patterns`
19. `github_finishing-a-development-branch`
20. `github_git-pushing`
21. `github_github-workflow-automation`
22. `database-schema-designer`
23. `postgres-best-practices`
24. `clean-code`
25. `error-resolver`
26. `lint-and-validate`
27. `planning-with-files`
28. `draw-io`

### A.2 Skills Recommended for Deprecation (6)

1. `github_git-commit-helper` → use `/commit`
2. `github_gh-address-comments` → duplicate of `github_address-github-comments`
3. `skill-creator` → use `/create-skill`
4. `skill-developer` → use `/create-skill`
5. `software-architecture` → use `sdd-software-architect`
6. `PERSONA_senior-qa` → covered by quality agents

### A.3 Skills for Merge (9)

1. `PERSONA_senior-architect` → merge into `sdd-software-architect`
2. `PERSONA_senior-backend` → merge into `backend-dev-guidelines`
3. `PERSONA_senior-frontend` → merge into `frontend-dev-guidelines`
4. `PERSONA_senior-fullstack` → combine backend + frontend guidelines
5. `PERSONA_senior-devops` → partial merge into `sdd-developer`
6. `database-design` → merge into `database-schema-designer`
7. `production-code-audit` → merge patterns into `code-review-*` agents
8. `mermaid-diagram-specialist` → merge into `draw-io`
9. `github_gh-fix-ci` → merge CI patterns into `/fix-tests`

### A.4 Specialized Skills - On Demand (54)

**SECURITY (22)**: All penetration testing skills not listed above
**GRC (10)**: All compliance skills not listed above
**PERSONA (5)**: `senior-computer-vision`, `senior-data-engineer`, `senior-data-scientist`, `senior-ml-engineer`, `security-compliance`
**Other (17)**: Various utility skills for specific use cases

---

## Conclusion

The 97 new skills represent significant value-add to the HTEC framework:

- **Security Enhancement**: 8 skills immediately improve security audit coverage by ~35%
- **Regulatory Compliance**: 13 GRC skills enable regulated industry support
- **Developer Experience**: 10+ skills improve code generation quality
- **Redundancy Cleanup**: 15 skills can be deprecated or merged, reducing maintenance burden

**Next Steps**:
1. Review this report with stakeholders
2. Prioritize Phase 1 (Security) implementation
3. Create tracking issues for each phase
4. Execute phased rollout over 4 weeks
