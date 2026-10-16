# BlueNexus x Hack&Hire

## Confidentiality and dataset identity
The datasets refer only to **Plant A** and **Plant B**. Actual plant names, client names, project locations and raw source-tag mappings are intentionally excluded. Please do not attempt to identify the original plants, and do not publish or redistribute the dataset without permission.

## Files
- `plant_A_equipment_daily.csv`: anonymized plant A equipment telemetry; original observations preserved.
- `plant_B_equipment_daily.csv`: anonymized plant B equipment telemetry; original observations preserved.
- `plant_daily_performance.csv`: daily production/consumption metrics with `plant` equal to `Plant A` or `Plant B`.
- `data_dictionary.xlsx`: English column definitions, tentative units and missingness notes. Original PLC/OPC source-code identifiers are excluded.

## Data alignment
Join data using the same plant identifier and `date`. The equipment data contain 244 daily records per plant. Daily plant-performance data contain 62 records per plant over the shared period.

Run All in `data_review.ipynb` to regenerate the main `Dataset/plant_daily_unified.csv` and its matching `Dataset/plant_daily_unified_dictionary.csv`. The focused table has **488 rows and 22 columns**, one row per plant and date. It keeps frequency, response and cumulative runtime for each of the six RO pumps, plus electricity, effluent volume, reported specific energy, reported recovery, effluent pH and conductivity. Equipment names are shortened; the matching dictionary maps each back to its exact source column. Plant A power-labelled readings and Plant B `a_out` readings remain separate. Shared frequency/runtime names indicate roles, not confirmed units or cross-plant comparability. Runtime remains cumulative, not daily runtime.

All other signals are retained in the original files and in `output/plant_daily_full.csv`, with `output/plant_daily_full_dictionary.csv`. Dates use `YYYY-MM-DD`; blank, `NULL` and `/` markers become missing values, never zeros. Plant A has no supplied pumps 3–4, and performance outside July–August stays blank. Repeats, outliers, constants and counter decreases remain for investigation. The original dictionary guides provisional meanings and units; the focused dictionary guides the selected fields and their source mappings. Originals are unchanged; generated exports carry the same confidentiality restrictions.

## Deliberately not cleaned
- Missing values and literal `NULL` markers, duplicated measurements, outliers, constant-value fields, counter resets and questionable readings are retained.
- Field interpretations and physical units are provisional unless verified. Some chemical fields display conflicting labels and units; do not assume reported dosing values are kilograms.
- Blank cached formula results in the source are not automatically zeros.

## Operational Data Analytics Challenge
Explore normal/abnormal operation and early indicators of possible inefficiency; supply reproducible cleaning and analysis, relevant indicators and a useful visualization. There are **no verified equipment-failure labels**.

## Scope and restrictions
A seven-day prototype challenge, daily time resolution. Findings must not be used for operational control or formal ESG reporting without independent validation. The filenames and visible identifiers are pseudonymized; this does not guarantee immunity from re-identification based on unusual operational patterns or dates.
