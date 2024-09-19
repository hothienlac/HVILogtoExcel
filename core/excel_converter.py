from pandas import DataFrame


def save_as_excel(data: DataFrame, file_path: str) -> None:
    """Saves a DataFrame to an Excel file."""
    if data is not None:
        data.to_excel(file_path, index=False, engine="openpyxl")
    else:
        raise ValueError("No data to save.")
