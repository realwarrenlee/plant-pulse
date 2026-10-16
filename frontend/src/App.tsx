import { useEffect, useRef, useState, type CSSProperties } from 'react'
import { CheckCircle2Icon } from 'lucide-react'
import { AppSidebar } from '@/components/app-sidebar'
import { SiteHeader } from '@/components/site-header'
import { SectionCards } from '@/components/section-cards'
import { ChartAreaInteractive } from '@/components/chart-area-interactive'
import { DataTable } from '@/components/data-table'
import { DetailSheet } from '@/components/detail-sheet'
import { AnalysisContent } from '@/components/analysis-content'
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar'
import { TooltipProvider } from '@/components/ui/tooltip'
import { Button } from '@/components/ui/button'
import { pages, totals, type PageId } from '@/lib/app-data'

export default function App() {
  const [pageId, setPageId] = useState<PageId>('overview')
  const page = pages.find(page => page.id === pageId)!
  const [plant, setPlant] = useState<'Plant A' | 'Plant B' | null>(null)
  const opener = useRef<HTMLElement | null>(null)
  useEffect(() => {
    if (window.location.pathname !== '/') window.history.replaceState(null, '', '/')
  }, [])
  useEffect(() => {
    document.title = `${page.title} · Plant Pulse`
    window.scrollTo(0, 0)
  }, [page])
  function openPlant(next: 'Plant A' | 'Plant B') {
    opener.current = document.activeElement as HTMLElement
    setPlant(next)
  }
  return <TooltipProvider><SidebarProvider style={{ '--sidebar-width': 'calc(var(--spacing) * 72)', '--header-height': 'calc(var(--spacing) * 12)' } as CSSProperties}>
    <AppSidebar active={page.id} onNavigate={setPageId} />
    <SidebarInset className="min-w-0">
      <SiteHeader title={page.title} />
      <main className="flex flex-1 flex-col"><div className="@container/main flex flex-1 flex-col gap-2"><div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6">
        {page.id === 'overview' ? <>
          <SectionCards />
          <div className="px-4 lg:px-6"><ChartAreaInteractive /></div>
          <DataTable onPlant={openPlant} />
          <div className="px-4 lg:px-6"><div className="flex flex-wrap items-center justify-between gap-2 rounded-lg border bg-muted/40 px-4 py-2 text-sm">
            <span className="flex items-center gap-2.5"><CheckCircle2Icon className="size-4 text-emerald-700" />{totals.reviews === 0 ? 'No energy review events' : `${totals.reviews} energy review events`}</span>
            <Button variant="ghost" size="sm" onClick={() => setPageId('quality')}>{totals.unavailable} unavailable</Button>
          </div></div>
        </> : <div className="page-analysis px-4 lg:px-6"><AnalysisContent panel={page.id} /></div>}
      </div></div></main>
    </SidebarInset>
    <DetailSheet plant={plant} onClose={() => setPlant(null)} returnFocus={() => opener.current?.focus()} />
  </SidebarProvider></TooltipProvider>
}
