# Databricks notebook source
# MAGIC %md
# MAGIC # 05 · Databricks Apps — put your data to work
# MAGIC
# MAGIC Dashboards are great for exploring. **Databricks Apps** let you build a real
# MAGIC **web application** — a custom UI your users interact with — that runs securely
# MAGIC inside Databricks and reads straight from Unity Catalog.
# MAGIC
# MAGIC In this workshop your instructor will deploy a small **Streamlit** app that reads
# MAGIC the Gold `fact_trips` / `dim_date` tables you built. This notebook explains how it
# MAGIC works and how *you* can deploy it yourself afterward.

# COMMAND ----------

# MAGIC %md
# MAGIC ## What is a Databricks App?
# MAGIC
# MAGIC - A lightweight web app (Streamlit, Dash, or Flask) hosted by Databricks.
# MAGIC - Runs as a **service principal** — it authenticates automatically, so there are
# MAGIC   no tokens or passwords in the code.
# MAGIC - **Governed by Unity Catalog** — the app can only read data it's granted access to.
# MAGIC - Great for turning a data model into a tool non-technical users can click through.

# COMMAND ----------

# MAGIC %md
# MAGIC ## The app's code (in the `app/` folder of this repo)
# MAGIC
# MAGIC | File | Purpose |
# MAGIC |---|---|
# MAGIC | `app.py` | The Streamlit app — KPIs and charts from `fact_trips` |
# MAGIC | `app.yaml` | Tells Databricks how to start the app |
# MAGIC | `requirements.txt` | Python libraries the app needs |
# MAGIC
# MAGIC The key idea in `app.py`: it uses the **Databricks SDK** to run SQL against your
# MAGIC star schema and draw charts — the same tables Genie and your dashboard use.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Deploy it yourself (optional, ~5 minutes)
# MAGIC
# MAGIC 1. In the left sidebar, click **Compute → Apps** (or search "Apps").
# MAGIC 2. Click **Create app** → **Custom**. Give it a name like `nyc-taxi-explorer`.
# MAGIC 3. When asked for the source code, point it at the **`app/`** folder of this repo
# MAGIC    in your workspace (the Git folder you cloned).
# MAGIC 4. Click **Deploy**. Databricks installs the requirements and starts it.
# MAGIC 5. When the status is **Running**, click the app URL to open your live app. 🎉
# MAGIC
# MAGIC > 💡 The app reads `workspace.tcu_taxi.fact_trips` and `dim_date`, so make sure
# MAGIC > you've run notebooks **00 → 03** first to create those tables.

# COMMAND ----------

# MAGIC %md
# MAGIC ## The big picture — you did end-to-end Data + AI 🎯
# MAGIC
# MAGIC ```
# MAGIC  samples.nyctaxi.trips
# MAGIC          │  (01) read + Delta
# MAGIC          ▼
# MAGIC     trips_bronze ──(02)──▶ trips_silver ──(03)──▶  ⭐ fact_trips
# MAGIC                                                       dim_date
# MAGIC                                                       dim_location
# MAGIC                                                          │
# MAGIC                     ┌────────────────────────────────────┼───────────────┐
# MAGIC                     ▼                                     ▼               ▼
# MAGIC              (04) Dashboard                        (04) Genie      (05) Databricks App
# MAGIC ```
# MAGIC
# MAGIC From raw data → clean layers → a star schema → dashboards, natural-language
# MAGIC analytics, and a live app. That's the Lakehouse in one afternoon.
# MAGIC
# MAGIC ### Keep learning
# MAGIC - **Databricks Free Edition** is yours to keep — rebuild this with your own data.
# MAGIC - Free self-paced training: **Databricks Academy** (customer-academy.databricks.com).
# MAGIC - Docs: **docs.databricks.com**
# MAGIC
# MAGIC **Thank you for joining the TCU x Databricks workshop!** 🚕
