# Business Memory

**Business Memory** is a data analytics and data quality pipeline for managing core enterprise datasets including Customers, Products, Suppliers, and Warehouses. It provides synthetic data generation, real-world data issue simulation, automated data quality auditing, and data cleaning pipelines.

---

## 📌 Project Status Overview

The project currently features a complete synthetic data generator and data quality pipeline for business data entities, along with exploratory analysis Jupyter notebooks.

### Key Capabilities
- **Synthetic Data Generation**: Scriptable generation for customers (500 records), products (1,000 records across 6 categories), suppliers (20 enterprise entities), and warehouses.
- **Data Quality Simulation**: Introduces realistic data issues (duplicates, invalid credit limits, malformed dates, whitespace/casing inconsistencies, missing fields) for testing cleaning pipelines.
- **Data Quality Reporting**: Automated reporting script to evaluate completeness, duplicate rates, and data standard compliance.
- **Data Cleaning Pipeline**: Automated standardization and hygiene process outputting clean datasets for downstream analytics.
- **Exploratory Data Analysis**: Interactive Jupyter notebooks analyzing customer demographics, credit limits, and data quality metrics.

---

## 📁 Repository Structure

```
business-memory/
├── analytics/                      # Python data processing & pipeline scripts
│   ├── generate_data.py            # Generates raw customer dataset
│   ├── introduce_data_issues.py    # Generates dirty customer dataset with simulated errors
│   ├── data_quality_report.py      # Generates data quality audit report
│   ├── clean_customers.py          # Data cleaning & standardization pipeline
│   ├── generate_products.py       # Generates synthetic products dataset
│   ├── generate_suppliers.py      # Generates synthetic suppliers dataset
│   └── generate_warehouses.py     # Generates synthetic warehouse dataset
├── data/
│   ├── raw/                        # Raw & dirty CSV datasets
│   │   ├── customers.csv
│   │   ├── customers_dirty.csv
│   │   ├── products.csv
│   │   ├── suppliers.csv
│   │   └── warehouses.csv
│   ├── processed/                  # Cleaned & standardized CSV datasets
│   │   └── customers_clean.csv
│   └── sample/                     # Sample datasets for quick testing
├── notebooks/                      # Jupyter notebooks for interactive analysis
│   ├── 01_customer_data_exploration.ipynb
│   └── 02_data_quality_analysis.ipynb
├── backend/                        # (Planned) Backend API service
├── database/                       # (Planned) Database schemas & migrations
├── frontend/                       # (Planned) Dashboard & Web UI
├── docs/                           # Project documentation
├── tests/                          # Automated unit & integration test suite
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

---

## 📊 Datasets & Schema Summary

| Entity | Raw File | Processed File | Primary Attributes |
| :--- | :--- | :--- | :--- |
| **Customers** | [`data/raw/customers.csv`](file:///c:/Users/hp/Downloads/projects/business-memory/data/raw/customers.csv) | [`data/processed/customers_clean.csv`](file:///c:/Users/hp/Downloads/projects/business-memory/data/processed/customers_clean.csv) | `customer_id`, `customer_name`, `city`, `state`, `customer_type`, `credit_limit`, `created_at` |
| **Products** | [`data/raw/products.csv`](file:///c:/Users/hp/Downloads/projects/business-memory/data/raw/products.csv) | N/A | `product_id`, `product_name`, `category`, `brand`, `supplier_id`, `cost_price`, `selling_price` |
| **Suppliers** | [`data/raw/suppliers.csv`](file:///c:/Users/hp/Downloads/projects/business-memory/data/raw/suppliers.csv) | N/A | `supplier_id`, `supplier_name`, `city`, `state`, `supplier_type` |
| **Warehouses** | [`data/raw/warehouses.csv`](file:///c:/Users/hp/Downloads/projects/business-memory/data/raw/warehouses.csv) | N/A | `warehouse_id`, `warehouse_name`, `city`, `state`, `capacity_units` |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- `pip` / virtual environment (`.venv`)

### Installation & Execution

1. **Activate Virtual Environment**:
   ```bash
   # Windows PowerShell
   .venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Data Generation Pipelines**:
   ```bash
   # Generate base datasets
   python analytics/generate_data.py
   python analytics/generate_suppliers.py
   python analytics/generate_products.py
   python analytics/generate_warehouses.py

   # Simulate data quality issues
   python analytics/introduce_data_issues.py

   # Run data quality audit report
   python analytics/data_quality_report.py

   # Run cleaning pipeline
   python analytics/clean_customers.py
   ```

---

## 📈 Roadmap

- [x] Synthetic customer, product, supplier, and warehouse generators
- [x] Data quality issue simulation & audit reporting
- [x] Automated customer data cleaning pipeline
- [x] Exploratory Jupyter analysis notebooks
- [ ] Product and supplier data cleaning & validation rules
- [ ] Database integration (SQLite / PostgreSQL) in `database/`
- [ ] RESTful API service in `backend/`
- [ ] Interactive Web Dashboard in `frontend/`
