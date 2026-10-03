import json
import pandas as pd

from agents import function_tool


def calculate_portfolio_analysis(portfolio_json: str) -> dict:
    """
    Deterministic portfolio calculations.
    """

    holdings = json.loads(portfolio_json)

    if not isinstance(holdings, list) or len(holdings) == 0:
        raise ValueError(
            "Portfolio must contain at least one holding."
        )

    df = pd.DataFrame(holdings)

    required_columns = [
        "ticker",
        "asset_name",
        "asset_class",
        "sector",
        "allocation_pct",
        "expense_ratio_pct",
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    total_allocation = float(
        df["allocation_pct"].sum()
    )

    if abs(total_allocation - 100) > 0.01:
        raise ValueError(
            f"Portfolio allocation must equal 100%. "
            f"Current allocation: {total_allocation}%"
        )

    asset_class_allocation = (
        df.groupby("asset_class")["allocation_pct"]
        .sum()
        .round(2)
        .to_dict()
    )

    sector_allocation = (
        df.groupby("sector")["allocation_pct"]
        .sum()
        .round(2)
        .sort_values(ascending=False)
        .to_dict()
    )

    top_holdings_df = (
        df.sort_values(
            "allocation_pct",
            ascending=False
        )
        .head(5)
    )

    top_holdings = (
        top_holdings_df[
            [
                "ticker",
                "asset_name",
                "allocation_pct",
            ]
        ]
        .to_dict(orient="records")
    )

    concentration_risks = []

    # Individual holding concentration
    for _, row in df.iterrows():

        if row["allocation_pct"] >= 20:

            concentration_risks.append(
                f"{row['ticker']} represents "
                f"{row['allocation_pct']:.1f}% "
                f"of the portfolio."
            )

    # Sector concentration
    for sector, allocation in sector_allocation.items():

        if allocation >= 40:

            concentration_risks.append(
                f"{sector} sector exposure is "
                f"{allocation:.1f}%."
            )

    if not concentration_risks:

        concentration_risks.append(
            "No major concentration threshold "
            "was detected."
        )

    # Expense ratio is stored as percentage points.
    #
    # Example:
    # 0.03 means 0.03%
    #
    weighted_expense_ratio_pct = float(
        (
            df["allocation_pct"]
            * df["expense_ratio_pct"]
        ).sum()
        / total_allocation
    )

    return {
        "total_allocation_pct": round(
            total_allocation,
            2
        ),
        "asset_class_allocation": (
            asset_class_allocation
        ),
        "sector_allocation": (
            sector_allocation
        ),
        "top_holdings": top_holdings,
        "concentration_risks": (
            concentration_risks
        ),
        "weighted_expense_ratio_pct": round(
            weighted_expense_ratio_pct,
            4
        ),
    }


@function_tool
def analyze_portfolio(
    portfolio_json: str
) -> str:
    """
    Analyze a client's portfolio using
    deterministic Python calculations.
    """

    try:

        result = calculate_portfolio_analysis(
            portfolio_json
        )

        return json.dumps(
            result,
            indent=2
        )

    except Exception as e:

        return json.dumps(
            {
                "error": str(e)
            },
            indent=2
        )