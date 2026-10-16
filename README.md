# Plant Pulse

A prototype that helps water-treatment operators investigate unusual readings and possible excess electricity use.

Built for **Projet: Hack & Hire**, which kicked off on **10 October 2026**: one week to build on a real company problem, followed by a 15-minute defence with its hiring team.

## BlueNexus

Water treatment plants generate operational data, but identifying inefficient or abnormal operation can still depend on manual monitoring and operator experience.

**How can BlueNexus use operational data to identify inefficient or abnormal plant operation and provide early insights that help reduce energy, chemical and water consumption while maintaining treatment performance?**

The expected outputs are:

- Identify operational variables relevant to efficiency and treatment performance.
- Analyse historical data for normal and abnormal operating patterns.
- Develop an analytical, statistical or machine-learning approach for early detection of performance degradation.
- Recommend practical indicators, thresholds or alerts for operators.
- Present the findings through a simple dashboard or decision-support concept.

The organisers clarified that the equipment daily datasets are the primary focus, with cleaning included in the task.

## What we built

- **Data review:** cleaning and historical analysis of two anonymised plants, each with 244 equipment days and 62 days of supporting plant-performance records.
- **Electricity monitor:** separate July references for each plant, adjusted for water output, with CUSUM accumulating evidence of excess electricity. Regression provides a comparison.
- **Dashboard:** React views for Overview, Historical trends, Energy review and Data quality, with inspectable plant readings. It displays saved analysis results.

The review found 21 adjacent repeated equipment records in Plant A and ten in Plant B, 183-day flat periods in both Plant A runtime counters, and eight recovery reconciliation mismatches in Plant B.

The August replay produced zero energy-review events across 56 comparable plant-days; six comparisons were unavailable. Constructed-change tests assess detector behaviour, but real fault accuracy, failure lead time and resource savings remain unverified. The selected monitor operates at plant level; pump diagnosis and live control are outside the prototype.

## Run the dashboard

Requires Node.js and npm. From the repository root:

```powershell
cd frontend
npm install
npm run dev
```

Open [localhost:5173](http://127.0.0.1:5173/). See the [frontend guide](frontend/README.md) for checks and data refresh instructions.

## Analysis and submission

- [Memo](MEMO.md): solution, results, limitations and next steps.
- [Presentation cues](PRESENTATION.md): speaking notes.
- [Q&A](QNA.md): eight priority questions for the BlueNexus discussion.
- [Notebook](data_review.ipynb): reproducible cleaning, analysis and evaluation. Run All with NumPy, pandas, Matplotlib and IPython available.
- [Operational variables](OPERATIONAL_VARIABLES.md), [historical findings](HISTORICAL_ANALYSIS.md) and [detection approach](DETECTION_APPROACH.md): supporting evidence and methodology.
- [Data notes](DATA.md): source descriptions, interpretation limits and confidentiality requirements. The supplied datasets and generated exports must not be published or redistributed without permission.
