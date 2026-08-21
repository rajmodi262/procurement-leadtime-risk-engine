# Dashboard Mockups

**These are design mockups, not Power BI screen captures.**

Each PNG in this folder is rendered by [`src/render_procurement_dashboard.py`](../../src/render_procurement_dashboard.py)
using **matplotlib**. They are the target layout for the Power BI report — page
composition, KPI card hierarchy, colour semantics, and the drill path — produced
as images so the design could be reviewed before building it in Power BI Desktop.

They are not screenshots of a running report, and they do not read from the
DuckDB warehouse at runtime. The vendor scorecard and the PO sentry table in
particular use values typed into the render script, not query output, so the
layout renders deterministically at a fixed size.

**Every supplier shown is fictional.** No performance rating, delay prediction,
or spend figure in these images refers to a real company.

## What in this repository *is* real Power BI

| Artifact | What it is |
|---|---|
| [`../Procurement_Risk_Platform.pbit`](../Procurement_Risk_Platform.pbit) | A Power BI template (`.pbit`) that opens in Power BI Desktop |
| [`../Procurement_Project.pbip`](../Procurement_Project.pbip) | Power BI Project format — `model.bim` dataset plus report definition |
| [`../Procurement_DataModel.xlsx`](../Procurement_DataModel.xlsx) | Star-schema Excel model over 25,000 modeled POs, loadable via Power Query |

The `.pbit` currently carries a starter layout with four visual containers. It
does **not** yet reproduce the three-page design shown in these mockups —
building that out in Power BI Desktop is the open work item.

## Data

All figures are synthetic. See the Data Provenance section in the
[repository README](../../README.md).
