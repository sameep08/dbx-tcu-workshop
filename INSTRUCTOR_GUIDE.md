# Instructor Guide — TCU × Databricks Workshop

Companion to the workshop deck (*Technical Introduction*) and the September 19
agenda. Notebooks are **L100**, run on **Free Edition serverless**, and use the
built-in `samples.nyctaxi.trips` dataset. Target: up to 45 students, follow-along.

## Agenda → notebook mapping

| Agenda slot | Deck section | Notebook(s) |
|---|---|---|
| 9:15–10:15 · Module 1: Lakehouse Foundations | Lakehouse, Delta, Unity Catalog | Demo `00_Start_Here`, `01_Lakehouse_and_Delta` |
| 10:30–12:00 · Module 2: AI, BI & App Dev | Notebooks, AI/BI, Genie, apps | Walk through `04` and `05` conceptually |
| 1:00–1:15 · Hands-On Lab Setup | — | Students clone the Git folder, open `00_Start_Here` |
| 1:15–2:15 · Lab: Data & AI | Data engineering, Genie | `01` → `02` → `03`, then intro Genie in `04` |
| 2:30–3:30 · Lab: Dashboards & Apps | AI/BI dashboards, apps | `04` (dashboard + Genie), `05` (app) |
| 3:45–4:00 · Wrap-Up | — | The "big picture" recap at the end of `05` |

## Pre-flight checklist (instructor, day-of)

- [ ] Confirm `samples.nyctaxi.trips` is readable (run notebook `00`).
- [ ] Pre-run notebooks `00`–`03` in your own workspace so the demo app in `05`
      has tables to read.
- [ ] Deploy the `app/` Streamlit app ahead of time and have its URL handy.
- [ ] Have the Git-folder clone URL on a slide for students.

## Focus areas (per Sameep's request)

- **Data engineering** — medallion Bronze/Silver in `02`.
- **Star schema** — fact + dimensions in `03` (the centerpiece).
- **Apps** — guided lightweight Streamlit app in `05` / `app/`.

## Common gotchas on Free Edition

- Everything is serverless — no cluster to start; first cell may take ~10s to warm.
- Each student's own account has its own `workspace` catalog, so there are no
  naming collisions between students.
- If a student re-runs out of order, notebooks `01`–`03` each `USE` the schema and
  recreate their tables, so re-running `00`→`03` in order fixes most issues.
