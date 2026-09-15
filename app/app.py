"""
NYC Taxi Explorer — a tiny Databricks App for the TCU workshop.

It reads the Gold star-schema tables you built in notebook 03
(workspace.tcu_taxi.fact_trips / dim_date) and shows them in a simple web app.

The app runs on Databricks Apps as a service principal, so we use the
Databricks SDK, which picks up its credentials automatically in that
environment — no tokens to paste.
"""
import os
import pandas as pd
import streamlit as st
from databricks.sdk import WorkspaceClient

CATALOG = "workspace"
SCHEMA = "tcu_taxi"

st.set_page_config(page_title="NYC Taxi Explorer", page_icon="🚕", layout="wide")
w = WorkspaceClient()


def get_warehouse_id() -> str:
    """Use the warehouse from the app config if set, else the first available one."""
    env_id = os.getenv("DATABRICKS_WAREHOUSE_ID")
    if env_id:
        return env_id
    warehouses = list(w.warehouses.list())
    if not warehouses:
        st.error("No SQL warehouse found. Create one in SQL Warehouses, then reload.")
        st.stop()
    return warehouses[0].id


@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    """Run SQL on the warehouse and return the rows as a pandas DataFrame."""
    resp = w.statement_execution.execute_statement(
        warehouse_id=get_warehouse_id(),
        statement=sql,
        wait_timeout="30s",
    )
    cols = [c.name for c in resp.manifest.schema.columns]
    rows = resp.result.data_array or []
    return pd.DataFrame(rows, columns=cols)


st.title("🚕 NYC Taxi Explorer")
st.caption(f"Live data from {CATALOG}.{SCHEMA} — built during the TCU x Databricks workshop")

# --- Headline metrics -------------------------------------------------------
kpis = run_query(f"""
    SELECT COUNT(*)                  AS trips,
           ROUND(SUM(fare_usd), 0)   AS revenue,
           ROUND(AVG(fare_usd), 2)   AS avg_fare,
           ROUND(AVG(trip_miles), 2) AS avg_miles
    FROM {CATALOG}.{SCHEMA}.fact_trips
""").iloc[0]

# The SDK returns values as strings, so convert before formatting.
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total trips", f"{int(float(kpis['trips'])):,}")
c2.metric("Total revenue", f"${int(float(kpis['revenue'])):,}")
c3.metric("Avg fare", f"${float(kpis['avg_fare']):.2f}")
c4.metric("Avg distance", f"{float(kpis['avg_miles']):.2f} mi")

# --- Charts -----------------------------------------------------------------
left, right = st.columns(2)

with left:
    st.subheader("Trips by hour of day")
    by_hour = run_query(f"""
        SELECT pickup_hour, COUNT(*) AS trips
        FROM {CATALOG}.{SCHEMA}.fact_trips
        GROUP BY pickup_hour ORDER BY pickup_hour
    """).astype({"pickup_hour": int, "trips": int})
    st.bar_chart(by_hour, x="pickup_hour", y="trips")

with right:
    st.subheader("Revenue by day of week")
    by_day = run_query(f"""
        SELECT d.day_of_week, ROUND(SUM(f.fare_usd), 0) AS revenue
        FROM {CATALOG}.{SCHEMA}.fact_trips f
        JOIN {CATALOG}.{SCHEMA}.dim_date  d ON f.pickup_date_key = d.date_key
        GROUP BY d.day_of_week ORDER BY revenue DESC
    """).astype({"revenue": float})
    st.bar_chart(by_day, x="day_of_week", y="revenue")

st.divider()
st.caption("Powered by Databricks Apps + Unity Catalog. Data is cached for 5 minutes.")
