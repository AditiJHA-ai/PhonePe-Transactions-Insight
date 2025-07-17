# Streamlit app placeholder
# 📁 app.py (Streamlit Dashboard)
import sys

try:
    import streamlit as st # type: ignore
except ModuleNotFoundError:
    print("❌ The 'streamlit' module is not installed. Please install it using: pip install streamlit")
    sys.exit(1)

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data with error handling
def load_csv(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError:
        st.error(f"❌ File not found: {path}")
        return pd.DataFrame()

a_transaction = load_csv("data/aggregated_transaction.csv")
a_user = load_csv("data/aggregated_user.csv")
t_transaction = load_csv("data/top_transaction.csv")
t_user = load_csv("data/top_user.csv")
m_user = load_csv("data/map_user_hover.csv")
m_transaction = load_csv("data/map_transaction_hover.csv")

st.set_page_config(layout="wide")
st.title("📱 PhonePe Transaction Insights Dashboard")

# Sidebar
section = st.sidebar.selectbox("Select Section", [
    "Aggregated Transactions",
    "Top Transactions",
    "Map Overview",
    "User Insights"
])

if section == "Aggregated Transactions" and not a_transaction.empty:
    st.header("📊 Aggregated Transactions Over Time")
    year = st.selectbox("Select Year", sorted(a_transaction['year'].dropna().unique()))
    df_filtered = a_transaction[a_transaction['year'] == year]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_filtered, x='quarter', y='transaction_amount', hue='transaction_type', ax=ax)
    ax.set_title(f"Transaction Amount by Type - {year}")
    st.pyplot(fig)

elif section == "Top Transactions" and not t_transaction.empty:
    st.header("🏆 Top States by Transaction Volume")
    top_states = t_transaction.groupby('entity_name')[['count', 'amount']].sum().reset_index()
    top_states = top_states.sort_values(by='amount', ascending=False).head(10)
    st.dataframe(top_states)

    fig, ax = plt.subplots()
    sns.barplot(data=top_states, y='entity_name', x='amount', ax=ax)
    ax.set_title("Top 10 States by Total Amount")
    st.pyplot(fig)

elif section == "Map Overview" and not m_transaction.empty:
    st.header("🗺️ State Map View (Hover Data)")
    year = st.selectbox("Select Year", sorted(m_transaction['year'].dropna().unique()))
    quarter = st.selectbox("Select Quarter", sorted(m_transaction['quarter'].dropna().unique()))
    map_df = m_transaction[(m_transaction['year'] == year) & (m_transaction['quarter'] == quarter)]
    st.dataframe(map_df[['state_name', 'amount', 'count']].sort_values(by='amount', ascending=False).head(10))

elif section == "User Insights" and not a_user.empty:
    st.header("👥 Aggregated Users Over Time")
    year = st.selectbox("Select Year", sorted(a_user['year'].dropna().unique()))
    df_filtered = a_user[a_user['year'] == year]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_filtered, x='quarter', y='registeredUsers', hue='brand', ax=ax)
    ax.set_title(f"User Growth by Brand - {year}")
    st.pyplot(fig)
else:
    st.warning("No data available for the selected section or failed to load datasets.")
