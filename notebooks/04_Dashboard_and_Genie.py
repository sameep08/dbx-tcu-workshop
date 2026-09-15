# Databricks notebook source
# MAGIC %md
# MAGIC # 04 · AI/BI Dashboard & Genie
# MAGIC
# MAGIC You've built a clean **star schema**. Now let's turn it into insight two ways:
# MAGIC 1. An **AI/BI Dashboard** — visual tiles anyone can read.
# MAGIC 2. **Genie** — ask questions of your data in **plain English**, no SQL needed.
# MAGIC
# MAGIC This notebook gives you the exact SQL for each dashboard tile, then walks you
# MAGIC through building the dashboard and Genie space in the UI.

# COMMAND ----------

CATALOG = "workspace"
SCHEMA  = "tcu_taxi"
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")
print(f"Working in {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part A — Dashboard tiles (run each query first)
# MAGIC
# MAGIC Run the four queries below to confirm they work. Then you'll paste each one
# MAGIC into a dashboard dataset in Part B.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TILE 1 · Trips by hour of day (use a Bar/Area chart)
# MAGIC SELECT pickup_hour, COUNT(*) AS trips
# MAGIC FROM fact_trips
# MAGIC GROUP BY pickup_hour
# MAGIC ORDER BY pickup_hour;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TILE 2 · Revenue by day of week (use a Bar chart)
# MAGIC SELECT d.day_of_week, ROUND(SUM(f.fare_usd), 0) AS total_revenue
# MAGIC FROM fact_trips f
# MAGIC JOIN dim_date  d ON f.pickup_date_key = d.date_key
# MAGIC GROUP BY d.day_of_week
# MAGIC ORDER BY total_revenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TILE 3 · Fare vs. distance buckets (use a Bar chart)
# MAGIC SELECT
# MAGIC   CASE
# MAGIC     WHEN trip_miles < 1  THEN '0-1 mi'
# MAGIC     WHEN trip_miles < 3  THEN '1-3 mi'
# MAGIC     WHEN trip_miles < 5  THEN '3-5 mi'
# MAGIC     WHEN trip_miles < 10 THEN '5-10 mi'
# MAGIC     ELSE '10+ mi'
# MAGIC   END                        AS distance_bucket,
# MAGIC   COUNT(*)                   AS trips,
# MAGIC   ROUND(AVG(fare_usd), 2)    AS avg_fare
# MAGIC FROM fact_trips
# MAGIC GROUP BY distance_bucket
# MAGIC ORDER BY avg_fare;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- TILE 4 · Headline numbers (use Counter tiles)
# MAGIC SELECT
# MAGIC   COUNT(*)                    AS total_trips,
# MAGIC   ROUND(SUM(fare_usd), 0)     AS total_revenue,
# MAGIC   ROUND(AVG(fare_usd), 2)     AS avg_fare,
# MAGIC   ROUND(AVG(trip_miles), 2)   AS avg_miles
# MAGIC FROM fact_trips;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part B — Build the AI/BI Dashboard (in the UI)
# MAGIC
# MAGIC 1. In the left sidebar, click **Dashboards** → **Create dashboard**.
# MAGIC 2. Go to the **Data** tab → **Create from SQL**. Paste **TILE 1**'s query and
# MAGIC    give the dataset a name like `trips_by_hour`. Repeat for tiles 2–4.
# MAGIC 3. Switch to the **Canvas** tab → **Add a visualization**.
# MAGIC    - Pick the dataset, choose a chart type (Bar, Area, or Counter), and drag the
# MAGIC      fields onto the X/Y axes.
# MAGIC 4. Add a title text box at the top: **"NYC Taxi — TCU Workshop"**.
# MAGIC 5. Click **Publish** (top right) so you can share it.
# MAGIC
# MAGIC > 💡 Try the **✨ AI-assisted** button in a dataset — describe the chart you want
# MAGIC > in words and let Databricks draft the SQL for you.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Part C — Create a Genie space (talk to your data)
# MAGIC
# MAGIC Genie lets anyone ask questions in natural language; it writes the SQL for them.
# MAGIC
# MAGIC 1. In the left sidebar, click **Genie** → **New**.
# MAGIC 2. **Add tables:** choose `workspace.tcu_taxi.fact_trips`, `dim_date`, and
# MAGIC    `dim_location`.
# MAGIC 3. Give it a name: **"NYC Taxi Genie"** and click **Save**.
# MAGIC 4. In **Instructions** (the ⚙️ / General instructions box), paste the text from
# MAGIC    the next cell — good instructions make Genie far more accurate.
# MAGIC 5. Start asking questions! Try the samples below.

# COMMAND ----------

# MAGIC %md
# MAGIC **Paste this into Genie's General Instructions:**
# MAGIC
# MAGIC ```
# MAGIC This is a NYC taxi dataset modeled as a star schema.
# MAGIC - fact_trips has one row per taxi trip with measures: fare_usd, trip_miles,
# MAGIC   duration_min, mph. Join it to the dimensions using the *_key columns.
# MAGIC - dim_date (join pickup_date_key = date_key) has day_of_week, month, is_weekend.
# MAGIC - dim_location (join pickup_location_key = location_key) has zip_code.
# MAGIC "Revenue" means SUM(fare_usd). "Trips" means COUNT(*). Currency is US dollars.
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC **Sample questions to ask Genie:**
# MAGIC - *How many trips were there in total?*
# MAGIC - *What is the total revenue by day of week?*
# MAGIC - *What is the average fare for trips longer than 5 miles?*
# MAGIC - *Which pickup zip codes have the most trips?*
# MAGIC - *Are weekends busier than weekdays?*
# MAGIC
# MAGIC 👀 Notice Genie shows the **SQL it wrote** — a great way to learn.
# MAGIC
# MAGIC 👉 **Next:** open **`05_Databricks_App`** to see your data powering a live app.
