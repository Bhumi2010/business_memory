from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.services import (
    get_overview,
    get_revenue_analysis,
    get_customer_analysis,
    get_retention_analysis,
    get_customer_segments,
    get_category_analysis,
    get_product_analysis,
    get_root_cause_analysis
)

app = FastAPI(
    title="Business Memory API",
    description="Business analytics API for the Business Memory project",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Business Memory API is running",
        "status": "success"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Business Memory API"
    }


@app.get("/api/overview")
def overview():
    return get_overview()


@app.get("/api/revenue")
def revenue():
    return get_revenue_analysis()


@app.get("/api/customers")
def customers():
    return get_customer_analysis()


@app.get("/api/retention")
def retention():
    return get_retention_analysis()


@app.get("/api/segments")
def segments():
    return get_customer_segments()


@app.get("/api/categories")
def categories():
    return get_category_analysis()


@app.get("/api/products")
def products():
    return get_product_analysis()

@app.get("/api/root-cause")
def root_cause():
    return get_root_cause_analysis()