# Plant Pulse dashboard

React dashboard built from shadcn `dashboard-01`, with its inset sidebar, card grid, chart area and table. Historical trends, Energy review and Data quality are full content views within the same page; only individual plant readings open in a sheet.

```powershell
npm install
npm run dev
```

Open http://127.0.0.1:5173. `npm run build` produces the static app in `dist`; `npm test` checks the summary calculations.

The URL stays at `/` when switching views. Refresh returns to Overview. Sidebar navigation updates the content without reloading the page or adding browser history entries.

The overview uses the saved August electricity replay. Historical details include July and August. `src/data/plant-data.json` is a local snapshot of the existing analysis, with source paths and SHA-256 hashes. No external services are called.

Run `npm run data` after regenerating the analysis outputs. This uses the project `.venv` Python and checks totals, exclusions, expected electricity and unchanged source files before exporting. All daily consumption contributes to totals; excluded comparisons remain missing in charts and tables.

Historical outliers are review candidates. CUSUM review events are separate, and no confirmed fault diagnosis is displayed.

The production dependency audit is clear. The full development audit reports seven advisory entries in the latest shadcn CLI's glob dependency chain; that CLI is only used for local component generation. A forced downgrade was not applied. See `design-qa.md` for the browser and build checks.
