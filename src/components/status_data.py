import pandas as pd

status = pd.read_parquet(
    "data/processed/current_status.parquet"
)

def get_status_data():
    return status