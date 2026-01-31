---
document_id: ROADMAP-EmergencyTriage
version: 1.0.0
created_at: 2026-01-16
updated_at: 2026-01-16
generated_by: Discovery_GenerateRoadmap
source_files:
  - 03-strategy/PRODUCT_STRATEGY.md
  - 02-research/JOBS_TO_BE_DONE.md
  - 02-research/personas/*.md
  - traceability/jtbd_registry.json
change_history:
  - version: "1.0.0"
    date: "2026-01-16"
    author: "Discovery_GenerateRoadmap"
    changes: "Initial roadmap generation from strategy and JTBD"
---

# Product Roadmap: Emergency Triage System

**Roadmap Date**: 2026-01-16
**Planning Horizon**: 12 months (Foundation to Production)
**Total Phases**: 3
**Total Epics**: 12

---

## 🗺️ Roadmap Overview

### Timeline Visualization

```
[Quarter 1]        [Quarter 2]        [Quarter 3]        [Quarter 4]
────────────       ────────────       ────────────       ────────────
  Phase 1            Phase 2            Phase 3           Maintenance
  Foundation         Pilot Go-Live      Optimization      Support
  [5 epics]          [4 epics]          [3 epics]        [Ongoing]
  12 weeks           12 weeks           12 weeks
```

### Phase Summary

| Phase | Name | Duration | Epics | Key Deliverable |
|-------|------|----------|-------|-----------------|
| 1 | Foundation & Core Workflow | 12 weeks | 5 | Minimum viable triage workflow operational on-premise |
| 2 | Pilot Go-Live & Clinical Adoption | 12 weeks | 4 | Full department adoption with real patient data |
| 3 | Optimization & Scale Readiness | 12 weeks | 3 | Production-ready system with metrics and documentation |

---

## 🏗️ Phase 1: Foundation & Core Workflow

**Timeline**: Week 1-12 (Month 1-3)
**Theme**: Build core infrastructure and establish minimum viable workflow
**Target Users**: Pilot ED staff (5-10 people across shifts)
**Status**: 🔴 Not Started

### Phase Objectives
1. Deliver sub-second real-time queue visibility for intake, triage, and doctor roles
2. Enable glove-friendly patient registration (<90 seconds) and vitals entry (<30 seconds)
3. Achieve 100% availability during internet outages with on-premise deployment
4. Demonstrate working system in test environment with synthetic data

### Epics

#### Epic 1.1: Real-Time Infrastructure & WebSocket Foundation

**Priority**: P0
**Estimated Effort**: L (8-10 story points)
**Duration**: 4 weeks

**Description**:
Establish the foundational real-time communication layer using WebSocket infrastructure to enable sub-second updates across all client views (intake, triage, doctor dashboard, public display). This epic delivers the core architectural backbone that all subsequent features depend on.

**User Value**:
> As a triage doctor, I will be able to see patient status changes instantly on my dashboard, which means I can make timely clinical decisions without manual refreshes or delays.

**JTBD Addressed**:
- JTBD-2.1: Real-Time Queue Visibility
- JTBD-4.1: Real-Time Status Updates

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| WebSocket server setup | Backend event bus with connection pooling | Must Have |
| Client subscription management | Frontend state sync with automatic reconnection | Must Have |
| Event-driven state updates | Broadcast patient status changes to all connected clients | Must Have |
| Connection health monitoring | Watchdog for stale connections with auto-recovery | Must Have |
| Load testing infrastructure | Simulate 50+ concurrent connections | Should Have |

**Acceptance Criteria**:
- [ ] Patient status changes propagate to all clients within 1 second
- [ ] System handles 50+ concurrent WebSocket connections without degradation
- [ ] Automatic reconnection on connection loss (<3 second recovery)
- [ ] Zero-downtime for client disconnects and reconnects
- [ ] Load test demonstrates <100ms latency for status updates

**Dependencies**:
- **Requires**: None (foundational)
- **Enables**: Epic 1.2, Epic 1.3, Epic 1.4

**Requirements**:
- REQ-001: WebSocket connection management
- REQ-002: Event broadcasting system
- REQ-003: Client state synchronization
- REQ-004: Connection health monitoring

**Risks**:
| Risk | Mitigation |
|------|------------|
| WebSocket performance degrades under load | Load test early (Week 2); optimize connection pooling and event throttling |
| Browser compatibility issues with Chromebit hardware | Test on target hardware (Week 1); ensure polyfills for older browsers |
| Connection storms during network interruptions | Implement exponential backoff and connection rate limiting |

---

#### Epic 1.2: Rapid Intake & Patient Registration

**Priority**: P0
**Estimated Effort**: M (5-6 story points)
**Duration**: 3 weeks

**Description**:
Build a streamlined patient intake interface optimized for speed and glove-friendly touchscreen interaction. Focus on minimal required fields (Name, DOB, Chief Complaint) with large touch targets (60x60px) and tab-enter keyboard navigation for fast data entry during peak hours.

**User Value**:
> As an intake nurse, I will be able to register patients in under 90 seconds using gloved hands, which means I can maintain high throughput without creating intake bottlenecks.

**JTBD Addressed**:
- JTBD-1.1: Rapid Patient Intake
- JTBD-1.4: Patient Identity Disambiguation
- JTBD-2.5: Zero-Training Interface

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| Minimal intake form | Name, DOB, Chief Complaint only | Must Have |
| Glove-friendly UI | 60x60px touch targets, high contrast | Must Have |
| Pseudonymous ID generation | Format: JS12-1, JS12-2 for name collisions | Must Have |
| Auto-save on keystroke | Prevent data loss on accidental closes | Must Have |
| Tab-enter navigation | Fast keyboard-only workflow | Should Have |
| Duplicate detection | Alert on same Name+DOB within 24 hours | Nice to Have |

**Acceptance Criteria**:
- [ ] Registration time average <90 seconds (measured across 20 test entries)
- [ ] Touch targets minimum 60x60px with WCAG AA contrast
- [ ] Pseudonymous ID correctly handles collisions (same initials + DOB day)
- [ ] Form accessible via keyboard-only (no mouse required)
- [ ] Auto-save triggers every 2 seconds or on blur
- [ ] Zero training time for float nurses (<5 minutes to first successful entry)

**Dependencies**:
- **Requires**: Epic 1.1 (real-time updates for queue status)
- **Enables**: Epic 1.3 (triage workflow needs intake completion)

**Requirements**:
- REQ-005: Intake form with minimal fields
- REQ-006: Glove-friendly touch targets
- REQ-007: Pseudonymous ID generator
- REQ-008: Auto-save mechanism
- REQ-009: Keyboard navigation
- REQ-010: Patient identity disambiguation

**Risks**:
| Risk | Mitigation |
|------|------------|
| Touch targets still too small for thick gloves | User test with multiple glove types (Week 4); adjust sizing to 70x70px if needed |
| Form complexity creeps with "nice to have" fields | Strict field review; enforce 3-field limit for pilot |
| Pseudonymous ID collisions cause confusion | Implement clear visual indicators and sequence numbers |

---

#### Epic 1.3: Triage Vitals Capture & ESI Assignment

**Priority**: P0
**Estimated Effort**: M (5-6 story points)
**Duration**: 3 weeks

**Description**:
Create a triage interface for nurses to capture vital signs (BP, HR, O2, Temp) and assign ESI levels (1-5) with glove-friendly input fields and clinical notes. Include internal-only notes field for behavioral observations that are visible to clinical staff but never exposed on public displays.

**User Value**:
> As a triage nurse, I will be able to document vitals and clinical observations in under 30 seconds without removing gloves, which means I can maintain infection control while keeping the queue moving.

**JTBD Addressed**:
- JTBD-2.2: Accurate Vitals Documentation
- JTBD-2.3: Clinical Notes Privacy
- JTBD-2.4: Role-Based Wait Time Assignment

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| Vitals entry form | BP, HR, O2 Saturation, Temperature | Must Have |
| ESI level selection | Dropdown with 1-5 levels and descriptions | Must Have |
| Internal-only notes | Text area marked with "Clinical Staff Only" | Must Have |
| Glove-optimized inputs | Large touch targets, numeric keypad for vitals | Must Have |
| Clear workflow handoff | Status transition: Intake → Triaged (no time assigned yet) | Must Have |
| Dark mode toggle | Charcoal background for night shifts | Should Have |

**Acceptance Criteria**:
- [ ] Vitals entry time average <30 seconds
- [ ] Internal notes field never exposed on public display or API
- [ ] ESI level selection with visual indicators (color + icon)
- [ ] Touch targets minimum 44x44px (WCAG compliance)
- [ ] Status transitions correctly: Intake → Triaged
- [ ] Dark mode reduces brightness by 70% without losing contrast

**Dependencies**:
- **Requires**: Epic 1.2 (intake completion triggers triage)
- **Enables**: Epic 1.4 (doctor dashboard needs triaged patients)

**Requirements**:
- REQ-011: Vitals capture interface
- REQ-012: ESI level assignment
- REQ-013: Internal-only clinical notes
- REQ-014: Glove-friendly input fields
- REQ-015: Status workflow (Intake → Triaged)
- REQ-016: Dark mode for night shifts

**Risks**:
| Risk | Mitigation |
|------|------------|
| Internal notes accidentally exposed | Strict API access controls; audit all public endpoints |
| Vitals entry errors due to touch issues | Input validation and confirmation dialogs for out-of-range values |
| Nurses unclear on when to assign time vs doctor | Clear UI labels and training; enforce workflow separation |

---

#### Epic 1.4: Doctor Dashboard & Kanban Queue Management

**Priority**: P0
**Estimated Effort**: XL (12-15 story points)
**Duration**: 5 weeks

**Description**:
Build a consolidated doctor dashboard with patient cards (age, chief complaint, vitals, ESI level) and a Kanban board for drag-and-drop queue management. Enable doctors to manually assign time categories (30m, 60m, 120m, Rest) based on clinical judgment, with touch-optimized interaction and progressive overdue alerts (yellow 110%, red 125%).

**User Value**:
> As a triage doctor, I will be able to review all triaged patients at a glance and re-prioritize the queue using drag-and-drop, which means I can perform rapid assessments (60-90 seconds per patient) and dynamically adjust to ER capacity changes.

**JTBD Addressed**:
- JTBD-3.1: Consolidated Patient Dashboard
- JTBD-3.2: Manual Clinical Judgment
- JTBD-3.3: Deterioration Alerts
- JTBD-3.4: Bulk Queue Management
- JTBD-3.5: Behavioral Risk Visibility
- JTBD-3.6: Overdue Patient Alerts
- JTBD-3.7: Touch-Optimized Interaction

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| Patient card dashboard | Grid view with age, chief complaint, vitals, ESI | Must Have |
| Kanban board | Columns: Triaged, 30m, 60m, 120m, Rest | Must Have |
| Drag-and-drop | Touch-optimized for Surface tablet | Must Have |
| Manual time slot assignment | No automated suggestions or overrides | Must Have |
| ESI escalation alerts | Red, pulsing visual alert for ESI 3→2 changes | Must Have |
| Progressive overdue alerts | Yellow (110%), red (125%) on doctor dashboard ONLY | Must Have |
| Behavioral risk flags | Warning icon (⚠️) with internal notes access | Must Have |
| Bulk selection | Multi-select for batch time updates | Should Have |

**Acceptance Criteria**:
- [ ] Dashboard loads all triaged patients within 2 seconds
- [ ] Drag-and-drop works on touch (no mouse required)
- [ ] ESI escalation alert visually distinct (red + pulse animation)
- [ ] Overdue alerts appear at correct thresholds (110%, 125%)
- [ ] Overdue alerts NEVER appear on public display
- [ ] Behavioral risk flag visible only to clinical staff
- [ ] Time slot assignments trigger instant public display updates (<1 second)
- [ ] Touch targets minimum 44x44px for all interactive elements

**Dependencies**:
- **Requires**: Epic 1.1 (real-time updates), Epic 1.3 (triaged patients)
- **Enables**: Epic 1.5 (public display needs time assignments)

**Requirements**:
- REQ-017: Patient card dashboard
- REQ-018: Kanban board interface
- REQ-019: Drag-and-drop queue management
- REQ-020: Manual time slot assignment
- REQ-021: ESI escalation visual alerts
- REQ-022: Progressive overdue alerts (doctor only)
- REQ-023: Behavioral risk flag visibility
- REQ-024: Touch-optimized interaction (44x44px targets)
- REQ-025: Bulk selection for batch updates

**Risks**:
| Risk | Mitigation |
|------|------------|
| Drag-and-drop performance degrades with 20+ patients | Virtualize list rendering; test with 50+ patient load |
| Overdue alerts distract from critical ESI escalations | Use distinct visual hierarchy (pulse for ESI, static for overdue) |
| Behavioral risk flags accidentally visible on public screen | Strict access controls; audit all display queries |
| Doctor overrides system logic causing confusion | Clear visual feedback on manual changes; training on clinical judgment use |

---

#### Epic 1.5: Air-Gapped Deployment & On-Premise Reliability

**Priority**: P0
**Estimated Effort**: L (8-10 story points)
**Duration**: 4 weeks

**Description**:
Containerize all services (frontend, backend, database) using Docker Compose for single-command deployment on hospital LAN. Ensure zero external dependencies (no CDN, no cloud APIs), configure LDAP/AD authentication, implement HTTPS with self-signed certificates, and enable auto-restart on container failure.

**User Value**:
> As an IT administrator, I will be able to deploy and recover the system in under 5 minutes using a single Docker Compose command, which means ER operations continue uninterrupted during internet outages.

**JTBD Addressed**:
- JTBD-5.1: On-Premise Reliability
- JTBD-5.2: Display Auto-Recovery
- JTBD-5.3: Simple Deployment
- JTBD-5.4: Security Without Complexity

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| Docker Compose orchestration | Frontend, backend, PostgreSQL in containers | Must Have |
| Bundled frontend assets | No CDN dependencies, all assets self-hosted | Must Have |
| LDAP/AD integration | Hospital directory authentication | Must Have |
| Self-signed HTTPS | TLS on LAN without external CA | Must Have |
| Auto-restart on failure | Watchdog monitoring with health checks | Must Have |
| Single-command deployment | `docker-compose up -d` | Must Have |
| 15-minute idle timeout | Auto-logout for security | Should Have |
| Simplified RBAC | Two roles: Clinical Staff, View Only | Should Have |

**Acceptance Criteria**:
- [ ] System runs with zero internet connectivity (LAN only)
- [ ] Deployment command: `docker-compose up -d` (single line)
- [ ] LDAP authentication working with hospital AD
- [ ] HTTPS enabled with self-signed cert (no browser errors after accept)
- [ ] Auto-restart on container failure (<30 second recovery)
- [ ] System survives VM reboot (containers auto-start)
- [ ] Public display auto-reconnects on Chromebit crash (<60 seconds)
- [ ] Idle timeout logs out users after 15 minutes of inactivity

**Dependencies**:
- **Requires**: All Phase 1 epics (final integration)
- **Enables**: Phase 2 (pilot go-live)

**Requirements**:
- REQ-026: Docker Compose containerization
- REQ-027: Bundled frontend assets (no CDN)
- REQ-028: LDAP/AD authentication
- REQ-029: Self-signed HTTPS configuration
- REQ-030: Auto-restart on container failure
- REQ-031: Single-command deployment
- REQ-032: 15-minute idle timeout
- REQ-033: Simplified RBAC (two roles)

**Risks**:
| Risk | Mitigation |
|------|------------|
| LDAP integration complexity | Early integration testing (Week 7); fallback local auth for dev |
| Container orchestration learning curve | Use simple Docker Compose; avoid Kubernetes for pilot |
| Performance issues on 4 vCPU / 16GB RAM | Performance testing (Week 10); request larger VM if needed |
| Self-signed cert deployment friction | Document cert installation steps; provide hospital IT script |

---

### Phase 1 Milestone

**Milestone Name**: Core Workflow Operational
**Target Date**: End of Week 12
**Validation Method**: End-to-end test with synthetic data on pilot hardware

**Exit Criteria**:
- [ ] All four views functional (Intake, Triage, Doctor, Public Display)
- [ ] Sub-second board updates demonstrated (<1 second latency)
- [ ] Glove-friendly testing passed (5 different glove types)
- [ ] On-premise deployment working on pilot hardware
- [ ] System survives internet outage with zero downtime
- [ ] Manual user testing with 3 nurses and 1 doctor (positive feedback)
- [ ] Zero-training time validated (<10 minutes for float nurses)

---

## 🏗️ Phase 2: Pilot Go-Live & Clinical Adoption

**Timeline**: Week 13-24 (Month 4-6)
**Theme**: Live operation with real patient data and full department adoption
**Target Users**: All pilot ED staff (all shifts, 15-20 people)
**Status**: 🔴 Not Started

### Phase Objectives
1. Achieve 100% daily active users (all on-shift staff using the system)
2. Track LWBS (Left Without Being Seen) as a critical performance metric
3. Enable patient walkout tracking with disposition statuses (Admitted, Discharged, LWBS, Transfer)
4. Collect staff feedback and iterate on usability issues within 48 hours
5. Demonstrate measurable improvement in registration time (baseline: 3-4 minutes → target: <90 seconds)

### Epics

#### Epic 2.1: Public Display & Wait Time Transparency

**Priority**: P0
**Estimated Effort**: M (5-6 story points)
**Duration**: 3 weeks

**Description**:
Build a public-facing display showing pseudonymous patient IDs with wait time categories (30m, 60m, 120m, Rest) updated in real-time. Ensure NO countdown timers, NO full names, and NO sensitive clinical data. Include dark mode for night shifts and large fonts for readability from waiting room seats.

**User Value**:
> As a waiting patient, I will be able to see my status update on the public display within 1 second of the doctor's assignment, which means I know the system has registered my case and I'm not forgotten.

**JTBD Addressed**:
- JTBD-4.1: Real-Time Status Updates
- JTBD-4.2: Wait Time Transparency
- JTBD-4.3: Patient Identity Recognition
- JTBD-4.4: Night Waiting Room Comfort

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| Pseudonymous ID display | Format: JS12-1, JS12-2 (no full names) | Must Have |
| Wait time categories | "Approx 30 mins", "Approx 60 mins", "Approx 2 hours", "Please wait" | Must Have |
| Real-time updates | Sub-second latency via WebSocket | Must Have |
| NO countdown timers | Category-based display only (no "25 minutes remaining") | Must Have |
| Large fonts | Minimum 24px body text, 48px headings | Must Have |
| Dark mode | Charcoal background for night shifts | Should Have |
| Auto-refresh on connection loss | Watchdog with reconnection | Must Have |

**Acceptance Criteria**:
- [ ] Public display updates within 1 second of doctor assignment
- [ ] NO full names or date of birth visible
- [ ] NO countdown timers or precise time estimates
- [ ] Font size readable from 15 feet away (validated with staff)
- [ ] Dark mode reduces brightness by 70% (night shifts)
- [ ] Auto-reconnect on Chromebit crash (<60 seconds)
- [ ] Kiosk mode prevents accidental exits

**Dependencies**:
- **Requires**: Epic 1.1 (WebSocket), Epic 1.4 (doctor time assignments)
- **Enables**: Epic 2.3 (patient feedback loop)

**Requirements**:
- REQ-034: Public display interface
- REQ-035: Pseudonymous ID display format
- REQ-036: Wait time category labels (no countdown)
- REQ-037: Real-time WebSocket updates
- REQ-038: Large fonts for readability
- REQ-039: Dark mode for night shifts
- REQ-040: Auto-reconnect on connection loss

**Risks**:
| Risk | Mitigation |
|------|------------|
| Countdown timers requested by stakeholders | Firm policy: category-based only; reference patient rights officer |
| Display lag causes patient complaints | Load test with 50+ patients; optimize rendering |
| Chromebit hardware instability | Watchdog monitoring; auto-restart on freeze |
| Privacy concerns about pseudonymous IDs | Audit with patient rights officer; ensure no reverse-engineering possible |

---

#### Epic 2.2: LWBS Tracking & Disposition Management

**Priority**: P1
**Estimated Effort**: S (3-4 story points)
**Duration**: 2 weeks

**Description**:
Implement patient disposition tracking with statuses (Admitted, Discharged, LWBS, Transfer) to capture walkouts without deleting records. Enable LWBS metric reporting for performance analysis and prevent accidental record deletion during triage.

**User Value**:
> As an intake nurse, I will be able to mark patients who leave without being seen (LWBS) with a disposition status, which means we can track this critical performance metric without losing their data.

**JTBD Addressed**:
- JTBD-1.3: Patient Walkout Tracking

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| Disposition dropdown | Admitted, Discharged, LWBS, Transfer | Must Have |
| LWBS metric reporting | Daily/weekly/monthly aggregates | Must Have |
| Prevent record deletion | Soft delete with disposition status | Must Have |
| Disposition timestamp | Record when status changed | Should Have |
| Disposition history | Audit trail for compliance | Nice to Have |

**Acceptance Criteria**:
- [ ] Disposition dropdown visible on intake and doctor dashboards
- [ ] LWBS status prevents record deletion
- [ ] LWBS metric report shows count by day/week/month
- [ ] Disposition timestamp captured for all status changes
- [ ] Records retained for 24 hours before auto-purge (Epic 2.4)

**Dependencies**:
- **Requires**: Epic 1.2 (intake records), Epic 1.4 (doctor dashboard)
- **Enables**: Epic 2.4 (ephemeral data cleanup logic)

**Requirements**:
- REQ-041: Disposition dropdown (Admitted, Discharged, LWBS, Transfer)
- REQ-042: LWBS metric reporting
- REQ-043: Soft delete with disposition status
- REQ-044: Disposition timestamp capture

**Risks**:
| Risk | Mitigation |
|------|------------|
| Staff forget to mark disposition | Training emphasis; reminder dialogs on patient idle >4 hours |
| LWBS metric misinterpreted | Clear reporting labels; training on metric usage |
| Disposition status conflicts with EHR | No EHR integration for pilot; disposition is internal only |

---

#### Epic 2.3: Feedback Collection & Iterative Improvements

**Priority**: P1
**Estimated Effort**: M (5-6 story points)
**Duration**: 4 weeks (ongoing throughout Phase 2)

**Description**:
Establish a feedback collection mechanism (in-app forms, weekly retrospectives, shift supervisor check-ins) to capture staff pain points and patient complaints. Prioritize issues and implement fixes within 48 hours for high-priority usability bugs. Track feedback trends to inform Phase 3 enhancements.

**User Value**:
> As a head nurse, I will be able to report usability issues and see fixes deployed within 48 hours, which means the system continuously adapts to our workflow without waiting for quarterly releases.

**JTBD Addressed**:
- JTBD-2.5: Zero-Training Interface (continuous refinement)
- JTBD-4.2: Wait Time Transparency (patient feedback loop)

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| In-app feedback form | Quick bug report from any screen | Must Have |
| Weekly retrospectives | 30-minute sessions with shift supervisors | Must Have |
| Feedback triage board | Kanban for P0/P1/P2 issue tracking | Must Have |
| 48-hour fix commitment | P0 usability bugs resolved within 2 days | Must Have |
| Feedback trends analysis | Monthly report to identify patterns | Should Have |
| Staff satisfaction survey | Quarterly survey (System Usability Scale) | Nice to Have |

**Acceptance Criteria**:
- [ ] In-app feedback form accessible from all views
- [ ] Weekly retrospectives scheduled with 100% attendance (shift supervisors)
- [ ] P0 usability bugs resolved within 48 hours (track resolve time)
- [ ] Feedback triage board visible to all stakeholders
- [ ] Monthly trends report shows top 3 pain points and resolution status
- [ ] Quarterly SUS survey shows score >70 (average usability)

**Dependencies**:
- **Requires**: Phase 2 live operation (real usage generates feedback)
- **Enables**: Phase 3 (optimization priorities driven by feedback)

**Requirements**:
- REQ-045: In-app feedback form
- REQ-046: Weekly retrospective schedule
- REQ-047: Feedback triage board (Kanban)
- REQ-048: 48-hour P0 bug fix commitment
- REQ-049: Monthly feedback trends report

**Risks**:
| Risk | Mitigation |
|------|------------|
| Feedback overwhelms dev capacity | Ruthless prioritization; focus on P0 only for 48-hour fixes |
| Staff reluctant to report issues | Anonymous feedback option; emphasize continuous improvement culture |
| Feedback trends misinterpreted | Collaborate with clinical leadership on prioritization |
| 48-hour commitment unsustainable | Adjust to "business day" definition; exclude weekends |

---

#### Epic 2.4: Ephemeral Data & Privacy Compliance

**Priority**: P1
**Estimated Effort**: M (5-6 story points)
**Duration**: 3 weeks

**Description**:
Implement 24-hour data retention with automatic purge of discharged/processed patients. Configure cron job at 04:00 AM to hard delete records >12 hours old with "Discharged" or "Processed" disposition. Retain audit logs with pseudonymous IDs for compliance. Ensure audit logs are searchable by time, action, and user.

**User Value**:
> As an IT administrator, I will have the system automatically delete patient data within 24 hours of discharge, which means we minimize data liability and comply with privacy policies as a flow tool, not a medical record.

**JTBD Addressed**:
- JTBD-5.5: Ephemeral Data Compliance
- JTBD-5.6: Audit Logging for Compliance

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| 24-hour data retention | Auto-purge discharged/processed patients | Must Have |
| Cron job at 04:00 AM | Daily cleanup task | Must Have |
| Hard delete from database | No soft delete for discharged records | Must Have |
| Audit logs retained | Pseudonymous IDs with action timestamps | Must Have |
| Audit log search | Filter by time, action, user | Should Have |
| Purge notification | Email report to IT on successful purge | Nice to Have |

**Acceptance Criteria**:
- [ ] Cron job runs daily at 04:00 AM
- [ ] Discharged/Processed records >12 hours old are deleted
- [ ] Audit logs retained with pseudonymous IDs (format: JS-12)
- [ ] Audit logs searchable by time range, action type, user
- [ ] Hard delete confirmed (no recovery possible)
- [ ] Purge notification email sent to IT (count of deleted records)

**Dependencies**:
- **Requires**: Epic 2.2 (disposition statuses define purge logic)
- **Enables**: Phase 3 (compliance documentation)

**Requirements**:
- REQ-050: 24-hour data retention policy
- REQ-051: Cron job for daily purge (04:00 AM)
- REQ-052: Hard delete from database
- REQ-053: Audit log retention with pseudonymous IDs
- REQ-054: Audit log search interface

**Risks**:
| Risk | Mitigation |
|------|------------|
| Auto-purge deletes needed data | Clear documentation; export capability before purge (manual) |
| Audit logging impacts performance | Async logging; optimize queries with indexes |
| Compliance audit requests unsupported | Audit log search interface; pre-built compliance reports |
| Purge failure causes data accumulation | Monitoring alert on purge failure; manual intervention escalation |

---

### Phase 2 Milestone

**Milestone Name**: Full Department Adoption
**Target Date**: End of Week 24
**Validation Method**: 100% daily active users + LWBS tracking operational

**Exit Criteria**:
- [ ] 100% of shifts using the system (all intake, triage, doctor roles)
- [ ] LWBS tracking operational with weekly reports
- [ ] Zero downtime during network issues (validated with intentional outage)
- [ ] Wait time escalation alerts working (no missed ESI escalations)
- [ ] Public display operational on Chromebit (auto-recovery tested)
- [ ] Staff satisfaction survey shows score >70 (System Usability Scale)
- [ ] Registration time average <90 seconds (measured across 100+ entries)
- [ ] P0 feedback items resolved within 48 hours (track resolve time)

---

## 🏗️ Phase 3: Optimization & Scale Readiness

**Timeline**: Week 25-36 (Month 7-9)
**Theme**: Refine based on real usage; prepare for expansion consideration
**Target Users**: Pilot ED (validated) + potential expansion stakeholders
**Status**: 🔴 Not Started

### Phase Objectives
1. Demonstrate measurable improvement in before/after metrics (registration time, LWBS rate)
2. Achieve staff satisfaction score >75 (System Usability Scale)
3. Document technical architecture and deployment procedures for other sites
4. Generate case study with ROI analysis for executive stakeholders
5. Prepare for expansion decision (Month 10-12)

### Epics

#### Epic 3.1: Metrics Dashboard & ROI Analysis

**Priority**: P2
**Estimated Effort**: M (5-6 story points)
**Duration**: 4 weeks

**Description**:
Build an internal metrics dashboard showing before/after comparisons (registration time, triage time, LWBS rate, wait time accuracy) with trend analysis. Generate monthly reports for clinical leadership and prepare case study with ROI analysis for executive stakeholders considering expansion.

**User Value**:
> As a clinical leader, I will be able to see measurable improvements in patient flow metrics, which means I can justify expansion to other EDs with concrete ROI data.

**JTBD Addressed**:
- (Supports expansion decision, not direct JTBD mapping)

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| Metrics dashboard | Registration time, triage time, LWBS rate, wait time accuracy | Must Have |
| Before/after comparison | Baseline (pre-system) vs pilot data | Must Have |
| Trend analysis | Weekly/monthly trend charts | Must Have |
| Monthly reports | PDF export for clinical leadership | Must Have |
| Case study template | ROI analysis with cost savings | Should Have |
| Executive presentation | Slide deck for expansion decision | Nice to Have |

**Acceptance Criteria**:
- [ ] Dashboard shows all key metrics with before/after comparison
- [ ] Trend charts demonstrate improvement over 12 weeks
- [ ] Monthly report generated automatically (PDF export)
- [ ] Case study includes ROI analysis (cost savings from LWBS reduction)
- [ ] Executive presentation ready for Month 10 decision meeting

**Dependencies**:
- **Requires**: Phase 2 (live usage data)
- **Enables**: Expansion decision (Month 10-12)

**Requirements**:
- REQ-055: Metrics dashboard with before/after comparison
- REQ-056: Trend analysis charts (weekly/monthly)
- REQ-057: Monthly report generation (PDF)
- REQ-058: Case study template with ROI analysis

**Risks**:
| Risk | Mitigation |
|------|------------|
| Metrics show no improvement | Investigate root causes; adjust workflow or training |
| Baseline data unavailable | Use historical estimates; document assumptions |
| ROI analysis disputed by stakeholders | Include conservative assumptions; sensitivity analysis |

---

#### Epic 3.2: Technical Documentation & Deployment Guide

**Priority**: P2
**Estimated Effort**: M (5-6 story points)
**Duration**: 4 weeks

**Description**:
Create comprehensive technical documentation including architecture diagrams, API specifications, deployment procedures, troubleshooting runbooks, and operations guide. Prepare for other sites to evaluate and deploy the system independently with minimal support.

**User Value**:
> As an IT administrator at another hospital, I will be able to deploy and operate the system with comprehensive documentation, which means I don't need ongoing vendor support for basic operations.

**JTBD Addressed**:
- (Supports expansion readiness, not direct JTBD mapping)

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| Architecture diagrams | C4 context, container, component views | Must Have |
| API specifications | OpenAPI/Swagger docs for all endpoints | Must Have |
| Deployment procedures | Step-by-step Docker Compose guide | Must Have |
| Troubleshooting runbooks | Common issues and resolution steps | Must Have |
| Operations guide | Monitoring, backups, disaster recovery | Must Have |
| Hardware requirements | VM specs, network topology, hardware list | Should Have |

**Acceptance Criteria**:
- [ ] Architecture diagrams generated (C4 model)
- [ ] API specifications complete (OpenAPI/Swagger)
- [ ] Deployment procedures validated (tested on fresh VM)
- [ ] Troubleshooting runbooks cover top 10 issues
- [ ] Operations guide includes monitoring and backup procedures
- [ ] Hardware requirements documented with cost estimates

**Dependencies**:
- **Requires**: Phase 2 (stable system for documentation)
- **Enables**: Expansion decision (Month 10-12)

**Requirements**:
- REQ-059: Architecture diagrams (C4 model)
- REQ-060: API specifications (OpenAPI/Swagger)
- REQ-061: Deployment procedures guide
- REQ-062: Troubleshooting runbooks
- REQ-063: Operations guide (monitoring, backups, DR)

**Risks**:
| Risk | Mitigation |
|------|------------|
| Documentation becomes outdated | Automate diagram generation; version control with code |
| Deployment procedures incomplete | Test on fresh VM with uninvolved IT staff |
| Runbooks miss edge cases | Collect feedback from pilot IT team; iterate |

---

#### Epic 3.3: Accessibility & Night Shift Enhancements

**Priority**: P2
**Estimated Effort**: S (3-4 story points)
**Duration**: 2 weeks

**Description**:
Complete accessibility audit (WCAG 2.1 AA compliance) and enhance night shift ergonomics with refined dark mode, high contrast options, and icon+text status indicators for color blindness support. Validate with float nurses and overnight staff.

**User Value**:
> As a nurse with visual impairments, I will be able to use the system effectively regardless of color blindness or low vision, which means the system is inclusive for all staff.

**JTBD Addressed**:
- JTBD-2.6: Night Shift Ergonomics
- JTBD-6.1: Accessibility for All Users

**Key Features**:
| Feature | Description | Priority |
|---------|-------------|----------|
| WCAG 2.1 AA compliance | Screen reader, keyboard nav, contrast ratios | Must Have |
| Icon + text status indicators | Warning triangle + "CRITICAL" (not color alone) | Must Have |
| High contrast mode | Enhanced contrast for low vision | Should Have |
| Dark mode refinement | Improved night shift ergonomics | Should Have |
| Font size adjustments | User-selectable font scaling | Nice to Have |

**Acceptance Criteria**:
- [ ] WCAG 2.1 AA compliance validated (automated audit tools)
- [ ] Screen reader announces all status changes
- [ ] Keyboard navigation works (no mouse required)
- [ ] Status indicators use icon + text (not color alone)
- [ ] High contrast mode tested with visually impaired staff
- [ ] Dark mode brightness reduced by 70% without losing contrast

**Dependencies**:
- **Requires**: Phase 2 (stable UI for accessibility testing)
- **Enables**: Expansion decision (accessibility compliance required)

**Requirements**:
- REQ-064: WCAG 2.1 AA compliance
- REQ-065: Icon + text status indicators
- REQ-066: High contrast mode
- REQ-067: Dark mode refinement

**Risks**:
| Risk | Mitigation |
|------|------------|
| Accessibility audit fails | Early testing with automated tools (Week 1); remediation |
| Icon + text indicators clutter UI | User testing with staff; iterate on design |
| Dark mode still causes eye strain | Night shift validation; adjust brightness and contrast |

---

### Phase 3 Milestone

**Milestone Name**: Production-Ready System
**Target Date**: End of Week 36
**Validation Method**: Executive approval for expansion consideration

**Exit Criteria**:
- [ ] Measurable improvement in registration time (baseline → target)
- [ ] Staff satisfaction scores positive (SUS >75)
- [ ] LWBS rate improved (baseline → pilot comparison)
- [ ] Technical documentation complete for other sites
- [ ] Case study with ROI analysis approved by executive leadership
- [ ] Accessibility audit passed (WCAG 2.1 AA)
- [ ] Expansion decision meeting scheduled (Month 10)

---

## 📊 Epic Dependency Map

```
┌──────────┐
│ Epic 1.1 │ Real-Time Infrastructure (Foundation)
└────┬─────┘
     │
     ├──────────────────────────────────┐
     ▼                                  ▼
┌──────────┐                      ┌──────────┐
│ Epic 1.2 │ Intake              │ Epic 1.4 │ Doctor Dashboard
└────┬─────┘                      └────┬─────┘
     │                                 │
     ▼                                 ▼
┌──────────┐                      ┌──────────┐
│ Epic 1.3 │ Triage              │ Epic 2.1 │ Public Display
└────┬─────┘                      └────┬─────┘
     │                                 │
     └─────────────┬───────────────────┘
                   ▼
              ┌──────────┐
              │ Epic 1.5 │ Deployment
              └────┬─────┘
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Epic 2.2 │ │ Epic 2.3 │ │ Epic 2.4 │
│ LWBS     │ │ Feedback │ │ Privacy  │
└──────────┘ └──────────┘ └──────────┘
                   │
     ┌─────────────┼─────────────┐
     ▼             ▼             ▼
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Epic 3.1 │ │ Epic 3.2 │ │ Epic 3.3 │
│ Metrics  │ │ Docs     │ │ A11y     │
└──────────┘ └──────────┘ └──────────┘
```

### Dependency Matrix

| Epic | Depends On | Blocks | Phase |
|------|------------|--------|-------|
| 1.1 | None | 1.2, 1.3, 1.4, 2.1 | 1 |
| 1.2 | 1.1 | 1.3 | 1 |
| 1.3 | 1.2 | 1.4 | 1 |
| 1.4 | 1.1, 1.3 | 1.5, 2.1 | 1 |
| 1.5 | 1.1, 1.2, 1.3, 1.4 | Phase 2 | 1 |
| 2.1 | 1.1, 1.4 | 2.3 | 2 |
| 2.2 | 1.2, 1.4 | 2.4 | 2 |
| 2.3 | Phase 2 live | 3.1 | 2 |
| 2.4 | 2.2 | 3.2 | 2 |
| 3.1 | 2.3 | None | 3 |
| 3.2 | Phase 2 stable | None | 3 |
| 3.3 | Phase 2 stable | None | 3 |

---

## 🎯 Feature Prioritization

### P0 - Must Have (Phase 1)
| Epic | Feature | JTBD Coverage |
|------|---------|---------------|
| 1.1 | WebSocket real-time infrastructure | JTBD-2.1, 4.1 |
| 1.2 | Rapid intake form (<90 sec) | JTBD-1.1 |
| 1.3 | Vitals capture (<30 sec) | JTBD-2.2, 2.3 |
| 1.4 | Doctor Kanban dashboard | JTBD-3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7 |
| 1.5 | On-premise deployment | JTBD-5.1, 5.3, 5.4 |
| 2.1 | Public display | JTBD-4.1, 4.2, 4.3 |

### P1 - Should Have (Phase 2)
| Epic | Feature | JTBD Coverage |
|------|---------|---------------|
| 2.2 | LWBS tracking | JTBD-1.3 |
| 2.3 | Feedback collection | JTBD-2.5, 4.2 (refinement) |
| 2.4 | Ephemeral data compliance | JTBD-5.5, 5.6 |

### P2 - Nice to Have (Phase 3)
| Epic | Feature | JTBD Coverage |
|------|---------|---------------|
| 3.1 | Metrics dashboard | Expansion ROI |
| 3.2 | Technical documentation | Expansion readiness |
| 3.3 | Accessibility enhancements | JTBD-2.6, 6.1 |

---

## 📈 Milestone Schedule

| Milestone | Date | Phase | Key Deliverables |
|-----------|------|-------|------------------|
| M1: Core Workflow Operational | Week 12 | 1 | All four views functional, sub-second updates, glove-friendly tested, on-premise deployed |
| M2: Full Department Adoption | Week 24 | 2 | 100% daily active users, LWBS tracking, public display operational, staff satisfaction >70 |
| M3: Production-Ready System | Week 36 | 3 | Metrics dashboard, technical docs, accessibility audit, expansion decision approved |

---

## 🔮 Future Considerations

### Backlog (Not Scheduled)
| Item | Rationale for Deferral | Potential Phase |
|------|------------------------|-----------------|
| Emergency Bypass button | Out of scope for pilot (JTBD-1.2 scope note) | Phase 4 (if expansion approved) |
| Mobile app (iOS/Android) | Pilot uses Surface tablets + desktop workstations | Phase 4+ (if multi-site expansion) |
| Integration with EHR/EMR | Explicitly out of scope (air-gapped requirement) | Not planned |
| Multi-language support | Not required for pilot site | Phase 4+ (if expansion to other hospitals) |
| Advanced analytics (ML/AI) | Pilot focuses on foundational workflow | Phase 5+ (if data patterns emerge) |

### Decision Points
| Decision | By When | Inputs Needed |
|----------|---------|---------------|
| Expansion to 2-3 additional EDs | Week 40 (Month 10) | Case study ROI, staff satisfaction, technical docs |
| Hardware upgrade (8 vCPU / 32GB RAM) | Week 20 (if performance issues) | Performance testing results, load metrics |
| EHR integration exploration | Week 48 (Month 12) | Expansion success, hospital IT strategy |
| Advanced features (Emergency Bypass, ML) | Phase 4+ | Multi-site validation, clinical demand |

---

## 📊 Resource Allocation

### By Phase

| Phase | Dev | Design | QA | DevOps | Total FTE |
|-------|-----|--------|----|--------|-----------|
| 1 (Foundation) | 2.0 | 0.5 | 0.5 | 0.5 | 3.5 |
| 2 (Pilot Go-Live) | 1.0 | 0.25 | 0.5 | 0.25 | 2.0 |
| 3 (Optimization) | 0.5 | 0.1 | 0.25 | 0.1 | 0.95 |

### Critical Path

**Minimum Timeline Sequence (cannot be parallelized):**

```
Epic 1.1 (4 weeks) →
Epic 1.2 (3 weeks) →
Epic 1.3 (3 weeks) →
Epic 1.4 (5 weeks) →
Epic 1.5 (4 weeks) →
Epic 2.1 (3 weeks) →
Phase 2 Go-Live
```

**Critical Path Duration**: 22 weeks (Foundation + Public Display)
**Total Roadmap Duration**: 36 weeks (with parallelization and optimization)

---

## 📋 Requirements Summary

**Total Requirements Created**: 67

### Requirements by Epic

| Epic | Requirements | ID Range |
|------|--------------|----------|
| Epic 1.1: Real-Time Infrastructure | REQ-001 to REQ-004 | 4 requirements |
| Epic 1.2: Rapid Intake | REQ-005 to REQ-010 | 6 requirements |
| Epic 1.3: Triage Vitals | REQ-011 to REQ-016 | 6 requirements |
| Epic 1.4: Doctor Dashboard | REQ-017 to REQ-025 | 9 requirements |
| Epic 1.5: Air-Gapped Deployment | REQ-026 to REQ-033 | 8 requirements |
| Epic 2.1: Public Display | REQ-034 to REQ-040 | 7 requirements |
| Epic 2.2: LWBS Tracking | REQ-041 to REQ-044 | 4 requirements |
| Epic 2.3: Feedback Collection | REQ-045 to REQ-049 | 5 requirements |
| Epic 2.4: Ephemeral Data | REQ-050 to REQ-054 | 5 requirements |
| Epic 3.1: Metrics Dashboard | REQ-055 to REQ-058 | 4 requirements |
| Epic 3.2: Technical Documentation | REQ-059 to REQ-063 | 5 requirements |
| Epic 3.3: Accessibility | REQ-064 to REQ-067 | 4 requirements |

### Requirements by Priority

| Priority | Count | Percentage |
|----------|-------|------------|
| P0 (Must Have) | 39 | 58% |
| P1 (Should Have) | 18 | 27% |
| P2 (Nice to Have) | 10 | 15% |

---

**Document Status**: 🟢 Complete
**Created**: 2026-01-16
**Last Updated**: 2026-01-16
**Next Review**: Weekly (during Phase 1 execution)
