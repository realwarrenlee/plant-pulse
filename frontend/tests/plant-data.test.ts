import assert from "node:assert/strict"
import test from "node:test"
import { summarizePlant, periodTotals, type Reading } from "../src/lib/plant-data.ts"

const readings: Reading[] = [
  { date: "2026-08-01", actual: 10, output: 2, expected: 9, excess: 1, eligible: true, score: 0.5, cusum: 0, review: false, reason: "" },
  { date: "2026-08-02", actual: 20, output: 8, expected: null, excess: null, eligible: false, score: null, cusum: null, review: false, reason: "Outside reference output range" },
  { date: "2026-08-03", actual: 30, output: 10, expected: 22, excess: 8, eligible: true, score: 4, cusum: 3.5, review: true, reason: "" },
]

test("period energy uses matching totals, including days unavailable to the detector", () => {
  const result = summarizePlant(readings)
  assert.equal(result.electricity, 60)
  assert.equal(result.water, 20)
  assert.equal(result.specificEnergy, 3)
  assert.equal(result.comparable, 2)
  assert.equal(result.unavailable, 1)
  assert.equal(result.reviews, 1)
  assert.equal(result.days, 3)
})

test("combined totals add consumption and volume, never plant ratios", () => {
  const first = summarizePlant(readings)
  const second = summarizePlant([{ ...readings[0], actual: 40, output: 10 }])
  assert.deepEqual(periodTotals([first, second]), { electricity: 100, water: 30, plants: 2, reviews: 1, comparable: 3, unavailable: 1 })
})

test("empty readings remain unavailable, rather than appearing energy efficient", () => {
  const result = summarizePlant([])
  assert.equal(result.specificEnergy, null)
  assert.equal(result.days, 0)
})

test("invalid source quantities cannot enter the overview totals", () => {
  for (const values of [{ actual: NaN }, { output: 0 }, { actual: -1 }, { output: Infinity }]) {
    assert.throws(() => summarizePlant([{ ...readings[0], ...values }]), /Invalid electricity or water output/)
  }
})
