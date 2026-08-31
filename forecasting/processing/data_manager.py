import pandas as pd
from config.config import settings

def load_merge_data():
    crude_oil_path = settings["data"]["crude_oil_prices"]
    refinery_path = settings["data"]["us_refinery_and_trade_weekly"]
    use_weekly = settings["merge"]["use_weekly"]
    direction = settings["merge"]["direction"]

    crude_oil = pd.read_csv(crude_oil_path)
    refinery_trade = pd.read_csv(refinery_path)

    crude_oil["date"] = pd.to_datetime(crude_oil["date"])
    refinery_trade["date"] = pd.to_datetime(refinery_trade["date"])

    crude_oil = crude_oil.sort_values("date")
    refinery_trade = refinery_trade.sort_values("date")

    if use_weekly:
        crude_oil = crude_oil.set_index("date").resample("W").mean(numeric_only=True).reset_index()

    master = pd.merge_asof(
        crude_oil,
        refinery_trade,
        on="date",
        direction=direction
    )

    return master