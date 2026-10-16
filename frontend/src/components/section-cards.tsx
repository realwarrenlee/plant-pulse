import { ClipboardListIcon, DropletsIcon, FactoryIcon, ZapIcon } from 'lucide-react'
import { Card, CardAction, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { number, totals } from '@/lib/app-data'

export function SectionCards() {
  const cards = [
    { label: 'Total electricity', value: totals.electricity, unit: 'kWh', icon: ZapIcon },
    { label: 'Treated-water output', value: totals.water, unit: 'm³', icon: DropletsIcon },
    { label: 'Plants included', value: totals.plants, unit: '', icon: FactoryIcon },
    { label: 'Energy review events', value: totals.reviews, unit: '', icon: ClipboardListIcon },
  ]
  return <section aria-label="Summary" className="grid grid-cols-2 gap-4 px-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card *:data-[slot=card]:shadow-xs lg:px-6 @5xl/main:grid-cols-4">
    {cards.map(card => <Card key={card.label} className="@container/card"><CardHeader>
      <CardDescription className="pr-4 text-xs">{card.label}</CardDescription>
      <CardTitle className="mt-2 flex flex-wrap items-baseline gap-x-2 text-2xl font-semibold tracking-tight tabular-nums @[250px]/card:text-3xl">{number(card.value)}{card.unit && <span className="text-xs font-normal tracking-normal text-muted-foreground">{card.unit}</span>}</CardTitle>
      <CardAction><card.icon className="size-4 text-muted-foreground" /></CardAction>
    </CardHeader></Card>)}
  </section>
}
