import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle } from '@/components/ui/sheet'
import { AnalysisContent } from '@/components/analysis-content'

export function DetailSheet({ plant, onClose, returnFocus }: { plant: 'Plant A' | 'Plant B' | null; onClose: () => void; returnFocus: () => void }) {
  return <Sheet open={plant !== null} onOpenChange={open => { if (!open) onClose() }}>
    <SheetContent className="gap-0 data-[side=right]:w-full data-[side=right]:sm:max-w-[640px]" onCloseAutoFocus={event => { event.preventDefault(); returnFocus() }}>
      <SheetHeader className="border-b px-6 py-5 pr-12"><SheetTitle className="text-xl">{plant}</SheetTitle><SheetDescription>Daily electricity readings in kWh.</SheetDescription></SheetHeader>
      <div className="min-h-0 overflow-y-auto px-6 py-6"><AnalysisContent panel={plant} /></div>
    </SheetContent>
  </Sheet>
}
