# Maintainability-First Architectural Principle

**Version**: 1.0.0
**Status**: Active
**Scope**: Framework-wide
**Injected**: 2026-01-27

---

## Overview

This document describes the **Maintainability-First Principle**, a core architectural decision-making guideline embedded across all HTEC accelerator artifacts that shape or implement the final code solution.

---

## The Principle

**Optimize for maintainability, not simplicity.**

When making architectural and implementation decisions:

1. **Prioritize long-term maintainability** over short-term simplicity
2. **Minimize complexity** by being strategic with dependencies and libraries
3. **Avoid "simplicity traps"** - adding libraries without considering downstream debugging and maintenance burden
4. **Think 6 months ahead** - will this decision make debugging easier or harder?
5. **Use libraries strategically** - not avoided, but chosen carefully with justification

---

## Rationale

### The Problem

Traditional "simplicity" often means "just add a library" - which creates:

- **Downstream Complexity**: Multiple dependency versions, transitive dependency conflicts
- **Debugging Nightmares**: Stack traces through 5 abstraction layers
- **Maintenance Burden**: Breaking changes, security patches, upgrade treadmills
- **Cognitive Overload**: Understanding "magic" abstractions takes longer than reading explicit code

### The Solution

**Maintainability** as the primary metric means:

- **Readable > Compact**: Explicit code beats clever one-liners
- **Debuggable > Abstract**: Clear error paths beat hidden metaprogramming
- **Stable > Novel**: Proven patterns beat trendy architectures
- **Justified > Convenient**: Every dependency must earn its place

---

## Decision-Making Protocol

### When the Decision is Clear

**Make it autonomously** and document the rationale in:
- ADR "Decision" section (for architecture decisions)
- Code comments (for implementation decisions)
- Task specifications (for planning decisions)

### When the Decision is Unclear

**Use `AskUserQuestion` tool** with:

```typescript
{
  question: "Should we [X] or [Y]?",
  header: "Architecture",
  options: [
    {
      label: "Option 1",
      description: "Pros: {...} | Cons: {...} | Maintainability: {...}"
    },
    {
      label: "Option 2",
      description: "Pros: {...} | Cons: {...} | Maintainability: {...}"
    },
    {
      label: "Option 3 (Recommended)",
      description: "Pros: {...} | Cons: {...} | Maintainability: {...}"
    }
  ]
}
```

**Required comparison dimensions**:
- Maintainability impact (short-term vs long-term)
- Complexity implications (cognitive load, debugging difficulty)
- Dependency graph (direct + transitive dependencies)
- 6-month projection (will this be easier or harder to debug?)

---

## Application by Agent Type

### 1. ADR Writers (solarch-adr-*)

When evaluating technology options:

- ✅ **Evaluate maintenance burden** as primary decision driver
- ✅ **Document dependency impact** in "Consequences" section
- ✅ **Prefer proven, stable technologies** over trendy ones
- ✅ **Include "Maintenance Complexity"** in comparison matrices
- ✅ **Show 6-month and 2-year projections** for stakeholders

### 2. Technology Researcher (solarch-tech-researcher)

Enhanced research dimensions:

| Criterion | Weight | Evaluation Method |
|-----------|--------|-------------------|
| Maintenance Burden | 15% | Update frequency, breaking changes, migration complexity |
| Debugging Experience | 10% | Error messages, stack traces, community support quality |
| Dependency Graph | 10% | Transitive dependencies, bundle size, supply chain risk |

**New metrics**:
- Debugging Experience Score (error quality, stack clarity)
- Dependency Footprint (direct + transitive count)
- Maintenance Risk Score (breaking changes + patches frequency)

### 3. Implementation Developer (implementation-developer)

**Before adding any dependency**, run this checklist:

1. ✅ Can this be solved with native APIs or existing dependencies?
2. ✅ Is the library well-maintained (releases in last 6 months)?
3. ✅ Does it have minimal dependencies (check `node_modules` impact)?
4. ✅ Will this make debugging easier or harder in 6 months?
5. ✅ Is the bundle size impact acceptable?

**Code quality standards**:
- Prefer explicit code over clever abstractions
- Prefer readable code over "DRY at all costs"
- Prefer boring, proven patterns over novel architectures
- Comment WHY, not WHAT

### 4. Code Quality Reviewer (quality-code-quality)

**New review checks**:

**Maintainability Anti-Patterns** 🚩:
- Unnecessary Dependency (library for <10 LOC functionality)
- Over-Abstraction (5+ layers of indirection)
- Premature Generalization (abstract interfaces with single impl)
- Clever Code (one-liner requiring 5 minutes to understand)
- Dependency Hell (multiple versions of same library)
- Magic Abstractions (metaprogramming hiding behavior)

**Maintainability Best Practices** ✅:
- Explicit Over Clever (readable > compact)
- Boring Code (proven patterns > novel architectures)
- Small Functions (<50 lines, single responsibility)
- Minimal Dependencies (justify every import)
- Self-Documenting (names explain intent)
- Debuggable (clear errors, good stack traces)

**New metric**:
- **Maintainability Score** (0-100):
  - Readability (30 points)
  - Dependency footprint (20 points)
  - Debugging ease (20 points)
  - Documentation quality (15 points)
  - Complexity management (15 points)

### 5. Tech Lead (planning-tech-lead)

**For each task**, include:

1. **Dependency Decision**: Why new libraries are needed (or avoided)
2. **Complexity Budget**: Cognitive load estimate (simple, moderate, complex)
3. **Debugging Projection**: How hard to debug in 6 months?
4. **Refactoring Risk**: One-way door or easily reversible?

**New strategy question**:
```
Question: "What is your dependency management strategy?"

Options:
1. Liberal Dependencies (Use libraries for most tasks)
2. Conservative Dependencies (Minimize, justify each one) (Recommended)
3. Zero External Dependencies (Build everything custom)
4. Balanced Approach (Use stable, well-maintained libraries only)
```

### 6. ProductSpecs Module Specifiers

**Add to each module spec**:

```markdown
### Dependency Recommendations

| Dependency | Purpose | Justification | Alternatives | Maintenance Risk |
|------------|---------|---------------|--------------|------------------|
| {name} | {feature} | {why} | {native? custom?} | {low/med/high} |

### Maintainability Considerations

- **Complexity Level**: {Low/Medium/High}
- **Dependency Footprint**: {N libraries, M transitive deps}
- **Debugging Difficulty**: {Easy/Moderate/Hard}
- **Refactoring Risk**: {Easily refactored / Hard to change}

⚠️ **If High Complexity**: Provide architectural alternatives.
```

---

## Scope of Injection

### Artifacts Modified (39 total)

#### P0 - Critical (21 artifacts)

**Solution Architecture**:
- solarch-orchestrator.md
- solarch-adr-foundation-writer.md ⭐
- solarch-adr-communication-writer.md
- solarch-adr-operational-writer.md
- solarch-tech-researcher.md ⭐
- solarch-arch-evaluator.md
- /solarch command

**Planning**:
- planning-tech-lead.md ⭐
- /htec-sdd-tasks command

**Implementation**:
- implementation-developer.md ⭐
- implementation-test-designer.md
- /htec-sdd-implement command

**Quality/Review**:
- quality-code-quality.md ⭐
- quality-bug-hunter.md
- quality-security-auditor.md
- implementation-pr-preparer.md
- /htec-sdd-review command

**ProductSpecs**:
- productspecs-orchestrator.md
- productspecs-ui-module-specifier.md
- productspecs-api-module-specifier.md
- productspecs-nfr-generator.md

#### P1 - High (10 artifacts)

- solarch-integration-analyst.md
- solarch-cost-estimator.md
- solarch-risk-scorer.md
- planning-code-explorer.md
- implementation-test-automation-engineer.md
- quality-contracts-reviewer.md
- quality-test-coverage.md
- solarch-performance-scenarios.md
- solarch-security-scenarios.md
- solarch-reliability-scenarios.md

#### P2 - Medium (8 artifacts)

- implementation-documenter.md
- quality-accessibility-auditor.md
- solarch-usability-scenarios.md
- solarch-c4-context-generator.md
- solarch-c4-container-generator.md
- solarch-c4-component-generator.md
- solarch-c4-deployment-generator.md
- /productspecs command

---

## Example Scenarios

### ✅ Good: Custom Lightweight Utility

**Scenario**: Need to debounce user input

**Decision**:
- Option 1: Add lodash.debounce (17KB, 15 dependencies)
- Option 2: Custom implementation (10 lines, 0 dependencies) ✅ **CHOSEN**

**Rationale**:
- Maintainability wins: No dependency, easier debugging, smaller bundle
- 10 lines of code vs 17KB + 15 transitive dependencies
- Clear implementation, no version conflicts

### ❌ Bad: Adding Multiple Utility Libraries

**Scenario**: Need date formatting, array utilities, string helpers

**Decision**:
- Option 1: moment.js (232KB) + lodash (71KB) + validator.js (44KB) ❌ **AVOID**
- Option 2: Native Intl + Array methods + custom validators ✅ **CHOSEN**

**Rationale**:
- Creates debugging nightmare: 3 libraries, 347KB, version conflicts
- Native APIs are sufficient for most cases
- Custom validators are 5-10 lines each, fully debuggable

---

## Success Criteria

1. ✅ All 39 artifacts contain the maintainability principle
2. ✅ Agents successfully spawn and execute with principle
3. ✅ Code Quality agent detects maintainability anti-patterns
4. ✅ ADR generation includes "Maintenance Burden" in criteria
5. ✅ Implementation developer justifies dependency additions
6. ✅ Tech Lead presents dependency strategy questions

---

## Verification

Run this command to verify injection:

```bash
grep -r "🎯 Guiding Architectural Principle" .claude/ | wc -l
# Expected: 39
```

---

## Related Documentation

- **CORE_RULES.md**: Framework-wide rules
- **CLAUDE.md**: Project overview and workflows
- **Skills_and_Registry_System.md**: Skill maintenance reference
- **Agent_Spawning_Architecture.md**: Multi-agent coordination

---

## Change History

| Date | Version | Change |
|------|---------|--------|
| 2026-01-27 | 1.0.0 | Initial injection across 39 artifacts |

---

**Principle Status**: ✅ **ACTIVE** - Enforced across all stages

**Contact**: HTEC Framework Maintainers
