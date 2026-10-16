import { ArrowUpRightIcon } from 'lucide-react'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Button } from '@/components/ui/button'
import { number, plants } from '@/lib/app-data'

export function DataTable({ onPlant }: { onPlant: (plant: 'Plant A' | 'Plant B') => void }) {
  return <section className="flex flex-col gap-4 px-4 lg:px-6"><h2 className="text-base font-semibold">Plant summary</h2><div className="overflow-hidden rounded-lg border">
    <Table><TableHeader className="bg-muted"><TableRow>
      <TableHead className="pl-4">Plant</TableHead><TableHead className="text-right">Electricity <span className="unit">kWh</span></TableHead><TableHead className="text-right">Treated water <span className="unit">m³</span></TableHead><TableHead className="text-right">Specific energy <span className="unit">kWh/m³</span></TableHead><TableHead className="text-right">Compared days</TableHead><TableHead className="pr-4 text-right">Reviews</TableHead>
    </TableRow></TableHeader><TableBody>{plants.map(plant => <TableRow key={plant.name}>
      <TableCell className="pl-4"><Button variant="link" className="h-9 px-0 font-medium text-foreground" aria-label={`View ${plant.name} readings`} aria-haspopup="dialog" onClick={() => onPlant(plant.name as 'Plant A' | 'Plant B')}>{plant.name}<ArrowUpRightIcon className="size-3.5 text-muted-foreground" /></Button></TableCell>
      <TableCell className="text-right tabular-nums">{number(plant.summary.electricity)}</TableCell><TableCell className="text-right tabular-nums">{number(plant.summary.water)}</TableCell><TableCell className="text-right tabular-nums">{number(plant.summary.specificEnergy!, 3)}</TableCell><TableCell className="text-right tabular-nums">{plant.summary.comparable}/{plant.summary.days}</TableCell><TableCell className="pr-4 text-right tabular-nums">{plant.summary.reviews}</TableCell>
    </TableRow>)}</TableBody></Table>
  </div></section>
}
