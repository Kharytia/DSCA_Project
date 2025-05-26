import pandas as pd

def sales_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by month."""
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Month'] = df['InvoiceDate'].dt.to_period('M')
    monthly_sales = df[df['Quantity'] > 0].groupby('Month')['TotalPrice'].sum().reset_index()
    return monthly_sales

def top_selling_products(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """Get top selling products by quantity."""
    product_sales = df[df['Quantity'] > 0].groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(top_n).reset_index()
    return product_sales

def product_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate returns by product."""
    returns = df[df['Quantity'] < 0].groupby('Description')['Quantity'].sum().sort_values().reset_index()
    return returns

def country_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue by country."""
    country_sales = df[df['Quantity'] > 0].groupby('Country')['TotalPrice'].sum().sort_values(ascending=False).reset_index()
    return country_sales

def country_orders(df: pd.DataFrame) -> pd.DataFrame
    """Aggregate orders by country"""
    country_orders = df[df['Quantity']>0].groupby('Country')['Quantity'].sum().sort_values(ascending=False).reset_index()
    return country_orders
