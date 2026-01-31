# Data Distribution Patterns

Reference for realistic data generation in prototype test data.

---

## Volume Profiles

```javascript
const VOLUME_PROFILES = {
  minimal: {
    description: "Quickstart testing - bare minimum data",
    catalogs: { departments: 3, skills: 10, locations: 5 },
    core: { users: 5, candidates: 20, jobs: 3 },
    transactional: { applications: 25, interviews: 30, feedback: 25 }
  },
  development: {
    description: "Standard development - realistic mid-size operation",
    catalogs: { departments: 8, skills: 50, locations: 15 },
    core: { users: 25, candidates: 150, jobs: 20 },
    transactional: { applications: 200, interviews: 300, feedback: 250 }
  },
  demo: {
    description: "Demo/sales - curated showcase data",
    catalogs: { departments: 5, skills: 25, locations: 8 },
    core: { users: 15, candidates: 75, jobs: 10 },
    transactional: { applications: 100, interviews: 150, feedback: 120 }
  },
  stress: {
    description: "Performance testing - high volume",
    catalogs: { departments: 15, skills: 200, locations: 50 },
    core: { users: 100, candidates: 5000, jobs: 200 },
    transactional: { applications: 8000, interviews: 15000, feedback: 12000 }
  }
};
```

---

## Entity Distribution Patterns

### Users by Role

```javascript
const USER_DISTRIBUTION = {
  recruiter: 0.32,      // 8 of 25
  hiring_manager: 0.40, // 10 of 25
  interviewer: 0.60,    // 15 of 25 (overlap with HMs)
  admin: 0.08,          // 2 of 25
  leadership: 0.12      // 3 of 25
};
```

### Candidates by Status

```javascript
const CANDIDATE_STATUS_DISTRIBUTION = {
  active: 0.57,       // Currently in pipeline
  passive: 0.20,      // Sourced but not applied
  hired: 0.13,        // Successfully hired
  archived: 0.07,     // Old/stale records
  blacklisted: 0.03   // Do not contact
};
```

### Applications by Stage

```javascript
const APPLICATION_STAGE_DISTRIBUTION = {
  new: 0.225,              // 45 of 200
  screening: 0.16,         // 32 of 200
  phone_interview: 0.09,   // 18 of 200
  technical: 0.125,        // 25 of 200
  onsite: 0.075,           // 15 of 200
  offer: 0.04,             // 8 of 200
  hired: 0.10,             // 20 of 200
  rejected: 0.15,          // 30 of 200
  withdrawn: 0.035         // 7 of 200
};
```

### Jobs by Status

```javascript
const JOB_STATUS_DISTRIBUTION = {
  open: 0.60,     // 12 of 20 - actively hiring
  paused: 0.10,   // 2 of 20 - temporarily on hold
  closed: 0.20,   // 4 of 20 - no longer hiring
  filled: 0.10    // 2 of 20 - position filled
};
```

---

## Temporal Patterns

### Application Age Distribution

```javascript
const APPLICATION_AGE_DISTRIBUTION = {
  last_7_days: 0.25,      // Recent applications
  last_30_days: 0.35,     // Within the month
  last_90_days: 0.25,     // Last quarter
  over_90_days: 0.15      // Legacy applications
};
```

### Interview Scheduling Patterns

```javascript
const INTERVIEW_SCHEDULING = {
  lead_time_days: { min: 2, max: 14, typical: 5 },
  duration_minutes: {
    phone_screen: 30,
    technical: 60,
    behavioral: 45,
    onsite: 180,
    final: 45
  },
  completion_rate: 0.85,
  feedback_submission_rate: 0.85,
  reschedule_rate: 0.12
};
```

### Hiring Velocity

```javascript
const HIRING_VELOCITY = {
  avg_days_to_hire: 23,
  by_department: {
    engineering: 28,
    sales: 18,
    marketing: 21,
    operations: 15,
    product: 25
  },
  stage_duration_days: {
    new_to_screening: 2,
    screening_to_interview: 5,
    interview_to_offer: 12,
    offer_to_hire: 4
  }
};
```

---

## Conversion Rates

### Pipeline Funnel

```javascript
const FUNNEL_CONVERSION_RATES = {
  new_to_screening: 0.71,           // 71% pass initial review
  screening_to_phone: 0.56,         // 56% get phone screen
  phone_to_technical: 0.72,         // 72% pass phone
  technical_to_onsite: 0.60,        // 60% pass technical
  onsite_to_offer: 0.53,            // 53% get offers
  offer_to_hired: 0.75              // 75% accept offers
};
```

### Source Effectiveness

```javascript
const SOURCE_EFFECTIVENESS = {
  linkedin: { applications: 0.30, quality_score: 3.8, hire_rate: 0.18 },
  indeed: { applications: 0.25, quality_score: 3.2, hire_rate: 0.12 },
  referral: { applications: 0.15, quality_score: 4.2, hire_rate: 0.40 },
  careers_page: { applications: 0.12, quality_score: 3.5, hire_rate: 0.15 },
  recruiter_outreach: { applications: 0.10, quality_score: 4.0, hire_rate: 0.22 },
  job_fair: { applications: 0.05, quality_score: 3.0, hire_rate: 0.08 },
  other: { applications: 0.03, quality_score: 3.3, hire_rate: 0.10 }
};
```

---

## Rating Distributions

### Interview Ratings

```javascript
const INTERVIEW_RATING_DISTRIBUTION = {
  5: 0.15,  // Exceptional
  4: 0.35,  // Strong
  3: 0.30,  // Meets expectations
  2: 0.15,  // Below expectations
  1: 0.05   // Poor
};
```

### Recommendation Distribution

```javascript
const RECOMMENDATION_DISTRIBUTION = {
  strong_hire: 0.12,
  hire: 0.28,
  neutral: 0.25,
  no_hire: 0.25,
  strong_no_hire: 0.10
};
```

---

## Persona Data Allocations

### Recruiter (Sarah)

```javascript
const RECRUITER_ALLOCATION = {
  assigned_candidates: 45,        // Active pipeline
  managed_jobs: 8,                // Jobs recruiting for
  daily_interviews: { min: 2, max: 6, typical: 4 },
  weekly_hires: { min: 0, max: 2, typical: 0.5 }
};
```

### Hiring Manager (Alex)

```javascript
const HIRING_MANAGER_ALLOCATION = {
  open_positions: 3,              // Roles hiring for
  candidates_to_review: 8,        // In interview stage
  pending_feedback: 2,            // Awaiting input
  team_size: 8                    // Direct reports
};
```

### Client (ACME Corp)

```javascript
const CLIENT_ALLOCATION = {
  open_positions: 3,              // Positions with agency
  submitted_candidates: 8,        // Candidates submitted
  pending_review: 4,              // Awaiting client feedback
  hired_ytd: 2                    // Successful placements
};
```

---

## Edge Case Scenarios

### Empty States

```javascript
const EMPTY_STATE_SCENARIOS = [
  { entity: 'job', condition: 'zero_applicants', count: 1 },
  { entity: 'candidate', condition: 'no_applications', count: 5 },
  { entity: 'interview', condition: 'no_feedback', count: 10 }
];
```

### High Volume Scenarios

```javascript
const HIGH_VOLUME_SCENARIOS = [
  { entity: 'job', condition: 'over_50_applicants', count: 2 },
  { entity: 'candidate', condition: 'over_5_applications', count: 3 }
];
```

### Error/Exception Scenarios

```javascript
const ERROR_SCENARIOS = [
  { type: 'duplicate_candidate', count: 2 },
  { type: 'withdrawn_at_offer', count: 3 },
  { type: 'rejected_after_onsite', count: 5 },
  { type: 'rescinded_offer', count: 1 }
];
```

---

## Reporting Data Patterns

### Weekly Snapshot Structure

```javascript
const WEEKLY_SNAPSHOT = {
  weeks_of_history: 12,
  metrics_captured: [
    'pipeline_by_stage',
    'applications_received',
    'interviews_completed',
    'offers_extended',
    'hires_made',
    'avg_time_in_stage'
  ]
};
```

### Dashboard Metrics

```javascript
const DASHBOARD_METRICS = {
  real_time: [
    'active_candidates',
    'open_positions',
    'interviews_today',
    'pending_feedback'
  ],
  period_based: [
    'applications_this_week',
    'hires_this_month',
    'avg_time_to_hire',
    'offer_acceptance_rate'
  ]
};
```

---

## Helper Functions

### Weighted Random Selection

```javascript
function weightedRandom(distribution) {
  const entries = Object.entries(distribution);
  const total = entries.reduce((sum, [, weight]) => sum + weight, 0);
  let random = Math.random() * total;
  
  for (const [value, weight] of entries) {
    random -= weight;
    if (random <= 0) return value;
  }
  return entries[entries.length - 1][0];
}
```

### Date Range Generation

```javascript
function generateDateInRange(startDaysAgo, endDaysAgo = 0) {
  const start = new Date();
  start.setDate(start.getDate() - startDaysAgo);
  const end = new Date();
  end.setDate(end.getDate() - endDaysAgo);
  
  return new Date(
    start.getTime() + Math.random() * (end.getTime() - start.getTime())
  );
}
```

### Ensure Temporal Ordering

```javascript
function ensureTemporalOrder(events, dateField = 'timestamp') {
  return events.sort((a, b) => 
    new Date(a[dateField]) - new Date(b[dateField])
  );
}
```

---

## Provenance

| Field | Value |
|-------|-------|
| Created | 2025-12-13 |
| Source | tools/01e-test-data-generator.md patterns |
| Purpose | Supporting reference for Prototype_TestData skill |
