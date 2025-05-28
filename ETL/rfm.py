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
    """Assign customer segments based on RFM score patterns (RFM_Score as string)."""
    
    def segment_map(score):
        r = int(score[0])
        f = int(score[1])
        m = int(score[2])
        
        if r == 5 and f == 5 and m == 5:
            return 'VIP'
        elif r >= 4 and f >= 4:
            return 'Loyal'
        elif f >= 4 and m >= 4:
            return 'Frequent Buyer'
        elif m == 5:
            return 'Big Spender'
        elif r <= 2 and f <= 2 and m <= 2:
            return 'Lost'
        elif r <= 2:
            return 'At Risk'
        else:
            return 'Others'

    rfm['Segment'] = rfm['RFM_Score'].apply(segment_map)
    return rfm