# PlantPulse presentation script

Read the paragraphs aloud. Each section follows one slide in the current 15-slide deck. The headings are navigation cues, not spoken text.

## PlantPulse

PlantPulse is a prototype to help operators investigate unusual plant readings.

When a reading stands out, the next question is: what was happening at the plant, and what should we check first?

I’ve brought the historical readings and a simple monitoring approach into one dashboard.

Today, I’ll use electricity and water production to show how that helps an operator investigate.

## Equipment data quality shaped my approach

I started by checking the data. Each plant has 244 days of equipment readings, from January to September. But the supporting plant-performance data covers only 62 days, in July and August.

I found 21 records that repeat the previous record in Plant A, and 10 in Plant B. Two Plant A runtime counters stay flat for 183 days.

We still need to confirm what some equipment readings mean and which pumps they belong to. So I focused on monitoring total plant electricity and water production. Pump diagnosis needs those details confirmed first.

## Dashboard: Overview

These screenshots walk through the dashboard. The overview brings electricity and water production together, with daily charts, plant totals, and the number of days the monitor can assess.

## Dashboard: Historical context

This view highlights unusual readings in each plant’s July and August history. Plant A’s specific energy stands out on 31 August. Specific energy means the electricity used per cubic metre of treated water.

## High energy per cubic metre needs production context

That day, Plant A used 3,660 kilowatt-hours to produce 1,881 cubic metres of water. That works out to about 1.946 kilowatt-hours per cubic metre.

Low water production contributed to that high ratio. Looking at electricity and production together gives us more context than the ratio alone.

I’d check the production schedule, operating hours and meter records before blaming an equipment problem.

## Dashboard: Plant A readings

Plant A’s table shows recorded electricity, what the monitor expected, and the difference. Let’s move down to 31 August.

The 3,660 kilowatt-hours is still here. Expected electricity and the difference show dashes because production was outside the July output range. The monitor couldn’t make that comparison. The dashes don’t mean zero consumption.

## Dashboard: Plant B readings

Plant B uses the same layout, with its own totals and July reference. Its actual electricity readings stay visible even when the comparison is unavailable.

Further down, the same columns let an operator check each day against the estimate. Next, the coverage view brings the unavailable comparisons together.

## Dashboard: Comparison coverage

The monitor could assess 26 August days for Plant A and 30 for Plant B. All electricity and water-output readings are present, but production was outside the July output range on five days for A and one for B.

Plant A’s 1,881 cubic metres on 31 August was below July’s lowest output of 2,589. Actual consumption still counts towards the totals.

Below that are other data checks: missing conductivity readings and differences between reported water recovery and the recovery calculated from the water readings.

## How the electricity monitor works

The three columns show how the monitor works. On the left, July’s total electricity divided by total treated water gives a reference for electricity per cubic metre, separately for each plant.

In the middle, multiplying that reference by today’s water production gives today’s expected electricity use.

On the right, CUSUM keeps a running score of excess use, allowing for July’s day-to-day variation. Repeated excesses build the score; readings below expected bring it towards zero. Crossing the limit prompts an operator review. A large isolated spike can trigger one too.

The score clears on days it can’t assess and restarts after each review flag.

I chose provisional limits in July-based simulations. The aim was to catch a sustained increase equal to ten percent of July’s average daily electricity, with no more than one in ten no-change months triggering any review.

## Dashboard: Actual August energy review

The blue lines show the running scores and the dashed lines show the review limits. Neither plant crossed its limit on the August days the monitor could assess: 26 for A and 30 for B.

I’d already examined August, so this shows its behaviour on historical data.

On days like 31 August, outside the July output range, the historical view still highlights the unusual reading for the operator to investigate.

## A constructed increase triggers a review

To show a review, I made an artificial Plant A example, adding about 485 kilowatt-hours every day from day eight. That’s ten percent of July’s average daily electricity.

The blue line first crosses the dashed limit on day seventeen. That’s slower than typical in the tests I’ll show next, but within fourteen days of the increase starting. Accumulation restarts, and it crosses again on day twenty-six. The red triangles mark both reviews.

Here’s what happened across many artificial months.

## Simulation detection and review workload

For each test, I built 400 artificial 31-day months per plant by reshuffling July’s electricity variation in three-day chunks, after accounting for production.

With the sustained increase, about 95 percent of Plant A’s test months and all of Plant B’s triggered a review within fourteen days of the increase starting. Among detected cases, the median wait was 6 days for A and 3 days for B. The increase was larger relative to Plant B’s July variation, helping explain its faster response. The plants also have different monitor settings.

With no increase added, seven to eight percent of the artificial months still triggered at least one review: roughly one month in fourteen. That suggests a review workload in simulations; I still need to measure it at the site.

These tests reuse July’s short history. I haven’t shown how reliably this detects real faults, how much warning it gives before failure, or whether it leads to savings.

## A pilot with BlueNexus operators

The next step would be a pilot with BlueNexus operators, following these three steps.

First, we’d confirm what each equipment reading means, its units, how the daily values are calculated, and which pump it belongs to. That gives us a clearer basis for using the equipment data.

Second, we’d review dated operating, maintenance and cleaning events with operators. That helps us connect changes in the readings to what was happening at the plant.

Third, we’d test fresh data together, agreeing which periods to use as references, when to flag a review, and when to reset the monitor’s score.

PlantPulse brings operational readings, historical context and electricity comparisons into one investigation workflow. Thank you.
