# Databricks notebook source
# MAGIC %md
# MAGIC # 🚕 TCU x Databricks Workshop — Start Here
# MAGIC
# MAGIC Welcome! Over the next few hours you'll go from raw NYC taxi data to a
# MAGIC **star schema**, an **AI/BI dashboard**, a **Genie** natural-language space,
# MAGIC and a small **Databricks App** — all on the **free** Databricks platform.
# MAGIC
# MAGIC ### What you'll build today
# MAGIC | Notebook | You will... |
# MAGIC |---|---|
# MAGIC | **00 Start Here** *(this one)* | Set up your workspace and check the data |
# MAGIC | **01 Lakehouse & Delta** | Read data, save a Delta table, see ACID + time travel |
# MAGIC | **02 Data Engineering** | Build Bronze → Silver layers (clean & transform) |
# MAGIC | **03 Star Schema** | Build Gold fact + dimension tables |
# MAGIC | **04 Dashboard & Genie** | Visualize and ask questions in plain English |
# MAGIC | **05 Databricks App** | See a live data app powered by your tables |
# MAGIC
# MAGIC > 💡 **No cluster setup needed.** Databricks Free Edition uses **serverless**
# MAGIC > compute. Just click into a cell and press **Shift + Enter** to run it.

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. How Unity Catalog organizes data
# MAGIC
# MAGIC Everything in Databricks lives in a **three-level namespace**:
# MAGIC
# MAGIC ```
# MAGIC catalog . schema . table
# MAGIC    │         │        └── a table of rows & columns (e.g. trips)
# MAGIC    │         └── a group of tables (like a folder / database)
# MAGIC    └── the top-level container (you get one called `workspace`)
# MAGIC ```
# MAGIC
# MAGIC We'll put everything we build into your own schema so it stays tidy.

# COMMAND ----------

# These two variables are used across all notebooks in this workshop.
# On Databricks Free Edition every account gets a writable catalog called `workspace`.
CATALOG = "workspace"
SCHEMA  = "tcu_taxi"

print(f"Your workspace area for today: {CATALOG}.{SCHEMA}")

# COMMAND ----------

# Create the schema (safe to re-run) and make it the default so we can
# refer to tables by their short name.
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")

print(f"✅ Ready. Current location: {spark.sql('SELECT current_catalog(), current_schema()').first()}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Meet the data: `samples.nyctaxi.trips`
# MAGIC
# MAGIC Databricks ships with a free sample catalog called **`samples`**. Inside it,
# MAGIC `nyctaxi.trips` holds real New York City taxi rides. Let's look at it.
# MAGIC
# MAGIC `DESCRIBE` shows the columns and their types — always a good first step.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE samples.nyctaxi.trips;

# COMMAND ----------

# MAGIC %md
# MAGIC Now let's preview a few rows. Click the **＋ / chart icons** above the results
# MAGIC to try Databricks' built-in visualizations later.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM samples.nyctaxi.trips LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- How much data are we working with?
# MAGIC SELECT
# MAGIC   COUNT(*)                          AS total_trips,
# MAGIC   MIN(tpep_pickup_datetime)         AS earliest_trip,
# MAGIC   MAX(tpep_pickup_datetime)         AS latest_trip,
# MAGIC   ROUND(AVG(fare_amount), 2)        AS avg_fare,
# MAGIC   ROUND(AVG(trip_distance), 2)      AS avg_miles
# MAGIC FROM samples.nyctaxi.trips;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ You're set up!
# MAGIC
# MAGIC You created your schema and confirmed you can read the sample data.
# MAGIC
# MAGIC 👉 **Next:** open **`01_Lakehouse_and_Delta`**.
