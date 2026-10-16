# BlueNexus Q&A

Eight questions to prepare. Start with a short answer; expand only when asked.

## 1. We asked for equipment analysis. Why is the detector plant-level?

I reviewed the equipment histories, but some signal meanings and units are unconfirmed, and mapped pump flow and pressure are insufficient for diagnosis. The selected monitor therefore uses the clearer plant electricity and output records. Pump-specific detection still needs confirmed measurements.

## 2. Why use a simple statistical method instead of more complex AI?

The data are limited and have no verified failure labels. The reference and CUSUM are easy to inspect, and the brief permits statistical approaches. I compared regression too: it had lower pooled July prediction error. The simpler reference is a provisional choice for transparency, rather than a proven accuracy winner.

## 3. Did you detect any actual faults?

No confirmed faults. The August replay produced zero energy-review events on eligible dates. With a constructed daily increase equal to 10% of July mean electricity, detection within 14 days was 95.25% for A and 100% for B. Median delays among detected paths were six and three days. These are simulation results, not real fault accuracy or lead time.

## 4. How did you choose the thresholds, and what about false alarms?

I compared 12 settings using July-based simulations, targeting detection of an added daily amount equal to 10% of July mean electricity within 14 days, while limiting simulated no-change review workload. Evaluation produced reviews in 6.75% of A and 7.5% of B no-change 31-day paths. These are path-level simulation proportions; the field false-alarm rate is unknown.

## 5. Why did the high specific-energy reading on 31 August not trigger an alert?

Plant A produced 1,881 m³, below its July reference minimum of 2,589 m³/day. The monitor withheld that comparison rather than extrapolate. The high ratio remains visible as a historical investigation case. This is a coverage gap, not evidence that operation was normal.

## 6. What should an operator do with a review event?

Check the readings, production and loading, then compare operating, maintenance and cleaning records before assigning a cause or changing settings. Review available water-quality evidence too. The prototype requests investigation and restarts accumulation after a crossing; acknowledgement and escalation procedures still need operator agreement.

## 7. How much energy, water or chemicals have you saved?

No savings caused by Plant Pulse have been measured. Historical consumption changes do not establish its impact. A pilot needs a suitable comparison and treatment-quality safeguards. Chemical records are too sparse and insufficiently defined for reliable dosing comparisons, and site quality acceptance limits are missing.

## 8. What would you need to use this at a real plant?

The dashboard currently uses saved results. First confirm signal definitions and units, obtain dated operating and maintenance events, and collect a longer history. Then run a supervised evaluation on fresh data, agreeing thresholds, comparison coverage, review workload and site quality limits with operators before live integration.
