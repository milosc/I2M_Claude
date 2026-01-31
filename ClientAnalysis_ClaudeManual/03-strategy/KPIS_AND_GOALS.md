# KPIs and Success Metrics - ClaudeManual

---
system_name: ClaudeManual
checkpoint: CP-8
date_created: 2026-01-31
session: disc-claude-manual-008
created_by: discovery-kpis-generator
---

## North Star Metric

**Time-to-Independent-Productivity**

**Definition**: Hours from first framework exposure to successfully executing a complete workflow (discovery/prototype/implementation) without assistance.

**Current Baseline**: 16 hours (manual training 3-4 hours + trial-and-error 12+ hours)

**Target**: 2 hours (self-guided exploration with ClaudeManual)

**Timeline**: End of Phase 2 (Week 12)

**Measurement Method**:
- User survey: "How long from first seeing framework to completing your first workflow independently?"
- Task completion tracking: Time from account creation to first successful command execution
- Training session elimination: Reduction in trainer hours per team member

**Traces To**: PP-1.1 (Knowledge Transfer Complexity), JTBD-1.1 (Enable Self-Service Learning), Product Vision North Star

**Why This Metric**: Directly measures the vision of enabling self-service learning and reducing dependency on manual knowledge transfer. This metric captures the combined impact of faster onboarding, better discoverability, and contextual documentation.

---

## KPI Dashboard

### Adoption Metrics (Leading Indicators)

| KPI | Current | Target | Timeline | Measurement Method | Traces To |
|-----|---------|--------|----------|-------------------|-----------|
| **Active Weekly Users** | 0 | 40-50 | Phase 2 (Week 12) | Unique visitors per week (analytics) | JTBD-1.1, PP-1.1 |
| **Framework Coverage** | 0% | 100% | Phase 1 (Week 4) | Components documented / total components (115+) | JTBD-1.2 |
| **Search Usage Rate** | N/A | 5+ searches/user/week | Phase 2 (Week 8) | Search queries per active user | JTBD-1.3, PP-1.3 |
| **Stage Filter Usage** | N/A | >50% of sessions | Phase 2 (Week 8) | Sessions with stage filter active | JTBD-1.4, PP-1.4 |
| **File Path Copy Rate** | N/A | >60% of developers | Phase 2 (Week 8) | Users who use "Copy Path" feature | JTBD-1.5, PP-1.6 |
| **Favorites Adoption** | N/A | >30% of users with 3+ favorites | Phase 2 (Week 12) | Users with 3+ favorites saved | JTBD-1.6, PP-1.5 |

---

### Engagement Metrics (Leading Indicators)

| KPI | Current | Target | Timeline | Measurement Method | Traces To |
|-----|---------|--------|----------|-------------------|-----------|
| **Search Success Rate** | N/A | >80% | Phase 2 (Week 8) | Searches leading to click on result | JTBD-1.3, PP-1.3 |
| **Average Session Duration** | N/A | 3-5 minutes | Phase 2 (Week 8) | Time spent per session (analytics) | JTBD-2.2 |
| **Return Rate** | N/A | >60% | Phase 2 (Week 12) | Weekly active users / monthly active users | JTBD-2.2 |
| **Detail View Depth** | N/A | >70% view examples tab | Phase 2 (Week 8) | Users clicking into Examples/Options/Workflow tabs | JTBD-1.2, JTBD-2.1 |
| **Comparison Feature Usage** | N/A | >20% of users | Phase 3 (optional) | Users opening side-by-side comparison view | JTBD-1.8 |

---

### Efficiency Metrics (Leading & Lagging Indicators)

| KPI | Current | Target | Timeline | Measurement Method | Traces To |
|-----|---------|--------|----------|-------------------|-----------|
| **Onboarding Time** | 3-4 hours | 30-60 minutes | Phase 2 (Week 12) | Training session duration tracking | PP-1.1, JTBD-1.1 |
| **Support Tickets/Slack Questions** | 40-50/month | 10-15/month | Phase 2 (Week 12) | Tagged framework-related Slack threads | PP-1.1, PP-1.2, PP-1.3 |
| **Time to Find Component** | >5 minutes | <30 seconds | Phase 2 (Week 8) | User task timing (sample study) | JTBD-1.3, PP-1.3 |
| **Time to Locate Source File** | 10-15 minutes | 10 seconds | Phase 2 (Week 8) | Developer customization workflow timing | JTBD-1.5, PP-1.6 |
| **Post-Training Retention** | 40-50% | >90% | Phase 2 (Week 6) | Quiz 5 users 1 week after onboarding | JTBD-1.1, JTBD-2.1 |

---

### Quality Metrics (Lagging Indicators)

| KPI | Current | Target | Timeline | Measurement Method | Traces To |
|-----|---------|--------|----------|-------------------|-----------|
| **Documentation Accuracy** | Unknown | >95% | Phase 2 (Week 8) | User feedback survey (5-point scale) | JTBD-1.2, JTBD-2.1 |
| **User Satisfaction (NPS)** | Unknown | >4.0/5 | Phase 2 (Week 12) | Post-usage survey (NPS or 5-star rating) | JTBD-2.2 |
| **User Confidence Score** | Unknown | >80% | Phase 2 (Week 12) | Survey: "I feel confident using the framework" (1-5 scale) | JTBD-2.1 |
| **Framework Adoption Rate** | 30% | 80%+ | Phase 2 (Week 12) | Unique users running commands / total eligible team members | PP-1.1, Vision Goal |
| **Framework Misuse Incidents** | Unknown | -70% reduction | Phase 2 (Week 12) | Errors due to using wrong tool for phase | JTBD-1.4, JTBD-2.1 |

---

### Business Impact Metrics (Lagging Indicators)

| KPI | Current | Target | Timeline | Measurement Method | Traces To |
|-----|---------|--------|----------|-------------------|-----------|
| **Trainer Hours per Team Member** | 3-4 hours | 0 hours | Phase 2 (Week 12) | Manual training session hours logged | PP-1.1, Vision Goal |
| **Framework Creator Time Spent on Training** | 20-30 hours/month | 5-10 hours/month | Phase 2 (Week 12) | Time tracking for training vs. feature development | PP-1.1, Business Goal |
| **Framework Command Execution Success Rate** | 60-70% | 85%+ | Phase 2 (Week 12) | Commands completed without errors (from pipeline_progress.json) | JTBD-2.1 |
| **Framework Contributions (PRs/Custom Agents)** | Baseline | +300% | Phase 3 (Week 24) | GitHub PRs, custom agent submissions | JTBD-3.2, Vision Goal |
| **Client Demo Preparation Time** | Unknown | -50% | Phase 2 (Week 12) | Time to prepare framework capability demos | JTBD-3.1 |

---

## Phase-Specific Goals

### Phase 1: Internal Pilot (Weeks 1-4)

**Target Users**: Framework team (2-3 people)

**Goals**:
1. ✅ **100% Framework Coverage**: All 115+ skills/commands/agents documented and indexed
2. ✅ **Search Performance**: Search returns relevant results in <2 seconds
3. ✅ **Master-Detail UI**: Hierarchical navigation + multi-section detail view functional
4. ✅ **Trainer Time Reduction**: Framework creators reduce onboarding prep time by 50%+
5. ✅ **File Path Copy**: Developers can locate source files in <10 seconds

**Success Criteria**:
- All components correctly parsed from markdown frontmatter
- Zero broken documentation links
- Framework team can onboard 1 new user using only ClaudeManual (no manual training)

**KPIs Tracked**:
- Framework Coverage: 0% → 100%
- Search Performance: N/A → <2s response time
- Trainer Prep Time: Baseline → -50%

---

### Phase 2: Team Rollout (Weeks 5-12)

**Target Users**: All HTEC teams (40-60 people: product, developers, delivery)

**Goals**:
1. ✅ **Onboarding Time**: 3-4 hours → 30-60 minutes (80% reduction)
2. ✅ **Support Reduction**: Slack questions 40-50/month → 10-15/month (60% reduction)
3. ✅ **Framework Adoption**: 30% → 80%+ within 30 days
4. ✅ **User Confidence**: >80% feel confident using framework without expert help
5. ✅ **Post-Training Retention**: >90% can locate tools 1 week after onboarding
6. ✅ **Search Success**: >80% of searches result in finding correct tool
7. ✅ **Stage Filter Usage**: >50% of sessions use stage-based filtering
8. ✅ **Favorites Adoption**: >30% of users have 3+ favorites saved

**Success Criteria**:
- Framework creator spends <10 hours/month on training (down from 20-30)
- Product managers independently run discovery workflows without developer support
- Developers use "Copy Path" feature for customization (>60% adoption)
- User satisfaction score >4.0/5

**KPIs Tracked**:
- All Adoption, Engagement, Efficiency, Quality, and Business Impact metrics
- Weekly tracking dashboard with trend analysis

---

### Phase 3: External Access (Weeks 13+, Optional)

**Target Users**: Client partners, conference attendees, open-source community

**Goals**:
1. ✅ **Client Self-Service**: Clients can explore framework capabilities without demo calls
2. ✅ **Conference Engagement**: Attendees can access documentation during/after presentations
3. ✅ **Export Usage**: >20% of business developers use export (PDF/PPTX) for proposals
4. ✅ **External Traffic**: 50+ external visitors/month (if public)
5. ✅ **Perceived Competence**: Build/client partners feel confident presenting framework

**Success Criteria**:
- Public deployment with anonymized examples
- Export functionality generates presentation-ready materials
- External users can answer "what can Claude framework do?" independently

**KPIs Tracked**:
- External Active Users: 0 → 50+/month
- Export Feature Usage: N/A → >20% of biz dev users
- Demo Prep Time: Baseline → -50%

---

## Success Criteria by Pain Point

| Pain Point | KPI | Success Threshold | Timeline | Measurement |
|------------|-----|-------------------|----------|-------------|
| **PP-1.1: Knowledge Transfer Complexity** | Onboarding Time | <1 hour | Phase 2 (Week 12) | Training session duration |
| **PP-1.1: Knowledge Transfer Complexity** | Trainer Hours/Month | <10 hours | Phase 2 (Week 12) | Time tracking |
| **PP-1.2: Lack of Contextual Documentation** | Detail View Depth | >70% view examples tab | Phase 2 (Week 8) | Analytics |
| **PP-1.2: Lack of Contextual Documentation** | User Confidence Score | >80% | Phase 2 (Week 12) | Survey |
| **PP-1.3: Discoverability Challenge** | Search Success Rate | >80% | Phase 2 (Week 8) | Search analytics |
| **PP-1.3: Discoverability Challenge** | Time to Find Component | <30 seconds | Phase 2 (Week 8) | Task timing |
| **PP-1.4: Organizational Chaos** | Stage Filter Usage | >50% of sessions | Phase 2 (Week 8) | Analytics |
| **PP-1.4: Organizational Chaos** | Framework Misuse | -70% incidents | Phase 2 (Week 12) | Error tracking |
| **PP-1.5: Lack of Personalization** | Favorites Adoption | >30% with 3+ favorites | Phase 2 (Week 12) | User profiles |
| **PP-1.6: Developer Friction** | Time to Locate Source File | <10 seconds | Phase 2 (Week 8) | Task timing |
| **PP-1.6: Developer Friction** | Path Copy Usage | >60% of developers | Phase 2 (Week 8) | Analytics |

---

## Success Criteria by JTBD

| JTBD | KPI | Success Threshold | Timeline |
|------|-----|-------------------|----------|
| **JTBD-1.1: Enable Self-Service Learning** | Onboarding Time | <1 hour | Phase 2 (Week 12) |
| **JTBD-1.1: Enable Self-Service Learning** | Post-Training Retention | >90% | Phase 2 (Week 6) |
| **JTBD-1.2: Understand Component Context** | Detail View Depth | >70% view examples | Phase 2 (Week 8) |
| **JTBD-1.3: Quickly Find Relevant Tools** | Search Success Rate | >80% | Phase 2 (Week 8) |
| **JTBD-1.3: Quickly Find Relevant Tools** | Time to Find Component | <30 seconds | Phase 2 (Week 8) |
| **JTBD-1.4: Understand Workflow Stage Applicability** | Stage Filter Usage | >50% of sessions | Phase 2 (Week 8) |
| **JTBD-1.5: Edit Source Files Efficiently** | Time to Locate File | <10 seconds | Phase 2 (Week 8) |
| **JTBD-1.5: Edit Source Files Efficiently** | Path Copy Usage | >60% developers | Phase 2 (Week 8) |
| **JTBD-1.6: Bookmark Frequently-Used Tools** | Favorites Adoption | >30% with 3+ favorites | Phase 2 (Week 12) |
| **JTBD-1.7: Navigate Hierarchies Visually** | Active Weekly Users | 40-50 | Phase 2 (Week 12) |
| **JTBD-1.8: Compare Similar Components** | Comparison Usage | >20% of users | Phase 3 (optional) |
| **JTBD-2.1: Feel Confident Using Framework** | User Confidence Score | >80% | Phase 2 (Week 12) |
| **JTBD-2.2: Feel Autonomous in Exploration** | Support Tickets | <15/month | Phase 2 (Week 12) |
| **JTBD-3.1: Be Perceived as Competent** | Demo Prep Time | -50% | Phase 2 (Week 12) |
| **JTBD-3.2: Contribute to Team Efficiency** | Framework Contributions | +300% | Phase 3 (Week 24) |

---

## Measurement Methodology

### Analytics Instrumentation (Phase 1)

**Tool**: Google Analytics 4 or Mixpanel

**Events to Track**:
- `page_view`: Master pane navigation, detail pane views
- `search_query`: Search terms, filters applied, results clicked
- `stage_filter_toggle`: Stage filter activated/deactivated
- `file_path_copy`: File path copied to clipboard
- `favorite_added`: Component added to favorites
- `tab_click`: Detail pane tab interactions (Purpose, Examples, Options, Workflow)
- `comparison_view`: Side-by-side comparison opened

**User Properties**:
- `user_type`: Framework Creator, Product Person, Developer, etc.
- `onboarding_date`: Date of first session
- `favorites_count`: Number of favorites saved

---

### Survey Instrumentation (Phase 2)

**Post-Onboarding Survey** (Week 1):
- "How long did it take you to complete your first framework workflow independently?" (Time to Independent Productivity)
- "Rate your confidence using the framework" (1-5 scale)
- "Did you find the documentation clear and helpful?" (Yes/No + comments)

**Monthly Satisfaction Survey**:
- "How likely are you to recommend ClaudeManual to a colleague?" (NPS: 0-10)
- "What feature do you use most?" (Multi-choice)
- "What's missing or confusing?" (Open text)

**Retention Test** (1 week post-onboarding):
- "Locate the skill for extracting JTBD from interviews" (Timed task)
- "Find the command to run multi-agent discovery" (Timed task)
- "Copy the file path for the Discovery_JTBD skill" (Timed task)

---

### Slack/Support Tracking (Ongoing)

**Method**: Tag all framework-related Slack messages with `#framework-question` channel or emoji reaction

**Baseline Measurement** (Pre-ClaudeManual):
- Count framework-related questions in last 30 days
- Categorize by question type (tool discovery, usage, debugging)

**Ongoing Tracking** (Post-ClaudeManual):
- Weekly count of framework questions
- Track if question was answerable via ClaudeManual (gap analysis)
- Monitor question types shifting from "how do I find X?" to "how do I debug X?"

---

## Risk Indicators (Leading Indicators of Failure)

| Risk Indicator | Threshold | Action Plan |
|----------------|-----------|-------------|
| **Low Return Rate** | <40% weekly active / monthly active | Investigate UX friction, add missing search keywords |
| **High Support Tickets** | >25/month after Phase 2 | Identify common questions → add missing documentation |
| **Low Search Usage** | <3 searches/user/week | Improve search visibility, add onboarding tutorial |
| **Low Favorites Adoption** | <15% of users | Re-evaluate UI placement, add prompts to save favorites |
| **Stale Documentation** | >5% broken links or outdated examples | Implement file watcher for auto-regeneration |
| **Low Developer Path Copy** | <40% of developers | Improve UI affordance (make button more prominent) |

---

## Traceability

### Pain Point Coverage
- **PP-1.1** (Knowledge Transfer Complexity): 3 KPIs (Onboarding Time, Trainer Hours, Active Users)
- **PP-1.2** (Lack of Contextual Documentation): 2 KPIs (Detail View Depth, User Confidence)
- **PP-1.3** (Discoverability Challenge): 2 KPIs (Search Success Rate, Time to Find Component)
- **PP-1.4** (Organizational Chaos): 2 KPIs (Stage Filter Usage, Framework Misuse)
- **PP-1.5** (Lack of Personalization): 1 KPI (Favorites Adoption)
- **PP-1.6** (Developer Friction): 2 KPIs (Time to Locate File, Path Copy Usage)

**Coverage**: 100% of pain points (6/6) have measurable KPIs

### JTBD Coverage
- **12 JTBD jobs** → **15 unique KPIs**
- All P0 jobs (JTBD-1.1, JTBD-1.2, JTBD-1.7, JTBD-2.1) have success criteria with <12 week timelines
- All P1 jobs have KPIs tracked in Phase 2
- P2 jobs (JTBD-1.6, JTBD-2.2, JTBD-3.2) have Phase 2-3 KPIs

**Coverage**: 100% of JTBD jobs (12/12) have measurable KPIs

### Strategic Pillars Coverage
1. **Visual-First Learning** → KPIs: Active Users, Detail View Depth, User Confidence
2. **Intelligent Discovery** → KPIs: Search Success Rate, Time to Find Component, Stage Filter Usage
3. **Developer Extensibility** → KPIs: Path Copy Usage, Time to Locate File, Framework Contributions
4. **Contextual Confidence** → KPIs: User Confidence Score, Detail View Depth, Framework Misuse Reduction

**Coverage**: All 4 strategic pillars have quantitative success metrics

---

## Appendix: KPI Calculation Formulas

### Time-to-Independent-Productivity (North Star)
```
Formula: Avg(Time from first framework exposure to first independent workflow completion)
Measurement: User survey + task completion timestamp delta
Target: <2 hours (median), <4 hours (90th percentile)
```

### Search Success Rate
```
Formula: (Searches with click on result / Total searches) × 100
Measurement: Analytics event tracking
Target: >80%
```

### Post-Training Retention
```
Formula: (Users passing retention test / Total onboarded users) × 100
Measurement: Timed task completion 1 week post-onboarding
Target: >90%
```

### Framework Adoption Rate
```
Formula: (Unique users running commands in last 30 days / Total eligible team members) × 100
Measurement: pipeline_progress.json logs
Target: >80%
```

### User Confidence Score
```
Formula: Avg("I feel confident using the framework" rating on 1-5 scale)
Measurement: Monthly survey
Target: >4.0/5 (equivalent to >80%)
```

### Trainer Hours Reduction
```
Formula: ((Baseline trainer hours - Current trainer hours) / Baseline trainer hours) × 100
Measurement: Time tracking logs
Target: >80% reduction (20-30 hours/month → 5-10 hours/month)
```

---

*This KPI document defines 25+ measurable success metrics across adoption, engagement, efficiency, quality, and business impact categories. All KPIs trace to validated pain points, JTBD jobs, and strategic pillars. Measurement methodology includes analytics instrumentation, user surveys, and Slack/support tracking.*
