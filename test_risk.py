import json

from tools.portfolio_analyzer import (
    calculate_portfolio_analysis
)

from tools.risk_analyzer import (
    calculate_risk_analysis
)


client_profile = {
    "name": "Alex Johnson",
    "age": 42,
    "risk_tolerance": "Moderate",
    "investment_goal": "Retirement",
    "investment_horizon_years": 15,
    "liquidity_needs": "Low"
}


portfolio = [
    {
        "ticker": "AAPL",
        "asset_name": "Apple Inc",
        "asset_class": "Equity",
        "sector": "Technology",
        "allocation_pct": 25,
        "expense_ratio_pct": 0
    },
    {
        "ticker": "MSFT",
        "asset_name": "Microsoft Corp",
        "asset_class": "Equity",
        "sector": "Technology",
        "allocation_pct": 20,
        "expense_ratio_pct": 0
    },
    {
        "ticker": "NVDA",
        "asset_name": "NVIDIA Corp",
        "asset_class": "Equity",
        "sector": "Technology",
        "allocation_pct": 15,
        "expense_ratio_pct": 0
    },
    {
        "ticker": "VOO",
        "asset_name": "Vanguard S&P 500 ETF",
        "asset_class": "Equity",
        "sector": "Diversified",
        "allocation_pct": 20,
        "expense_ratio_pct": 0.03
    },
    {
        "ticker": "BND",
        "asset_name": "Vanguard Total Bond Market ETF",
        "asset_class": "Fixed Income",
        "sector": "Bonds",
        "allocation_pct": 20,
        "expense_ratio_pct": 0.03
    }
]


portfolio_json = json.dumps(portfolio)
client_json = json.dumps(client_profile)


portfolio_analysis = calculate_portfolio_analysis(
    portfolio_json
)


risk_analysis = calculate_risk_analysis(
    json.dumps(portfolio_analysis),
    client_json
)


print(
    json.dumps(
        risk_analysis,
        indent=2
    )
)