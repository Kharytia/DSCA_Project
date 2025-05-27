import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

#RFM analysis
def plot_rfm_segments(rfm: pd.DataFrame, output_path: str) -> None:
    """Plot distribution of RFM segments and save to file."""
    segment_counts = rfm["Segment"].value_counts().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=segment_counts.index, y=segment_counts.values, palette="viridis")
    plt.title("Customer Segments by Count")
    plt.ylabel("Number of Customers")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_revenue_by_segment(rfm: pd.DataFrame, output_path: str) -> None:
    """Plot total revenue per customer segment."""
    revenue_by_segment = rfm.groupby("Segment")["Monetary"].sum().sort_values(ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=revenue_by_segment.index, y=revenue_by_segment.values, palette="magma")
    plt.title("Total Revenue by Segment")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_frequency_distribution(rfm: pd.DataFrame, output_path: str) -> None:
    """Plot histogram of frequency values."""
    plt.figure(figsize=(8, 5))
    sns.histplot(rfm["Frequency"], bins=30, kde=True, color="skyblue")
    plt.title("Distribution of Purchase Frequency")
    plt.xlabel("Frequency")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

#Sales analysis
def plot_sales_over_time(monthly_sales: pd.DataFrame):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_sales, x='Month', y='TotalPrice')
    plt.title("Monthly Sales Over Time")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_top_selling_products(product_sales: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.barplot(data=product_sales, y='Description', x='Quantity', palette='Blues_r')
    plt.title("Top Selling Products")
    plt.xlabel("Total Quantity Sold")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.show()

def plot_product_returns(returns: pd.DataFrame):
    top_returns = returns.head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_returns, y='Description', x='Quantity', palette='Reds_r')
    plt.title("Top Returned Products")
    plt.xlabel("Total Quantity Returned")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.show()

def plot_country_revenue(country_sales: pd.DataFrame):
    top_countries = country_sales.head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top_countries, y='Country', x='TotalPrice', palette='Greens_r')
    plt.title("Revenue by Country")
    plt.xlabel("Total Revenue")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()

#Churn analysis
def plot_churn_distribution(summary_df: pd.DataFrame):
    plt.figure(figsize=(8, 5))
    sns.barplot(data=summary_df, x='Churn Status', y='Number of Customers', palette='coolwarm')
    plt.title('Customer Churn Risk Breakdown')
    plt.xlabel('Churn Risk Segment')
    plt.ylabel('Number of Customers')
    plt.tight_layout()
    plt.show()

#Market Basket analysis
def plot_association_rules(rules_df: pd.DataFrame, top_n=10):
    top = rules_df.head(top_n).copy()
    top['rule'] = top['antecedents'].apply(lambda x: ', '.join(list(x))) + ' → ' + top['consequents'].apply(lambda x: ', '.join(list(x)))

    plt.figure(figsize=(10, 6))
    sns.barplot(data=top, y='rule', x='lift', palette='Blues_d')
    plt.title('Top Product Association Rules (by Lift)')
    plt.xlabel('Lift')
    plt.ylabel('Rule')
    plt.tight_layout()
    plt.show()

#Customer Lifetime Value
def plot_clv_distribution(customer_df: pd.DataFrame):
    plt.figure(figsize=(8, 5))
    sns.histplot(customer_df['CLV'], bins=50, kde=True)
    plt.title("Customer Lifetime Value Distribution")
    plt.xlabel("Estimated CLV (£)")
    plt.ylabel("Number of Customers")
    plt.tight_layout()
    plt.show()
