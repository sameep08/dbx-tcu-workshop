# Databricks notebook source
# MAGIC %md
# MAGIC # 01 · Lakehouse Foundations & Delta Lake
# MAGIC
# MAGIC In the slides you saw the **Lakehouse** idea: one place for all your data that
# MAGIC is both *reliable like a warehouse* and *open like a data lake*. The magic that
# MAGIC makes that possible is **Delta Lake** — the default table format on Databricks.
# MAGIC
# MAGIC In this notebook you'll:
# MAGIC 1. Read the sample data with **Python (PySpark)** and **SQL**
# MAGIC 2. Save your own **Delta table**
# MAGIC 3. See Delta superpowers: **history**, **time travel**, and safe **updates**

# COMMAND ----------

# Make sure our schema from notebook 00 is the active location.
CATALOG = "workspace"
SCHEMA  = "tcu_taxi"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")
spark.sql(f"USE CATALOG {CATALOG}")
spark.sql(f"USE SCHEMA {SCHEMA}")
print(f"Working in {CATALOG}.{SCHEMA}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Two ways to read the same data
# MAGIC
# MAGIC Databricks notebooks let you mix languages. Here's the **Python** way —
# MAGIC `spark.table(...)` gives you a DataFrame, and `display()` renders it nicely.

# COMMAND ----------

df = spark.table("samples.nyctaxi.trips")
print(f"The sample table has {df.count():,} rows and these columns: {df.columns}")
display(df.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC And here's the **SQL** way — same data, different language. Use whichever
# MAGIC feels natural; analysts often prefer SQL, engineers often prefer Python.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM samples.nyctaxi.trips LIMIT 5;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Save your first Delta table
# MAGIC
# MAGIC Right now the data lives in the read-only `samples` catalog. Let's make our
# MAGIC **own copy** as a Delta table we control. Writing a managed table is one line.

# COMMAND ----------

(
    spark.table("samples.nyctaxi.trips")
         .write
         .format("delta")           # Delta is the default, shown here to be explicit
         .mode("overwrite")         # replace the table if we run this again
         .saveAsTable("trips_raw")  # lands at workspace.tcu_taxi.trips_raw
)

print("✅ Created table: workspace.tcu_taxi.trips_raw")
display(spark.sql("SELECT COUNT(*) AS rows_saved FROM trips_raw"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Delta superpower #1 — every change is versioned
# MAGIC
# MAGIC Delta keeps a transaction log. `DESCRIBE HISTORY` shows every operation that
# MAGIC ever touched the table. Right now there's just one: our write.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY trips_raw;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Delta superpower #2 — safe UPDATE / DELETE (ACID)
# MAGIC
# MAGIC Classic data lakes can't reliably update a single row. Delta gives you
# MAGIC **ACID transactions** — real `UPDATE` and `DELETE`, just like a database.
# MAGIC
# MAGIC Some rows in this dataset have a `fare_amount` of 0 or less (bad data). Let's
# MAGIC see how many, then delete them.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) AS zero_or_negative_fares
# MAGIC FROM trips_raw
# MAGIC WHERE fare_amount <= 0;

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM trips_raw WHERE fare_amount <= 0;

# COMMAND ----------

# MAGIC %md
# MAGIC Look at the history again — notice a new **DELETE** version was added.

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY trips_raw;

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. Delta superpower #3 — time travel ⏳
# MAGIC
# MAGIC Because every version is kept, you can query the table **as it was before**
# MAGIC your delete. `VERSION AS OF 0` is the original write.

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   (SELECT COUNT(*) FROM trips_raw VERSION AS OF 0) AS rows_at_version_0,
# MAGIC   (SELECT COUNT(*) FROM trips_raw)                 AS rows_now;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ Recap
# MAGIC
# MAGIC - The **Lakehouse** stores open files but behaves like a reliable warehouse.
# MAGIC - **Delta Lake** gives you versioning, ACID `UPDATE`/`DELETE`, and time travel.
# MAGIC - **Unity Catalog** organized your table as `workspace.tcu_taxi.trips_raw`.
# MAGIC
# MAGIC 👉 **Next:** open **`02_Data_Engineering_Bronze_Silver`** to clean and shape this data.
