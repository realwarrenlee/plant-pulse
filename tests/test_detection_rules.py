import unittest
import ast
import json
from pathlib import Path

import numpy as np
import pandas as pd

from detection_rules import ewma_scores, persistent_warnings
import detection_rules


class NotebookSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        notebook = json.loads((Path(__file__).resolve().parents[1]/'data_review.ipynb').read_text(encoding='utf-8'))
        source = next(''.join(cell['source']) for cell in notebook['cells']
                      if cell['cell_type'] == 'code' and 'def simulation_metrics(' in ''.join(cell['source']))
        functions = ast.Module(body=[node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)], type_ignores=[])
        cls.scope = {'pd': pd, 'np': np, 'cusum_scores': detection_rules.cusum_scores,
                     'persistent_warnings': persistent_warnings,
                     'simulation_dates': pd.date_range('2026-08-01', periods=31)}
        exec(compile(functions, 'notebook-simulation-functions', 'exec'), cls.scope)

    def test_no_change_and_small_isolated_spike_do_not_cross(self):
        metrics = self.scope['simulation_metrics']
        paths = np.zeros((2,31))
        paths[1,7] = 2.
        self.assertEqual(metrics(paths,.5,5.)['fraction_with_any_review'], 0.)

    def test_detection_denominator_includes_undetected_paths(self):
        paths = np.zeros((2,31))
        paths[0,7:] = 1.
        result = self.scope['simulation_metrics'](paths,.5,1.,onset=7)
        self.assertEqual(result['detection_within_14_days'], .5)
        self.assertEqual(result['median_delay_days_detected'], 3.)
        result = self.scope['simulation_metrics'](paths,.5,1.,method='Three-day >2 scales',onset=7)
        self.assertEqual(result['detection_within_14_days'], 0.)
        self.assertTrue(np.isnan(result['median_delay_days_detected']))

    def test_pre_change_review_is_reported_separately_from_detection_delay(self):
        paths = np.zeros((1,31))
        paths[0,0] = 3.
        paths[0,7:] = 1.
        result = self.scope['simulation_metrics'](paths,.5,1.,onset=7)
        self.assertEqual(result['fraction_review_before_change'], 1.)
        self.assertEqual(result['median_delay_days_detected'], 3.)

    def test_residual_blocks_preserve_local_order_and_pair_model_draws(self):
        reference = pd.DataFrame({'effluent_volume_m3':np.arange(100.,131.),
                                  'daily_electricity_kwh':np.arange(100.,131.)+np.arange(31.)})
        model = {'intercept_kwh':0.,'slope_kwh_per_m3':1.,'residual_scale_kwh':1.}
        paths = self.scope['residual_paths'](reference,model,822,3,block_days=7)
        self.assertEqual(paths.shape,(3,31))
        self.assertTrue(((paths >= -15.) & (paths <= 15.)).all())
        # Known centred residuals are -15..15, so every intact block advances by one.
        np.testing.assert_allclose(np.diff(paths[:,:28].reshape(3,4,7),axis=2),1.)
        half = self.scope['residual_paths'](reference,{**model,'residual_scale_kwh':2.},822,3,block_days=7)
        np.testing.assert_allclose(half,paths/2.)


class EnergyPrototypeTests(unittest.TestCase):
    def training(self):
        # Independent fixture: y = 10 + 2*x, with orthogonal residuals [1,-1,-1,1].
        return pd.DataFrame({'effluent_volume_m3': [1., 2., 3., 4.],
                             'daily_electricity_kwh': [13., 13., 15., 19.]},
                            index=pd.date_range('2026-07-01', periods=4))

    def test_baseline_learns_known_coefficients_and_robust_scale(self):
        self.assertTrue(hasattr(detection_rules, 'fit_energy_baseline'), 'Energy baseline is not implemented')
        model = detection_rules.fit_energy_baseline(self.training())
        self.assertAlmostEqual(model['intercept_kwh'], 10.)
        self.assertAlmostEqual(model['slope_kwh_per_m3'], 2.)
        self.assertAlmostEqual(model['residual_scale_kwh'], 1.4826)

    def test_specific_energy_baseline_uses_volume_weighted_reference(self):
        # Total electricity 60 / total volume 10 = 6; residual MAD is 3.
        model = detection_rules.fit_energy_baseline(self.training(), method='specific_energy')
        self.assertEqual(model['intercept_kwh'], 0.)
        self.assertAlmostEqual(model['slope_kwh_per_m3'], 6.)
        self.assertAlmostEqual(model['residual_scale_kwh'], 4.4478)
        later = self.training().iloc[[1]].copy()
        later.index = pd.to_datetime(['2026-08-01'])
        later.daily_electricity_kwh = 17.
        result = detection_rules.score_energy(later, model)
        self.assertAlmostEqual(result.expected_electricity_kwh.iloc[0], 12.)
        self.assertAlmostEqual(result.excess_electricity_kwh.iloc[0], 5.)
        self.assertAlmostEqual(result.residual_score.iloc[0], 5./4.4478)

    def test_specific_energy_baseline_rejects_unknown_method_and_zero_noise(self):
        with self.assertRaises(ValueError):
            detection_rules.fit_energy_baseline(self.training(), method='unknown')
        with self.assertRaises(ValueError):
            detection_rules.fit_energy_baseline(self.training().assign(daily_electricity_kwh=[2.,4.,6.,8.]), method='specific_energy')
        with self.assertRaises(ValueError):
            detection_rules.fit_energy_baseline(self.training().assign(effluent_volume_m3=2.), method='specific_energy')

    def test_baseline_rejects_unusable_reference(self):
        for bad in [self.training().iloc[:2], self.training().assign(effluent_volume_m3=2.),
                    self.training().assign(daily_electricity_kwh=[12.,14.,16.,18.]),
                    self.training().assign(daily_electricity_kwh=[19.,15.,13.,13.]),
                    self.training().assign(daily_electricity_kwh=np.nan),
                    self.training().assign(effluent_volume_m3=0.)]:
            with self.subTest(bad=bad.to_dict()):
                with self.assertRaises(ValueError):
                    detection_rules.fit_energy_baseline(bad)

    def test_energy_replay_masks_out_of_range_and_invalid_inputs(self):
        model = detection_rules.fit_energy_baseline(self.training())
        later = pd.DataFrame({'effluent_volume_m3': [2., 5., 0., 2., 2.],
                              'daily_electricity_kwh': [17., 20., 4., np.nan, -1.]},
                             index=pd.date_range('2026-08-01', periods=5))
        result = detection_rules.score_energy(later, model)
        self.assertEqual(result.eligible.tolist(), [True, False, False, False, False])
        self.assertAlmostEqual(result.expected_electricity_kwh.iloc[0], 14.)
        self.assertAlmostEqual(result.excess_electricity_kwh.iloc[0], 3.)
        self.assertAlmostEqual(result.residual_score.iloc[0], 3./1.4826)
        self.assertTrue(result.residual_score.iloc[1:].isna().all())

    def test_replay_rejects_reference_overlap_and_duplicate_daily_dates(self):
        model = detection_rules.fit_energy_baseline(self.training())
        with self.assertRaises(ValueError):
            detection_rules.score_energy(self.training(), model)
        bad = self.training().copy()
        bad.index = pd.to_datetime(['2026-08-01', '2026-08-01', '2026-08-02', '2026-08-03'])
        with self.assertRaises(ValueError):
            detection_rules.score_energy(bad, model)

    def test_cusum_accumulates_positive_evidence_and_restarts_after_crossing(self):
        self.assertTrue(hasattr(detection_rules, 'cusum_scores'), 'CUSUM is not implemented')
        scores = pd.Series([1., 1., 1., 1., -1., 1.], index=pd.date_range('2026-08-01', periods=6))
        result = detection_rules.cusum_scores(scores, allowance=.5, decision_limit=1.)
        np.testing.assert_allclose(result.cusum_score, [.5, 1., 1.5, .5, 0., .5])
        self.assertEqual(result.review_flag.tolist(), [False, False, True, False, False, False])
        self.assertEqual(result.evidence_start.iloc[2], scores.index[0])
        self.assertEqual(result.evidence_start.iloc[3], scores.index[3])

    def test_cusum_resets_on_invalid_readings_and_calendar_gaps(self):
        for unavailable in [np.nan, np.inf, -np.inf]:
            scores = pd.Series([1., 1., unavailable, 1., 1.], index=pd.date_range('2026-08-01', periods=5))
            result = detection_rules.cusum_scores(scores, allowance=.5, decision_limit=1.)
            self.assertFalse(result.review_flag.any())
            self.assertTrue(np.isnan(result.cusum_score.iloc[2]))
            self.assertEqual(result.evidence_start.iloc[-1], scores.index[3])
        scores = pd.Series([1., 1., 1.], index=pd.to_datetime(['2026-08-01', '2026-08-02', '2026-08-04']))
        np.testing.assert_allclose(detection_rules.cusum_scores(scores, allowance=.5, decision_limit=1.).cusum_score, [.5,1.,.5])

    def test_future_readings_cannot_change_energy_or_cusum_results(self):
        model = detection_rules.fit_energy_baseline(self.training())
        later = self.training().copy()
        later.index = pd.date_range('2026-08-01', periods=4)
        later.daily_electricity_kwh += 4
        full = detection_rules.score_energy(later, model)
        chart = detection_rules.cusum_scores(full.residual_score)
        for end in range(1, len(later)+1):
            early = detection_rules.score_energy(later.iloc[:end], model)
            pd.testing.assert_frame_equal(early, full.iloc[:end])
            pd.testing.assert_frame_equal(detection_rules.cusum_scores(early.residual_score), chart.iloc[:end])

    def test_cusum_validates_limits_and_keeps_empty_schema(self):
        empty = pd.Series([], index=pd.DatetimeIndex([]), dtype=float)
        for allowance, limit in [(-1.,5.), (np.nan,5.), (.5,0.), (.5,np.inf)]:
            with self.assertRaises(ValueError):
                detection_rules.cusum_scores(empty, allowance=allowance, decision_limit=limit)
        result = detection_rules.cusum_scores(empty)
        self.assertTrue(result.empty)
        self.assertEqual(result.columns.tolist(), ['cusum_score', 'review_flag', 'evidence_start'])


class WarningRuleTests(unittest.TestCase):
    def readings(self, values, dates=None):
        index = pd.date_range("2026-04-01", periods=len(values)) if dates is None else pd.to_datetime(dates)
        return pd.Series(values, index=index, dtype=float)

    def test_warning_starts_on_third_day_and_keeps_confirmation_date(self):
        score = self.readings([2.1, 2.2, 2.3, 2.4, 0])
        result = persistent_warnings(score)
        self.assertEqual(result.Warning.tolist(), [False, False, True, True, False])
        self.assertTrue(result["Confirmation date"].iloc[:2].isna().all())
        self.assertEqual(result["Candidate onset"].iloc[2], score.index[0])
        self.assertEqual(result["Confirmation date"].iloc[3], score.index[2])
        self.assertEqual(result["Streak days"].tolist(), [1, 2, 3, 4, 0])

    def test_negative_change_has_its_own_direction(self):
        result = persistent_warnings(self.readings([-2.1, -2.2, -2.3]))
        self.assertTrue(result.Warning.iloc[-1])
        self.assertEqual(result.Direction.iloc[-1], "Below expected")

    def test_exact_limits_and_isolated_spike_do_not_confirm(self):
        for values in ([2, 2, 2], [-2, -2, -2], [0, 9, 0], [2.1, 2, 2.1]):
            with self.subTest(values=values):
                self.assertFalse(persistent_warnings(self.readings(values)).Warning.any())

    def test_direction_change_starts_a_new_streak(self):
        result = persistent_warnings(self.readings([3, 3, -3, -3, -3]))
        self.assertEqual(result.Warning.tolist(), [False, False, False, False, True])
        self.assertEqual(result["Candidate onset"].iloc[-1], result.index[2])

    def test_missing_and_invalid_readings_reset_confirmation(self):
        for missing in [np.nan, np.inf, -np.inf]:
            with self.subTest(missing=missing):
                result = persistent_warnings(self.readings([3, 3, missing, 3, 3, 3]))
                self.assertEqual(result.Warning.tolist(), [False, False, False, False, False, True])
                self.assertEqual(result["Streak days"].iloc[2], 0)

    def test_calendar_gap_does_not_count_as_a_consecutive_day(self):
        score = self.readings([3, 3, 3, 3, 3], ["2026-04-01", "2026-04-02", "2026-04-04", "2026-04-05", "2026-04-06"])
        result = persistent_warnings(score)
        self.assertEqual(result.Warning.tolist(), [False, False, False, False, True])
        self.assertEqual(result["Candidate onset"].iloc[-1], score.index[2])

    def test_excluded_readings_cannot_support_a_warning(self):
        score = self.readings([3, 3, 3, 3, 3])
        eligible = pd.Series([True, True, False, True, True], index=score.index)
        self.assertFalse(persistent_warnings(score.where(eligible)).Warning.any())

    def test_threshold_sensitivity_changes_eligibility(self):
        score = self.readings([1.8, 1.8, 1.8])
        self.assertTrue(persistent_warnings(score, threshold=1.5).Warning.iloc[-1])
        self.assertFalse(persistent_warnings(score, threshold=2.0).Warning.any())

    def test_warning_replay_does_not_use_future_values(self):
        score = self.readings([3, 3, 3, 3, np.nan, -3, -3, -3])
        full = persistent_warnings(score)
        for end in range(1, len(score) + 1):
            pd.testing.assert_frame_equal(persistent_warnings(score.iloc[:end]), full.iloc[:end], check_dtype=False)

    def test_replay_before_any_change_keeps_missing_direction_identical(self):
        score = self.readings([0, 0, 3, 3, 3])
        early = persistent_warnings(score.iloc[:2])
        full = persistent_warnings(score).iloc[:2]
        pd.testing.assert_frame_equal(early, full, check_dtype=False)

    def test_ewma_uses_reference_start_and_weight_point_two(self):
        result = ewma_scores(self.readings([2, 2, 2]), initial=0)
        np.testing.assert_allclose(result, [0.4, 0.72, 0.976])

    def test_ewma_resets_after_missing_value_and_calendar_gap(self):
        result = ewma_scores(self.readings([2, np.nan, 2]), initial=0)
        self.assertTrue(np.isnan(result.iloc[1]))
        np.testing.assert_allclose(result.iloc[[0, 2]], [0.4, 0.4])
        gap = self.readings([2, 2], ["2026-04-01", "2026-04-03"])
        np.testing.assert_allclose(ewma_scores(gap, initial=0), [0.4, 0.4])

    def test_ewma_replay_does_not_use_future_values(self):
        score = self.readings([2, 2, np.nan, -2, -2, -2])
        full = ewma_scores(score, initial=0)
        for end in range(1, len(score) + 1):
            pd.testing.assert_series_equal(ewma_scores(score.iloc[:end], initial=0), full.iloc[:end])

    def test_duplicate_or_unordered_dates_are_rejected(self):
        for dates in (["2026-04-01", "2026-04-01"], ["2026-04-02", "2026-04-01"]):
            score = self.readings([3, 3], dates)
            for rule in [persistent_warnings, ewma_scores]:
                with self.subTest(dates=dates, rule=rule):
                    with self.assertRaises(ValueError):
                        rule(score)

    def test_invalid_threshold_and_reference_start_are_rejected(self):
        score = self.readings([3, 3, 3])
        for limit in [0, -1, np.nan, np.inf]:
            with self.assertRaises(ValueError):
                persistent_warnings(score, threshold=limit)
        with self.assertRaises(ValueError):
            ewma_scores(score, initial=np.nan)

    def test_empty_input_keeps_the_output_schema(self):
        score = self.readings([])
        result = persistent_warnings(score)
        self.assertTrue(result.empty)
        self.assertEqual(result.columns.tolist(), ["Candidate onset", "Confirmation date", "Direction", "Streak days", "Warning"])
        self.assertTrue(ewma_scores(score).empty)


if __name__ == "__main__":
    unittest.main()
