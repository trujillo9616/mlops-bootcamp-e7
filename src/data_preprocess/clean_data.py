import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw data.
    Args:
        df {pd.DataFrame}: raw data
    Returns:
        pd.DataFrame: cleaned data
    """

    # Drop duplicates and NA values
    df = df.drop_duplicates()
    df = df.dropna(subset=["CustomerID"])

    # Remove negative quantites and unit prices
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

    # Make StockCode and CustomerID strings
    df["StockCode"] = df["StockCode"].astype(str)
    df["CustomerID"] = df["CustomerID"].astype(str)

    # Format CustomerID to remove decimal points
    df["CustomerID"] = df["CustomerID"].str.split(".").str[0]

    return df
