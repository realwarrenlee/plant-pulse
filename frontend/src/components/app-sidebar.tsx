import { ActivityIcon, ChartBarIcon, DatabaseIcon, LayoutDashboardIcon, DropletIcon } from 'lucide-react'
import { NavMain } from '@/components/nav-main'
import { Sidebar, SidebarContent, SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem, useSidebar } from '@/components/ui/sidebar'
import { pages, type PageId } from '@/lib/app-data'

const icons = { overview: LayoutDashboardIcon, history: ChartBarIcon, review: ActivityIcon, quality: DatabaseIcon }

export function AppSidebar({ active, onNavigate }: { active: PageId; onNavigate: (page: PageId) => void }) {
  const { setOpenMobile } = useSidebar()
  function navigate(page: PageId) { setOpenMobile(false); onNavigate(page) }
  return <Sidebar collapsible="offcanvas" variant="inset">
    <SidebarHeader><SidebarMenu><SidebarMenuItem>
      <SidebarMenuButton onClick={() => navigate('overview')} className="data-[slot=sidebar-menu-button]:p-1.5!">
        <DropletIcon className="size-5!" /><span className="text-base font-semibold">Plant Pulse</span>
      </SidebarMenuButton>
    </SidebarMenuItem></SidebarMenu></SidebarHeader>
    <SidebarContent><NavMain active={active} onNavigate={navigate} items={pages.map(page => { const Icon = icons[page.id]; return { ...page, icon: <Icon /> } })} /></SidebarContent>
  </Sidebar>
}
