import os
import pandas as pd
import numpy as np
import seaborn as sns
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
    plot_top_selling_products,
    plot_country_orders
)

# Load and clean data
df = load_data("data/OnlineRetail.csv")
df = clean_data(df)
df = add_return_flag(df)
sales, returns = split_sales_returns(df)

# RFM Analysis 
rfm = calculate_rfm(sales)
rfm = assign_rfm_scores(rfm)
rfm = assign_customer_segments(rfm)
plot_rfm_segments(rfm,"visualizations/rfm_segments.png" )
plot_frequency_distribution(rfm, "visualizations/frequency_distribution.png")
plot_revenue_by_segment(rfm, "visualizations/revenue_by_segment.png")


# Churn Analysis
churn_df = calculate_customer_metrics(sales)
churn_df = classify_churn_status(churn_df)
churn_df_summary = get_churn_summary(churn_df)
plot_churn_distribution(churn_df_summary, "visualizations/churn_distribution.png")

# Sales Trends 
monthly_sales = sales_over_time(sales)
top_products = top_selling_products(sales)
top_returns = product_returns(returns)
country_sales = country_revenue(sales)
orders_country = country_orders(sales)

plot_sales_over_time(monthly_sales, "visualizations/sales_trends.png")
plot_product_returns(top_returns, "visualizations/returns_trends.png")
plot_top_selling_products(top_products, "visualizations/top_products.png")
plot_country_revenue(country_sales, "visualizations/country_revenue.png")
plot_country_orders(orders_country, "visualizations/country_orders.png")

# Market Basket
basket = prepare_basket_data(df)
rules = generate_association_rules(basket)
top_rules = get_top_rules(rules)

plot_association_rules(rules, "visualizations/association_rules.png", top_n=10)


# CLV
clv_df = calculate_customer_metrics(df)
clv_df = estimate_clv(clv_df)
loss = simulate_churn_loss(clv_df, churn_df)

print(f"Estimated churn loss: £{loss:,.2f}")
