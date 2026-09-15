# 🚕 TCU × Databricks Workshop

A hands-on, beginner-friendly (L100) introduction to the Databricks Data
Intelligence Platform, built around the **NYC taxi** dataset. You'll go from raw
data to a **star schema**, an **AI/BI dashboard**, a **Genie** natural-language
space, and a small **Databricks App** — all on **Databricks Free Edition**.

> **Workshop date:** September 19 · Texas Christian University
> **Instructor:** Sameep Mohta, Delivery Solutions Architect, Databricks

---

## ✅ Before you arrive

1. **Create a free Databricks account** (5 minutes) at
   [Databricks Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition).
   Complete the sign-up so you're ready to go on workshop day.
2. Bring a laptop with a modern browser. Everything runs in the browser — nothing
   to install.

## 🚀 Getting the notebooks (during the lab)

Your instructor will walk you through this, but in short:

1. In Databricks, open **Workspace** in the left sidebar.
2. Click your username → **Create → Git folder** (or **Repos → Add**).
3. Paste this repository's URL and click **Create**:
   ```
   https://github.com/sameep08/dbx-tcu-workshop
   ```
   All the notebooks appear in your workspace.
4. Open the **`notebooks/`** folder and start with **`00_Start_Here`**.

## 📚 What you'll build

| # | Notebook | Topic |
|---|----------|-------|
| 00 | `00_Start_Here` | Set up your schema, meet the data |
| 01 | `01_Lakehouse_and_Delta` | Lakehouse & Delta Lake (ACID, time travel) |
| 02 | `02_Data_Engineering_Bronze_Silver` | Clean & transform (medallion) |
| 03 | `03_Star_Schema_Gold` | Build a Gold **star schema** |
| 04 | `04_Dashboard_and_Genie` | AI/BI dashboard + natural-language Genie |
| 05 | `05_Databricks_App` | A live data app on your tables |

Run them **in order** — each notebook builds on the tables from the previous one.

## 🗂 Repo layout

```
dbx_tcu_workshop/
├── notebooks/     # the 6 workshop notebooks (run in order)
├── app/           # the Streamlit Databricks App (notebook 05)
└── INSTRUCTOR_GUIDE.md
```

## 💡 Good to know

- **No cluster setup** — Free Edition uses serverless. Just press **Shift + Enter**.
- Everything lands in **`workspace.tcu_taxi`**, your own schema, so it stays tidy.
- Notebooks are safe to re-run — they recreate tables cleanly.

---

*Adapted for TCU from Josh Melton's
[databricks-crash-course](https://github.com/josh-melton-db/databricks-crash-course).*
