import pandas as pd
import numpy as np

def calculate_customer_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Compute days since last purchase, number of purchases, and AOV."""
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # Total price per row
    df['TotalPrice'] = df['Quantity'] * df['Price']

    today = df['InvoiceDate'].max() + pd.Timedelta(days=1)

    customer_df = df[df['Quantity'] > 0].groupby('Customer ID').agg(
        last_purchase=('InvoiceDate', 'max'),
        num_purchases=('Invoice', 'nunique'),
        total_spent=('TotalPrice', 'sum')
    ).reset_index()

    customer_df['days_since_last_purchase'] = (today - customer_df['last_purchase']).dt.days
    customer_df['avg_order_value'] = customer_df['total_spent'] / customer_df['num_purchases']

    return customer_df

def classify_churn_status(customer_df: pd.DataFrame, churn_threshold_days: int = 180) -> pd.DataFrame:
    """Classify churn risk based on days since last purchase."""
    bins = [0, 90, churn_threshold_days, np.inf]
    labels = ['Active', 'At Risk', 'Lost']
    customer_df['churn_status'] = pd.cut(
        customer_df['days_since_last_purchase'],
        bins=bins,
        labels=labels,
        right=False
    )
    return customer_df

def get_churn_summary(customer_df: pd.DataFrame) -> pd.DataFrame:
    """Return churn status summary for plotting or reporting."""
    summary = customer_df['churn_status'].value_counts().reset_index()
    summary.columns = ['Churn Status', 'Number of Customers']
