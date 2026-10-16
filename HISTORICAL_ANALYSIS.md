# Historical operating patterns

The question is what was commonly observed and which dates depart from that history. Reference-consistent readings are not verified healthy operation; unusual readings are investigation cases, not confirmed faults.

## Data and calculations

Equipment history covers 244 daily dates per plant, 1 January-1 September 2026. Plant A has two supplied RO pumps and Plant B has four. Interpretable plant-performance records cover 62 dates per plant, 1 July-31 August. All 124 plant/date keys are unique; comparisons and ratios use matching plant/date records.

| Available input | Source field | Use |
| --- | --- | --- |
| Daily electricity | `daily_electricity_kwh` | Energy consumption |
| Treated-water volume | `effluent_volume_m3` | Production and energy per unit of output |
| Incoming-water volume | `influent_volume_m3` | Plant water recovery |
| Treated-water conductivity | `effluent_conductivity_us_cm` | Water-quality trends |
| Treated-water pH | `effluent_ph` | Water-chemistry trends |

- Daily specific energy = electricity / treated-water volume, in kWh/m³.
- Daily plant recovery = treated-water volume / incoming-water volume × 100, in %.
- Period specific energy = total electricity / total treated-water volume over the same eligible dates. Do not average daily ratios for this period result.

Use paired finite readings and positive denominator volumes. Plant quantities cannot establish an individual pump's efficiency or RO-stage recovery. Electricity, both volumes and pH are complete; Plant A has eight missing conductivity readings. Chemical records remain too sparse and insufficiently defined for reliable dosing comparisons.

## Commonly observed patterns

The median and middle 50% (lower to upper quartile) describe each plant's supplied July-August history. They are descriptive ranges, not physical operating limits. A value outside the middle 50% alone is not classified as abnormal.

| Plant | Indicator | Valid days | Median | Lower quartile | Upper quartile |
| --- | --- | --- | --- | --- | --- |
| Plant A | Specific energy (kWh/m³) | 62 | 1.145 | 1.023 | 1.259 |
| Plant A | Plant recovery (%) | 62 | 75.000 | 75.000 | 75.000 |
| Plant A | Treated-water pH | 62 | 6.700 | 6.630 | 6.850 |
| Plant A | Conductivity (µS/cm) | 54 | 96.500 | 82.750 | 115.750 |
| Plant B | Specific energy (kWh/m³) | 62 | 1.071 | 1.035 | 1.089 |
| Plant B | Plant recovery (%) | 62 | 75.234 | 74.410 | 75.720 |
| Plant B | Treated-water pH | 62 | 7.000 | 6.800 | 7.275 |
| Plant B | Conductivity (µS/cm) | 62 | 100.000 | 77.250 | 114.500 |

Plant A's calculated recovery remains effectively 75% throughout. This agrees with the reported value but does not establish independent variation or validated process performance. Monthly median pH is 6.7 for Plant A and 7.0 for Plant B in both months; individual spikes still occur.

### Energy and production changed together

| Plant | Month | Days | Electricity (kWh) | Treated water (m³) | Specific energy (kWh/m³) |
| --- | --- | --- | --- | --- | --- |
| Plant A | 2026-07 | 31 | 150336 | 128903 | 1.166 |
| Plant A | 2026-08 | 31 | 126221 | 114855 | 1.099 |
| Plant B | 2026-07 | 31 | 640361 | 593727 | 1.079 |
| Plant B | 2026-08 | 31 | 589016 | 563234 | 1.046 |

| Plant | Electricity change % | Production change % | Specific energy change % |
| --- | --- | --- | --- |
| Plant A | -16.0% | -10.9% | -5.8% |
| Plant B | -8.0% | -5.1% | -3.0% |

August specific energy is lower than July by 5.8% in Plant A and 3.0% in Plant B. Electricity falls more than production in both plants. This explains the ratio change mathematically; its operational cause and any attributable savings are unverified. Conductivity medians change from 105 to 80 µS/cm in Plant A and from 98 to 106 µS/cm in Plant B. Missing values and unknown quality limits prevent a conclusion that treatment quality improved or remained acceptable.

![Actual plant energy and production history](output/historical/plant_energy_history.png)

## Unusual plant readings to investigate

Use strict retrospective fences below Q1 − 1.5 × IQR or above Q3 + 1.5 × IQR, calculated separately for each plant and indicator from all available July-August dates. Missing values are excluded. An effectively constant IQR has no usable outlier screen. These full-history fences describe this dataset and must not be presented as prospective early-warning thresholds.

### High electricity per unit of water

| Plant | Date | Electricity (kWh) | Treated water (m³) | Specific energy (kWh/m³) |
| --- | --- | --- | --- | --- |
| Plant A | 2026-07-01 | 4261 | 2589 | 1.646 |
| Plant A | 2026-08-05 | 3062 | 1797 | 1.704 |
| Plant A | 2026-08-13 | 2701 | 1531 | 1.764 |
| Plant A | 2026-08-31 | 3660 | 1881 | 1.946 |
| Plant B | 2026-07-16 | 20389 | 15591 | 1.308 |

Upper historical fences are 1.613 kWh/m³ for Plant A and 1.170 for Plant B. The highest Plant A case is 31 August: 3,660 kWh / 1,881 m³ = 1.946 kWh/m³. Its absolute electricity use is below Plant A's daily median, while output is also below the median. Review low production and operating conditions before attributing the high ratio to increased equipment consumption.

### Low electricity per unit of water

| Plant | Date | Specific energy (kWh/m³) |
| --- | --- | --- |
| Plant B | 2026-07-15 | 0.953 |
| Plant B | 2026-08-07 | 0.945 |

The Plant B lower fence is 0.954 kWh/m³. These two small lower-end departures do not establish improved efficiency. Check water output and quality together; the 15 July record also has unusual recovery and conductivity.

### Recovery, pH and conductivity

| Plant | date | Indicator | Value | Unit |
| --- | --- | --- | --- | --- |
| Plant A | 2026-07-03 | Treated-water pH | 7.250 | pH |
| Plant A | 2026-07-27 | Conductivity | 282.000 | µS/cm |
| Plant A | 2026-08-03 | Treated-water pH | 7.250 | pH |
| Plant B | 2026-07-15 | Plant recovery | 87.506 | % |
| Plant B | 2026-07-15 | Conductivity | 183.000 | µS/cm |
| Plant B | 2026-07-16 | Plant recovery | 63.075 | % |
| Plant B | 2026-08-19 | Treated-water pH | 8.800 | pH |
| Plant B | 2026-08-26 | Treated-water pH | 8.500 | pH |

Plant B's 15 July record combines unusually high calculated recovery (87.506%) with high conductivity (183 µS/cm). On 16 July, recovery is unusually low (63.075%) and specific energy is high (1.308 kWh/m³). This date alignment warrants checking source records and operating conditions; it does not establish a causal link.

Verify the pH spikes and conductivity spikes against instrument records and site limits. Statistical unusualness does not establish a water-quality violation.

![Actual plant recovery and quality history](output/historical/plant_quality_history.png)

## Data-quality findings

- Plant A has 21 adjacent full-equipment-reading repeats; Plant B has 10. They may be legitimate repeated operation or collection problems and need verification.
- Both Plant A runtime counters have a 183-day identical period and decrease on 3 July. Do not interpret negative counter differences as consumption or operating hours.
- Plant A has positive power-labelled readings on its zero-frequency dates. Check signal definitions, timing and aggregation; neither reading alone establishes an off/on state.
- Plant B has eight reported-versus-calculated recovery differences on 28-31 July and 28-31 August. Keep these reconciliation cases separate from the two recovery outliers above; rounding or reporting rules need clarification.
- Missing Plant A conductivity remains unavailable, not zero.

## Existing equipment patterns: exploratory only

The previous analysis uses frequency-labelled readings against Plant A power-labelled readings and Plant B `a_out`. Their source mappings are in `Dataset/plant_daily_unified_dictionary.csv`; physical meanings, scales and aggregation remain provisional. `a_out` is not a selected physical efficiency indicator. These results document the existing experiment rather than validate it as an operational degradation detector.

Fit a separate least-squares line `a + b × frequency` from each pump's first 90 calendar days, using finite positive-frequency pairs without adjacent full-row repeats. At least 30 pairs and three distinct frequency readings are required; the supplied histories have 67-86 training pairs. Set `c` to the median training residual and `s` to 1.4826 times the residual median absolute deviation. Expected response is `a + b × frequency + c`; comparison score is `(response − expected) / s`.

The supplied reference covers 1 January-31 March; later evaluation covers 1 April-1 September. Missing/invalid pairs, repeated rows, nonpositive frequency, out-of-range frequency and unusable residual scales have unavailable comparisons. The fixed reference is historical, not verified healthy operation; frequency alone does not account for flow, pressure, feed conditions or loading.

| Plant | Pump | Comparable later days | No review flag | Review days | Outside frequency range |
| --- | --- | --- | --- | --- | --- |
| Plant A | RO pump 1 | 104 | 104 | 0 | 1 |
| Plant A | RO pump 2 | 95 | 94 | 1 | 1 |
| Plant B | RO pump 1 | 97 | 63 | 34 | 40 |
| Plant B | RO pump 2 | 10 | 10 | 0 | 113 |
| Plant B | RO pump 3 | 131 | 124 | 7 | 0 |
| Plant B | RO pump 4 | 10 | 10 | 0 | 128 |

There are 447 comparable later pump-dates and 42 single-day review dates under the existing absolute score > 3.5 rule. Plant B pump 1's longest contiguous review period is 3-13 May (11 dates), with a median response difference of 14.1% above expected. No plant-performance records overlap that May case, so an energy effect cannot be established. Plant B pumps 2 and 4 each permit comparison on only 10 of 154 later dates (6.5%); unavailable comparisons do not establish stable operation.

See [DETECTION_APPROACH.md](DETECTION_APPROACH.md) for the chosen detection target, proposed method and status of the existing experiment. This historical report does not implement a replacement detector or operational alarm thresholds.

## Evidence and checks

Reproduce the analysis by running [data_review.ipynb](data_review.ipynb) top-to-bottom with the project Python environment. Inputs are the original equipment CSVs, plant-performance CSV and dictionary in `Dataset/`; source-file SHA-256 hashes are checked before and after execution.

Inspect the exported [indicator ranges](output/historical/plant_indicator_profile.csv), [unusual plant readings](output/historical/unusual_plant_readings.csv), [recovery reconciliation](output/historical/recovery_reconciliation.csv), [monthly totals](output/historical/plant_months.csv), [monthly changes](output/historical/plant_month_changes.csv), [high-energy dates](output/historical/high_specific_energy_dates.csv), and [equipment summary](output/historical/pump_summary.csv).

Checks cover unique daily keys, finite ratio inputs, positive denominators, missing-versus-zero handling, strict outlier fences, constant recovery, monthly ratio reconciliation and equipment-day categories. No verified fault labels, maintenance history or site quality limits are supplied; the findings support investigation rather than confirmed degradation or compliance conclusions.
