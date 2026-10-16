# Dashboard checks

final result: passed

Source visual truth: `output/dashboard-build/shadcn-dashboard-01-reference.jpg`, captured from https://ui.shadcn.com/view/new-york-v4/dashboard-01. The installed source is the current `radix-nova` registry block. Its inset sidebar, header, card grid, chart area and table structure are retained. The earlier navy concept is superseded by the user's explicit dashboard-01 instruction.

Implementation: http://127.0.0.1:5173, captured in `output/dashboard-build/overview.jpg`. Source and implementation were opened together in one comparison input. Both desktop captures are 1440 × 1000 pixels at a 1440 × 1000 CSS viewport, device pixel ratio 1; no density rescaling. Source data and chart animation are illustrative, so chart values and curves are not fidelity targets.

## Findings

No actionable P0/P1/P2 findings remain.

- Typography: bundled Geist, clear card values, compact labels and legible table text. Smaller headings follow the installed block.
- Layout: inset main surface, 18rem sidebar, 48px header, 24px desktop gutters, four summary cards and a full-width chart card. Compact KPI cards intentionally omit the template's sales commentary. The two plant plots use separate scales within the chart area.
- Colors: default shadcn neutral tokens and subtle card gradients. Blue actual values and amber dashed expected values remain distinct without color alone.
- Assets: installed Lucide icons and Recharts-generated plots; no decorative raster assets or custom-drawn icons. The block's Command brand icon is retained.
- Copy: demo sales content, extra menus, date selectors and prototype wording removed. Actual readings supply the totals and plots. Expected comparisons remain missing outside the supported range.
- Focused header evidence: `output/dashboard-build/header.jpg` visibly confirms removal of the vertical separator. DOM inspection also confirms zero separator elements in the shared header.

## Interaction evidence

- Overview, Historical trends, Energy review and Data quality switch full content views at `/`. All four views were checked on desktop and mobile with URL and heading assertions. Active navigation updates and the mobile menu closes after selection. The overview's unavailable-count shortcut opens the quality view at `/`.
- Refresh resets the view to Overview. Switching views does not add browser history entries. These checks supersede the earlier separate-URL implementation.
- Plant A and B reading buttons show 31 daily records each. Missing comparisons display em dashes. Escape closes the plant sheet and returns focus to the initiating button.
- Keyboard arrow navigation on the first plot displays 2 August: actual 4,797 kWh, expected 4,667 kWh.
- Mobile tested at 390 × 844 CSS pixels. Cards and plots stack; tables scroll within their containers. Sidebar links navigate to pages and dismiss the mobile menu. No document horizontal overflow was observed. Mobile evidence: `output/dashboard-build/overview-mobile.jpg`.
- Supporting captures: `history.jpg`, `energy-review.jpg`, `data-quality.jpg` in the same output directory. These predate the final shared-header separator removal.
- No warnings or errors after the final hard reload and primary interaction checks. Earlier hot-reload errors occurred while the CLI replaced the component files; they do not recur in the completed app.

## Comparison history

1. Initial implementation used the earlier navy mockup and sheets. User superseded that direction: reinstalled dashboard-01, retained its default neutral/inset layout, and moved all three analysis sections to pages.
2. CUSUM axis labels initially exposed floating-point tails. Fixed explicit ticks and number formatting; subsequent Energy review capture shows clean 0/1/2/3 and 0/4/8/12 ticks.
3. User requested removing the header separator. Removed it from the shared header, adjusted the gap and captured the revised header and overview. The final combined source/implementation comparison found no remaining actionable issues within the requested adaptations.
4. User requested keeping the views under `/`. Replaced route links with in-page sidebar buttons, updated the shortcut and documentation, and verified all four view headings and unchanged URLs on desktop and mobile. No layout changes. Brand now reads Plant Pulse with the installed Lucide droplet icon.

## Verification

- `npm run build`: passed; Vite notes the chart bundle exceeds 500 kB.
- `npm test`: 4 passed.
- `npm run data`: passed all export assertions; source hashes unchanged.
- `npm audit --omit=dev`: zero vulnerabilities. The full development audit reports seven entries in the latest shadcn CLI's glob dependency chain. CLI tooling is a development dependency; no forced downgrade was applied.

Not checked: live plant integration, public hosting or field detection accuracy. View selection is not persisted across refresh.
