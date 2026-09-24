from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    service: str


class OverviewResponse(BaseModel):
    total_revenue: float
    total_orders: int
    total_units_sold: int
    average_order_value: float