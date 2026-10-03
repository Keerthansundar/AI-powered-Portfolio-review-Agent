from pydantic import BaseModel
from typing import List


class PortfolioHolding(BaseModel):
    ticker: str
    asset_name: str
    asset_class: str
    sector: str
    allocation_pct: float
    expense_ratio: float


class ClientProfile(BaseModel):
    name: str
    age: int
    risk_tolerance: str
    investment_goal: str
    investment_horizon_years: int
    liquidity_needs: str


class PortfolioAnalysis(BaseModel):
    total_allocation: float
    asset_class_allocation: dict
    sector_allocation: dict
    top_holdings: List[dict]
    concentration_risks: List[str]
    weighted_expense_ratio: float


class RiskAnalysis(BaseModel):
    client_risk_tolerance: str
    portfolio_risk_level: str
    risk_alignment: str
    observations: List[str]