import type { ReactNode } from 'react'
import { SidebarGroup, SidebarGroupContent, SidebarMenu, SidebarMenuButton, SidebarMenuItem } from '@/components/ui/sidebar'
import type { PageId } from '@/lib/app-data'

export function NavMain({ items, active, onNavigate }: { items: { id: PageId; title: string; icon: ReactNode }[]; active: PageId; onNavigate: (page: PageId) => void }) {
  return <SidebarGroup><SidebarGroupContent className="flex flex-col gap-2"><SidebarMenu>
    {items.map(item => <SidebarMenuItem key={item.id}><SidebarMenuButton tooltip={item.title} isActive={active === item.id} onClick={() => onNavigate(item.id)} aria-current={active === item.id ? 'page' : undefined}>
      {item.icon}<span>{item.title}</span>
    </SidebarMenuButton></SidebarMenuItem>)}
  </SidebarMenu></SidebarGroupContent></SidebarGroup>
}
