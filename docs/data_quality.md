# Business Memory — Data Quality Report

## 1. Overview

Data quality is an important part of the Business Memory analytics pipeline.

The project includes a data quality reporting script that examines the customer dataset before analysis. It identifies missing values, duplicate records, invalid values, inconsistent formatting, and date parsing problems.

**Script:** `analytics/data_quality_report.py`

**Input Dataset:** `data/raw/customers_dirty.csv`

**Technology:** Python, Pandas

---

## 2. Data Quality Dimensions

The report evaluates the following dimensions:

| Dimension | Validation |
|---|---|
| Dataset Structure | Checks the number of rows and columns |
| Completeness | Identifies missing values |
| Uniqueness | Counts duplicate rows |
| Validity | Identifies credit limits less than or equal to zero |
| Date Validity | Detects dates that cannot be parsed |
| Consistency | Identifies extra whitespace in customer names |
| Standardization | Detects names not following title case |

---

## 3. Validation Methodology

### 3.1 Dataset Structure

The script uses the dataset shape to report the total number of rows and columns.

### 3.2 Missing Values

Pandas `isnull()` is used to identify missing values in each column.

Only columns containing missing values are displayed.

### 3.3 Duplicate Records

The `duplicated()` function identifies repeated rows and reports their count.

### 3.4 Invalid Credit Limits

Records with a credit limit less than or equal to zero are flagged.

### 3.5 Invalid Dates

The `created_at` column is converted using `pd.to_datetime()` with `errors="coerce"`.

Values that cannot be parsed become `NaT` and are counted as invalid dates.

### 3.6 Whitespace Issues

Customer names are compared with their stripped versions to identify leading or trailing whitespace.

### 3.7 Name Format Issues

Customer names are compared with their title-case versions to identify formatting inconsistencies.

---

## 4. Data Cleaning

The project also includes a customer cleaning script:

`analytics/clean_customers.py`

The cleaning workflow produces a cleaned customer dataset:

`data/processed/customers_clean.csv`

The quality report and cleaning script serve different purposes:

- The quality report identifies and counts potential issues.
- The cleaning script prepares a cleaned dataset for downstream use.

---
### 4.1 Cleaning Rules

| Field | Cleaning Rule |
|---|---|
| Customer Name | Remove surrounding whitespace and convert to title case |
| City | Standardize formatting; replace missing values with `Unknown` |
| Customer Type | Standardize formatting; replace missing values with `Unknown` |
| Credit Limit | Convert values less than or equal to zero into missing values |
| Created At | Convert to datetime; unparseable values become `NaT` |
| Duplicate Rows | Remove exact duplicate records |

The cleaning script prints validation results for the processed dataset and exports it to the designated output path.

## 5. Running the Report

From the project root directory, execute:

```powershell
python analytics/data_quality_report.py
```

The report prints the validation results in the terminal.

---

## 6. Business Value

Data quality checks help reduce the risk of inaccurate analytics caused by incomplete, duplicated, invalid, or inconsistently formatted customer data.

This supports more reliable customer analysis, segmentation, and business reporting.

---

## 7. Future Improvements

- Add automated validation tests.
- Validate customer identifiers and referential integrity.
- Generate a machine-readable quality report.
- Track data quality metrics across dataset versions.
- Add explicit validation rules for sales and product datasets.
