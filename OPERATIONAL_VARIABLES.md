# Relevant operational variables

The variables below exist in the supplied data and are relevant to energy use, water production, treatment quality or equipment operation. Equipment names use the aliases in [the focused field dictionary](Dataset/plant_daily_unified_dictionary.csv), which maps them to original source columns.

| Available variable | Dataset field | Why it matters | Interpretation limitation |
| --- | --- | --- | --- |
| Daily electricity | `daily_electricity_kwh` | Measures energy consumption; interpret alongside water production. | Whole-plant total, not individual pump consumption. |
| Treated-water volume | `effluent_volume_m3` | Measures treatment output and provides context for resource consumption. | Daily plant volume, not instantaneous or per-pump flow. |
| Incoming-water volume | `influent_volume_m3` | Helps assess how much incoming water becomes treated output. | Whole-plant boundary, not an identified RO-stage feed. |
| Treated-water conductivity | `effluent_conductivity_us_cm` | Tracks changes in dissolved-salt content as a water-quality indicator. | Some readings are missing; acceptance limits are absent. It does not identify a membrane fault. |
| Treated-water pH | `effluent_ph` | Tracks treated-water chemistry. | Acceptance limits are absent; a stable pH does not establish overall treatment quality. |
| Frequency-labelled pump readings | `pump*_frequency` | Candidate operating-condition variable for comparing equipment readings. | Units, scaling and daily aggregation require confirmation; zero alone does not prove an off state. |
| Plant A power-labelled readings | `pump1_power_reading`, `pump2_power_reading` | Candidate indicator of electrical demand alongside operating conditions. | Meaning and scale remain provisional; these readings cannot establish pump efficiency without mapped flow and pressure. |
| Actual chemical dosing | `actual_*_dose_reported` in the performance file | Candidate indicator of chemical use relative to treatment output. | Sparse records and ambiguous dose units/definitions prevent reliable interpretation at present. |

Assess efficiency together with production and water quality. Reduced consumption alone does not establish improved performance.

Plant B `a_out` is excluded from the selected physical indicators because its meaning is unconfirmed. Pressure, temperature and per-pump flow are not selected without confirmed definitions and instrument mappings. Runtime counters support data-quality checks rather than a direct efficiency measurement.

Dataset coverage, calculations and observed normal/abnormal patterns belong in [HISTORICAL_ANALYSIS.md](HISTORICAL_ANALYSIS.md). The detection target, proposed method and evaluation belong in [DETECTION_APPROACH.md](DETECTION_APPROACH.md); operational alerts follow detector validation.

Sources: [DOE pump assessment guidance](https://www.energy.gov/sites/default/files/2014/05/f16/pump.pdf), [DuPont RO technical manual](https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/RO-NF-FilmTec-Manual-45-D01504-en.pdf), and [DuPont UF process manual](https://www.dupont.com/content/dam/water/amer/us/en/water/public/documents/en/UF-IntegraTec-P-Series-PVDF-OI-Process-Design-Manual-45-D00874-en.pdf).
