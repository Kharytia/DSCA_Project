#!/opt/anaconda3/bin/python

import os
import pandas as pd
import matplotlib.pyplot as plt

from ETL.extract import load_data
from ETL.transform import clean_data, add_return_flag, split_sales_returns
from ETL.load import save_to_csv
from ETL.rfm import calculate_rfm, assign_rfm_scores, score_rfm, assign_customer_segments
from ETL.churn import calculate_customer_metrics, classify_churn_status, get_churn_summary
from ETL.sales_analysis import (
    sales_over_time,
    top_selling_products,
    product_returns,
    country_orders,
    country_revenue
)
from ETL.market_basket import prepare_basket_data, generate_association_rules, get_top_rules
from ETL.clv import estimate_clv, calculate_customer_metrics, simulate_churn_loss

from utils.plotting import (
    plot_rfm_segments,
    plot_frequency_distribution,
    plot_revenue_by_segment,
    plot_association_rules,
    plot_churn_distribution,
    plot_clv_distribution,
    plot_country_revenue,
    plot_product_returns,
    plot_sales_over_time,
    plot_top_selling_products
)

# Load and clean data
df = load_data("data/OnlineRetail.csv")
df = clean_data(df)
df = add_return_flag(df)
sales, returns = split_sales_returns(df)

# --- RFM Analysis ---
rfm = calculate_rfm(sales)
rfm = assign_rfm_scores(rfm)
rfm = assign_customer_segments(rfm)
plot_rfm_segments(rfm)
plt.savefig("visualizations/rfm_segments.png")
plot_frequency_distribution(rfm)
plt.savefig("visualizations/frequency_distribution.png")
plot_revenue_by_segment(sales, rfm)
plt.savefig("visualizations/revenue_by_segment.png")

# --- Churn Analysis ---
churn_df = calculate_customer_metrics(sales)
churn_df = classify_churn_status(churn_df)
plot_churn_distribution(churn_df)
plt.savefig("visualizations/churn_distribution.png")

# --- Sales Trends ---
plot_sales_over_time(df)
plt.savefig("visualizations/sales_trends.png")
plot_product_returns(df)
plt.savefig("visualizations/returns_trends.png")
plot_top_selling_products(df)
plt.savefig("visualizations/top_products.png")
plot_country_revenue(df)
plt.savefig("visualizations/country_revenue.png")

# --- Market Basket ---
basket_df = prepare_basket_data(sales)
rules = generate_association_rules(basket_df)
top_rules = get_top_rules(rules)
plot_association_rules(top_rules)
plt.savefig("visualizations/item_combinations.png")

# --- CLV ---
clv_df = calculate_customer_metrics(sales)
clv_df = estimate_clv(clv_df)
loss = simulate_churn_loss(clv_df, churn_df)
plot_clv_distribution(clv_df)
plt.savefig("visualizations/clv_distribution.png")

print(f"Estimated churn loss: £{loss:,.2f}")
