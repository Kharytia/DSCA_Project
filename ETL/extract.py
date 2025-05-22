import pandas as pd

def load_data(filepath: str) -> pd.DataFrame:
    """Load retail dataset from CSV file."""
    return pd.read_csv(filepath, encoding='ISO-8859-1')