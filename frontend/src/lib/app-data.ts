import source from '@/data/plant-data.json'
import { periodTotals, summarizePlant } from '@/lib/plant-data'

export const plants = source.plants.map(plant => ({ ...plant, summary: summarizePlant(plant.readings) }))
export type Plant = (typeof plants)[number]
export const totals = periodTotals(plants.map(plant => plant.summary))
export const { outliers, quality } = source
export type Panel = 'history' | 'review' | 'quality' | 'Plant A' | 'Plant B' | null
export const pages = [
  { id: 'overview', title: 'Overview' },
  { id: 'history', title: 'Historical trends' },
  { id: 'review', title: 'Energy review' },
  { id: 'quality', title: 'Data quality' },
] as const
export type PageId = (typeof pages)[number]['id']
export const number = (value: number, digits = 0) => new Intl.NumberFormat('en-GB', { minimumFractionDigits: digits, maximumFractionDigits: digits }).format(value)
export const day = (date: string) => new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', timeZone: 'UTC' }).format(new Date(`${date}T00:00:00Z`))
