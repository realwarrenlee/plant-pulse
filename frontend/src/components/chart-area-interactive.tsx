import { CartesianGrid, Line, LineChart, ReferenceLine, XAxis, YAxis } from 'recharts'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { ChartContainer, ChartTooltip, ChartTooltipContent, type ChartConfig } from '@/components/ui/chart'
import { day, number, plants, type Plant } from '@/lib/app-data'

const energyConfig = { actual: { label: 'Actual', color: '#236acc' }, expected: { label: 'Expected', color: '#b4741c' } } satisfies ChartConfig
const reviewConfig = { cusum: { label: 'CUSUM', color: '#236acc' } } satisfies ChartConfig

export function ChartAreaInteractive() {
  return <Card className="@container/card"><CardHeader><CardTitle>Daily electricity</CardTitle><CardDescription>kWh</CardDescription></CardHeader><CardContent className="px-2 pt-1 sm:px-5">
    <div className="grid gap-6 @3xl/card:grid-cols-2">{plants.map(plant => <section key={plant.name} className="min-w-0">
      <div className="mb-4 flex items-center justify-between px-2"><h2 className="text-sm font-medium">{plant.name}</h2><span className="text-xs text-muted-foreground">{plant.summary.comparable}/{plant.summary.days} days compared</span></div>
      <PlantEnergyChart plant={plant} />
    </section>)}</div>
    <div className="mt-4 flex items-center justify-center gap-6 text-xs text-muted-foreground"><span className="flex items-center gap-2"><i className="w-5 border-t-2 border-[#236acc]" />Actual</span><span className="flex items-center gap-2"><i className="w-5 border-t-2 border-dashed border-[#b4741c]" />Expected</span></div>
  </CardContent></Card>
}

function PlantEnergyChart({ plant }: { plant: Plant }) {
  return <ChartContainer config={energyConfig} className="h-[240px] w-full aspect-auto" aria-label={`${plant.name} daily actual and expected electricity`}>
    <LineChart accessibilityLayer data={plant.readings} margin={{ top: 8, right: 12, bottom: 0, left: 0 }}>
      <CartesianGrid vertical={false} strokeDasharray="3 3" />
      <XAxis dataKey="date" tickLine={false} axisLine={false} tickMargin={12} minTickGap={10} ticks={[0, 7, 14, 21, 30].map(i => plant.readings[i].date)} tickFormatter={day} />
      <YAxis width={44} tickLine={false} axisLine={false} tickMargin={8} tickCount={5} domain={plant.name === 'Plant A' ? [2000, 6500] : [11000, 23000]} tickFormatter={value => `${number(value / 1000, value % 1000 ? 1 : 0)}k`} />
      <ChartTooltip content={<ChartTooltipContent labelFormatter={value => day(String(value))} formatter={(value, name) => <div className="flex min-w-36 justify-between gap-4"><span className="text-muted-foreground">{name === 'actual' ? 'Actual' : 'Expected'}</span><span className="font-medium tabular-nums">{number(Number(value))} kWh</span></div>} />} />
      <Line type="linear" dataKey="actual" stroke="var(--color-actual)" strokeWidth={2.3} dot={false} isAnimationActive={false} />
      <Line type="linear" dataKey="expected" stroke="var(--color-expected)" strokeWidth={2} strokeDasharray="6 5" dot={false} connectNulls={false} isAnimationActive={false} />
    </LineChart>
  </ChartContainer>
}

export function ReviewChart({ plant }: { plant: Plant }) {
  return <ChartContainer config={reviewConfig} className="h-52 w-full aspect-auto" aria-label={`${plant.name} CUSUM and review threshold`}>
    <LineChart accessibilityLayer data={plant.readings} margin={{ top: 12, right: 12, left: 0, bottom: 0 }}>
      <CartesianGrid vertical={false} strokeDasharray="3 3" />
      <XAxis dataKey="date" tickFormatter={day} tickLine={false} axisLine={false} minTickGap={45} />
      <YAxis width={34} domain={[0, plant.reference.limit * 1.15]} ticks={[0, plant.reference.limit / 3, plant.reference.limit * 2 / 3, plant.reference.limit]} tickFormatter={value => number(value, value % 1 ? 1 : 0)} tickLine={false} axisLine={false} />
      <ReferenceLine y={plant.reference.limit} stroke="#b4741c" strokeDasharray="6 5" />
      <ChartTooltip content={<ChartTooltipContent labelFormatter={value => day(String(value))} formatter={value => <span className="tabular-nums">CUSUM <strong className="ml-3 font-medium">{number(Number(value), 2)}</strong></span>} />} />
      <Line dataKey="cusum" type="linear" dot={false} stroke="var(--color-cusum)" strokeWidth={2} connectNulls={false} isAnimationActive={false} />
    </LineChart>
  </ChartContainer>
}
