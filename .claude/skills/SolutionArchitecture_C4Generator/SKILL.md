---
name: generating-c4-diagrams
description: Use when you need to generate C4 Model diagrams (Context, Container, Component) in Mermaid format from product specifications.
model: sonnet
allowed-tools: Bash, Edit, Grep, Read, Write
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-c4-diagrams started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-c4-diagrams ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill generating-c4-diagrams instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# Generate C4 Diagrams

> **Implements**: [VERSION_CONTROL_STANDARD.md](../VERSION_CONTROL_STANDARD.md) for output file versioning
> **Supports**: Smart Obsolescence Handling for non-UI projects

## Metadata
- **Skill ID**: SolutionArchitecture_C4Generator
- **Version**: 2.0.0
- **Created**: 2024-12-16
- **Updated**: 2025-12-26
- **Author**: Milos Cigoj
- **Change History**:
  - v2.0.0 (2025-12-26): Added NOT_APPLICABLE handling for non-UI projects with backend-focused C4 diagrams
  - v1.1.0 (2025-12-19): Updated metadata for consistency
  - v1.0.0 (2024-12-16): Initial release

---

## Execution Logging (MANDATORY)

This skill logs all execution to the global pipeline progress registry. Logging is automatic and requires no manual configuration.

### How Logging Works

Every execution of this skill is logged to `_state/lifecycle.json`:

- **start_event**: Logged when skill execution begins
- **end_event**: Logged when skill execution completes

Events include:
- skill_name, intent, stage, system_name
- start/end timestamps
- status (completed/failed)
- output files created (C4 diagrams)
- error messages (if failed)

### View Execution Progress

```bash
# See recent pipeline events
cat _state/lifecycle.json | grep '\"skill_name\": \"generating-c4-diagrams\"'

# Or query by stage
python3 _state/pipeline_query_api.py --skill \"generating-c4-diagrams\" --stage solarch
```

Logging is handled automatically by the skill framework. No user action required.

---

# C4 Diagram Generator Skill

> **Version**: 2.0.0
> **Purpose**: Generate C4 Model diagrams in Mermaid format from Product Specifications
> **Supports**: Smart Obsolescence Handling for non-UI projects

---

## APPLICABILITY CHECK (Smart Obsolescence Handling)

**BEFORE generating C4 diagrams**, check project classification:

```
1. Read _state/solarch_config.json
2. Check project_type from upstream
3. IF project_type IN [BACKEND_ONLY, DATABASE_ONLY, INTEGRATION, INFRASTRUCTURE]:
   → Generate C4 diagrams WITHOUT UI containers
   → Use API Consumer instead of User persona where appropriate
   → Skip frontend component diagrams
4. IF project_type == FULL_STACK:
   → Proceed with normal C4 generation (all containers including UI)
```

### C4 Element Applicability by Project Type

| C4 Element | FULL_STACK | BACKEND_ONLY | DATABASE_ONLY | INTEGRATION |
|------------|------------|--------------|---------------|-------------|
| Person (End User) | ✅ | ❌ N/A | ❌ N/A | ❌ N/A |
| Person (API Consumer) | ✅ | ✅ | ✅ | ✅ |
| Person (Admin) | ✅ | ✅ | ✅ | ✅ |
| Container (Mobile App) | ✅ | ❌ N/A | ❌ N/A | ❌ N/A |
| Container (Web App) | ✅ | ❌ N/A | ❌ N/A | ❌ N/A |
| Container (API) | ✅ | ✅ | ❌ N/A | ✅ |
| Container (Database) | ✅ | ✅ | ✅ | ✅ |
| Container (Message Queue) | ✅ | ✅ | ✅ | ✅ |
| Component (UI Module) | ✅ | ❌ N/A | ❌ N/A | ❌ N/A |
| Component (API Module) | ✅ | ✅ | ❌ N/A | ✅ |
| Component (Domain Module) | ✅ | ✅ | ✅ | ✅ |

### Backend-Only Context Diagram Template

```mermaid
C4Context
    title System Context - {SystemName} (API-Only)

    Person(api_consumer, "API Consumer", "External systems/services consuming the API")
    Person(admin, "System Admin", "Configures and monitors the system")

    System(system, "{SystemName}", "Provides {core_purpose} via REST APIs")

    System_Ext(ext1, "{External System 1}", "{Integration purpose}")
    System_Ext(monitoring, "Monitoring System", "Tracks system health and metrics")

    Rel(api_consumer, system, "Calls APIs", "HTTPS/JSON")
    Rel(admin, system, "Manages", "HTTPS")
    Rel(system, ext1, "Integrates with", "HTTPS/Events")
    Rel(system, monitoring, "Sends metrics", "HTTPS")

    %% NOTE: End-user personas excluded - project type {PROJECT_TYPE}
```

### Backend-Only Container Diagram Template

```mermaid
C4Container
    title Container Diagram - {SystemName} (API-Only)

    Person(api_consumer, "API Consumer", "External systems")

    System_Boundary(system, "{SystemName}") {
        Container(api, "API Gateway", "{Technology}", "Routes and validates API requests")
        Container(service, "Core Service", "{Technology}", "Business logic implementation")
        ContainerDb(db, "Database", "{DB Technology}", "Stores application data")
        Container(cache, "Cache", "Redis", "Caching layer")
        Container(queue, "Message Queue", "RabbitMQ", "Async processing")
    }

    System_Ext(ext, "External System", "Third-party integration")

    Rel(api_consumer, api, "Calls", "HTTPS/JSON")
    Rel(api, service, "Routes to", "Internal")
    Rel(service, db, "Reads/Writes")
    Rel(service, cache, "Caches")
    Rel(service, queue, "Publishes")
    Rel(queue, ext, "Notifies")

    %% NOTE: UI containers (Mobile App, Web App) excluded - project type {PROJECT_TYPE}
```

### Database-Only Container Diagram Template

```mermaid
C4Container
    title Container Diagram - {SystemName} (Database-Only)

    Person(data_engineer, "Data Engineer", "Manages data pipelines")

    System_Boundary(system, "{SystemName}") {
        ContainerDb(db_primary, "Primary Database", "{DB Technology}", "Main data store")
        ContainerDb(db_replica, "Read Replica", "{DB Technology}", "Query optimization")
        Container(etl, "ETL Pipeline", "Airflow/dbt", "Data transformation")
    }

    System_Ext(source, "Source System", "Data source")
    System_Ext(warehouse, "Data Warehouse", "Analytics destination")

    Rel(source, etl, "Feeds data")
    Rel(etl, db_primary, "Transforms and loads")
    Rel(db_primary, db_replica, "Replicates")
    Rel(db_replica, warehouse, "Exports to")

    %% NOTE: API and UI containers excluded - project type DATABASE_ONLY
```

### NOT_APPLICABLE Component Diagram Placeholder

When frontend component diagrams are not applicable:

```markdown
---
document_id: c4-component-{module}-frontend
version: 1.0.0
status: NOT_APPLICABLE
created_at: {TIMESTAMP}
generated_by: SolutionArchitecture_C4Generator
---

# C4 Component Diagram: {Module} - Frontend

## Status: NOT APPLICABLE

This C4 Component diagram has been marked as **NOT APPLICABLE** for the current project.

### Reason

This project is classified as **{PROJECT_TYPE}** which does not include user interface components.
Frontend component architecture is not relevant for API-only or backend-focused systems.

### Project Classification

- **Project Type**: {PROJECT_TYPE}
- **UI Artifacts Applicable**: false

### Alternative Documentation

- Backend components documented in: `c4-component-{module}-backend.mermaid`
- API architecture documented in: `06-runtime-view/api-design.md`

---

*This placeholder maintains framework integrity while acknowledging that frontend component diagrams are not applicable to this project type.*
```

---

## Overview

The C4 Model provides four levels of abstraction for visualizing software architecture:

| Level | View | Audience | Shows |
|-------|------|----------|-------|
| 1 | Context | Everyone | System in its environment |
| 2 | Container | Technical | High-level technology choices |
| 3 | Component | Developers | Module internal structure |
| 4 | Code | Developers | Class/function level |

This skill generates Levels 1-3 in Mermaid format. Level 4 is generated from code, not specifications.

---

## Input Sources

| C4 Level | Primary Source | Reference Sources |
|----------|---------------|-------------------|
| Context | MASTER_DEVELOPMENT_PLAN.md | ANALYSIS_SUMMARY.md |
| Container | ADR-002 (Tech Stack), ADR-003 (Modules) | modules.json |
| Component | MOD-*.md (module specs) | API contracts |

---

## Level 1: System Context Diagram

### Purpose
Show the system as a box surrounded by its users (personas) and external systems.

### Source Extraction

From MASTER_DEVELOPMENT_PLAN.md:
```yaml
extract:
  product_name: "1.1 Product Vision" section
  personas: "1.2 Target Personas" table
  
from_analysis:
  external_systems: "Integration Points" section
  
from_modules:
  core_purpose: Aggregate module purposes
```

### Template

```mermaid
C4Context
    title System Context Diagram - {System Name}
    
    Enterprise_Boundary(b0, "{Organization}") {
        Person(persona1, "{Persona Name}", "{Role/Description}")
        Person(persona2, "{Persona Name}", "{Role/Description}")
        
        System(system, "{System Name}", "{Core Purpose}")
    }
    
    System_Ext(ext1, "{External System 1}", "{What it provides}")
    System_Ext(ext2, "{External System 2}", "{What it provides}")
    
    Rel(persona1, system, "{Uses for}", "{Protocol}")
    Rel(persona2, system, "{Uses for}", "{Protocol}")
    Rel(system, ext1, "{Integrates with}", "{Protocol}")
    Rel_Back(ext2, system, "{Provides}", "{Protocol}")
    
    UpdateRelStyle(persona1, system, $textColor="blue", $lineColor="blue")
```

### Example: Inventory System

```mermaid
C4Context
    title System Context - Inventory Management System
    
    Enterprise_Boundary(warehouse, "Warehouse Operations") {
        Person(coordinator, "Operations Coordinator", "Monica K. - Manages stock adjustments")
        Person(picker, "Warehouse Picker", "Jake P. - Picks and reports discrepancies")
        Person(manager, "Operations Manager", "Jessica L. - Reviews exceptions")
        
        System(ims, "Inventory Management System", "Stock adjustment workflow with audit trail and real-time propagation")
    }
    
    System_Ext(erp, "ERP System", "Source of item master data, reconciliation")
    System_Ext(picking, "Picking System", "Receives stock updates for pick operations")
    System_Ext(azure, "Azure AD", "Identity provider for SSO")
    
    Rel(coordinator, ims, "Adjusts stock", "HTTPS")
    Rel(picker, ims, "Reports discrepancies", "HTTPS")
    Rel(manager, ims, "Reviews exceptions", "HTTPS")
    Rel(ims, picking, "Pushes stock changes", "Event/API")
    Rel(ims, erp, "Syncs item data", "API")
    Rel(azure, ims, "Authenticates users", "OIDC")
```

---

## Level 2: Container Diagram

### Purpose
Zoom into the system to show containers (applications, databases, message queues).

### Source Extraction

From ADR-002 (Technology Stack):
```yaml
extract:
  frontend: "Frontend Stack" section
  backend: "Backend Stack" section
  database: "Database" selection
  cache: "Cache" selection
  messaging: "Message Bus" selection
```

From ADR-003 (Module Structure):
```yaml
extract:
  modules: List of module IDs
  boundaries: Module boundaries
```

### Template

```mermaid
C4Container
    title Container Diagram - {System Name}
    
    Person(persona, "{Primary Persona}")
    
    Container_Boundary(c1, "{System Name}") {
        Container(spa, "Web Application", "{Framework}", "{Description}")
        Container(api, "API Application", "{Runtime}", "{Description}")
        ContainerDb(db, "Database", "{Technology}", "{Description}")
        Container(cache, "Cache", "{Technology}", "{Description}")
        Container(events, "Event Bus", "{Technology}", "{Description}")
    }
    
    System_Ext(ext, "{External System}")
    
    Rel(persona, spa, "Uses", "HTTPS")
    Rel(spa, api, "Calls", "JSON/HTTPS")
    Rel(api, db, "Reads/Writes", "SQL/TCP")
    Rel(api, cache, "Caches", "Redis Protocol")
    Rel(api, events, "Publishes/Subscribes")
    Rel(api, ext, "Integrates")
```

### Example: Inventory System

```mermaid
C4Container
    title Container Diagram - Inventory Management System
    
    Person(coordinator, "Operations Coordinator")
    Person(manager, "Operations Manager")
    
    Container_Boundary(ims, "Inventory Management System") {
        Container(spa, "Inventory Web App", "React + TypeScript", "Single-page application for stock management")
        Container(api, "Inventory API", ".NET 8 / ASP.NET Core", "REST API with business logic")
        ContainerDb(db, "Inventory Database", "PostgreSQL 16", "Stock records, transactions, audit log")
        Container(cache, "Cache", "Redis 7", "Session, lookup data, query cache")
        Container(events, "Event Bus", "MediatR + SignalR", "In-process events with WebSocket push")
    }
    
    System_Ext(erp, "ERP System", "Oracle")
    System_Ext(picking, "Picking System")
    System_Ext(azure, "Azure AD")
    
    Rel(coordinator, spa, "Uses", "HTTPS")
    Rel(manager, spa, "Uses", "HTTPS")
    Rel(spa, api, "Calls", "REST/JSON")
    Rel(spa, events, "Receives", "WebSocket")
    Rel(api, db, "Reads/Writes", "EF Core")
    Rel(api, cache, "Caches", "StackExchange.Redis")
    Rel(api, events, "Publishes", "MediatR")
    Rel(events, picking, "Notifies", "HTTP Webhook")
    Rel(api, erp, "Syncs", "REST API")
    Rel(azure, api, "Authenticates", "JWT")
```

---

## Level 3: Component Diagram

### Purpose
Zoom into a container to show components (services, controllers, repositories).

### Source Extraction

From MOD-*.md:
```yaml
extract:
  screens: "3. Screen Specifications" section
  api_endpoints: "7. API Contracts" section
  entities: "Data Requirements" sections
  rbac: "4. Access Control" section
  state_logic: "UI State Logic" diagrams
```

### Template

```mermaid
C4Component
    title Component Diagram - {Module Name}
    
    Container_Boundary(mod, "{Module Name}") {
        Component(ctrl, "{Controller}", "{Technology}", "Handles HTTP requests")
        Component(svc, "{Service}", "{Technology}", "Business logic")
        Component(repo, "{Repository}", "{Technology}", "Data access")
        Component(events, "{Event Handler}", "{Technology}", "Processes events")
        Component(facade, "{Facade}", "{Technology}", "Cross-module queries")
    }
    
    ContainerDb(db, "Database")
    Container(bus, "Event Bus")
    
    Rel(ctrl, svc, "Delegates to")
    Rel(svc, repo, "Uses")
    Rel(svc, facade, "Queries via")
    Rel(repo, db, "Reads/Writes")
    Rel(svc, bus, "Publishes")
    Rel(events, bus, "Subscribes")
    Rel(events, svc, "Triggers")
```

### Example: Stock Adjustment Module

```mermaid
C4Component
    title Component Diagram - MOD-INV-ADJUST-01 Stock Adjustment
    
    Container(spa, "Web App")
    
    Container_Boundary(adjustment, "Stock Adjustment Module") {
        Component(ctrl, "AdjustmentController", "ASP.NET Core", "POST /adjustments, GET /items")
        Component(svc, "AdjustmentService", "C#", "Validation, business rules, orchestration")
        Component(validator, "AdjustmentValidator", "FluentValidation", "Input validation rules")
        Component(repo, "AdjustmentRepository", "EF Core", "Adjustment CRUD operations")
        Component(itemFacade, "IItemsModuleFacade", "Interface", "Query item data from Items module")
        Component(binFacade, "IBinsModuleFacade", "Interface", "Query bin data from Bins module")
        Component(eventPub, "EventPublisher", "MediatR", "Publishes StockChangedEvent")
    }
    
    ContainerDb(db, "PostgreSQL", "adjustments schema")
    Container(bus, "Event Bus", "MediatR")
    Container(ws, "WebSocket Hub", "SignalR")
    
    Rel(spa, ctrl, "Calls", "REST/JSON")
    Rel(ctrl, validator, "Validates input")
    Rel(ctrl, svc, "Delegates to")
    Rel(svc, repo, "Persists via")
    Rel(svc, itemFacade, "Gets item info")
    Rel(svc, binFacade, "Gets bin info")
    Rel(svc, eventPub, "Publishes events")
    Rel(repo, db, "SQL")
    Rel(eventPub, bus, "StockChangedEvent")
    Rel(bus, ws, "Notifies")
    Rel(ws, spa, "Push", "WebSocket")
```

---

## Cross-Module Diagram

### Purpose
Show how modules communicate via facades and events.

### Template

```mermaid
C4Container
    title Module Communication - {System Name}
    
    Container_Boundary(system, "System Modules") {
        Container(mod1, "{Module 1}", "Facade: I{Mod1}Facade")
        Container(mod2, "{Module 2}", "Facade: I{Mod2}Facade")
        Container(mod3, "{Module 3}", "Facade: I{Mod3}Facade")
        Container(shared, "Shared Kernel", "Common types, base classes")
    }
    
    Container(bus, "Event Bus")
    
    Rel(mod1, mod2, "Queries via", "Facade (sync)")
    Rel(mod1, bus, "Publishes", "Event (async)")
    Rel(bus, mod3, "Notifies", "Event Handler")
    Rel(mod1, shared, "Uses")
    Rel(mod2, shared, "Uses")
    
    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

### Example: Inventory System Module Communication

```mermaid
flowchart TB
    subgraph Modules
        ADJ[MOD-INV-ADJUST-01<br/>Stock Adjustment]
        HIST[MOD-INV-HISTORY-01<br/>Transaction History]
        BIN[MOD-INV-BINMGMT-01<br/>Bin Management]
        EXCEPT[MOD-INV-EXCEPT-01<br/>Exception Dashboard]
        APPROV[MOD-INV-APPROV-01<br/>Approval Workflow]
    end
    
    subgraph Facades [Module Facades - Sync Queries]
        IF[IItemsFacade]
        BF[IBinsFacade]
    end
    
    subgraph Events [Integration Events - Async]
        E1[StockAdjustedEvent]
        E2[ApprovalRequestedEvent]
        E3[ApprovalCompletedEvent]
    end
    
    ADJ -->|queries| IF
    ADJ -->|queries| BF
    ADJ -->|publishes| E1
    ADJ -->|publishes| E2
    
    E1 -->|subscribes| HIST
    E1 -->|subscribes| EXCEPT
    E1 -->|subscribes| BIN
    
    APPROV -->|publishes| E3
    E3 -->|subscribes| ADJ
    
    BIN -->|provides| BF
```

---

## Deployment Diagram

### Purpose
Show how containers are deployed to infrastructure.

### Template

```mermaid
C4Deployment
    title Deployment Diagram - {Environment}
    
    Deployment_Node(cloud, "{Cloud Provider}", "{Region}") {
        Deployment_Node(vpc, "VPC") {
            Deployment_Node(web, "Web Tier") {
                Container(spa, "Web App", "React")
            }
            Deployment_Node(app, "Application Tier") {
                Container(api, "API", ".NET")
            }
            Deployment_Node(data, "Data Tier") {
                ContainerDb(db, "Database", "PostgreSQL")
                Container(cache, "Cache", "Redis")
            }
        }
    }
    
    Rel(spa, api, "HTTPS")
    Rel(api, db, "SQL/TLS")
    Rel(api, cache, "Redis Protocol")
```

### Example: AWS Deployment

```mermaid
C4Deployment
    title Deployment - Production (AWS eu-central-1)
    
    Deployment_Node(aws, "AWS", "eu-central-1 Frankfurt") {
        Deployment_Node(vpc, "VPC", "10.0.0.0/16") {
            Deployment_Node(public, "Public Subnets", "10.0.1.0/24, 10.0.2.0/24") {
                Deployment_Node(alb, "Application Load Balancer") {
                    Container(lb, "ALB", "HTTPS termination, path routing")
                }
                Deployment_Node(cdn, "CloudFront") {
                    Container(cf, "CDN", "Static assets, caching")
                }
            }
            
            Deployment_Node(private, "Private Subnets", "10.0.10.0/24, 10.0.11.0/24") {
                Deployment_Node(ecs, "ECS Cluster", "Fargate") {
                    Container(api1, "API Instance 1", ".NET 8")
                    Container(api2, "API Instance 2", ".NET 8")
                }
            }
            
            Deployment_Node(data_sub, "Data Subnets", "10.0.20.0/24, 10.0.21.0/24") {
                Deployment_Node(rds, "RDS", "Multi-AZ") {
                    ContainerDb(pg, "PostgreSQL 16", "db.r6g.large")
                }
                Deployment_Node(elasticache, "ElastiCache") {
                    Container(redis, "Redis 7", "cache.r6g.large")
                }
            }
        }
    }
    
    Deployment_Node(client, "Client Browser") {
        Container(browser, "Browser", "React SPA")
    }
    
    Rel(browser, cf, "HTTPS")
    Rel(cf, lb, "HTTPS")
    Rel(lb, api1, "HTTP/8080")
    Rel(lb, api2, "HTTP/8080")
    Rel(api1, pg, "PostgreSQL/5432")
    Rel(api2, pg, "PostgreSQL/5432")
    Rel(api1, redis, "Redis/6379")
    Rel(api2, redis, "Redis/6379")
```

---

## Output Files

For each level, generate:

| Level | Output File | Location |
|-------|-------------|----------|
| Context | c4-context.mermaid | 03-context-scope/diagrams/ |
| Container | c4-container.mermaid | 05-building-blocks/ |
| Component | c4-component-{module}.mermaid | 05-building-blocks/modules/{module}/ |
| Deployment | c4-deployment.mermaid | 07-deployment-view/ |
| Cross-Module | c4-module-communication.mermaid | 05-building-blocks/ |

---

## Registry Entry

For each diagram, add to `_registry/components.json`:

```json
{
  "diagrams": [
    {
      "level": "context",
      "file": "03-context-scope/diagrams/c4-context.mermaid",
      "personas": ["coordinator", "picker", "manager"],
      "externalSystems": ["erp", "picking", "azure"]
    },
    {
      "level": "container",
      "file": "05-building-blocks/c4-container.mermaid",
      "containers": ["spa", "api", "db", "cache", "events"]
    },
    {
      "level": "component",
      "module": "MOD-INV-ADJUST-01",
      "file": "05-building-blocks/modules/adjustment/c4-component.mermaid",
      "components": ["controller", "service", "repository", "facade", "eventPublisher"]
    }
  ],
  "modules": [
    {
      "id": "MOD-INV-ADJUST-01",
      "diagramFile": "05-building-blocks/modules/adjustment/c4-component.mermaid",
      "facades": {
        "provides": [],
        "consumes": ["IItemsFacade", "IBinsFacade"]
      },
      "events": {
        "publishes": ["StockChangedEvent"],
        "subscribes": ["ApprovalCompletedEvent"]
      }
    }
  ]
}
```

---

## State Management Integration

### Command System Integration

This skill is invoked by these commands:

```
Commands that use this skill:
├─ /solarch-context (checkpoint 2) - C4 Context diagram
├─ /solarch-blocks (checkpoint 4) - C4 Container, Component diagrams
└─ /solarch-deploy (checkpoint 7) - C4 Deployment diagram
```

### Registry Updates

After generating diagrams, update `_registry/components.json`:

```json
{
  "diagrams": [
    {
      "id": "C4-CTX-001",
      "level": "context",
      "file": "diagrams/c4-context.mmd",
      "generated_at": "ISO8601"
    }
  ],
  "modules": [
    {
      "id": "MOD-INV-ADJUST-01",
      "component_diagram": "diagrams/modules/MOD-INV-ADJUST-01/c4-component.mmd"
    }
  ]
}
```

### Output Locations

| Diagram Type | Location |
|--------------|----------|
| Context | `SolArch_{name}/diagrams/c4-context.mmd` |
| Container | `SolArch_{name}/diagrams/c4-container.mmd` |
| Component | `SolArch_{name}/diagrams/modules/{mod}/c4-component.mmd` |
| Deployment | `SolArch_{name}/diagrams/c4-deployment.mmd` |

### Quality Gate Validation

```bash
# Checkpoint 4 requires C4 diagrams
python3 .claude/hooks/solarch_quality_gates.py --validate-checkpoint 4 --dir SolArch_X/
```

---

**Skill Status**: Ready for Use
