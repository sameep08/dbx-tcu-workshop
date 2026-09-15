# Databricks notebook source
# MAGIC %md
# MAGIC # 03 · The Gold Layer — a Star Schema ⭐
# MAGIC
# MAGIC Analysts and dashboards love data shaped as a **star schema**. It has:
# MAGIC
# MAGIC - **One fact table** in the middle — the *events* you measure (each taxi trip),
# MAGIC   holding **measures** (fare, miles, duration) and **keys** to the dimensions.
# MAGIC - **Dimension tables** around it — the *context* you slice by (date, location).
# MAGIC
# MAGIC ```
# MAGIC         dim_date                 dim_location
# MAGIC             \                      /
# MAGIC              \                    /
# MAGIC               \                  /
# MAGIC                +----------------+
# MAGIC                |   fact_trips   |   <- measures + foreign keys
# MAGIC                +----------------+
# MAGIC ```
# MAGIC
# MAGIC Why bother? It keeps the big fact table **small and fast**, avoids repeating
# MAGIC text everywhere, and makes BI tools and Genie generate simple, correct joins.

# COMMAND ----------

CATALOG = "workspace"
SCHEMA  = "tcu_taxi"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")
print(f"Working in {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Dimension: `dim_date`
# MAGIC
# MAGIC One row per calendar date, with attributes we can group by. The **`date_key`**
# MAGIC (an integer like `20160115`) is the **surrogate key** — a simple, stable ID the
# MAGIC fact table will point to.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE dim_date AS
# MAGIC SELECT DISTINCT
# MAGIC   CAST(DATE_FORMAT(pickup_date, 'yyyyMMdd') AS INT) AS date_key,
# MAGIC   pickup_date                                        AS full_date,
# MAGIC   YEAR(pickup_date)                                  AS year,
# MAGIC   MONTH(pickup_date)                                 AS month,
# MAGIC   DAY(pickup_date)                                   AS day,
# MAGIC   DATE_FORMAT(pickup_date, 'EEEE')                   AS day_of_week,
# MAGIC   CASE WHEN DAYOFWEEK(pickup_date) IN (1, 7) THEN true ELSE false END AS is_weekend
# MAGIC FROM trips_silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM dim_date ORDER BY date_key LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Dimension: `dim_location`
# MAGIC
# MAGIC One row per ZIP code seen in the data (as either a pickup or a dropoff). Here
# MAGIC the ZIP code itself is the key. In a real project you'd enrich this with
# MAGIC neighborhood, borough, latitude/longitude, etc.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE dim_location AS
# MAGIC SELECT DISTINCT zip AS location_key, zip AS zip_code
# MAGIC FROM (
# MAGIC   SELECT pickup_zip  AS zip FROM trips_silver
# MAGIC   UNION
# MAGIC   SELECT dropoff_zip AS zip FROM trips_silver
# MAGIC )
# MAGIC WHERE zip IS NOT NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS num_locations FROM dim_location;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Fact: `fact_trips`
# MAGIC
# MAGIC The grain is **one row per taxi trip**. We keep the **measures** (the numbers we
# MAGIC add up) and **foreign keys** that point at the dimensions.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE fact_trips AS
# MAGIC SELECT
# MAGIC   -- foreign keys → dimensions
# MAGIC   CAST(DATE_FORMAT(pickup_date, 'yyyyMMdd') AS INT) AS pickup_date_key,
# MAGIC   pickup_zip                                         AS pickup_location_key,
# MAGIC   dropoff_zip                                        AS dropoff_location_key,
# MAGIC   pickup_hour,
# MAGIC   -- measures ↓ (the numbers we analyze)
# MAGIC   fare_usd,
# MAGIC   trip_miles,
# MAGIC   duration_min,
# MAGIC   mph,
# MAGIC   1 AS trip_count
# MAGIC FROM trips_silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM fact_trips LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Use the star ⭐ — join fact to dimensions
# MAGIC
# MAGIC This is the payoff. We answer a real question by joining the small fact table
# MAGIC to the dimensions — exactly the kind of query a dashboard runs.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Revenue and trips by day of week and weekend flag
# MAGIC SELECT
# MAGIC   d.day_of_week,
# MAGIC   d.is_weekend,
# MAGIC   COUNT(*)                    AS trips,
# MAGIC   ROUND(SUM(f.fare_usd), 0)   AS total_revenue,
# MAGIC   ROUND(AVG(f.fare_usd), 2)   AS avg_fare
# MAGIC FROM fact_trips f
# MAGIC JOIN dim_date   d ON f.pickup_date_key = d.date_key
# MAGIC GROUP BY d.day_of_week, d.is_weekend
# MAGIC ORDER BY total_revenue DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Top 10 pickup ZIP codes by number of trips
# MAGIC SELECT
# MAGIC   l.zip_code,
# MAGIC   COUNT(*)                  AS trips,
# MAGIC   ROUND(AVG(f.fare_usd), 2) AS avg_fare
# MAGIC FROM fact_trips  f
# MAGIC JOIN dim_location l ON f.pickup_location_key = l.location_key
# MAGIC GROUP BY l.zip_code
# MAGIC ORDER BY trips DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Recap — your Gold star schema
# MAGIC
# MAGIC | Table | Type | Grain |
# MAGIC |---|---|---|
# MAGIC | `fact_trips` | Fact | one taxi trip |
# MAGIC | `dim_date` | Dimension | one calendar date |
# MAGIC | `dim_location` | Dimension | one ZIP code |
# MAGIC
# MAGIC These three tables are exactly what we'll point our **dashboard**, **Genie**, and
# MAGIC **app** at next.
# MAGIC
# MAGIC 👉 **Next:** open **`04_Dashboard_and_Genie`**.
