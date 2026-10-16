# Plant Pulse: Water Treatment Monitoring and Early Warnings

## 1. What we built

We built Plant Pulse, a prototype dashboard that helps water-treatment operators review unusual equipment readings and possible excess electricity use.

Plant Pulse brings historical trends, energy comparisons and data-quality findings into one place. It shows which plant and dates need review, with the readings behind each finding. Operators can use this evidence to decide what to investigate.

The prototype includes a reproducible data-cleaning and analysis workflow, a statistical energy monitor, and a dashboard with Overview, Historical trends, Energy review and Data quality views.

## 2. How it works

We analysed two anonymised plants. Each plant has 244 days of equipment readings, covering 1 January to 1 September 2026. A separate dataset provides 62 days of electricity, water-production and treatment-performance records per plant, covering July and August.

We converted blank, `NULL` and `/` markers to missing values. We checked dates, repeated readings, constant fields and equipment-counter decreases. Missing readings remain missing rather than becoming zero. The original files are preserved.

For energy monitoring, Plant Pulse estimates expected daily electricity from the amount of treated water produced. Each plant has its own July reference: total electricity divided by total treated-water volume. Multiplying this reference by today's water output gives expected electricity.

Plant Pulse compares recorded electricity with the estimate. A cumulative sum method, called CUSUM, accumulates evidence of electricity use above the reference. When the accumulated evidence exceeds a provisional limit, the system requests investigation. Missing, invalid or out-of-range inputs have an unavailable comparison and reset the accumulated evidence.

We compared this method with regression, which fits a relationship between production and electricity. July checks fitted each model using earlier dates and tested it on later dates. Regression had lower pooled July prediction error for both plants. We selected the simpler reference for transparency, rather than claiming it was the most accurate model.

The analysis uses Python, pandas, NumPy and Matplotlib in a reproducible notebook. The dashboard uses React, TypeScript, shadcn and Recharts. It displays saved results and does not require a live plant connection.

## 3. Results

The equipment review found:

- **21 adjacent repeated equipment records in Plant A and 10 in Plant B.** These require verification against collection and operating records.
- **183-day flat periods in both Plant A runtime counters**, followed by counter decreases. These counters cannot be used directly to calculate daily runtime.
- **Eight reported-versus-calculated recovery mismatches in Plant B.** These require reconciliation with source records and reporting rules.

An exploratory equipment comparison also identified an 11-day investigation period for Plant B's first RO pump, from 3 to 13 May. Its recorded response was approximately 14.1% above the historical expectation at the observed frequencies, measured as the median daily percentage difference. All 11 dates exceeded the existing retrospective review limit. We recommend checking the signal definition, aggregation and operating records for changes in settings, pump duty, maintenance or logging. The response signal's physical meaning and units remain unconfirmed, and plant electricity records do not cover May, so this finding does not establish a pump fault or energy loss. Operator verification remains pending.

We tested the energy monitor using constructed changes in electricity use. Each evaluation scenario used 400 simulated 31-day paths. The results below use three-day blocks resampled from centred July residuals, which are the differences between recorded and expected electricity. The sustained increase was an added daily amount equal to 10% of each plant's July mean daily electricity.

| Simulation measure | Plant A | Plant B |
| --- | ---: | ---: |
| Added sustained electricity, kWh/day, rounded | 485 | 2,066 |
| Sustained increase detected within 14 days | 95.25% | 100% |
| Median detection delay among detected paths | 6 days | 3 days |
| No-change paths that triggered at least one review | 6.75% | 7.5% |

These figures describe performance under the simulation assumptions. They are not real equipment-failure detection accuracy or measured site false-alarm rates. Parameters were selected using separate simulations from the same short July history, so the evaluation does not provide independent plant validation.

The August historical replay produced no energy-review events on the 26 eligible dates for Plant A and 30 eligible dates for Plant B. Five Plant A dates and one Plant B date were unavailable for comparison. No review event does not establish healthy or efficient operation.

The prototype makes the findings available in a dashboard with supporting readings. Energy savings and operator time savings have not yet been measured.

## 4. Limitations and next steps

The data contain no verified failure labels, confirmed healthy baseline or complete maintenance records. Some equipment meanings, units and daily aggregation methods remain uncertain. Daily readings can miss short events, and two months of performance data cannot establish seasonal behaviour.

The energy monitor works at plant level. It cannot diagnose a pump fault or establish hydraulic efficiency without confirmed equipment measurements and mappings. A review event can also follow an isolated spike, so it does not confirm sustained degradation. Water-quality acceptance limits are absent, which prevents compliance conclusions.

August had already been inspected, so its replay is exploratory rather than an independent test. The dashboard uses saved data; live monitoring and automatic control are outside the current prototype.

Our next steps are to:

1. Confirm sensor meanings, units and aggregation with operators, and resolve the data-quality findings.
2. Collect dated maintenance and operating events, confirmed pump measurements, and a longer history of production, energy and water quality.
3. Agree the reference period, target change, acceptable review workload and alert-reset policy with operators.
4. Evaluate the monitor on fresh data during a supervised pilot. Measure confirmed-event detection, review workload, investigation time and any verified resource savings before considering live integration.
