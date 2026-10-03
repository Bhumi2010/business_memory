# Business Memory — Business Intelligence & Analytics Platform

An end-to-end business analytics and decision-support platform that transforms raw retail transaction data into actionable business insights through data processing, customer analytics, product performance analysis, and an interactive dashboard.

Business Memory helps understand revenue movements, customer retention, churn, and product performance through a combination of Python analytics, FastAPI, and a web-based dashboard.

---

## Project Overview

Business Memory is designed to simulate a real-world business intelligence workflow:

**Raw Data → Data Quality → Data Processing → Analytics → REST APIs → Interactive Dashboard**

The platform analyzes business performance across July and August 2026, helping identify revenue changes, customer behavior, and category-level performance.

## Key Features

- **Synthetic Data Generation:** Generates business datasets for sales, customers, products, suppliers, warehouses, and sale items.
- **Data Quality Management:** Simulates data issues and performs data cleaning and quality checks.
- **Business Performance Metrics:** Calculates revenue, total orders, units sold, average order value, and customer counts.
- **Customer Analytics:** Analyzes active, inactive, new, and returning customers.
- **Retention & Churn Analysis:** Measures customer retention, churn rate, and associated revenue impact.
- **Customer Segmentation:** Classifies customers into business segments using revenue and purchase-frequency thresholds.
- **Product Performance:** Identifies top revenue decliners, growing products, and product-level revenue changes.
- **Category Analysis:** Compares category revenue across two months.
- **Root Cause Analysis:** Combines revenue, order, customer, category, and product metrics to explain business movement.
- **REST API:** Exposes analytics through a FastAPI backend.
- **Interactive Dashboard:** Presents business metrics and insights through a responsive web interface.

## Technology Stack

| Layer | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas |
| Backend | FastAPI |
| API Server | Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Data Storage / Input | CSV |
| Development Tools | VS Code / Antigravity, Git, GitHub |
| API Documentation | Swagger UI |

## Business Metrics

### Overall Dataset

| Metric | Value |
|---|---:|
| Total Revenue | ₹185,633,539.05 |
| Total Orders | 10,000 |
| Total Units Sold | 316,768 |
| Total Customers | 500 |
| Average Order Value | ₹18,563.35 |

### July–August 2026 Performance

| Metric | July | August |
|---|---:|---:|
| Revenue | ₹10,441,060.17 | ₹9,321,427.97 |
| Orders | 558 | 504 |
| Average Order Value | ₹18,711.58 | ₹18,494.90 |

**Revenue Change:** -10.72%

**Order Change:** -9.68%

### Customer Retention

| Metric | Result |
|---|---:|
| Retained Customers | 205 |
| Churned Customers | 127 |
| New / Returning Customers | 109 |
| Retention Rate | 61.75% |
| Churn Rate | 38.25% |

*Note: Overall metrics cover the complete dataset, while the performance and retention comparisons use July–August 2026.*

## Project Architecture

```text
             Business Data (CSV)
                    |
                    v
          Data Quality & Cleaning
                    |
                    v
          Pandas Analytics Layer
                    |
          +---------+----------+
          |         |          |
          v         v          v
       Revenue   Customer   Product &
       Analysis  Analytics  Category
          |         |       Analysis
          +---------+----------+
                    |
                    v
             FastAPI Backend
                    |
                    v
          Interactive Dashboard
             HTML / CSS / JS
                    |
                    v
           Business Insights
```

## Project Structure

```text
business-memory/
│
├── analytics/
│   ├── data_loader.py
│   ├── generate_data.py
│   ├── generate_sales.py
│   ├── generate_sale_items.py
│   ├── generate_products.py
│   ├── generate_suppliers.py
│   ├── generate_warehouses.py
│   ├── introduce_data_issues.py
│   ├── clean_customers.py
│   ├── data_quality_report.py
│   ├── metrics.py
│   ├── business_events.py
│   ├── root_cause_analysis.py
│   ├── category_analysis.py
│   ├── product_analysis.py
│   ├── customer_analysis.py
│   ├── retention_analysis.py
│   └── customer_segmentation.py
│
├── backend/
│   ├── main.py
│   ├── services.py
│   └── schemas.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
├── database/
├── docs/
├── notebooks/
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md
```

## API Endpoints

The FastAPI backend exposes the following endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | API health check |
| GET | `/api/overview` | Overall business metrics |
| GET | `/api/revenue` | Revenue performance |
| GET | `/api/customers` | Customer analysis |
| GET | `/api/retention` | Retention and churn |
| GET | `/api/segments` | Customer segmentation |
| GET | `/api/categories` | Category performance |
| GET | `/api/products` | Product performance |
| GET | `/api/root-cause` | Combined business insights |

Interactive API documentation is available at `/docs` when the backend is running.

## Getting Started

### Prerequisites

- Python 3.9+
- pip
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Bhumi2010/business_memory.git
cd business_memory
```

### 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate the Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the Backend

Run this command from the project root:

```powershell
python -m uvicorn backend.main:app
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Frontend

Open a second terminal in the project root and run:

```powershell
python -m http.server 5500 --directory frontend
```

Open the dashboard:

```text
http://127.0.0.1:5500
```

Keep both servers running while using the application.

## Business Insights

The July–August analysis highlights:

- Revenue declined by 10.72%.
- Order volume declined by 9.68%.
- Customer churn contributed a negative revenue impact of approximately ₹42.22 lakh.
- Household recorded the largest category-level revenue decline.
- Personal Care was the only category showing positive revenue growth.

These insights demonstrate how business analytics can support performance monitoring and decision-making.

## Future Enhancements

- Automated testing and API test coverage
- Expanded data quality validation
- Database integration and persistence
- Interactive date-range filters
- Advanced customer behavior analytics
- Deployment and cloud hosting
- Automated reporting and business alerts

---

## Author

**Bhumi Singh**

B.Tech Computer Science & Engineering

Interested in Data Analytics, Business Intelligence, Python, and data-driven decision-making.

[LinkedIn](https://www.linkedin.com/in/bhumi-singh-818b18334)

[GitHub](https://github.com/Bhumi2010)

---

*Business Memory — Turning business data into meaningful insights.*