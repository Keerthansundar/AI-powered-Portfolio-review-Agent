import asyncio
import json

import pandas as pd
import streamlit as st

import time

from agents import Runner

from agent_core.portfolio_agent import portfolio_agent


st.set_page_config(
    page_title="Mili Portfolio Review",
    page_icon="📊",
    layout="wide",
)


st.title("📊 Mili Portfolio Review Agent")

st.markdown(
    """
    Upload a client's portfolio and provide their profile.
    The AI agent will analyze the portfolio, identify risks,
    and generate potential actions for advisor review.
    """
)


# ---------------------------------------------------------
# Sidebar - Client Profile
# ---------------------------------------------------------

st.sidebar.header("Client Profile")

client_name = st.sidebar.text_input(
    "Client name",
    value="Alex Johnson",
)

age = st.sidebar.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=42,
)

risk_tolerance = st.sidebar.selectbox(
    "Risk tolerance",
    [
        "Conservative",
        "Moderate",
        "Aggressive",
    ],
    index=1,
)

investment_goal = st.sidebar.text_input(
    "Investment goal",
    value="Retirement",
)

investment_horizon = st.sidebar.number_input(
    "Investment horizon (years)",
    min_value=1,
    max_value=100,
    value=15,
)

liquidity_needs = st.sidebar.selectbox(
    "Liquidity needs",
    [
        "Low",
        "Medium",
        "High",
    ],
)


# ---------------------------------------------------------
# Portfolio Upload
# ---------------------------------------------------------

st.header("1. Upload Portfolio")

uploaded_file = st.file_uploader(
    "Upload portfolio CSV",
    type=["csv"],
)


if uploaded_file is not None:

    try:
        portfolio_df = pd.read_csv(uploaded_file)

        st.subheader("Portfolio Preview")

        st.dataframe(
            portfolio_df,
            use_container_width=True,
        )

    except Exception as e:

        st.error(
            f"Could not read the CSV file: {e}"
        )

        st.stop()

else:

    st.info(
        "No file uploaded. Using the sample portfolio."
    )

    portfolio_df = pd.read_csv(
        "data/sample_portfolio.csv"
    )

    st.subheader("Sample Portfolio")

    st.dataframe(
        portfolio_df,
        use_container_width=True,
    )


# ---------------------------------------------------------
# Client JSON
# ---------------------------------------------------------

client_profile = {
    "name": client_name,
    "age": age,
    "risk_tolerance": risk_tolerance,
    "investment_goal": investment_goal,
    "investment_horizon_years": investment_horizon,
    "liquidity_needs": liquidity_needs,
}


portfolio_records = portfolio_df.to_dict(
    orient="records"
)

portfolio_json = json.dumps(
    portfolio_records
)

client_json = json.dumps(
    client_profile
)


# ---------------------------------------------------------
# Run Agent
# ---------------------------------------------------------

st.header("2. Generate Portfolio Review")


if st.button(
    "🔍 Analyze Portfolio",
    type="primary",
    use_container_width=True,
):

    agent_input = f"""
CLIENT PROFILE:

{client_json}


PORTFOLIO HOLDINGS:

{portfolio_json}


Please analyze this portfolio using your tools.

Return an advisor-friendly portfolio review with:

1. Executive summary
2. Asset allocation
3. Key concentration risks
4. Expense observations
5. Risk alignment
6. Two or three potential actions for advisor review

Do not execute or recommend automatic trades.
"""

    with st.spinner(
        "Portfolio agent is analyzing the client..."
    ):

        try:

            start_time = time.time()

            result = asyncio.run(
                Runner.run(
                    portfolio_agent,
                    agent_input,
                )
            )

            elapsed = time.time() - start_time

            final_output = result.final_output

            st.info(
                f"Agent execution time: {elapsed:.2f} seconds"
            )

        except Exception as e:

            st.error(
                f"Agent execution failed: {e}"
            )

            st.stop()


    # -----------------------------------------------------
    # Display result
    # -----------------------------------------------------

    st.success(
        "Portfolio review generated successfully."
    )

    st.subheader("📋 Advisor Review")

    st.markdown(final_output)


    # -----------------------------------------------------
    # Raw input / structured data
    # -----------------------------------------------------

    with st.expander(
        "🔎 View underlying structured data"
    ):

        st.subheader("Client Profile")

        st.json(client_profile)

        st.subheader("Portfolio Data")

        st.json(portfolio_records)


st.divider()

st.caption(
    "Prototype for the Mili FDE take-home assignment. "
    "Recommendations are for advisor review and are not "
    "automated financial advice."
)