import pandas as pd

def calculate_customer_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute metrics per customer for CLV estimation."""
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    
    customer_df = df.groupby('CustomerID').agg({
        'InvoiceDate': ['min', 'max', 'nunique'],
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    })

    customer_df.columns = ['FirstPurchase', 'LastPurchase', 'NumActiveDays', 'NumPurchases', 'TotalRevenue']
    customer_df['AvgOrderValue'] = customer_df['TotalRevenue'] / customer_df['NumPurchases']
    customer_df['CustomerAge'] = (customer_df['LastPurchase'] - customer_df['FirstPurchase']).dt.days + 1
    customer_df['PurchaseFrequency'] = customer_df['NumPurchases'] / customer_df['CustomerAge']
    
    return customer_df

def estimate_clv(customer_df: pd.DataFrame, lifespan_days=180) -> pd.DataFrame:
    """Estimate CLV based on purchase frequency and average order value."""
    customer_df['CLV'] = customer_df['AvgOrderValue'] * customer_df['PurchaseFrequency'] * lifespan_days
    return customer_df

def simulate_churn_loss(customer_df: pd.DataFrame, churned_customers: pd.Series) -> float:
    """Estimate potential revenue loss from churned customers."""
    churn_loss = customer_df.loc[customer_df.index.isin(churned_customers), 'CLV'].sum()
    return churn_loss
