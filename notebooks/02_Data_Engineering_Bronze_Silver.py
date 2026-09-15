# Databricks notebook source
# MAGIC %md
# MAGIC # 02 · Data Engineering — Bronze → Silver
# MAGIC
# MAGIC Real data is messy. **Data engineering** is the craft of turning raw data into
# MAGIC clean, trustworthy data that analysts and AI can rely on.
# MAGIC
# MAGIC The **medallion architecture** from the slides organizes this into layers:
# MAGIC
# MAGIC ```
# MAGIC  🥉 BRONZE            🥈 SILVER                 🥇 GOLD
# MAGIC  raw, as-ingested     cleaned & enriched        business-ready
# MAGIC  (keep everything)    (filter bad rows,         (star schema —
# MAGIC                        add useful columns)        next notebook)
# MAGIC ```
# MAGIC
# MAGIC In this notebook we build **Bronze** and **Silver** for the taxi data.

# COMMAND ----------

CATALOG = "workspace"
SCHEMA  = "tcu_taxi"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")
print(f"Working in {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. 🥉 Bronze — land the raw data
# MAGIC
# MAGIC The Bronze layer is a faithful copy of the source, plus a little metadata so we
# MAGIC always know *when* and *from where* the data arrived. We change nothing else.

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

bronze = (
    spark.table("samples.nyctaxi.trips")
         .withColumn("_ingested_at", current_timestamp())        # when we loaded it
         .withColumn("_source", lit("samples.nyctaxi.trips"))     # where it came from
)

bronze.write.format("delta").mode("overwrite").saveAsTable("trips_bronze")
print("✅ Created workspace.tcu_taxi.trips_bronze")
display(spark.table("trips_bronze").limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Explore before you clean
# MAGIC
# MAGIC Good engineers look at the data before transforming it. Let's find the quality
# MAGIC problems we need to fix.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   COUNT(*)                                             AS total_rows,
# MAGIC   SUM(CASE WHEN fare_amount   <= 0 THEN 1 ELSE 0 END)  AS bad_fare,
# MAGIC   SUM(CASE WHEN trip_distance <= 0 THEN 1 ELSE 0 END)  AS bad_distance,
# MAGIC   SUM(CASE WHEN tpep_dropoff_datetime <= tpep_pickup_datetime THEN 1 ELSE 0 END) AS bad_time
# MAGIC FROM trips_bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. 🥈 Silver — clean and enrich
# MAGIC
# MAGIC Now we:
# MAGIC - **Filter out** rows with impossible values (zero/negative fare or distance,
# MAGIC   dropoff before pickup).
# MAGIC - **Add useful columns** that make later analysis easy: trip duration, pickup
# MAGIC   date/hour/day-of-week, and average speed.
# MAGIC
# MAGIC We'll do it in **SQL** here (it reads almost like English).

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE trips_silver AS
# MAGIC WITH cleaned AS (
# MAGIC   SELECT
# MAGIC     tpep_pickup_datetime                                             AS pickup_ts,
# MAGIC     tpep_dropoff_datetime                                            AS dropoff_ts,
# MAGIC     trip_distance                                                    AS trip_miles,
# MAGIC     fare_amount                                                      AS fare_usd,
# MAGIC     pickup_zip,
# MAGIC     dropoff_zip,
# MAGIC     -- derived columns ↓
# MAGIC     ROUND((UNIX_TIMESTAMP(tpep_dropoff_datetime) - UNIX_TIMESTAMP(tpep_pickup_datetime)) / 60.0, 1)
# MAGIC                                                                      AS duration_min,
# MAGIC     CAST(tpep_pickup_datetime AS DATE)                               AS pickup_date,
# MAGIC     HOUR(tpep_pickup_datetime)                                       AS pickup_hour,
# MAGIC     DATE_FORMAT(tpep_pickup_datetime, 'EEEE')                        AS pickup_day_of_week
# MAGIC   FROM trips_bronze
# MAGIC   WHERE fare_amount   > 0
# MAGIC     AND trip_distance > 0
# MAGIC     AND tpep_dropoff_datetime > tpep_pickup_datetime
# MAGIC )
# MAGIC SELECT
# MAGIC   *,
# MAGIC   -- average speed in miles per hour (guard against divide-by-zero)
# MAGIC   ROUND(trip_miles / NULLIF(duration_min / 60.0, 0), 1) AS mph
# MAGIC FROM cleaned;

# COMMAND ----------

# MAGIC %md
# MAGIC ### How many rows survived cleaning?

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   (SELECT COUNT(*) FROM trips_bronze) AS bronze_rows,
# MAGIC   (SELECT COUNT(*) FROM trips_silver) AS silver_rows;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Explore the clean data
# MAGIC
# MAGIC Try turning these results into a **bar chart**: run the cell, then click the
# MAGIC **+** above the results and choose **Visualization → Bar**.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Busiest hours of the day
# MAGIC SELECT pickup_hour, COUNT(*) AS trips
# MAGIC FROM trips_silver
# MAGIC GROUP BY pickup_hour
# MAGIC ORDER BY pickup_hour;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Average fare by day of week
# MAGIC SELECT pickup_day_of_week, ROUND(AVG(fare_usd), 2) AS avg_fare, COUNT(*) AS trips
# MAGIC FROM trips_silver
# MAGIC GROUP BY pickup_day_of_week
# MAGIC ORDER BY avg_fare DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Recap
# MAGIC
# MAGIC - **Bronze** = raw + metadata (keep everything).
# MAGIC - **Silver** = cleaned + enriched (bad rows removed, helpful columns added).
# MAGIC - You used both **SQL** and **Python**, and explored the data with charts.
# MAGIC
# MAGIC 👉 **Next:** open **`03_Star_Schema_Gold`** to model this into a star schema.
