"""Export saved analysis results for the static dashboard; never change source files."""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = {
    'replay': ROOT/'output/detection/energy_replay.csv',
    'models': ROOT/'output/detection/energy_models.csv',
    'months': ROOT/'output/historical/plant_months.csv',
    'unusual': ROOT/'output/historical/unusual_plant_readings.csv',
    'recovery': ROOT/'output/historical/recovery_reconciliation.csv',
    'performance': ROOT/'Dataset/plant_daily_performance.csv',
}
hashes = {path: hashlib.sha256(path.read_bytes()).hexdigest() for path in SOURCES.values()}

def rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))

def number(value):
    if value in ['', 'NULL', '/']:
        return None
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('Non-finite source value')
    return result

data = {key: rows(path) for key,path in SOURCES.items()}
plants = []
for name in ['Plant A', 'Plant B']:
    model = next(row for row in data['models'] if row['Plant'] == name)
    readings = []
    for row in sorted((r for r in data['replay'] if r['Plant'] == name), key=lambda r:r['date']):
        eligible = row['eligible'] == 'True'
        actual, output = number(row['recorded_electricity_kwh']), number(row['effluent_volume_m3'])
        assert actual is not None and actual >= 0 and output is not None and output > 0
        expected = number(row['expected_electricity_kwh'])
        excess = number(row['excess_electricity_kwh'])
        if eligible:
            assert math.isclose(expected, float(model['slope_kwh_per_m3'])*output, rel_tol=1e-12)
            assert math.isclose(actual-expected, excess, abs_tol=1e-8)
        else:
            assert expected is None and excess is None and row['cusum_score'] == ''
        readings.append({'date':row['date'], 'actual':actual, 'output':output, 'expected':expected,
            'excess':excess, 'eligible':eligible, 'score':number(row['residual_score']),
            'cusum':number(row['cusum_score']), 'review':row['review_flag']=='True', 'reason':row['exclusion_reason']})
    assert len(readings)==31 and len({row['date'] for row in readings})==31
    month = next(row for row in data['months'] if row['plant']==name and row['Month']=='2026-08')
    assert sum(row['actual'] for row in readings)==float(month['Electricity_kwh'])
    assert sum(row['output'] for row in readings)==float(month['Water_m3'])
    plants.append({'name':name, 'readings':readings,
        'reference':{'specificEnergy':float(model['slope_kwh_per_m3']), 'scale':float(model['residual_scale_kwh']),
            'allowance':float(model['allowance_k']), 'limit':float(model['decision_limit_h']),
            'outputMin':float(model['output_min_m3']), 'outputMax':float(model['output_max_m3'])},
        'months':[{'month':r['Month'], 'electricity':float(r['Electricity_kwh']), 'output':float(r['Water_m3']),
            'specificEnergy':float(r['Specific energy kwh_m3'])} for r in data['months'] if r['plant']==name]})

indicator_names = {'Calculated recovery %':('Recovery','%'), 'Calculated specific energy':('Specific energy','kWh/m³'),
    'effluent_conductivity_us_cm':('Conductivity','µS/cm'), 'effluent_ph':('pH','')}
outliers = [{'plant':r['Plant'], 'date':r['date'], 'indicator':indicator_names[r['Indicator']][0],
    'unit':indicator_names[r['Indicator']][1], 'value':number(r['Value']), 'direction':r['Direction']} for r in data['unusual']]
missing_conductivity = [{'plant':r['plant'], 'date':r['date']} for r in data['performance'] if number(r['effluent_conductivity_us_cm']) is None]
payload = {'plants':plants, 'outliers':outliers, 'quality':{'missingConductivity':missing_conductivity,
    'recoveryDifferences':[{'plant':r['plant'], 'date':r['date'], 'reported':float(r['reported_recovery_rate'])*100,
        'calculated':float(r['Calculated recovery %'])} for r in data['recovery']]},
    'sources':[{'path':str(path.relative_to(ROOT)).replace('\\','/'), 'sha256':hashes[path]} for path in SOURCES.values()]}
assert len(outliers)==15 and len(missing_conductivity)==8 and len(payload['quality']['recoveryDifferences'])==8
target = ROOT/'frontend/src/data/plant-data.json'
target.parent.mkdir(parents=True, exist_ok=True)
temporary = target.with_suffix('.json.tmp')
temporary.write_text(json.dumps(payload,ensure_ascii=False,allow_nan=False,indent=2), encoding='utf-8')
temporary.replace(target)
assert all(hashlib.sha256(path.read_bytes()).hexdigest()==digest for path,digest in hashes.items())
print('Exported 62 daily comparisons, 4 monthly records and 15 historical outliers; sources unchanged.')
