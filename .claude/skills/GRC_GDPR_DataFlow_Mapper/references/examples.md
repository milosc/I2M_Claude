# GDPR Data Flow Diagram Examples

## Example 1: E-Commerce Platform

### Context Diagram (Level 0)

```mermaid
flowchart TB
    subgraph External["External Entities"]
        CUST[/"👤 Customer"/]
        VENDOR[/"🏭 Vendor/Supplier"/]
        PAYMENT[/"💳 Payment Gateway"/]
        SHIPPING[/"📦 Logistics Partner"/]
        MARKETING[/"📧 Email Service"/]
    end

    subgraph System["E-Commerce Platform"]
        ECOM(("🛒 E-Commerce<br/>System"))
    end

    subgraph Storage["Data Stores"]
        CUSTDB[(Customer DB)]
        ORDERDB[(Orders DB)]
        ANALYTICS[(Analytics)]
    end

    CUST -->|"📜 Consent<br/>Registration, Orders"| ECOM
    ECOM -->|"Order Confirmation,<br/>Service Communications"| CUST

    VENDOR -->|"Product Data"| ECOM
    ECOM -->|"Purchase Orders"| VENDOR

    ECOM -->|"📄 Contract<br/>Payment Data"| PAYMENT
    PAYMENT -->|"Transaction Status"| ECOM

    ECOM -->|"📄 Contract<br/>Delivery Details"| SHIPPING
    SHIPPING -->|"Tracking Info"| ECOM

    ECOM -->|"📜 Consent<br/>Marketing Lists"| MARKETING
    MARKETING -->|"Campaign Metrics"| ECOM

    ECOM <--> CUSTDB
    ECOM <--> ORDERDB
    ECOM --> ANALYTICS

    style CUST fill:#e2e8f0,stroke:#a0aec0
    style VENDOR fill:#e2e8f0,stroke:#a0aec0
    style PAYMENT fill:#9f7aea,stroke:#6b46c1,color:#fff
    style SHIPPING fill:#9f7aea,stroke:#6b46c1,color:#fff
    style MARKETING fill:#9f7aea,stroke:#6b46c1,color:#fff
    style ECOM fill:#4299e1,stroke:#2b6cb0,color:#fff
    style CUSTDB fill:#48bb78,stroke:#2f855a,color:#fff
    style ORDERDB fill:#48bb78,stroke:#2f855a,color:#fff
    style ANALYTICS fill:#48bb78,stroke:#2f855a,color:#fff
```

### Level 1: System Decomposition

```mermaid
flowchart TB
    subgraph Customers["👤 Customers"]
        NEW_CUST[/"New Customer"/]
        EXIST_CUST[/"Existing Customer"/]
    end

    subgraph Registration["1. Customer Registration"]
        REG(("1.1 Account<br/>Creation"))
        CONSENT(("1.2 Consent<br/>Collection"))
    end

    subgraph Shopping["2. Shopping & Orders"]
        BROWSE(("2.1 Product<br/>Browsing"))
        CART(("2.2 Cart<br/>Management"))
        CHECKOUT(("2.3 Checkout"))
    end

    subgraph Fulfillment["3. Order Fulfillment"]
        PAYMENT_PROC(("3.1 Payment<br/>Processing"))
        INVENTORY(("3.2 Inventory<br/>Check"))
        SHIP(("3.3 Shipping"))
    end

    subgraph Marketing["4. Marketing"]
        SEGMENT(("4.1 Customer<br/>Segmentation"))
        CAMPAIGN(("4.2 Campaign<br/>Execution"))
    end

    subgraph Storage["Data Stores"]
        PROFILE[(Customer<br/>Profiles<br/>📅 Account + 3y)]
        ORDERS[(Order<br/>History<br/>📅 7 years)]
        CONSENT_DB[(Consent<br/>Records<br/>📅 Permanent)]
        ANALYTICS[(Analytics<br/>📅 2 years)]
    end

    NEW_CUST --> REG
    REG --> CONSENT
    CONSENT --> PROFILE
    CONSENT --> CONSENT_DB

    EXIST_CUST --> BROWSE
    BROWSE --> CART
    CART --> CHECKOUT
    CHECKOUT --> PAYMENT_PROC
    PAYMENT_PROC --> INVENTORY
    INVENTORY --> SHIP

    PROFILE --> SEGMENT
    ORDERS --> SEGMENT
    SEGMENT --> CAMPAIGN
    BROWSE --> ANALYTICS

    CHECKOUT --> ORDERS

    style NEW_CUST fill:#e2e8f0,stroke:#a0aec0
    style EXIST_CUST fill:#e2e8f0,stroke:#a0aec0
    style REG fill:#4299e1,stroke:#2b6cb0,color:#fff
    style CONSENT fill:#4299e1,stroke:#2b6cb0,color:#fff
    style BROWSE fill:#4299e1,stroke:#2b6cb0,color:#fff
    style CART fill:#4299e1,stroke:#2b6cb0,color:#fff
    style CHECKOUT fill:#4299e1,stroke:#2b6cb0,color:#fff
    style PAYMENT_PROC fill:#4299e1,stroke:#2b6cb0,color:#fff
    style INVENTORY fill:#4299e1,stroke:#2b6cb0,color:#fff
    style SHIP fill:#4299e1,stroke:#2b6cb0,color:#fff
    style SEGMENT fill:#4299e1,stroke:#2b6cb0,color:#fff
    style CAMPAIGN fill:#4299e1,stroke:#2b6cb0,color:#fff
    style PROFILE fill:#48bb78,stroke:#2f855a,color:#fff
    style ORDERS fill:#48bb78,stroke:#2f855a,color:#fff
    style CONSENT_DB fill:#48bb78,stroke:#2f855a,color:#fff
    style ANALYTICS fill:#48bb78,stroke:#2f855a,color:#fff
```

---

## Example 2: Healthcare Application

### Context with Special Category Data

```mermaid
flowchart TB
    subgraph Subjects["Data Subjects"]
        PATIENT[/"🏥 Patient"/]
        DOCTOR[/"👨‍⚕️ Healthcare Provider"/]
    end

    subgraph System["Healthcare Platform"]
        HEALTH(("🏥 Health<br/>Management<br/>System"))
    end

    subgraph SpecialData["⚠️ Special Category Processing"]
        DIAGNOSIS[(🔴 Medical<br/>Diagnoses)]
        PRESCRIPTIONS[(🔴 Prescriptions)]
        LAB[(🔴 Lab Results)]
    end

    subgraph Processors["Processors"]
        LAB_PARTNER[/"🔬 Lab Partner"/]
        PHARMACY[/"💊 Pharmacy"/]
        INSURANCE[/"📋 Insurance"/]
    end

    PATIENT -->|"📜 Explicit Consent<br/>Art.9(2)(a)"| HEALTH
    DOCTOR -->|"📋 Professional Obligation"| HEALTH

    HEALTH -->|"🔐 Encrypted"| DIAGNOSIS
    HEALTH -->|"🔐 Encrypted"| PRESCRIPTIONS
    HEALTH -->|"🔐 Encrypted"| LAB

    HEALTH -->|"📄 DPA<br/>Lab Orders"| LAB_PARTNER
    LAB_PARTNER -->|"Results"| HEALTH

    HEALTH -->|"📜 Patient Consent<br/>Prescription Data"| PHARMACY

    HEALTH -->|"📜 Patient Consent<br/>Claims Data"| INSURANCE

    style PATIENT fill:#e2e8f0,stroke:#a0aec0
    style DOCTOR fill:#e2e8f0,stroke:#a0aec0
    style HEALTH fill:#4299e1,stroke:#2b6cb0,color:#fff
    style DIAGNOSIS fill:#f56565,stroke:#c53030,color:#fff
    style PRESCRIPTIONS fill:#f56565,stroke:#c53030,color:#fff
    style LAB fill:#f56565,stroke:#c53030,color:#fff
    style LAB_PARTNER fill:#9f7aea,stroke:#6b46c1,color:#fff
    style PHARMACY fill:#9f7aea,stroke:#6b46c1,color:#fff
    style INSURANCE fill:#9f7aea,stroke:#6b46c1,color:#fff
```

### Security-Focused Detail View

```mermaid
flowchart LR
    subgraph Input["Patient Data Entry"]
        ENTRY[/"📝 Health Data"/]
    end

    subgraph Security["🛡️ Security Controls"]
        MFA{{"🔐 MFA<br/>Authentication"}}
        ENCRYPT{{"🔒 Field-Level<br/>Encryption"}}
        ACCESS{{"👥 Role-Based<br/>Access"}}
        AUDIT{{"📊 Audit<br/>Logging"}}
        MASK{{"🎭 Data<br/>Masking"}}
    end

    subgraph Storage["Secure Storage"]
        DB[(("🔒 Encrypted<br/>Health DB"))]
        AUDIT_LOG[(Immutable<br/>Audit Trail)]
    end

    ENTRY --> MFA
    MFA -->|"Authenticated"| ENCRYPT
    ENCRYPT --> ACCESS
    ACCESS --> AUDIT
    AUDIT --> DB
    AUDIT --> AUDIT_LOG
    DB --> MASK

    style ENTRY fill:#f56565,stroke:#c53030,color:#fff
    style MFA fill:#4299e1,stroke:#2b6cb0,color:#fff
    style ENCRYPT fill:#4299e1,stroke:#2b6cb0,color:#fff
    style ACCESS fill:#4299e1,stroke:#2b6cb0,color:#fff
    style AUDIT fill:#4299e1,stroke:#2b6cb0,color:#fff
    style MASK fill:#4299e1,stroke:#2b6cb0,color:#fff
    style DB fill:#48bb78,stroke:#2f855a,color:#fff
    style AUDIT_LOG fill:#48bb78,stroke:#2f855a,color:#fff
```

---

## Example 3: SaaS B2B Platform

### Multi-Tenant Data Flow

```mermaid
flowchart TB
    subgraph Tenants["Tenant Organizations"]
        T1[/"🏢 Tenant A (EU)"/]
        T2[/"🏢 Tenant B (US)"/]
        T3[/"🏢 Tenant C (UK)"/]
    end

    subgraph Platform["SaaS Platform"]
        API(("🔌 API Gateway"))
        AUTH(("🔐 Auth Service"))
        CORE(("⚙️ Core Logic"))
    end

    subgraph DataLayer["Data Isolation"]
        DB_EU[(🇪🇺 EU Region<br/>Tenant A Data)]
        DB_US[(🇺🇸 US Region<br/>Tenant B Data)]
        DB_UK[(🇬🇧 UK Region<br/>Tenant C Data)]
    end

    subgraph Shared["Shared Services"]
        LOGGING[(📊 Centralized<br/>Logging)]
        BACKUP[(💾 Backup<br/>Service)]
    end

    T1 -->|"🔐 OAuth"| API
    T2 -->|"🔐 OAuth"| API
    T3 -->|"🔐 OAuth"| API

    API --> AUTH
    AUTH --> CORE

    CORE <-->|"Data Residency:<br/>Frankfurt"| DB_EU
    CORE <-->|"Data Residency:<br/>Virginia<br/>📜 SCCs"| DB_US
    CORE <-->|"Data Residency:<br/>London<br/>✅ Adequacy"| DB_UK

    CORE -.->|"Anonymized<br/>Metrics Only"| LOGGING
    DB_EU --> BACKUP
    DB_US --> BACKUP
    DB_UK --> BACKUP

    style T1 fill:#e2e8f0,stroke:#a0aec0
    style T2 fill:#e2e8f0,stroke:#a0aec0
    style T3 fill:#e2e8f0,stroke:#a0aec0
    style API fill:#4299e1,stroke:#2b6cb0,color:#fff
    style AUTH fill:#4299e1,stroke:#2b6cb0,color:#fff
    style CORE fill:#4299e1,stroke:#2b6cb0,color:#fff
    style DB_EU fill:#48bb78,stroke:#2f855a,color:#fff
    style DB_US fill:#f59e0b,stroke:#d97706,color:#fff
    style DB_UK fill:#48bb78,stroke:#2f855a,color:#fff
    style LOGGING fill:#9f7aea,stroke:#6b46c1,color:#fff
    style BACKUP fill:#9f7aea,stroke:#6b46c1,color:#fff
```

---

## Example 4: HR/Employee Management

### Complete HR Data Flow

```mermaid
flowchart TB
    subgraph Subjects["Data Subjects"]
        APPLICANT[/"📝 Job Applicant"/]
        EMPLOYEE[/"👤 Employee"/]
        FORMER[/"📤 Former Employee"/]
    end

    subgraph Recruitment["1. Recruitment"]
        APPLY(("1.1 Application<br/>Receipt"))
        SCREEN(("1.2 CV<br/>Screening"))
        INTERVIEW(("1.3 Interview<br/>Process"))
    end

    subgraph Onboarding["2. Onboarding"]
        VERIFY(("2.1 Background<br/>Check"))
        CONTRACT(("2.2 Contract<br/>Creation"))
        SETUP(("2.3 System<br/>Access"))
    end

    subgraph Employment["3. Employment"]
        PAYROLL(("3.1 Payroll<br/>Processing"))
        PERFORM(("3.2 Performance<br/>Management"))
        TRAINING(("3.3 Training<br/>Records"))
    end

    subgraph Offboarding["4. Offboarding"]
        EXIT(("4.1 Exit<br/>Process"))
        ARCHIVE(("4.2 Record<br/>Archival"))
        DELETE(("4.3 Data<br/>Deletion"))
    end

    subgraph Storage["Data Stores"]
        ATS[(ATS Database<br/>📅 Rejected: 6mo<br/>📅 Hired: Employment)]
        HRIS[(HRIS<br/>📅 Employment + 7y)]
        PAYROLL_DB[(Payroll<br/>📅 7 years)]
        ARCHIVE_DB[(Archive<br/>📅 Legal minimum)]
    end

    subgraph External["External Processors"]
        BG_CHECK[/"🔍 Background<br/>Check Provider"/]
        PAYROLL_SVC[/"💰 Payroll<br/>Provider"/]
        BENEFITS[/"🏥 Benefits<br/>Provider"/]
    end

    APPLICANT --> APPLY
    APPLY --> SCREEN
    SCREEN --> INTERVIEW
    INTERVIEW -->|"Hired"| VERIFY
    APPLY --> ATS
    SCREEN --> ATS

    VERIFY -->|"📄 DPA"| BG_CHECK
    BG_CHECK --> VERIFY
    VERIFY --> CONTRACT
    CONTRACT --> SETUP
    CONTRACT --> HRIS

    EMPLOYEE --> PAYROLL
    PAYROLL -->|"📄 DPA"| PAYROLL_SVC
    PAYROLL --> PAYROLL_DB
    EMPLOYEE --> PERFORM
    PERFORM --> HRIS
    EMPLOYEE --> TRAINING
    TRAINING --> HRIS

    HRIS -->|"📜 Consent"| BENEFITS

    FORMER --> EXIT
    EXIT --> ARCHIVE
    HRIS --> ARCHIVE_DB
    ARCHIVE --> DELETE

    style APPLICANT fill:#e2e8f0,stroke:#a0aec0
    style EMPLOYEE fill:#e2e8f0,stroke:#a0aec0
    style FORMER fill:#e2e8f0,stroke:#a0aec0
    style APPLY fill:#4299e1,stroke:#2b6cb0,color:#fff
    style SCREEN fill:#4299e1,stroke:#2b6cb0,color:#fff
    style INTERVIEW fill:#4299e1,stroke:#2b6cb0,color:#fff
    style VERIFY fill:#4299e1,stroke:#2b6cb0,color:#fff
    style CONTRACT fill:#4299e1,stroke:#2b6cb0,color:#fff
    style SETUP fill:#4299e1,stroke:#2b6cb0,color:#fff
    style PAYROLL fill:#4299e1,stroke:#2b6cb0,color:#fff
    style PERFORM fill:#4299e1,stroke:#2b6cb0,color:#fff
    style TRAINING fill:#4299e1,stroke:#2b6cb0,color:#fff
    style EXIT fill:#4299e1,stroke:#2b6cb0,color:#fff
    style ARCHIVE fill:#4299e1,stroke:#2b6cb0,color:#fff
    style DELETE fill:#f56565,stroke:#c53030,color:#fff
    style ATS fill:#48bb78,stroke:#2f855a,color:#fff
    style HRIS fill:#48bb78,stroke:#2f855a,color:#fff
    style PAYROLL_DB fill:#48bb78,stroke:#2f855a,color:#fff
    style ARCHIVE_DB fill:#48bb78,stroke:#2f855a,color:#fff
    style BG_CHECK fill:#9f7aea,stroke:#6b46c1,color:#fff
    style PAYROLL_SVC fill:#9f7aea,stroke:#6b46c1,color:#fff
    style BENEFITS fill:#9f7aea,stroke:#6b46c1,color:#fff
```

---

## Example 5: Cross-Border Transfer Mapping

### Global Data Transfer Architecture

```mermaid
flowchart TB
    subgraph EU["🇪🇺 European Union (Controller HQ)"]
        EU_MAIN(("EU Main<br/>Operations"))
        EU_DB[(EU Customer<br/>Database)]
        EU_HR[(EU Employee<br/>Data)]
    end

    subgraph Adequate["✅ Adequacy Decision Countries"]
        UK_SUB[/"🇬🇧 UK Subsidiary"/]
        JP_SUB[/"🇯🇵 Japan Office"/]
        CH_BANK[/"🇨🇭 Swiss Bank"/]
    end

    subgraph SCC["📜 Standard Contractual Clauses"]
        US_CLOUD[/"🇺🇸 AWS<br/>(Cloud Hosting)"/]
        US_CRM[/"🇺🇸 Salesforce<br/>(CRM)"/]
        IN_SUPPORT[/"🇮🇳 Support Center"/]
        PH_BPO[/"🇵🇭 BPO Services"/]
    end

    subgraph BCR["🏛️ Binding Corporate Rules"]
        BR_SUB[/"🇧🇷 Brazil<br/>Subsidiary"/]
        MX_SUB[/"🇲🇽 Mexico<br/>Subsidiary"/]
        SG_SUB[/"🇸🇬 Singapore<br/>Regional HQ"/]
    end

    EU_MAIN <--> EU_DB
    EU_MAIN <--> EU_HR

    %% Adequacy transfers
    EU_MAIN -->|"✅ Direct Transfer"| UK_SUB
    EU_MAIN -->|"✅ Direct Transfer"| JP_SUB
    EU_MAIN -->|"✅ Direct Transfer"| CH_BANK

    %% SCC transfers
    EU_DB -->|"📜 SCC + TIA"| US_CLOUD
    EU_MAIN -->|"📜 SCC"| US_CRM
    EU_MAIN -->|"📜 SCC + TIA"| IN_SUPPORT
    EU_MAIN -->|"📜 SCC"| PH_BPO

    %% BCR transfers
    EU_MAIN -->|"🏛️ BCR Approved"| BR_SUB
    EU_MAIN -->|"🏛️ BCR Approved"| MX_SUB
    EU_MAIN -->|"🏛️ BCR Approved"| SG_SUB

    style EU_MAIN fill:#4299e1,stroke:#2b6cb0,color:#fff
    style EU_DB fill:#48bb78,stroke:#2f855a,color:#fff
    style EU_HR fill:#48bb78,stroke:#2f855a,color:#fff
    style UK_SUB fill:#48bb78,stroke:#2f855a
    style JP_SUB fill:#48bb78,stroke:#2f855a
    style CH_BANK fill:#48bb78,stroke:#2f855a
    style US_CLOUD fill:#f59e0b,stroke:#d97706
    style US_CRM fill:#f59e0b,stroke:#d97706
    style IN_SUPPORT fill:#f59e0b,stroke:#d97706
    style PH_BPO fill:#f59e0b,stroke:#d97706
    style BR_SUB fill:#9f7aea,stroke:#6b46c1
    style MX_SUB fill:#9f7aea,stroke:#6b46c1
    style SG_SUB fill:#9f7aea,stroke:#6b46c1
```

### Transfer Impact Assessment Summary

| Destination | Mechanism | TIA Required | Additional Measures |
|-------------|-----------|--------------|---------------------|
| 🇬🇧 UK | Adequacy | No | Standard DPA |
| 🇯🇵 Japan | Adequacy | No | Standard DPA |
| 🇨🇭 Switzerland | Adequacy | No | Standard DPA |
| 🇺🇸 USA (AWS) | SCC | Yes | Encryption, Supplementary Measures |
| 🇺🇸 USA (Salesforce) | SCC + DPF | Reduced | DPF Certification Verified |
| 🇮🇳 India | SCC | Yes | Enhanced security, access controls |
| 🇵🇭 Philippines | SCC | Yes | Pseudonymization, audit rights |
| 🇧🇷 Brazil | BCR | No | BCR compliance monitoring |
| 🇲🇽 Mexico | BCR | No | BCR compliance monitoring |
| 🇸🇬 Singapore | BCR | No | BCR compliance monitoring |

---

## Data Inventory Summary Template

After creating diagrams, generate this summary:

```markdown
# Data Flow Inventory Summary

## Organization
- **Controller**: [Name]
- **DPO Contact**: [Email]
- **Last Updated**: [Date]

## Data Categories

| Category | Data Elements | Legal Basis | Retention |
|----------|---------------|-------------|-----------|
| Customer Identity | Name, Email, Phone | Contract | Account + 3y |
| Transaction | Orders, Payments | Contract | 7 years |
| Marketing | Preferences, History | Consent | Until withdrawal |
| Technical | IP, Cookies, Logs | Legit Interest | 90 days |

## Processors

| Processor | Purpose | Location | Mechanism |
|-----------|---------|----------|-----------|
| AWS | Hosting | US | SCC |
| Salesforce | CRM | US | DPF |
| Stripe | Payments | US | SCC |

## Cross-Border Transfers

| Destination | Data Type | Volume | Mechanism |
|-------------|-----------|--------|-----------|
| USA | All | High | SCC/DPF |
| India | Support tickets | Medium | SCC |

## Security Controls

| Control | Implementation | Data Scope |
|---------|----------------|------------|
| Encryption at rest | AES-256 | All PII |
| Encryption in transit | TLS 1.3 | All data |
| Access control | RBAC + MFA | All systems |
| Audit logging | Centralized SIEM | All access |
```
