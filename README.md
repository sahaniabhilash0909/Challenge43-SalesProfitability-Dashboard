# Challenge 43 — Holiday P&L & Discount Effectiveness Dashboard

Power BI Project (PBIP) entry for **FP20 Analytics & ZoomCharts Challenge 43**, styled with the **Slate-Coral Editorial Boardroom Analytics** design system (V11).

## Overview

- **Scope:** Three October–January holiday seasons (`2023/24`, `2024/25`, `2025/26`) across 8 European city markets (`7,735` sales lines / `5,406` orders), comparing Actual (`AC`) vs. Prior Year (`PY`) on contribution profit, margin, discounting, and returns.
- **Architecture:** Pure `#FFFFFF` zero-shadow editorial sheet over `#F2F3F5` outer mat, asymmetric `34.5% / 65.5%` executive rail + analytical canvas split, and two-hue semantic discipline:
  - **Blue Slate (`#4F5D75`)**: AC bars, favorable variances, positive bridge lifts, primary actions.
  - **Silver-Grey (`#8B909E` / `#B5BECC`)**: PY reference lines, PY bars, historical context.
  - **Coral Glow (`#EF8354`) / Burnt Coral (`#BA4B1D`)**: Margin erosion, adverse variances, and `15%+` return alerts.

## Report Structure

- **`1 · What happened & why` (`p1_what_why`)**: Thesis headline, inline `Season` & `Channel` segmented controls, 5 hairline-stacked KPI rows with Oct–Jan sparklines/variance bars, horizontal P&L Contribution Bridge, and **3 ZoomCharts visuals** (Monthly Contribution Combo, Discount Depth Combo, Campaign Scorecard Combo Bar).
- **`2 · Where it leaks` (`p2_leaks`)**: 5 leak KPIs, Category × Campaign Type Returns Heatmap, and **4 ZoomCharts visuals** (Products 3-level Combo Bar, Segments › Channels Donut, Markets Scatter, Channel › Category Combo Bar).
- **`3 · What to do` (`p3_actions`)**: Dashed projected-upside callout, Upside by Move bar chart, analytical limitations, and `ACT-01`–`ACT-04` recommendation rails with deep-links back to Chapters 1–2.
- **`Campaign profile` (`p4_campaign_profile`, drill-through)**: Campaign Event Facts, 4-column P&L bar table, and **2 ZoomCharts visuals** (Daily Net Sales Combo, Discount Depth Combo).
- **`Snapshot tooltip` (`tt_snapshot`)** + slide-over **`Filters` / `Guide` / `Notes`** drawers via 20 PBIR bookmarks.

## Repository Contents

- `Challenge43_SalesProfitability.pbip` — Power BI Project entry point
- `Challenge43_SalesProfitability.Report/` — PBIR page, visual, bookmark, theme, and 2× retina background definitions
- `Challenge43_SalesProfitability.SemanticModel/` — TMDL semantic model, calculation groups, and DAX measures
- `_build/src_v11/` — Python PBIR generator, Playwright Chromium SVG-to-PNG rasterizer, and model palette patcher
- `_build/merge_zc_license.py` — Helper script to merge a local ZoomCharts license into `HolidayPnL_C43_Theme.json`

## ZoomCharts License Note

The public repository intentionally excludes ZoomCharts trial/paid license keys from `Challenge43_SalesProfitability.Report/StaticResources/RegisteredResources/HolidayPnL_C43_Theme.json`. To apply your own license locally before opening in Power BI Desktop or exporting `.pbix`, place your license block in `_build/private/zc_license_theme.json` and run:

```powershell
python _build\merge_zc_license.py
```
