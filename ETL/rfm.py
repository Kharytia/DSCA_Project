import pandas as pd

def calculate_rfm(df: pd.DataFrame, today: pd.Timestamp = None) -> pd.DataFrame:
    """Calculate RFM metrics for each customer."""
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    
    if today is None:
        today = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df[df["Quantity"] > 0].copy()
    rfm["TotalValue"] = rfm["Quantity"] * rfm["Price"]

    rfm_summary = rfm.groupby("Customer ID").agg({
        "InvoiceDate": lambda x: (today - x.max()).days,
        "Invoice": "nunique",
        "TotalValue": "sum"
    }).reset_index()

    rfm_summary.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]
    return rfm_summary


def assign_rfm_scores(rfm: pd.DataFrame) -> pd.DataFrame:
    """Assign quantile-based RFM scores (1-5) for each metric."""
    rfm["R"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1])
    rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5])
    rfm["M"] = pd.qcut(rfm["Monetary"], 5, labels=[1,2,3,4,5])
    
    rfm["RFM_Score"] = rfm["R"].astype(str) + rfm["F"].astype(str) + rfm["M"].astype(str)
    return rfm

def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    rfm = rfm.copy()
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)
    return rfm


def assign_customer_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    """Assign customer segment based on RFM Score patterns."""
    def segment_map(score):
        if score == '555':
            return 'VIP'
        elif score[0] == '5':
            return 'Loyal'
        elif score[1] == '5':
            return 'Frequent Buyer'
        elif score[2] == '5':
            return 'Big Spender'
        elif score in ['111', '112', '113']:
            return 'Lost'
        elif score.startswith('1'):
            return 'At Risk'
        else:
            return 'Others'

    rfm['Segment'] = rfm['RFM_Score'].apply(segment_map)
    return rfm
 