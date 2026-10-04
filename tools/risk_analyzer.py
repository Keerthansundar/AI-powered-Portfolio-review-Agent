import json

from agents import function_tool


def calculate_risk_analysis(
    portfolio_analysis_json: str,
    client_profile_json: str,
) -> dict:

    portfolio = json.loads(
        portfolio_analysis_json
    )

    client = json.loads(
        client_profile_json
    )

    if "error" in portfolio:
        raise ValueError(
            portfolio["error"]
        )

    risk_tolerance = (
        client["risk_tolerance"]
        .lower()
        .strip()
    )

    equity_allocation = (
        portfolio
        .get("asset_class_allocation", {})
        .get("Equity", 0)
    )

    investment_horizon = (
        client["investment_horizon_years"]
    )

    observations = []

    # Portfolio risk level

    if equity_allocation >= 80:

        portfolio_risk_level = "High"

    elif equity_allocation >= 60:

        portfolio_risk_level = "Moderate-High"

    elif equity_allocation >= 40:

        portfolio_risk_level = "Moderate"

    else:

        portfolio_risk_level = "Conservative"

    # Risk alignment

    if risk_tolerance == "conservative":

        if equity_allocation > 60:

            risk_alignment = "Potential mismatch"

            observations.append(
                "Equity allocation may be high "
                "for a conservative risk profile."
            )

        else:

            risk_alignment = "Generally aligned"

    elif risk_tolerance == "moderate":

        if equity_allocation > 80:

            risk_alignment = "Potential mismatch"

            observations.append(
                "Equity allocation may be aggressive "
                "for a moderate-risk investor."
            )

        else:

            risk_alignment = "Generally aligned"

    elif risk_tolerance == "aggressive":

        risk_alignment = "Generally aligned"

    else:

        risk_alignment = "Unable to determine"

        observations.append(
            "Risk tolerance was not recognized."
        )

    # Investment horizon

    if (
        investment_horizon < 5
        and equity_allocation > 70
    ):

        observations.append(
            "High equity exposure should be reviewed "
            "given the relatively short investment horizon."
        )

    if not observations:

        observations.append(
            "No obvious risk-profile mismatch was "
            "detected from the supplied inputs."
        )

    return {
        "client_risk_tolerance": client["risk_tolerance"],
        "portfolio_risk_level": portfolio_risk_level,
        "risk_alignment": risk_alignment,
        "observations": observations,
    }


@function_tool
def analyze_risk_profile(
    equity_allocation: float,
    risk_tolerance: str,
    investment_horizon_years: int,
) -> str:
    """
    Evaluate portfolio risk against the client's
    risk tolerance and investment horizon.

    Inputs:
    - equity_allocation: Equity allocation percentage.
    - risk_tolerance: Conservative, Moderate, or Aggressive.
    - investment_horizon_years: Investment horizon in years.

    Returns deterministic risk analysis.
    """

    try:

        risk_tolerance_normalized = (
            risk_tolerance.lower().strip()
        )

        observations = []

        # -----------------------------------------
        # Portfolio risk level
        # -----------------------------------------

        if equity_allocation >= 80:
            portfolio_risk_level = "High"

        elif equity_allocation >= 60:
            portfolio_risk_level = "Moderate-High"

        elif equity_allocation >= 40:
            portfolio_risk_level = "Moderate"

        else:
            portfolio_risk_level = "Conservative"

        # -----------------------------------------
        # Risk alignment
        # -----------------------------------------

        if risk_tolerance_normalized == "conservative":

            if equity_allocation > 60:
                risk_alignment = "Potential mismatch"

                observations.append(
                    "Equity allocation may be high "
                    "for a conservative risk profile."
                )
            else:
                risk_alignment = "Generally aligned"

        elif risk_tolerance_normalized == "moderate":

            if equity_allocation > 80:
                risk_alignment = "Potential mismatch"

                observations.append(
                    "Equity allocation may be aggressive "
                    "for a moderate-risk investor."
                )
            else:
                risk_alignment = "Generally aligned"

        elif risk_tolerance_normalized == "aggressive":

            risk_alignment = "Generally aligned"

        else:

            risk_alignment = "Unable to determine"

            observations.append(
                "Risk tolerance was not recognized."
            )

        # -----------------------------------------
        # Investment horizon
        # -----------------------------------------

        if (
            investment_horizon_years < 5
            and equity_allocation > 70
        ):

            observations.append(
                "High equity exposure should be reviewed "
                "given the relatively short investment horizon."
            )

        if not observations:

            observations.append(
                "No obvious risk-profile mismatch was "
                "detected from the supplied inputs."
            )

        result = {
            "client_risk_tolerance": risk_tolerance,
            "investment_horizon_years": investment_horizon_years,
            "equity_allocation_pct": equity_allocation,
            "portfolio_risk_level": portfolio_risk_level,
            "risk_alignment": risk_alignment,
            "observations": observations,
        }

        return json.dumps(
            result,
            separators=(",", ":")
        )

    except Exception as e:

        return json.dumps(
            {"error": str(e)},
            separators=(",", ":")
        )