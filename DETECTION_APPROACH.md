# Early-detection target and approach

## Target and provisional choice

Screen for sustained plant electricity above an output-adjusted reference using `daily_electricity_kwh` and `effluent_volume_m3`. This is a plant-level investigation target, not pump diagnosis or a verified efficiency measurement.

Use **fixed specific energy + positive CUSUM** as the simplest transparent prototype reference for both plants. Regression remains a tested alternative. This choice is an exploratory judgement, not a proven prediction winner: regression has lower pooled July error; Plant A's individual July folds disagree, while Plant B's regression performs much worse in the already-inspected August replay. Neither reference establishes healthy operation or seasonal adequacy.

## Baseline comparison

Chronological July splits train 1–14 July / test 15–21 July, then train 1–21 July / test 22–31 July. Both methods use identical eligible dates, with no future readings used for fitting. Pooled RMSE uses summed squared errors across comparable predictions. August has already been examined and is an **exploratory replay**, not a fresh independent test.

| Plant / period | Comparable days | Regression RMSE, kWh/day | Fixed specific-energy RMSE, kWh/day |
| --- | --- | --- | --- |
| A / July chronological checks | 17/17 | 557 | 597 |
| B / July chronological checks | 14/17 | 774 | 838 |
| A / August exploratory replay | 26/31 | 760 | 772 |
| B / August exploratory replay | 30/31 | 1,292 | 871 |

There were zero August CUSUM review events for either candidate on eligible dates. This does not prove normal or efficient operation. [Individual July splits](output/detection/energy_chronological_comparison.csv), [pooled errors](output/detection/energy_chronological_pooled.csv), and [both August candidates](output/detection/energy_candidate_replay_summary.csv) preserve the comparison, including results favouring regression.

## Indicators and prototype review limits

1. **Daily specific energy:** `electricity / treated-water output`, in kWh/m³. Show output alongside it; low production can increase the ratio without high electricity consumption.
2. **Expected electricity:** `c × today's output`, where `c = total July electricity / total July output`. This volume-weighted reference is not the mean of daily ratios or a zero-intercept least-squares fit.
3. **Daily excess:** `recorded − expected electricity`, in kWh/day. Divide by the July residual MAD scale, `1.4826 × median(abs(residual − median(residual)))`, to obtain a dimensionless score. The factor does not prove normality.
4. **Accumulated positive evidence:** `C_t = max(0, C_(t−1) + score_t − k)`. Request investigation when `C_t > h`; equality does not cross the limit.
5. **Comparison status:** eligible or unavailable, with the exclusion reason. Require finite paired inputs, positive output, nonnegative electricity and output inside the reference range.

| Plant | Reference c, kWh/m³ | Residual scale, kWh/day | Allowance k | Review above CUSUM h | Reference output range, m³/day |
| --- | --- | --- | --- | --- | --- |
| A | 1.1663 | 738.0 | 0.25 | 3 | 2,589–5,443 |
| B | 1.0785 | 381.5 | 1 | 12 | 15,591–20,808 |

These are **provisional investigation thresholds**, not physical safety limits. Missing, invalid and out-of-range readings remain unavailable and reset evidence; a calendar gap also resets it. Restart on the next day after a crossing in this prototype, so an unresolved change can generate repeated review events. Operator acknowledgement and reset policy remain to be agreed.

## Detection and workload checks

July-only parameter selection compares 12 `(k,h)` combinations on 300 constructed 31-day paths per candidate. It resamples non-circular three-day blocks of centred July residuals. The demonstration workload budget is at most 10% of no-change paths with a review; within that budget, prefer detection within 14 days of an added daily kWh amount equal to 10% of July mean electricity. Both models receive the same physical increase at a plant. This target and workload budget require operator agreement.

Evaluation uses 400 newly seeded paths per candidate/scenario, still drawn from the same July source. These are conditional simulations, not independent plant observations or real degradation labels.

| Selected reference | Added sustained kWh/day | Detected within 14 days | Median delay among detected paths | No-change paths with review, 3-day blocks | No-change paths with review, 7-day blocks |
| --- | --- | --- | --- | --- | --- |
| A / fixed specific energy | 485 | 95.25% | 6 days | 6.75% | 0.5% |
| B / fixed specific energy | 2,066 | 100% | 3 days | 7.5% | 2.5% |

The same limits were checked with seven-day residual blocks. Plant B regression's simulated no-change review fraction increased from 9.5% to 19.75%, while the selected fixed reference stayed below the demonstration budget in these checks. These results illustrate dependence sensitivity; they are not site false-alarm rates or guarantees.

Also tested gradual increases, isolated spikes, three-day interruptions and the earlier positive three-day rule. An isolated 20%-of-July-mean spike produced reviews in 24.25% of A paths and 32.5% of B paths, so a crossing cannot establish sustained degradation. A three-day interruption reduced A's sustained-increase detection within 14 days to 77.25%. Short residual histories and blocks do not capture seasonality, model-fitting uncertainty or all dependence. [Parameter sensitivity](output/detection/energy_parameter_sensitivity.csv) and [all constructed checks](output/detection/energy_simulation_checks.csv).

## Operator interpretation and implementation

Suggested review wording: **“Electricity above the production-adjusted reference; check readings, loading, treatment settings and operating records.”** Show plant/date, supporting dates, output, actual and expected kWh, daily excess, CUSUM and comparison status. Reduced energy use alone does not establish improved treatment performance; water-quality readings provide context without supplied acceptance limits. Do not automatically change operating settings.

The [notebook](data_review.ipynb) and [shared functions](detection_rules.py) implement both baselines, CUSUM, chronological comparisons and simulations. Tests check known coefficients/scale, the volume-weighted ratio, invalid references, exclusions, strict crossings, resets, simulation denominators and future-data independence. [Selected model parameters](output/detection/energy_models.csv), [selected August replay](output/detection/energy_replay.csv), and [review evidence](output/detection/energy_warning_evidence.csv) are reproducible exports; the last currently contains a header and no review rows.

Before operator use, agree the reference, target shift, acceptable review workload and reset policy; check warnings against dated operating/maintenance records and fresh data. Daily records cannot establish intraday detection. There are no verified fault labels, confirmed healthy baseline or complete maintenance history, so actual degradation accuracy, failure lead time and attributable savings remain unverified.

The older frequency/response experiment remains inspectable, including its tests and CSVs; it is not the chosen physical target. `a_out` remains unconfirmed. Plant-level screening cannot replace confirmed equipment measurements for the organiser's pump-specific focus. Historical findings remain in [HISTORICAL_ANALYSIS.md](HISTORICAL_ANALYSIS.md).

## Research basis

| Source | What it supports | Applicability limit |
| --- | --- | --- |
| [DOE energy baselining guidance](https://www.energy.gov/sites/prod/files/2015/01/f19/Energy%20Intensity%20Baselining%20and%20Tracking%20Guidance.pdf) | Regression-based energy baselines adjusted for production and other relevant variables, with technical and statistical model checks. | General industrial guidance, not validation of water volume as our only predictor. Its 12-month baseline is a Better Plants annual-reporting requirement; our two-month dataset supports a limited pilot, not a seasonal baseline. |
| [Firdaus and Samat, 2024 water-treatment case study](https://iopscience.iop.org/article/10.1088/1755-1315/1386/1/012024) | Direct precedent for production-based electricity regression and CUSUM of recorded-minus-predicted energy in water-treatment equipment. | Conference case study at another plant; it does not validate our data, thresholds or fault accuracy. |
| [Lee, Fu and Lai, 2024 water-purification baseline study](https://www.cell.com/heliyon/fulltext/S2405-8440(24)10012-6) | Energy-baseline modelling for four water-purification plants using water quantities and weather data. | Different plants and multiple predictors; output-only regression must still be evaluated here. |
| [NIST CUSUM guidance](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc323.htm) | Cumulative monitoring for small sustained mean shifts, with explicit allowance and decision-limit design. | Standard design properties depend on the reference and statistical assumptions; our MAD-scaled residuals require calibration. |
| [NIST residual diagnostics](https://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm) and [autocorrelated-process research](https://www.nist.gov/publications/comparisons-control-charts-autocorrelated-data) | Check model adequacy and time dependence before applying residual monitoring. | Consecutive daily readings cannot be assumed independent. |
| [NIST control-chart rules](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm) and [SciPy MAD documentation](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.median_abs_deviation.html) | Clarify standard run rules and the robust scale's normal-consistency factor. | They do not establish a false-alarm rate for our former two-scale/three-day heuristic. |

Research supports the baseline-plus-residual-monitoring architecture. The chosen predictor, reference period, CUSUM parameters and missing-data policy remain prototype decisions to evaluate on the supplied data. This is not a claim of ISO compliance or validated degradation detection.
