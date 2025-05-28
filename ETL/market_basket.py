import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def prepare_basket_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare data in basket format for market basket analysis."""
    df = df[df['Quantity'] > 0]
    df = df[df['Invoice'].astype(str).str.startswith('C') == False]  # remove returns

    basket = (
        df.groupby(['Invoice', 'Description'])['Quantity']
        .sum().unstack().reset_index().fillna(0)
        .set_index('Invoice')
    )

    # Convert to binary presence matrix
    basket = basket.applymap(lambda x: 1 if x > 0 else 0)
    return basket

def generate_association_rules(basket: pd.DataFrame, min_support=0.01, min_confidence=0.3) -> pd.DataFrame:
    """Generate association rules from basket data."""
    frequent_itemsets = apriori(basket, min_support=min_support, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    return rules.sort_values("lift", ascending=False)

def get_top_rules(rules: pd.DataFrame, top_n=10) -> pd.DataFrame:
    """Return top N rules based on lift."""
    return rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(top_n)