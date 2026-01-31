# SolArch v3.0 Multi-Agent Architecture

**Version**: 3.0.0 (Hierarchical Architecture with Architecture Board)
**Date**: 2026-01-27
**Status**: Active

---

## Overview

SolArch v3.0 introduces a **hierarchical multi-agent system** with:

- **Architecture Board**: 3 Architect personas for collaborative decision-making
- **Weighted Voting Consensus**: Decisions made with confidence scores
- **Self-Validation System**: Per-ADR quality checks using Haiku
- **4 Entry Points**: System, subsystem, layer, single-ADR
- **Auto-Rework with OBVIOUS Notification**: Max 2 attempts before user escalation

---

## 1. Hierarchical Architecture

```
/solarch <SystemName> [OPTIONS]
    │
    v
┌─────────────────────────────────────────────────────────────────────────┐
│ solarch-orchestrator (Master, Sonnet)                                    │
│ - Parse flags (--subsystem/--layer/--adr/--quality)                     │
│ - Scope filtering (4 entry points)                                       │
│ - Load priority map (P0/P1/P2)                                          │
│ - Spawn sub-orchestrators                                                │
└─────────────────────────────────────────────────────────────────────────┘
    │
    ├─> CP-3: Research [Parallel: 3 agents]
    │   - solarch-tech-researcher (Sonnet)
    │   - solarch-integration-analyst (Sonnet)
    │   - solarch-cost-estimator (Haiku)
    │
    ├─> CP-4-9: ADR Generation via Architecture Board
    │   └─> Task(solarch-adr-board-orchestrator) [Sub-Orchestrator]
    │       │
    │       ├─> For each ADR in scope:
    │       │   ├─> ADR Writer generates draft
    │       │   ├─> Self-Validator (Haiku) validates (15 checks)
    │       │   ├─> Architecture Board reviews (3 Architects, Sonnet)
    │       │   ├─> Weighted voting consensus
    │       │   ├─> [Confidence < 60%] -> AskUserQuestion
    │       │   └─> [Auto-rework needed] -> Retry (max 2) with OBVIOUS notice
    │       │
    │       └─> Merge gate (consolidated ADR registry)
    │
    └─> CP-10: Global Validation [BLOCKING]
        └─> Task(solarch-validation-orchestrator) [Sub-Orchestrator]
            │
            ├─> [Parallel: 4 validators]
            │   - solarch-adr-consistency-validator
            │   - solarch-adr-completeness-validator
            │   - solarch-traceability-validator
            │   - solarch-coverage-validator
            │
            └─> Blocking gate check (100% coverage required)
```

---

## 2. Architecture Board

### 2.1 Three Architect Personas

| Architect | Agent | Focus | Personality |
|-----------|-------|-------|-------------|
| **Pragmatist** | `solarch-architect-pragmatist` | Scalability, cost, delivery | Practical, cost-conscious |
| **Perfectionist** | `solarch-architect-perfectionist` | Security, compliance | Thorough, risk-averse |
| **Skeptic** | `solarch-architect-skeptic` | Maintainability, tech debt | Questions assumptions |

### 2.2 Evaluation Criteria by Architect

#### Pragmatist (Scalability Focus)
| Criterion | Weight |
|-----------|--------|
| Scalability (10x load) | 30% |
| Cost efficiency | 25% |
| Delivery feasibility | 25% |
| Operational complexity | 20% |

#### Perfectionist (Security Focus)
| Criterion | Weight |
|-----------|--------|
| OWASP Top 10 | 35% |
| Data protection (GDPR, PII) | 30% |
| Auth/AuthZ robustness | 20% |
| Audit trails | 15% |

#### Skeptic (Maintainability Focus)
| Criterion | Weight |
|-----------|--------|
| Code maintainability | 35% |
| Debugging difficulty | 25% |
| Dependency justification | 25% |
| Maintainability principle alignment | 15% |

### 2.3 Weighted Voting Consensus

**Algorithm**:
```
Score = Sum(Vote × Confidence) / Sum(Confidence)
Dissent = (Max Confidence - Min Confidence) / Max Confidence
```

**Thresholds**:
- **Confidence threshold**: >= 60% average confidence
- **Dissent threshold**: <= 40% dissent score
- **Escalation trigger**: Either threshold violated

**Decision Flow**:
1. If `Confidence >= 60%` AND `Dissent <= 40%` → **APPROVE** (use highest-confidence option)
2. If `Confidence < 60%` OR `Dissent > 40%` → **ESCALATE** to user via `AskUserQuestion`

---

## 3. Self-Validation System

### 3.1 Per-ADR Validation (15 Checks)

**Agent**: `solarch-self-validator` (Haiku)
**Performance**: ~$0.05/validation, <15 seconds

#### Frontmatter Checks (5 points)
| # | Check | Criteria |
|---|-------|----------|
| 1 | ID Format | `id` matches `ADR-NNN` |
| 2 | Title Present | `title` exists, > 10 chars |
| 3 | Status Valid | `proposed`, `accepted`, `deprecated`, `superseded` |
| 4 | Date Present | ISO 8601 format |
| 5 | Decision Makers | At least one stakeholder |

#### Context Section Checks (3 points)
| # | Check | Criteria |
|---|-------|----------|
| 6 | Problem Statement | Clear, > 50 chars |
| 7 | Constraints Listed | At least one constraint |
| 8 | Assumptions Listed | At least one assumption |

#### Decision Section Checks (4 points)
| # | Check | Criteria |
|---|-------|----------|
| 9 | Rationale Present | Why, not just what |
| 10 | Alternatives Count | >= 2 alternatives considered |
| 11 | Consequences | Positive AND negative |
| 12 | Impact Assessment | Scope, effort, risk |

#### Traceability Checks (3 points)
| # | Check | Criteria |
|---|-------|----------|
| 13 | Requirements Links | At least one REQ-XXX |
| 14 | Module Links | MOD-XXX IDs (if applicable) |
| 15 | Related ADRs | References to related ADRs |

### 3.2 Auto-Rework Protocol

```
Attempt 1: Generate ADR
    │
    v
Self-Validation
    │-> [PASS, score >= 70] -> Continue to Board
    │-> [FAIL OR score < 70] -> Auto-Rework

Attempt 2: Regenerate with Feedback
    │
    v
Self-Validation
    │-> [PASS] -> Continue to Board
    │-> [FAIL] -> ESCALATE TO USER (with OBVIOUS notification)
```

### 3.3 OBVIOUS Notification (MANDATORY)

When auto-rework occurs, display:

```
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!                                                   !!
!!  AUTO-REWORK ALERT                                !!
!!                                                   !!
!!  ADR-007 required automatic rework (1/2 attempts) !!
!!                                                   !!
!!  Original Issues:                                 !!
!!  - Missing decision rationale                     !!
!!  - Only 1 alternative considered (need >= 2)      !!
!!                                                   !!
!!  Fixes Applied:                                   !!
!!  - Added detailed rationale section               !!
!!  - Added 2 additional alternatives                !!
!!                                                   !!
!!  PLEASE REVIEW THIS DECISION CAREFULLY            !!
!!                                                   !!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
```

---

## 4. Entry Points System

### 4.1 Four Entry Point Types

| Entry Point | Flag | Example | Scope |
|-------------|------|---------|-------|
| **System-Level** | (default) | `/solarch InventorySystem` | All ADRs |
| **Subsystem-Level** | `--subsystem` | `--subsystem authentication` | Subsystem ADRs |
| **Layer-Level** | `--layer` | `--layer frontend` | Layer ADRs |
| **ADR-Level** | `--adr` | `--adr ADR-007` | Single ADR |

### 4.2 Time Savings

| Entry Point | ADRs Processed | Estimated Time | Savings |
|-------------|----------------|----------------|---------|
| System-Level | 12/12 (100%) | 68 min | 0% (baseline) |
| Subsystem-Level | 4/12 (33%) | 23 min | 66% |
| Layer-Level | 3/12 (25%) | 17 min | 75% |
| ADR-Level | 1/12 (8%) | 6 min | 91% |

### 4.3 Quality Modes

| Mode | Flag | Board Reviews | Use Case |
|------|------|---------------|----------|
| Standard | `--quality standard` | P0 ADRs only | Default, balanced |
| Critical | `--quality critical` | ALL ADRs | High-stakes projects |

---

## 5. Agent Registry

### 5.1 Agent Categories (v3.0)

| Category | Count | Model | Agents |
|----------|-------|-------|--------|
| **Orchestration** | 3 | Sonnet | Master, ADR-Board, Validation |
| **Research** | 3 | Sonnet/Haiku | Tech, Integration, Cost |
| **Architecture Board** | 3 | Sonnet | Pragmatist, Perfectionist, Skeptic |
| **ADR Writers** | 4 | Sonnet | Foundation, Communication, Operational, Emergency |
| **Validation** | 5 | Haiku | Self-Validator + 4 Global |
| **C4 Diagrams** | 4 | Haiku | Context, Container, Component, Deployment |
| **Quality Scenarios** | 4 | Haiku | Perf, Security, Reliability, Usability |
| **Evaluation** | 2 | Sonnet/Haiku | Arch-Evaluator, Risk-Scorer |

**Total**: 28 agents

### 5.2 Agent Files

#### Orchestrators
- `.claude/agents/solarch-orchestrator.md` (Master)
- `.claude/agents/solarch-adr-board-orchestrator.md` (ADR Board)
- `.claude/agents/solarch-validation-orchestrator.md` (Validation)

#### Architecture Board
- `.claude/agents/solarch-architect-pragmatist.md`
- `.claude/agents/solarch-architect-perfectionist.md`
- `.claude/agents/solarch-architect-skeptic.md`
- `.claude/agents/solarch-board-consensus.md`

#### Validation
- `.claude/agents/solarch-self-validator.md`

---

## 6. Configuration Schemas

### 6.1 Filtered Scope Schema

**File**: `_state/solarch_filtered_scope.json`

```json
{
  "$schema": "solarch-filtered-scope-v1",
  "system_name": "InventorySystem",
  "entry_point": {
    "type": "subsystem",
    "value": "authentication"
  },
  "quality_mode": "critical",
  "adrs": [
    {
      "id": "ADR-007",
      "title": "Authentication Strategy",
      "priority": "P0",
      "subsystem": "authentication",
      "layer": "backend",
      "needs_board_review": true
    }
  ],
  "total_adrs": 4,
  "p0_count": 2,
  "estimated_time_minutes": 23
}
```

### 6.2 Board Decision Schema

**File**: `_state/solarch_board_decisions.json`

```json
{
  "$schema": "solarch-board-decision-v1",
  "adr_id": "ADR-007",
  "votes": [
    {
      "architect": "pragmatist",
      "option": "A",
      "confidence": 90,
      "rationale": "JWT is simpler and scales better",
      "scores": {
        "scalability": 85,
        "cost_efficiency": 90,
        "delivery_feasibility": 80,
        "operational_complexity": 75
      }
    },
    {
      "architect": "perfectionist",
      "option": "B",
      "confidence": 75,
      "rationale": "Session-based has better revocation",
      "scores": {
        "owasp_top_10": 85,
        "data_protection": 90,
        "auth_authz": 80,
        "audit_trails": 85
      }
    },
    {
      "architect": "skeptic",
      "option": "A",
      "confidence": 85,
      "rationale": "JWT has fewer moving parts",
      "scores": {
        "maintainability": 85,
        "debugging_difficulty": 80,
        "dependency_justification": 90,
        "maintainability_principle": 85
      }
    }
  ],
  "result": {
    "decision": "APPROVED",
    "winning_option": "A",
    "confidence": 84,
    "dissent": 0.15,
    "unanimous": false,
    "escalated": false
  },
  "auto_rework": {
    "occurred": false,
    "attempts": 0,
    "issues_fixed": []
  }
}
```

---

## 7. Quality Metrics

### 7.1 Performance Comparison

| Metric | v1.0 (Flat) | v3.0 (Hierarchical) |
|--------|-------------|---------------------|
| Quality Score | 75 | 92 (+23%) |
| Time (12 ADRs) | 45 min | 68 min (+50%) |
| Cost | $75 | $110 (+47%) |
| User Decisions | 0 | 2-5 (critical only) |

### 7.2 Success Criteria

**Quality**:
- [ ] Quality score improvement: 75 -> 92 (+23%)
- [ ] ADR consistency: 100% pass self-validation
- [ ] Traceability coverage: 100% pain points, 95%+ requirements

**User Experience**:
- [ ] Auto-rework notifications are OBVIOUS
- [ ] User escalation provides clear options
- [ ] Entry points reduce time by 66%+ for subsystem-level

**Technical**:
- [ ] Board consensus reached in 80%+ of cases
- [ ] User escalations limited to 2-5 per full run
- [ ] Self-validation time < 15s per ADR

---

## 8. Checkpoint Integration

### 8.1 Updated Checkpoint Flow

| CP | Phase | v3.0 Changes |
|----|-------|--------------|
| 0 | Init | Entry point parsing, scope filtering |
| 1 | Validate | No change |
| 2 | Context | No change |
| 3 | Strategy | Research agents parallel |
| 4-9 | Decisions | **ADR Board Orchestrator** with Architecture Board |
| 10 | Validation | **Validation Orchestrator** with 4 parallel validators |
| 11 | Glossary | No change |
| 12 | Final | No change |

### 8.2 Blocking Gates

| CP | Gate | Requirement |
|----|------|-------------|
| 1 | Input Validation | ProductSpecs CP8+, Prototype CP14+ |
| 10 | Global Validation | 100% pain point coverage, 100% P0 requirement coverage |

---

## 9. Command Reference

### 9.1 Available Commands

| Command | Mode | Description | Time Savings |
|---------|------|-------------|--------------|
| `/solarch` | Sequential | Full SolArch pipeline (13 checkpoints) - runs in main session | Baseline |
| **`/solarch-multiagent`** | **Multi-Agent** | **Hierarchical orchestration with Architecture Board - spawns agents for parallel execution** | **35-50%** |

### 9.2 Multi-Agent Command Syntax (RECOMMENDED)

```bash
/solarch-multiagent <SystemName> [--subsystem <name>] [--layer <name>] [--adr <id>] [--quality <mode>] [--resume] [--checkpoint N]
```

**Benefits of Multi-Agent Mode**:
- **65% context savings** (work distributed to agents)
- **35-50% time savings** (parallel execution at CP-3 and CP-10)
- **+23% quality improvement** (Architecture Board review)
- **Automatic escalation** when architect consensus fails

### 9.3 Sequential Command Syntax (Fallback)

```bash
/solarch <SystemName> [--subsystem <name>] [--layer <name>] [--adr <id>] [--quality <mode>]
```

**Use sequential mode when**:
- Debugging agent issues
- Need full visibility of all operations in main session
- Context window is not a concern

### 9.4 Examples

```bash
# Multi-Agent Mode (RECOMMENDED)
# System-level (all ADRs) - spawns 28 agents across checkpoints
/solarch-multiagent InventorySystem

# Subsystem-level (66% time savings)
/solarch-multiagent InventorySystem --subsystem authentication

# Layer-level (75% time savings)
/solarch-multiagent InventorySystem --layer frontend

# ADR-level (91% time savings)
/solarch-multiagent InventorySystem --adr ADR-007

# Quality critical mode (all ADRs get board review)
/solarch-multiagent InventorySystem --quality critical

# Combined
/solarch-multiagent InventorySystem --subsystem authentication --quality critical

# Resume from failure
/solarch-multiagent InventorySystem --resume

# Resume from specific checkpoint
/solarch-multiagent InventorySystem --resume --checkpoint 5

# Sequential Mode (Fallback)
/solarch InventorySystem
/solarch InventorySystem --subsystem authentication
```

### 9.5 Command Comparison

| Aspect | `/solarch` (Sequential) | `/solarch-multiagent` (Multi-Agent) |
|--------|-------------------------|-------------------------------------|
| Context Usage | HIGH (all in main session) | LOW (distributed to agents) |
| Execution Time | ~68 min (12 ADRs) | ~35-45 min (-35-50%) |
| Parallelism | None | CP-3 (3 agents), CP-4-9 (board), CP-10 (4 validators) |
| Quality | Good | Better (+23% via Architecture Board) |
| Architecture Board | No | Yes (3 architects vote on each ADR) |
| Auto-Rework | No | Yes (max 2 attempts with OBVIOUS notification) |
| User Escalation | No | Yes (when confidence < 60% or dissent > 40%) |

---

## 10. Related Documentation

| Document | Location |
|----------|----------|
| **Multi-Agent Command** | **`.claude/commands/solarch-multiagent.md`** |
| Sequential Command | `.claude/commands/solarch.md` |
| Orchestrator Agent | `.claude/agents/solarch-orchestrator.md` |
| ADR Board Orchestrator | `.claude/agents/solarch-adr-board-orchestrator.md` |
| Validation Orchestrator | `.claude/agents/solarch-validation-orchestrator.md` |
| Architect Agents | `.claude/agents/solarch-architect-*.md` |
| Self-Validator | `.claude/agents/solarch-self-validator.md` |
| Agent Registry | `.claude/skills/SOLARCH_AGENT_REGISTRY.json` |
| Command Reference | `.claude/commands/SOLARCH_COMMAND_REFERENCE.md` |
| Implementation Plan | `_state/SOLARCH_V2_IMPLEMENTATION_PLAN.md` |

---

**Document Status**: Active
**Last Updated**: 2026-01-29



 flowchart TD                                                                                                                                                                                          
      subgraph UserInput["🎯 User Command Layer"]                                                                                                                                                       
          User((👤 User))                                                                                                                                                                               
          CMD["/solarch-multiagent SystemName"]                                                                                                                                                         
          User -->|Types| CMD                                                                                                                                                                           
      end                                                                                                                                                                                               
                                                                                                                                                                                                        
      subgraph MasterOrch["🔷 Master Orchestrator (Sonnet)"]                                                                                                                                            
          CP0["CP-0: Initialize<br/>Parse Flags"]                                                                                                                                                       
          CP1["CP-1: Validate Inputs<br/>ProductSpecs CP8+<br/>Prototype CP14+"]                                                                                                                        
          CP2["CP-2: Load Context"]                                                                                                                                                                     
                                                                                                                                                                                                        
          Filter{{"🔍 Entry Point?"}}                                                                                                                                                                   
          System["(default)<br/>All ADRs"]                                                                                                                                                              
          Subsystem["--subsystem<br/>Subsystem ADRs"]                                                                                                                                                   
          Layer["--layer<br/>Layer ADRs"]                                                                                                                                                               
          SingleADR["--adr<br/>Single ADR"]                                                                                                                                                             
                                                                                                                                                                                                        
          QualityMode{{"--quality?"}}                                                                                                                                                                   
                                                                                                                                                                                                        
          CMD --> CP0                                                                                                                                                                                   
          CP0 --> Filter                                                                                                                                                                                
                                                                                                                                                                                                        
          Filter --> System                                                                                                                                                                             
          Filter --> Subsystem                                                                                                                                                                          
          Filter --> Layer                                                                                                                                                                              
          Filter --> SingleADR                                                                                                                                                                          
                                                                                                                                                                                                        
          System --> CP1                                                                                                                                                                                
          Subsystem --> CP1                                                                                                                                                                             
          Layer --> CP1                                                                                                                                                                                 
          SingleADR --> CP1                                                                                                                                                                             
                                                                                                                                                                                                        
          CP1 --> CP2                                                                                                                                                                                   
          CP2 --> QualityMode                                                                                                                                                                           
      end                                                                                                                                                                                               
                                                                                                                                                                                                        
      subgraph ResearchPhase["🔬 CP-3: Research Phase (Parallel)"]                                                                                                                                      
          direction TB                                                                                                                                                                                  
          ResearchStart["Load Scope"]                                                                                                                                                                   
                                                                                                                                                                                                        
          subgraph ResearchAgents["Research Agents"]                                                                                                                                                    
              Tech["Tech<br/>Researcher<br/>(Sonnet)"]                                                                                                                                                  
              Integ["Integration<br/>Analyst<br/>(Sonnet)"]                                                                                                                                             
              Cost["Cost<br/>Estimator<br/>(Haiku)"]                                                                                                                                                    
          end                                                                                                                                                                                           
                                                                                                                                                                                                        
          ResearchMerge["🔀 Merge Gate<br/>Research Findings"]                                                                                                                                          
                                                                                                                                                                                                        
          ResearchStart --> ResearchAgents                                                                                                                                                              
          Tech --> ResearchMerge                                                                                                                                                                        
          Integ --> ResearchMerge                                                                                                                                                                       
          Cost --> ResearchMerge                                                                                                                                                                        
      end                                                                                                                                                                                               
                                                                                                                                                                                                        
      subgraph ADRBoard["🏛️ CP-4-9: ADR Board Orchestrator"]                                                                                                                                            
          direction TB                                                                                                                                                                                  
          ADRStart["Load ADRs in Scope"]                                                                                                                                                                
                                                                                                                                                                                                        
          subgraph ADRLoop["For Each ADR"]                                                                                                                                                              
              direction TB                                                                                                                                                                              
                                                                                                                                                                                                        
              subgraph Writers["📝 ADR Writers (Sonnet)"]                                                                                                                                               
                  Foundation["Foundation<br/>Writer"]                                                                                                                                                   
                  Communication["Communication<br/>Writer"]                                                                                                                                             
                  Operational["Operational<br/>Writer"]                                                                                                                                                 
              end                                                                                                                                                                                       
                                                                                                                                                                                                        
              SelfVal["Self-Validator<br/>(Haiku)<br/>15 Checks"]                                                                                                                                       
                                                                                                                                                                                                        
              ScoreCheck{{"Score ≥ 70?"}}                                                                                                                                                               
                                                                                                                                                                                                        
              subgraph AutoRework["🔄 Auto-Rework"]                                                                                                                                                     
                  Retry["Regenerate<br/>with Feedback"]                                                                                                                                                 
                  RetryCount{{"Attempt ≤ 2?"}}                                                                                                                                                          
                  Escalate1["⚠️ ESCALATE<br/>to User"]                                                                                                                                                  
                  Obvious["!!!!!!!!!!!!!!<br/>AUTO-REWORK<br/>ALERT<br/>!!!!!!!!!!!!!!"]                                                                                                                
              end                                                                                                                                                                                       
                                                                                                                                                                                                        
              subgraph ArchBoard["🎭 Architecture Board (Sonnet)"]                                                                                                                                      
                  Pragmatist["🔧 Pragmatist<br/>Scalability<br/>Cost<br/>Delivery"]                                                                                                                     
                  Perfectionist["🔒 Perfectionist<br/>Security<br/>Compliance<br/>Data Protection"]                                                                                                     
                  Skeptic["🤔 Skeptic<br/>Maintainability<br/>Tech Debt<br/>Dependencies"]                                                                                                              
              end                                                                                                                                                                                       
                                                                                                                                                                                                        
              Consensus["⚖️ Weighted Voting<br/>Consensus<br/>(Haiku)"]                                                                                                                                 
                                                                                                                                                                                                        
              ConsensusCheck{{"Confidence ≥ 60%<br/>AND<br/>Dissent ≤ 40%?"}}                                                                                                                           
                                                                                                                                                                                                        
              AskUser["❓ AskUserQuestion<br/>Present Options"]                                                                                                                                         
              Approve["✅ APPROVED<br/>Use Highest<br/>Confidence Option"]                                                                                                                              
          end                                                                                                                                                                                           
                                                                                                                                                                                                        
          ADRMerge["🔀 Merge Gate<br/>Consolidated ADR Registry"]                                                                                                                                       
                                                                                                                                                                                                        
          ADRStart --> Writers                                                                                                                                                                          
          Foundation --> SelfVal                                                                                                                                                                        
          Communication --> SelfVal                                                                                                                                                                     
          Operational --> SelfVal                                                                                                                                                                       
                                                                                                                                                                                                        
          SelfVal --> ScoreCheck                                                                                                                                                                        
                                                                                                                                                                                                        
          ScoreCheck -->|No| Retry                                                                                                                                                                      
          Retry --> Obvious                                                                                                                                                                             
          Obvious --> RetryCount                                                                                                                                                                        
          RetryCount -->|Yes| SelfVal                                                                                                                                                                   
          RetryCount -->|No| Escalate1                                                                                                                                                                  
                                                                                                                                                                                                        
          ScoreCheck -->|Yes| ArchBoard                                                                                                                                                                 
                                                                                                                                                                                                        
          Pragmatist --> Consensus                                                                                                                                                                      
          Perfectionist --> Consensus                                                                                                                                                                   
          Skeptic --> Consensus                                                                                                                                                                         
                                                                                                                                                                                                        
          Consensus --> ConsensusCheck                                                                                                                                                                  
                                                                                                                                                                                                        
          ConsensusCheck -->|No| AskUser                                                                                                                                                                
          ConsensusCheck -->|Yes| Approve                                                                                                                                                               
          AskUser --> Approve                                                                                                                                                                           
                                                                                                                                                                                                        
          Approve --> ADRMerge                                                                                                                                                                          
          Escalate1 --> ADRMerge                                                                                                                                                                        
      end                                                                                                                                                                                               
                                                                                                                                                                                                        
      subgraph ValidationOrch["🔴 CP-10: Validation Orchestrator (BLOCKING)"]                                                                                                                           
          direction TB                                                                                                                                                                                  
          ValStart["Load All ADRs"]                                                                                                                                                                     
                                                                                                                                                                                                        
          subgraph Validators["🛡️ Validators (Parallel)"]                                                                                                                                               
              Consist["ADR Consistency<br/>Validator"]                                                                                                                                                  
              Complete["ADR Completeness<br/>Validator"]                                                                                                                                                
              Trace["Traceability<br/>Validator"]                                                                                                                                                       
              Cover["Coverage<br/>Validator"]                                                                                                                                                           
          end                                                                                                                                                                                           
                                                                                                                                                                                                        
          BlockCheck{{"100% Pain Point<br/>100% P0 REQ<br/>Coverage?"}}                                                                                                                                 
                                                                                                                                                                                                        
          ValReport["Validation Report"]                                                                                                                                                                
                                                                                                                                                                                                        
          ValStart --> Validators                                                                                                                                                                       
          Consist --> BlockCheck                                                                                                                                                                        
          Complete --> BlockCheck                                                                                                                                                                       
          Trace --> BlockCheck                                                                                                                                                                          
          Cover --> BlockCheck                                                                                                                                                                          
      end                                                                                                                                                                                               
                                                                                                                                                                                                        
      subgraph FinalPhase["📦 Final Output"]                                                                                                                                                            
          CP11["CP-11: Generate<br/>Glossary"]                                                                                                                                                          
          CP12["CP-12: Finalize<br/>Package"]                                                                                                                                                           
                                                                                                                                                                                                        
          subgraph Outputs["SolArch_SystemName/"]                                                                                                                                                       
              ADRs["01-decisions/<br/>ADR-001.md...<br/>ADR-012.md"]                                                                                                                                    
              C4["02-c4-diagrams/<br/>Context, Container<br/>Component, Deployment"]                                                                                                                    
              Quality["03-quality/<br/>Performance, Security<br/>Reliability, Usability"]                                                                                                               
              Eval["04-evaluation/<br/>Risk Assessment<br/>Trade-off Analysis"]                                                                                                                         
          end                                                                                                                                                                                           
                                                                                                                                                                                                        
          Done((✅ Complete))                                                                                                                                                                           
      end                                                                                                                                                                                               
                                                                                                                                                                                                        
      subgraph BlockPath["⛔ Blocking Path"]                                                                                                                                                            
          Stop["BLOCK<br/>Require Fix"]                                                                                                                                                                 
      end                                                                                                                                                                                               
                                                                                                                                                                                                        
      %% Main Flow Connections                                                                                                                                                                          
      QualityMode --> ResearchStart                                                                                                                                                                     
      ResearchMerge --> ADRStart                                                                                                                                                                        
      ADRMerge --> ValStart                                                                                                                                                                             
      BlockCheck -->|PASS| ValReport                                                                                                                                                                    
      BlockCheck -->|FAIL| Stop                                                                                                                                                                         
      ValReport --> CP11                                                                                                                                                                                
      CP11 --> CP12                                                                                                                                                                                     
      CP12 --> Outputs                                                                                                                                                                                  
      Outputs --> Done                                                                                                                                                                                  
      Stop -.->|Fix Issues| ADRStart                                                                                                                                                                    
                                                                                                                                                                                                        
      %% Styling                                                                                                                                                                                        
      style User fill:#e1f5fe                                                                                                                                                                           
      style CMD fill:#bbdefb                                                                                                                                                                            
      style MasterOrch fill:#e3f2fd                                                                                                                                                                     
      style ResearchPhase fill:#f3e5f5                                                                                                                                                                  
      style ADRBoard fill:#fff3e0                                                                                                                                                                       
      style ArchBoard fill:#ffe0b2                                                                                                                                                                      
      style ValidationOrch fill:#ffebee                                                                                                                                                                 
      style FinalPhase fill:#e8f5e9                                                                                                                                                                     
      style BlockPath fill:#ffcdd2                                                                                                                                                                      
      style Consensus fill:#fff9c4                                                                                                                                                                      
      style ConsensusCheck fill:#ffeb3b                                                                                                                                                                 
      style BlockCheck fill:#ef5350,color:#fff                                                                                                                                                          
      style Done fill:#81c784                                                                                                                                                                           
      style Stop fill:#ef5350,color:#fff                                                                                                                                                                
      style Obvious fill:#ff5722,color:#fff                                                                                                                                                             
      style AskUser fill:#2196f3,color:#fff                                                                                                                                                             
      style Pragmatist fill:#4caf50,color:#fff                                                                                                                                                          
      style Perfectionist fill:#f44336,color:#fff                                                                                                                                                       
      style Skeptic fill:#ff9800,color:#fff 