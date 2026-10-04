# Mili Portfolio Review Agent — Project Context

This project is a lightweight portfolio-review assistant built with Python, Streamlit, and the OpenAI Agents SDK. Its purpose is to let a user upload a portfolio CSV, describe the client profile, and receive an advisor-facing summary that highlights:

- asset allocation
- concentration risks
- expense observations
- risk alignment
- recommended next steps for advisor review

The system is intentionally deterministic in its portfolio/risk calculations and uses an LLM only to interpret those results and produce the final narrative.

## 1. High-level purpose

The app acts like a financial review assistant for a wealth advisor. It does not place trades or generate automated investment actions. Instead, it:

1. reads a portfolio from a CSV upload or sample file
2. combines that with a client profile
3. runs deterministic analysis tools
4. passes those structured results to an agent
5. asks the agent to produce a concise advisor-facing review

This follows a safe design: the numeric analysis is computed by code, and the LLM is restricted to summarizing and framing the output without inventing facts.

## 2. Tech stack

- Python 3
- Streamlit for the UI
- Pandas for CSV/portfolio processing
- OpenAI Agents SDK (`agents` package)
- Ollama-compatible OpenAI endpoint for the LLM backend
- Pydantic models for schema definitions

## 3. Application entry point

The main app is [app.py](./app.py).

What it does:

- sets the page title and layout
- builds the sidebar for client profile inputs
- allows CSV upload of portfolio holdings
- falls back to a sample portfolio if no file is uploaded
- converts the portfolio/client inputs to JSON
- calls the agent workflow
- renders the final advisor review in the Streamlit UI

### Main flow in app.py

1. load client fields:
   - name
   - age
   - risk tolerance
   - investment goal
   - investment horizon
   - liquidity needs
2. upload CSV or use [data/sample_portfolio.csv](./data/sample_portfolio.csv)
3. convert the uploaded data to a list of dictionary records
4. call `Runner.run(portfolio_agent, agent_input)`
5. print the final output in the Streamlit page

The app also contains an "underlying structured data" expander so the user can inspect the exact client and portfolio payload being sent to the agent.

## 4. Agent architecture

The agent is declared in [agent_core/portfolio_agent.py](./agent_core/portfolio_agent.py).

It uses:

- `model` from [services/llm.py](./services/llm.py)
- `analyze_portfolio` tool from [tools/portfolio_analyzer.py](./tools/portfolio_analyzer.py)
- `analyze_risk_profile` tool from [tools/risk_analyzer.py](./tools/risk_analyzer.py)

The agent instructions explicitly say:

- call `analyze_portfolio` first
- then call `analyze_risk_profile`
- treat numerical values from tools as authoritative
- never recalculate numbers manually
- never invent client characteristics
- only use the provided client profile, portfolio holdings, and tool outputs
- do not mention internal tool calls in the final response
- produce a concise advisor-facing report under 500 words

This makes the agent a summarization and interpretation layer on top of deterministic calculations.

## 5. LLM configuration

[services/llm.py](./services/llm.py) configures the model connection.

Key environment-driven settings:

- `OLLAMA_BASE_URL` — default: `http://localhost:11434/v1`
- `OLLAMA_API_KEY` — default: `ollama`
- `OLLAMA_MODEL` — default: `qwen3:4b`

These values are loaded from [.env](./.env), which keeps the app ready to use a local Ollama-compatible model.

The system disables tracing with `set_tracing_disabled(True)` and creates an `AsyncOpenAI` client pointed at the local LLM endpoint.

## 6. Tool layer: deterministic analysis

The project intentionally separates calculations from the LLM. The tool modules return JSON strings and are exposed to the agent via `@function_tool`.

### 6.1 Portfolio analysis tool

File: [tools/portfolio_analyzer.py](./tools/portfolio_analyzer.py)

This tool:

- loads the portfolio JSON
- validates that holdings are present
- checks required columns:
  - ticker
  - asset_name
  - asset_class
  - sector
  - allocation_pct
  - expense_ratio_pct
- ensures total allocation sums to 100%
- computes:
  - asset class allocations
  - sector allocations
  - top holdings by allocation
  - concentration risks (single holding and sector-level)
  - weighted expense ratio

It raises a `ValueError` if data is invalid or if allocations do not sum correctly.

### 6.2 Risk analysis tool

File: [tools/risk_analyzer.py](./tools/risk_analyzer.py)

This tool takes:

- portfolio analysis JSON
- client profile JSON

Then it calculates:

- portfolio risk level from equity allocation
- risk alignment compared to client risk tolerance
- observations such as mismatch or short-horizon concerns

Examples of logic:

- high equity allocation => `High` risk level
- moderate equity allocation => `Moderate`
- low equity allocation => `Conservative`
- if a conservative client holds >60% equity, it flags a mismatch
- if a moderate client holds >80% equity, it flags a mismatch
- if the investment horizon is short and equity is high, it adds a cautionary observation

## 7. Data models

The schema definitions live in [models/schemas.py](./models/schemas.py).

They define:

- `PortfolioHolding`
- `ClientProfile`
- `PortfolioAnalysis`
- `RiskAnalysis`

These are Pydantic models used to structure portfolio and risk information. The project currently uses them more as schema definitions than as the main runtime validation layer.

## 8. Sample data and validation

There is sample portfolio data at [data/sample_portfolio.csv](./data/sample_portfolio.csv).

The sample file contains a simple portfolio:

- AAPL — 25%
- MSFT — 20%
- NVDA — 15%
- VOO — 20%
- BND — 20%

This adds up to 100% and is used by the app when the user has not uploaded a CSV.

## 9. Tests and validation scripts

There are quick verification scripts at the repository root:

- [test_calculation.py](./test_calculation.py)
- [test_risk.py](./test_risk.py)

These scripts validate the calculation logic by constructing a client profile and a portfolio, then printing a JSON result.

The project also includes a test directory: [tests](./tests) — currently populated with test modules for portfolio and risk checks.

## 10. Project structure

Top-level layout:

- [app.py](./app.py) — Streamlit app entry point
- [agent_core/portfolio_agent.py](./agent_core/portfolio_agent.py) — agent definition and instructions
- [services/llm.py](./services/llm.py) — LLM/client configuration
- [tools/portfolio_analyzer.py](./tools/portfolio_analyzer.py) — deterministic portfolio math
- [tools/risk_analyzer.py](./tools/risk_analyzer.py) — risk mismatch logic
- [models/schemas.py](./models/schemas.py) — typed schema definitions
- [data/sample_portfolio.csv](./data/sample_portfolio.csv) — fallback sample portfolio
- [.env](./.env) — local LLM endpoint configuration
- [requirements.txt](./requirements.txt) — Python dependencies

## 11. Example execution flow

The app flow can be summarized like this:

```python
portfolio_df = pd.read_csv(uploaded_file)
client_profile = {...}
portfolio_json = json.dumps(portfolio_df.to_dict(orient="records"))
agent_input = f"""
CLIENT PROFILE:
{client_json}
PORTFOLIO HOLDINGS:
{portfolio_json}
... analyze portfolio ...
"""
result = asyncio.run(Runner.run(portfolio_agent, agent_input))
final_output = result.final_output
``` 

The agent then uses its tools to generate a structured analysis, and the final narrative is displayed to the advisor.

## 12. What the project is not

This project is not a full trading system and does not:

- auto-trade securities
- execute buy/sell operations
- guarantee returns
- directly model every realistic portfolio-risk factor
- replace a professional financial advisor

Its goal is to provide a domain-specific review of a portfolio using constrained deterministic logic and generative summarization.

## 13. How to run

From the project root:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Make sure Ollama is running locally, or point `OLLAMA_BASE_URL` in [.env](./.env) to a valid OpenAI-compatible endpoint.

## 14. Summary

In plain English, this project is a portfolio-review assistant that helps an advisor assess whether a client's portfolio matches their profile and risk tolerance, without directly making trade decisions. It combines:

- a Streamlit frontend
- deterministic analysis functions for portfolio math and risk checks
- an OpenAI-style agent to synthesize the results into a readable review

That makes it a good example of a bounded, advisor-friendly AI workflow where the LLM is used for explanation rather than for core numeric decision-making.
