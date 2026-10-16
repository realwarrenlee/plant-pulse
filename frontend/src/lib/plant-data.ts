export type Reading = {
  date: string
  actual: number
  output: number
  expected: number | null
  excess: number | null
  eligible: boolean
  score: number | null
  cusum: number | null
  review: boolean
  reason: string
}

export function summarizePlant(readings: Reading[]) {
  let electricity = 0, water = 0, comparable = 0, reviews = 0
  for (const reading of readings) {
    if (!Number.isFinite(reading.actual) || reading.actual < 0 || !Number.isFinite(reading.output) || reading.output <= 0) {
      throw new Error("Invalid electricity or water output")
    }
    electricity += reading.actual
    water += reading.output
    comparable += Number(reading.eligible)
    reviews += Number(reading.review)
  }
  return { electricity, water, specificEnergy: water > 0 ? electricity / water : null, comparable,
    unavailable: readings.length - comparable, reviews, days: readings.length }
}

export type PlantSummary = ReturnType<typeof summarizePlant>

export function periodTotals(summaries: PlantSummary[]) {
  return summaries.reduce((totals, plant) => ({
    electricity: totals.electricity + plant.electricity,
    water: totals.water + plant.water,
    plants: totals.plants + 1,
    reviews: totals.reviews + plant.reviews,
    comparable: totals.comparable + plant.comparable,
    unavailable: totals.unavailable + plant.unavailable,
  }), { electricity: 0, water: 0, plants: 0, reviews: 0, comparable: 0, unavailable: 0 })
}
