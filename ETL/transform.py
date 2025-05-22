import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset by removing rows with missing customer or invoice info."""
    df = df.dropna(subset=["Invoice", "Customer ID"])
    return df

def add_return_flag(df: pd.DataFrame) -> pd.DataFrame:
    """Addcolumn indicating if a row represents a return."""
    df["is_return"] = df["Quantity"] < 0
    return df

def split_sales_returns(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split the dataset into sales and returns based on quantity."""
    sales = df[df["Quantity"] > 0].copy()
    returns = df[df["Quantity"] < 0].copy()
    return sales, returns
