from datetime import timedelta

import numpy as np
import pandas as pd


def _validate_scores(scores):
    dates = scores.index
    if not isinstance(dates, pd.DatetimeIndex) or dates.hasnans:
        raise ValueError("Scores must have valid daily dates")
    if not dates.normalize().is_unique or not dates.is_monotonic_increasing:
        raise ValueError("Score dates must be unique and in increasing order")


def persistent_warnings(scores, threshold=2.0):
    """Confirm a change on its third consecutive valid calendar day."""
    _validate_scores(scores)
    if not np.isfinite(threshold) or threshold <= 0:
        raise ValueError("The warning threshold must be finite and positive")
    rows = []
    previous_date = previous_direction = None
    onset = confirmation = pd.NaT
    streak = 0
    for date, score in scores.items():
        direction = None
        if pd.notna(score) and np.isfinite(score):
            direction = "Above expected" if score > threshold else "Below expected" if score < -threshold else None
        consecutive = previous_date is not None and date.date() - previous_date.date() == timedelta(days=1)
        if direction is None:
            streak, onset, confirmation = 0, pd.NaT, pd.NaT
        elif consecutive and direction == previous_direction:
            streak += 1
        else:
            streak, onset, confirmation = 1, date, pd.NaT
        if streak == 3:
            confirmation = date
        rows.append((onset, confirmation, direction, streak, streak >= 3))
        previous_date, previous_direction = date, direction
    return pd.DataFrame(rows, index=scores.index, columns=["Candidate onset", "Confirmation date", "Direction", "Streak days", "Warning"]).astype({"Direction": "string"})


def ewma_scores(scores, initial=0.0):
    """Use weight 0.2; reset to the reference start after a gap or exclusion."""
    _validate_scores(scores)
    if not np.isfinite(initial):
        raise ValueError("The EWMA reference start must be finite")
    values = []
    state, previous_date = initial, None
    for date, score in scores.items():
        if previous_date is None or date.date() - previous_date.date() != timedelta(days=1):
            state = initial
        if pd.isna(score) or not np.isfinite(score):
            values.append(np.nan)
            state = initial
        else:
            state = 0.2 * score + 0.8 * state
            values.append(state)
        previous_date = date
    return pd.Series(values, index=scores.index, dtype=float, name="EWMA score")


def fit_energy_baseline(reference, method='regression'):
    """Fit one plant's fixed electricity/output reference; adequacy needs separate evaluation."""
    _validate_scores(reference)
    if method not in ['regression', 'specific_energy']:
        raise ValueError("Choose regression or specific_energy")
    x = reference['effluent_volume_m3'].to_numpy(dtype=float)
    y = reference['daily_electricity_kwh'].to_numpy(dtype=float)
    if len(x) < 3 or not np.isfinite(x).all() or not np.isfinite(y).all() or (x <= 0).any() or (y < 0).any():
        raise ValueError("Reference needs at least three finite paired days with positive output and nonnegative energy")
    if np.ptp(x) == 0:
        raise ValueError("Reference needs varying output")
    if method == 'specific_energy':
        intercept, slope = 0., y.sum()/x.sum()
    else:
        design = np.column_stack([np.ones(len(x)), x])
        coefficients, _, rank, _ = np.linalg.lstsq(design, y, rcond=None)
        if rank != 2:
            raise ValueError("Reference output does not support a regression fit")
        intercept, slope = coefficients
    if slope <= 0 or (intercept + slope*x <= 0).any():
        raise ValueError("Reference needs varying output and a positive, physically plausible prediction relationship")
    residual = y - (intercept + slope*x)
    scale = 1.4826 * np.median(np.abs(residual - np.median(residual)))
    if not np.isfinite(scale) or scale <= np.finfo(float).eps * max(1., np.max(np.abs(y))) * 100:
        raise ValueError("Reference has no usable residual scale")
    return {'baseline_method': method, 'intercept_kwh': float(intercept), 'slope_kwh_per_m3': float(slope),
            'residual_scale_kwh': float(scale), 'output_min_m3': float(x.min()),
            'output_max_m3': float(x.max()), 'trained_through': reference.index[-1].isoformat(),
            'training_days': len(x)}


def score_energy(readings, model):
    """Score only later, valid days within the training output range; never refit."""
    _validate_scores(readings)
    if (readings.index.normalize() <= pd.Timestamp(model['trained_through']).normalize()).any():
        raise ValueError("Evaluation dates must follow the reference period")
    parameters = [model[key] for key in ['intercept_kwh', 'slope_kwh_per_m3', 'residual_scale_kwh', 'output_min_m3', 'output_max_m3']]
    if not np.isfinite(parameters).all() or model['residual_scale_kwh'] <= 0 or model['slope_kwh_per_m3'] <= 0 or not 0 < model['output_min_m3'] < model['output_max_m3']:
        raise ValueError("Energy baseline parameters are invalid")
    volume = readings['effluent_volume_m3'].astype(float)
    energy = readings['daily_electricity_kwh'].astype(float)
    valid = np.isfinite(volume) & np.isfinite(energy) & volume.gt(0) & energy.ge(0)
    in_range = volume.between(model['output_min_m3'], model['output_max_m3'])
    expected = model['intercept_kwh'] + model['slope_kwh_per_m3'] * volume
    eligible = valid & in_range & expected.gt(0)
    excess = energy - expected
    reason = pd.Series('', index=readings.index, dtype='string')
    reason.loc[~in_range] = 'Outside reference output range'
    reason.loc[~valid] = 'Invalid electricity or output'
    reason.loc[valid & in_range & ~expected.gt(0)] = 'Nonpositive expected electricity'
    return pd.DataFrame({'effluent_volume_m3': volume, 'recorded_electricity_kwh': energy,
                         'expected_electricity_kwh': expected.where(eligible),
                         'excess_electricity_kwh': excess.where(eligible),
                         'residual_score': (excess/model['residual_scale_kwh']).where(eligible),
                         'eligible': eligible, 'exclusion_reason': reason})


def cusum_scores(scores, allowance=0.5, decision_limit=5.0):
    """Positive CUSUM; reset after a crossing, calendar gap or unavailable reading."""
    _validate_scores(scores)
    if not np.isfinite(allowance) or allowance < 0 or not np.isfinite(decision_limit) or decision_limit <= 0:
        raise ValueError("CUSUM needs a finite nonnegative allowance and positive decision limit")
    rows = []
    state, previous_date, onset, crossed = 0., None, pd.NaT, False
    for date, score in scores.items():
        if crossed or previous_date is None or date.date()-previous_date.date() != timedelta(days=1):
            state, onset = 0., pd.NaT
        crossed = False
        if pd.isna(score) or not np.isfinite(score):
            rows.append((np.nan, False, pd.NaT))
            state, onset = 0., pd.NaT
        else:
            if state == 0:
                onset = date
            state = max(0., state + score - allowance)
            if state == 0:
                onset = pd.NaT
            crossed = state > decision_limit
            rows.append((state, crossed, onset))
        previous_date = date
    return pd.DataFrame(rows, index=scores.index, columns=['cusum_score', 'review_flag', 'evidence_start']).astype(
        {'cusum_score': float, 'review_flag': bool, 'evidence_start': 'datetime64[ns]'})
