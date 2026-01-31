---
name: csv-excel-data-wrangler
description: Clean, filter, join, pivot, and export CSV/XLSX data reliably with reproducible steps.
model: sonnet
allowed-tools: Read, Write, Edit, Bash
hooks:
  PreToolUse:
    - matcher: "*"
      once: true
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill csv-excel-data-wrangler started '{"stage": "utility"}'
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill csv-excel-data-wrangler ended '{"stage": "utility"}'
---

## FIRST ACTION (MANDATORY)

Before doing ANYTHING else, run this command:

```bash
"$CLAUDE_PROJECT_DIR/.claude/hooks/log-lifecycle.sh" skill csv-excel-data-wrangler instruction_start '{"stage": "utility", "method": "instruction-based"}'
```

---

# CSV & Excel Data Wrangler Skill

## What This Skill Enables

Claude can clean, transform, analyze, and merge CSV and Excel files with pandas. Upload messy spreadsheets and get production-ready data pipelines, statistical summaries, and formatted exports.

## Prerequisites

**Required:**
- Claude Pro subscription
- Code Interpreter feature enabled
- CSV or Excel file uploaded to conversation

**What Claude handles:**
- Installing pandas, openpyxl, and data processing libraries
- Detecting file encodings and formats
- Type inference and conversion
- Memory-efficient processing of large files

## How to Use This Skill

### Quick Data Cleaning

**Prompt:** "Clean this CSV file: remove duplicates, fix missing values, standardize column names, and export as clean.csv"

Claude will:
1. Load and analyze the file structure
2. Identify data quality issues
3. Apply cleaning transformations
4. Export cleaned version

### Data Merging & Joining

**Prompt:** "Merge customers.csv and orders.csv on customer_id. Show me the combined data and export as customer_orders.xlsx"

Claude will:
1. Load both files
2. Detect join keys
3. Perform the merge (inner/left/right/outer)
4. Validate results
5. Export formatted Excel file

### Data Analysis & Summaries

**Prompt:** "Analyze this sales data: show me summary statistics, identify top products, calculate monthly trends, and create a pivot table by region."

Claude will:
1. Generate descriptive statistics
2. Perform aggregations
3. Create pivot tables
4. Calculate trends
5. Present insights

### Format Conversion

**Prompt:** "Convert this Excel workbook to CSV files, one per sheet, with UTF-8 encoding."

Claude will:
1. Read all Excel sheets
2. Export each as separate CSV
3. Handle encoding properly
4. Preserve data types where possible

## Common Workflows

### CRM Data Cleanup
```
"Clean this customer export:
1. Remove duplicate emails (keep most recent)
2. Standardize phone numbers to (XXX) XXX-XXXX format
3. Fill missing company names with 'Unknown'
4. Split full_name into first_name and last_name
5. Export as customers_clean.xlsx"
```

### Sales Report Generation
```
"Analyze this sales data:
1. Calculate total revenue by product category
2. Identify top 10 customers by revenue
3. Show month-over-month growth
4. Create a pivot table: rows=salesperson, columns=month, values=revenue
5. Export summary as sales_report.xlsx with formatted numbers"
```

### Data Validation
```
"Validate this CSV:
1. Check for duplicate IDs
2. Identify rows with missing required fields (name, email, phone)
3. Flag invalid email formats
4. Report data quality issues
5. Export clean rows and error rows separately"
```

### Multi-File Consolidation
```
"Combine all CSV files I upload into one master file:
1. Ensure columns match (add missing ones)
2. Add a 'source_file' column
3. Remove duplicates across all files
4. Sort by date column
5. Export as consolidated_data.csv"
```

## Tips for Best Results

1. **Be Specific About Columns**: Name the exact columns you want to work with
2. **Describe Your Data**: Mention what each column represents for better context
3. **Specify Output Format**: Tell Claude exactly how you want the result formatted
4. **Handle Missing Data**: Be explicit about how to handle nulls (drop, fill with value, forward-fill, etc.)
5. **Large Files**: For files >100MB, ask Claude to process in chunks or sample first
6. **Date Formats**: Specify your expected date format (MM/DD/YYYY vs DD/MM/YYYY)
7. **Encoding Issues**: If you see garbled text, ask Claude to try different encodings (UTF-8, latin-1, etc.)

## Advanced Operations

### Complex Transformations
- Unpivoting (melt) wide data to long format
- Creating calculated columns with business logic
- Grouping and aggregating with custom functions
- Handling multi-index data
- Time series resampling and rolling windows

### Data Quality Checks
- Outlier detection and reporting
- Referential integrity validation
- Format consistency checks
- Statistical anomaly detection

## Troubleshooting

**Issue:** File encoding errors or garbled characters
**Solution:** Ask Claude to detect encoding or try: "Read this with UTF-8-SIG encoding" or "Try latin-1 encoding"

**Issue:** Memory errors on large files
**Solution:** "Process this file in 10,000 row chunks" or "Sample 10% of rows first to test"

**Issue:** Wrong data types (dates as strings, numbers as text)
**Solution:** Be explicit: "Convert created_at column to datetime" or "Cast price to float"

**Issue:** Merge produces unexpected results
**Solution:** Ask Claude to show sample rows before/after merge and explain the join type used

**Issue:** Excel export loses formatting
**Solution:** "Export with formatted numbers, bold headers, and auto-column-width"

## Learn More

- [Pandas Documentation](https://pandas.pydata.org/docs/) - Comprehensive data manipulation guide
- [Excel to Pandas Mapping](https://pandas.pydata.org/docs/getting_started/comparison/comparison_with_spreadsheets.html) - Translate Excel operations
- [Data Cleaning Best Practices](https://github.com/Quartz/bad-data-guide) - Common data issues and solutions
- [Claude Code Interpreter Guide](https://www.anthropic.com/news/code-interpreter) - How Claude processes data


## Key Features

- Import/export with explicit schema control
- Deduplicate and null-safe transformations
- Join/merge/pivot with predictable results
- Encoding-aware IO with UTF-8/UTF-8-SIG handling
- Parquet round-trips for performance

## Use Cases

- Clean messy CRM exports
- Join sales and marketing datasets
- Generate analyst-ready summary tables

## Examples

### Example 1: Load, dedupe, and export

```python
import pandas as pd

customers = pd.read_csv('customers.csv', dtype=str)
orders = pd.read_excel('orders.xlsx')

# Normalize and dedupe
customers['email'] = customers['email'].str.strip().str.lower()
customers = customers.drop_duplicates(subset=['email'])

# Join and summarize
df = orders.merge(customers, on='customer_id', how='left')
sales_by_region = df.groupby('region', dropna=False)['total'].sum().reset_index()

sales_by_region.to_excel('sales_by_region.xlsx', index=False)
```

### Example 2: Explicit types and safe parsing

```python
import pandas as pd

dtypes = {
  'id': 'Int64',
  'price': 'float64',
  'created_at': 'string'
}
df = pd.read_csv('input.csv', dtype=dtypes, encoding='utf-8-sig')

# Coerce dates after load
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce', utc=True)

df.to_parquet('output.parquet')
```

## Troubleshooting

### Weird characters or BOM appearing in first column name

Use encoding='utf-8-sig' when reading CSV to strip byte order mark, or manually rename columns after load with df.columns.

### MemoryError when loading large CSV or Excel files

Use chunksize parameter in read_csv to process incrementally, or convert to Parquet format first for more efficient handling.

### Excel file opens but all values are NaN or None

Install openpyxl engine with pip install openpyxl, then use pd.read_excel('file.xlsx', engine='openpyxl').

### Date columns imported as strings instead of datetime objects

Use parse_dates parameter: pd.read_csv('file.csv', parse_dates=['date_column']) or convert post-load with pd.to_datetime().

### DtypeWarning about mixed types in columns when reading CSV

Specify dtype explicitly with dtype={'column': str} or use dtype=str for all, then convert types after inspection.

## Learn More

For additional documentation and resources, visit:

https://pandas.pydata.org/
