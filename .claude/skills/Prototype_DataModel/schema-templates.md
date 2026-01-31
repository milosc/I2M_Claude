# Schema Templates

Templates for entity schema definitions used by Prototype_DataModel.

---

## Entity Schema Template

```json
{
  "$schema": "entity-schema-v1",
  "entity": "[EntityName]",
  "classification": "[core|catalog|transactional|junction|audit|config]",
  "volume": "[low|medium|high]",
  "description": "[Brief description of entity purpose]",
  
  "fields": [
    {
      "name": "[fieldName]",
      "type": "[string|number|boolean|date|uuid|enum|array|object]",
      "required": true,
      "unique": false,
      "indexed": false,
      "default": null,
      "description": "[Field description]",
      "example": "[Example value]",
      
      "validation": {
        "minLength": null,
        "maxLength": null,
        "min": null,
        "max": null,
        "pattern": null,
        "format": null
      },
      
      "enumRef": null,
      "foreignKey": null,
      "computedFrom": null
    }
  ],
  
  "timestamps": {
    "createdAt": true,
    "updatedAt": true,
    "deletedAt": false
  },
  
  "softDelete": false,
  
  "indexes": [
    {
      "name": "[index_name]",
      "fields": ["[field1]", "[field2]"],
      "unique": false
    }
  ],
  
  "displayField": "[fieldName]",
  "displayTemplate": "${field1} ${field2}",
  "searchFields": ["[field1]", "[field2]"],
  
  "requirements_trace": ["[US-XXX]", "[FR-XXX]"]
}
```

---

## Field Type Reference

| Type | IndexedDB | TypeScript | Description |
|------|-----------|------------|-------------|
| `string` | string | string | Text data |
| `number` | number | number | Numeric (int or float) |
| `boolean` | boolean | boolean | True/false |
| `date` | string (ISO) | string | ISO 8601 date-time |
| `uuid` | string | string | Unique identifier |
| `enum` | string | union type | Constrained string |
| `array` | array | T[] | List of items |
| `object` | object | Record<K,V> | Nested structure |

---

## Relationship Template

```json
{
  "id": "REL-[XXX]",
  "name": "[relationship_name]",
  "type": "[one-to-many|many-to-one|many-to-many]",
  "from": {
    "entity": "[ParentEntity]",
    "field": "id",
    "role": "parent"
  },
  "to": {
    "entity": "[ChildEntity]",
    "field": "[foreignKeyField]",
    "role": "child"
  },
  "cascadeDelete": false,
  "cascadeUpdate": true,
  "required": true,
  "description": "[Relationship description]"
}
```

---

## Many-to-Many Junction Template

```json
{
  "id": "REL-[XXX]",
  "name": "[entity1]_[entity2]",
  "type": "many-to-many",
  "junction": {
    "entity": "[JunctionEntity]",
    "leftKey": "[entity1Id]",
    "rightKey": "[entity2Id]"
  },
  "from": "[Entity1]",
  "to": "[Entity2]",
  "description": "[Relationship description]"
}
```

---

## Enumeration Template

```json
{
  "[EnumName]": {
    "description": "[What this enum represents]",
    "values": [
      {
        "key": "[snake_case_key]",
        "label": "[Display Label]",
        "description": "[Optional description]",
        "isDefault": false,
        "order": 1,
        "category": "[optional grouping]",
        "terminal": false
      }
    ],
    "transitions": [
      {
        "from": "[fromKey]",
        "to": ["[toKey1]", "[toKey2]"]
      }
    ]
  }
}
```

---

## Validation Rule Template

```json
{
  "id": "VR-[XXX]",
  "entity": "[EntityName]",
  "rule": "[rule_name]",
  "type": "[uniqueness|custom|comparison|range|format]",
  "fields": ["[field1]"],
  "condition": "[SQL-like condition or description]",
  "message": "[User-facing error message]",
  "onlyOn": ["create", "update"],
  "requirements_trace": ["[FR-XXX]"]
}
```

---

## Computed Field Template

```json
{
  "entity": "[EntityName]",
  "field": "[computedFieldName]",
  "formula": "[Computation description or pseudo-SQL]",
  "type": "[derived|aggregation]",
  "returns": "[string|number|object|array]",
  "dependencies": ["[field1]", "[field2]"]
}
```

---

## IndexedDB Store Template

```javascript
const STORE_TEMPLATE = {
  "[storeName]": {
    keyPath: "id",
    autoIncrement: false,
    indexes: [
      {
        name: "by_[field]",
        keyPath: "[fieldName]",
        unique: false
      },
      {
        name: "by_[field1]_[field2]",
        keyPath: ["[field1]", "[field2]"],
        unique: false
      }
    ]
  }
};
```

---

## Common Entity Patterns

### Core Entity (User, Candidate, Job)

- Has `id`, `createdAt`, `updatedAt`
- Has `status` enum field
- Has display field (name/title)
- Has search fields
- May have soft delete

### Catalog Entity (Department, Skill)

- Has `id`, `name`, `code`
- Usually unique constraint on name/code
- Rarely updated after creation
- Small volume

### Transactional Entity (Application, Interview)

- Has foreign keys to core entities
- Has `createdAt` timestamp
- Often has `status` with transitions
- Higher volume

### Junction Entity (JobSkill, TeamMember)

- Compound primary key or surrogate
- Two foreign key fields
- May have additional metadata
- Indexes on both FK fields

### Audit Entity (ActivityLog)

- Has `timestamp`, `action`, `userId`
- Has `entityType`, `entityId` for polymorphic reference
- Usually append-only
- High volume
