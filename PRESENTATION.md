# Plant Pulse presentation script

Audience: BlueNexus team. Team slot: 10 minutes, including questions.

Target: **eight minutes of presentation and approximately two minutes for questions**. This script follows the live deck inspected on 16 October 2026. It tells one continuous story: available data, a Plant A investigation in the dashboard, a brief Plant B view, comparison coverage, the monitoring method, observed results, constructed tests and the proposed pilot.

Deck: [Plant Pulse](https://docs.google.com/presentation/d/1mwT12h-GhOn_o8MrpagHtgtZePwIYAiui1KtRn6dsW0/edit).

## Slide handling

- **Slides 6–7 are one Plant A walkthrough.** Begin with the top of the readings panel, then advance to its lower portion while continuing the same explanation. Do not restart the story or read every daily value.
- **Slides 8–9 are one brief Plant B walkthrough.** Show that the same reading/comparison layout works for Plant B. Advance through both screenshots in about 15 seconds; no second case study is needed.
- **Current slide 13 is superseded.** The live deck still contains the older mixed observed-history/constructed-warning layout. Skip it during delivery. Current slides 14 and 15 are the replacement constructed example and simulation summary. This document uses the current physical slide numbers; if the older slide is removed, the final three numbers shift down by one.
- Dashboard slides still share the visible title “Dashboard.” The descriptive labels below identify the screenshot stage, rather than claim those slide titles have already changed.
- Main-slide notes use short bullet-point prompts. Bold text highlights key numbers and actions. Expand the cues naturally; use the [Q&A](QNA.md) for technical backup.

### Slide 1 — Plant Pulse

**0:00–0:20 · 20 seconds.** Establish the purpose, then move to the data.

- Purpose: help water-treatment operators investigate unusual operation.
- Built: equipment/performance analysis, statistical electricity monitor and dashboard.
- Story: one investigation, how monitoring works, and what testing shows.

### Slide 2 — Equipment data quality shaped my approach

**0:20–1:05 · 45 seconds.** Point to coverage, repeated records and runtime counters.

- History per plant: **244 equipment days**; **62 performance days**, July–August.
- Findings: **21 repeated records in A / 10 in B**; **183-day flat periods** in both A runtime counters. Verify against source records.
- Cleaning: preserve originals; keep missing values missing.
- Scope: equipment meanings remain uncertain; selected monitor uses clearer **plant-level electricity and output**.
- **Next:** show how an operator inspects the results.

### Slide 3 — Dashboard: Overview

**1:05–1:30 · 25 seconds.** Point to summaries and actual-versus-expected plots.

- Electricity, treated-water output, plant summaries and review counts together.
- Plots: actual electricity against an estimate adjusted for production.
- Saved analysis results; no live sensor connection.
- **Next:** follow a specific Plant A investigation.

### Slide 4 — Dashboard: Historical context

**1:30–2:00 · 30 seconds.** Point to Plant A’s 31 August row; pause for the audience to locate it.

- Historical screen: readings outside each plant’s retrospective comparison ranges.
- Case: **Plant A, 31 August**, unusually high specific energy.
- A date to investigate; statistical unusualness alone does not establish a fault.
- **Next:** inspect electricity and production together.

### Slide 5 — High energy per cubic metre needs production context

**2:00–2:40 · 40 seconds.** Read the three quantities once.

- **3,660 kWh / 1,881 m³ = 1.946 kWh/m³.**
- Electricity below the plant’s daily median; production also low.
- High ratio does not establish increased equipment consumption.
- Suggested checks: production schedule, operating hours and meter records before assigning a cause.
- **Next:** open Plant A’s underlying readings.

### Slides 6–7 — Dashboard: Plant A readings

**2:40–3:25 · 45 seconds for both screenshots together.** One continuous explanation; the slide advance represents scrolling the same panel.

- **Slide 6:** monthly totals and the Actual, Expected and Excess columns.
- **Advance to slide 7:** point to **31 August — actual 3,660 kWh**.
- Expected/excess: **unavailable because output is outside the reference range**.
- Dashes mean an unsupported estimate; they do not establish normal operation. Actual readings remain visible.
- **Next:** briefly show the same layout for Plant B.

### Slides 8–9 — Dashboard: Plant B readings

**3:25–3:40 · 15 seconds for both screenshots together.** No second case study or row-by-row explanation.

- Same layout for Plant B, with **its own totals and electricity reference**.
- **Advance from slide 8 to 9:** top and bottom of the same daily-readings panel.
- **Next:** coverage explains unavailable comparisons.

### Slide 10 — Dashboard: Comparison coverage

**3:40–4:15 · 35 seconds.** Point to coverage counts, then Plant A’s 31 August output.

- **A: 26/31 dates compared. B: 30/31.** Five A dates and one B date outside the July output range.
- Electricity and output readings are present; exclusions affect comparisons. Actual consumption stays in totals.
- **31 August: 1,881 m³**, below A’s **2,589 m³/day** reference minimum.
- Other visible checks: missing conductivity and recovery discrepancies.
- **Next:** how the monitor works for comparable operating conditions.

### Slide 11 — How the electricity monitor works

**4:15–5:05 · 50 seconds.** Follow the method stages. Explain CUSUM as accumulated evidence.

- July reference: **total electricity / total treated water**, separately per plant. Expected electricity = reference × today’s output.
- Compare actual and expected; scale the difference against July variation; accumulate evidence with **CUSUM**.
- Crossing the provisional limit requests investigation. Missing/unsupported comparisons reset evidence; an isolated spike can also cross.
- July is historical, with health unverified. Regression had lower pooled July error; simpler reference selected provisionally for transparency.
- **Next:** actual August monitoring results.

### Slide 12 — Dashboard: Actual August energy review

**5:05–5:40 · 35 seconds.** Point to actual CUSUM lines and dashed thresholds.

- **Zero crossings** on **26 eligible A dates / 30 eligible B dates**.
- No crossing does not establish healthy or efficient operation; six unsupported comparisons remain separate.
- August already inspected: **exploratory replay**, rather than independent detection validation.
- **Next:** no verified failure labels, so test the response to constructed increases.

### Slide 13 — Older mixed-chart layout: skip

**No speaking time. Advance directly to slide 14.** Slide 14 replaces the older mixed-chart layout; do not restart the historical explanation.

### Slide 14 — A constructed increase triggers a review

**5:40–6:25 · 45 seconds.** Point to day 8, the dashed limit and the red triangles.

- **One constructed Plant A path**, based on July residuals.
- Add approximately **485 kWh/day from simulated day 8**: 10% of July mean daily electricity.
- Blue line: accumulated evidence. Dashed line: limit. Red triangles: review crossings.
- Drops after crossings: accumulation restarts. Simulated response does not establish observed degradation.
- **Next:** evaluate repeated scenarios, beyond this single illustration.

### Slide 15 — Simulation detection and review workload

**6:25–7:20 · 55 seconds.** Point to detection, delay and workload in that order.

- **400 constructed 31-day paths per plant per scenario**; resample three-day July residual blocks. Sustained increase: added daily kWh equal to **10% of July mean electricity**.
- Detected within 14 days: **A 95.25% / B 100%**.
- Median delay **among detected paths**: **A 6 days / B 3 days**.
- No-change paths with at least one review: **A 6.75% / B 7.5% over 31 days**. Path-level proportions, not daily or measured site false-alarm rates.
- Same short July history used for calibration and simulations. Field fault accuracy, failure lead time and savings remain unverified. **Next: operator pilot.**

### Slide 16 — A pilot with BlueNexus operators

**7:20–8:00 · 40 seconds.** Follow the pilot stages, then finish on the question.

- Delivered: reproducible analysis, inspectable monitor and dashboard with supporting readings and comparison limits.
- Pilot: confirm equipment meanings/mappings; connect findings with dated operating/maintenance events; evaluate fresh data with agreed thresholds and review procedures.
- Measure investigation usefulness and workload. Assess resource savings separately, with treatment-quality safeguards.
- **Closing question:** “Which operating or maintenance events would you want us to compare these findings against first?”
