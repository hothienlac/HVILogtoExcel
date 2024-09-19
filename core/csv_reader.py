import pandas as pd
from pandas import DataFrame


def read_csv(file_path: str) -> DataFrame:
    """Reads a CSV file and returns it as a DataFrame."""
    return pd.read_csv(file_path)
