import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import create_engine
import pydeck as pdk

# Auto-refresh every 2 seconds (requires Streamlit >=1.23)
if hasattr(st, "autorefresh"):
    st.autorefresh(interval=2000, key="refresh")

st.set_page_config(page_title="Fraud Detection Dashboard", page_icon="⚡", layout="wide")
engine = create_engine('sqlite:///data/fraud_detector.db')

# --- Helper Functions ---
def get_data():
    # Load up to 200 transactions and 100 most recent alerts
    tx = pd.read_sql("SELECT * FROM transactions ORDER BY timestamp DESC LIMIT 200", engine)
    alerts = pd.read_sql("SELECT * FROM alerts ORDER BY id DESC LIMIT 100", engine)
    return tx, alerts

# --- Main Title ---
st.title("Real-Time Fraud Detection Dashboard")

# Fetch data from DB
tx, alerts = get_data()

# --- Sidebar filters ---
st.sidebar.header("Filter Alerts")
min_risk = st.sidebar.slider("Minimum Risk Score", 0, 100, 30)
country_filter = st.sidebar.multiselect(
    "Country", 
    sorted(tx['location'].unique()), 
    default=list(tx['location'].unique())
)
filtered_alerts = alerts[(alerts['risk_score'] >= min_risk)]
if country_filter:
    filtered_alerts = filtered_alerts[filtered_alerts['transaction_id'].isin(
        tx[tx['location'].isin(country_filter)]['transaction_id']
    )]

# --- Tabs for navigation ---
tab1, tab2, tab3, tab4 = st.tabs([
    "Recent Transactions", 
    "Flagged Alerts", 
    "Analytics", 
    "Geo Map"
])

# --- Tab 1: Recent Transactions ---
with tab1:
    st.subheader("Recent Transactions")
    st.dataframe(tx)

# --- Tab 2: Flagged Alerts with details ---
with tab2:
    st.subheader(f"Flagged Alerts (Risk >= {min_risk})")
    for _, row in filtered_alerts.iterrows():
        # Each alert as an expandable panel
        with st.expander(f"Alert {row['id']} — Tx {row['transaction_id']}, Score: {row['risk_score']}"):
            st.write({
                "Transaction ID": row['transaction_id'],
                "Risk Score": row['risk_score'],
                "Reasons": row['reasons'],
                "Explanation": row['explanation']
            })

# --- Tab 3: Analytics and Charts ---
with tab3:
    st.subheader("Analytics & Visualizations")

    col1, col2 = st.columns(2)
    # Bar: Transactions per Country
    with col1:
        st.markdown("**Transactions per Country**")
        cnt = tx['location'].value_counts().reset_index()
        cnt.columns = ['Country', 'Count']
        st.bar_chart(cnt.set_index('Country'))

    with col2:
        st.markdown("**Alerts by Reason (Pie)**")
        reasons_series = alerts['reasons'].str.split(",").explode().str.strip()
        reason_counts = reasons_series.value_counts()
        st.pyplot(
            reason_counts.plot.pie(autopct='%1.1f%%', figsize=(4, 4), title="Alert Reasons").get_figure()
        )

    # Line: Alerts Over Time
    st.markdown("**Alerts Over Time**")
    if not alerts.empty:
        alerts['timestamp'] = pd.to_datetime(alerts['transaction_id'].map(
            dict(zip(tx['transaction_id'], tx['timestamp'].astype(str)))
        ))
        chart = alt.Chart(alerts).mark_line().encode(
            x='timestamp:T', y='risk_score:Q'
        ).properties(height=300)
        st.altair_chart(chart, use_container_width=True)

# --- Tab 4: Map Visualization ---
with tab4:
    st.subheader("Geo Map of Transactions (Last 200)")

    # Check if lat/lon columns exist and contain data
    if 'lat' in tx.columns and 'lon' in tx.columns and tx['lat'].notnull().all() and tx['lon'].notnull().all():
        # Streamlit's st.map requires lat/lon columns
        st.map(tx[['lat', 'lon']])
    else:
        st.write("No latitude/longitude data available. Please add geocoding to your transactions.")

