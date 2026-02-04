# Mermaid Patterns for GDPR Data Flow Diagrams

## Quick Reference

### Node Shapes

```mermaid
flowchart LR
    A[/"External Entity<br/>(Data Subject)"/]
    B(("Process<br/>(Circle)"))
    C[(Database)]
    D{Decision}
    E[["Sub-process"]]
    F[Standard Box]
```

| Shape | Syntax | Use For |
|-------|--------|---------|
| Parallelogram | `[/"text"/]` | External entities, data subjects |
| Circle | `(("text"))` | Processes, transformations |
| Cylinder | `[("text")]` | Data stores, databases |
| Diamond | `{"text"}` | Decisions, validations |
| Stadium | `(["text"])` | Terminals, endpoints |
| Subroutine | `[["text"]]` | Sub-processes |

### Arrow Types

```mermaid
flowchart LR
    A --> B
    C -.-> D
    E ==> F
    G --o H
    I --x J
```

| Arrow | Syntax | Meaning |
|-------|--------|---------|
| Solid | `-->` | Primary data flow |
| Dotted | `-.->` | Optional/conditional flow |
| Thick | `==>` | High-volume/critical flow |
| Circle end | `--o` | Asynchronous/batch |
| Cross end | `--x` | Terminated/blocked |

### Labeled Arrows

```mermaid
flowchart LR
    A -->|"Personal Data"| B
    C -->|"Consent: Yes"| D
    E -->|"Encrypted"| F
```

---

## GDPR-Specific Patterns

### Legal Basis Indicators

```mermaid
flowchart TB
    subgraph LegalBasis["Legal Basis Labels"]
        A[/"User"/] -->|"📜 Consent<br/>Art.6(1)(a)"| P1(("Registration"))
        B[/"Customer"/] -->|"📄 Contract<br/>Art.6(1)(b)"| P2(("Order Processing"))
        C[/"Visitor"/] -->|"⚖️ Legitimate Interest<br/>Art.6(1)(f)"| P3(("Analytics"))
        D[/"Employee"/] -->|"📋 Legal Obligation<br/>Art.6(1)(c)"| P4(("Tax Reporting"))
    end
```

### Data Category Styling

```mermaid
flowchart LR
    subgraph Categories["Data Categories"]
        BASIC[/"Basic PII<br/>(Name, Email)"/]
        FINANCIAL[/"Financial Data<br/>(Bank, Card)"/]
        SPECIAL[/"Special Category<br/>(Health, Biometric)"/]
        TECHNICAL[/"Technical Data<br/>(IP, Cookies)"/]
    end

    style BASIC fill:#4299e1,stroke:#2b6cb0
    style FINANCIAL fill:#f59e0b,stroke:#d97706
    style SPECIAL fill:#f56565,stroke:#c53030
    style TECHNICAL fill:#9f7aea,stroke:#6b46c1
```

### Retention Period Labels

```mermaid
flowchart TB
    DB1[(Customer DB<br/>📅 7 years)]
    DB2[(Session Logs<br/>📅 30 days)]
    DB3[(Marketing<br/>📅 Until withdrawal)]
    DB4[(Archive<br/>📅 Legal minimum)]
```

### Security Control Icons

```mermaid
flowchart LR
    A[Data] -->|"🔐 TLS 1.3"| B{Gateway}
    B -->|"🔒 Encrypted"| C[(Storage)]
    C -->|"🛡️ Access Controlled"| D(Process)
```

---

## Subgraph Patterns

### Organization Boundaries

```mermaid
flowchart TB
    subgraph Controller["🏢 Data Controller (Your Org)"]
        direction TB
        P1(("Core Processing"))
        DB1[(Primary Storage)]
    end

    subgraph Processor["☁️ Data Processor (Vendor)"]
        direction TB
        P2(("Outsourced Task"))
        DB2[(Vendor Storage)]
    end

    subgraph SubProcessor["🔧 Sub-Processor"]
        P3(("Specialized Service"))
    end

    P1 --> P2
    P2 --> P3
```

### Geographic Boundaries

```mermaid
flowchart TB
    subgraph EU["🇪🇺 European Union"]
        EU_SYS(("EU Processing"))
        EU_DB[(EU Database)]
    end

    subgraph US["🇺🇸 United States"]
        US_SYS(("US Processing"))
        US_DB[(US Database)]
    end

    EU_SYS -->|"SCCs Required"| US_SYS
```

### Data Lifecycle Phases

```mermaid
flowchart LR
    subgraph Collection["📥 Collection"]
        C1(("Capture"))
    end

    subgraph Processing["⚙️ Processing"]
        P1(("Transform"))
        P2(("Analyze"))
    end

    subgraph Storage["💾 Storage"]
        S1[(Active)]
        S2[(Archive)]
    end

    subgraph Deletion["🗑️ Deletion"]
        D1(("Purge"))
    end

    C1 --> P1 --> P2 --> S1 --> S2 --> D1
```

---

## Complex Flow Patterns

### Consent-Based Branching

```mermaid
flowchart TB
    USER[/"User"/] --> COLLECT(("Collect Data"))
    COLLECT --> CONSENT{Consent?}

    CONSENT -->|"Marketing: Yes"| MARKETING(("Marketing"))
    CONSENT -->|"Analytics: Yes"| ANALYTICS(("Analytics"))
    CONSENT -->|"All: No"| MINIMUM(("Essential Only"))

    MARKETING --> DB[(Full Profile)]
    ANALYTICS --> DB
    MINIMUM --> DB_MIN[(Minimal Data)]
```

### Data Subject Request Handling

```mermaid
flowchart TB
    DSR[/"📨 DSR Received"/] --> IDENTIFY{Request Type}

    IDENTIFY -->|"Access"| ACCESS(("Compile Data"))
    IDENTIFY -->|"Erasure"| ERASE(("Mark for Deletion"))
    IDENTIFY -->|"Rectification"| RECTIFY(("Update Records"))
    IDENTIFY -->|"Portability"| PORT(("Export Data"))

    ACCESS --> RESPOND[/"📤 Respond to Subject"/]
    ERASE --> RESPOND
    RECTIFY --> RESPOND
    PORT --> RESPOND
```

### Third-Party Data Sharing

```mermaid
flowchart LR
    subgraph Internal["Internal Systems"]
        CRM[(CRM)]
        ERP[(ERP)]
    end

    subgraph Partners["📤 Data Recipients"]
        PAYMENT[/"💳 Payment Provider"/]
        SHIPPING[/"📦 Shipping Partner"/]
        MARKETING[/"📧 Email Service"/]
    end

    CRM -->|"Contract"| PAYMENT
    ERP -->|"Contract"| SHIPPING
    CRM -->|"Consent"| MARKETING
```

---

## Styling Reference

### Complete Style Block

```mermaid
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#4299e1',
    'primaryTextColor': '#ffffff',
    'primaryBorderColor': '#2b6cb0',
    'lineColor': '#718096',
    'secondaryColor': '#48bb78',
    'tertiaryColor': '#f59e0b',
    'background': '#ffffff',
    'mainBkg': '#ffffff',
    'nodeBorder': '#2d3748',
    'clusterBkg': '#f7fafc',
    'clusterBorder': '#e2e8f0',
    'titleColor': '#2d3748',
    'edgeLabelBackground': '#ffffff'
  }
}}%%
flowchart TB
    A(("Process")) --> B[(Store)]
```

### Individual Node Styling

```
style NODE_ID fill:#COLOR,stroke:#BORDER,color:#TEXT
```

| Purpose | Fill | Stroke | Text |
|---------|------|--------|------|
| Controller | `#4299e1` | `#2b6cb0` | `#fff` |
| Processor | `#9f7aea` | `#6b46c1` | `#fff` |
| Data Store | `#48bb78` | `#2f855a` | `#fff` |
| External Entity | `#e2e8f0` | `#a0aec0` | `#2d3748` |
| Special Category | `#f56565` | `#c53030` | `#fff` |
| Warning/Attention | `#f59e0b` | `#d97706` | `#fff` |
| Success/Compliant | `#48bb78` | `#2f855a` | `#fff` |

---

## Common Emoji Reference

| Emoji | Meaning |
|-------|---------|
| 👤 | Individual data subject |
| 👥 | Group of data subjects |
| 🏢 | Organization/company |
| ☁️ | Cloud service/processor |
| 🔐 | Encryption in transit |
| 🔒 | Encryption at rest |
| 🛡️ | Security control |
| 📜 | Consent-based |
| 📄 | Contract-based |
| ⚖️ | Legitimate interest |
| 📋 | Legal obligation |
| 🇪🇺 | EU/EEA region |
| 🇺🇸 | United States |
| 🇬🇧 | United Kingdom |
| ✅ | Adequate/compliant |
| ⚠️ | Requires attention |
| ❌ | Non-compliant/blocked |
| 📅 | Retention period |
| 🗑️ | Deletion/purge |
| 📥 | Data input |
| 📤 | Data output |
| 💳 | Financial data |
| 🏥 | Health data |
| 🔬 | Biometric data |
