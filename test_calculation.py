import json
import pandas as pd

from tools.portfolio_analyzer import (
    calculate_portfolio_analysis
)


df = pd.read_csv(
    "data/sample_portfolio.csv"
)

portfolio_json = json.dumps(
    df.to_dict(orient="records")
)

result = calculate_portfolio_analysis(
    portfolio_json
)

print(
    json.dumps(
        result,
        indent=2
    )
)