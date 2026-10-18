"""Apply the captured cloud migration without refitting any estimator."""
import json
import joblib
import pandas as pd
from agrocebada.common import ROOT, ARTIFACTS, code_hash, sha256, write_json
from agrocebada.inference import Predictor, verify_artifacts

snapshot = ARTIFACTS / 'versions/cloud-portability-2026-10-18'
state = json.loads((snapshot / 'before.json').read_text(encoding='utf-8'))
current = {p.name: sha256(p) for p in (ROOT / 'src/agrocebada').glob('*.py')}
assert current.keys() == state['source_hashes'].keys()
changed = {k for k in current if current[k] != state['source_hashes'][k]}
assert changed == {'cli.py', 'inference.py'}, changed
before_configs = json.loads((snapshot / 'feature-configs.json').read_text())
after_configs = json.loads((ROOT / 'data/processed/feature-configs.json').read_text())
assert after_configs == {k: v.replace('\\', '/') for k, v in before_configs.items()}
records = {}
for name in ['selected', 'official']:
    model_path = ARTIFACTS / f'model_{name}.joblib'
    contract_path = ARTIFACTS / f'contract_{name}.json'
    assert sha256(model_path) == state['models'][name]
    contract = json.loads(contract_path.read_text(encoding='utf-8'))
    assert contract['code_hash'] == state['code_hash']
    bundle = joblib.load(model_path)
    assert bundle['contract']['code_hash'] == state['code_hash']
    bundle['contract']['code_hash'] = code_hash()
    contract['code_hash'] = code_hash()
    joblib.dump(bundle, model_path)
    contract['model_hash'] = sha256(model_path)
    write_json(contract_path, contract)
    predictor = Predictor(name)
    actual = predictor.predict(predictor.master.ID_POLIGONO.tolist())
    expected = pd.read_parquet(snapshot / f'predictions_{name}.parquet')
    pd.testing.assert_frame_equal(actual, expected, check_exact=True)
    records[name] = {'before_model_hash': state['models'][name], 'after_model_hash': contract['model_hash'], 'parcels_compared': len(actual), 'predictions_and_intervals_exactly_equal': True}
write_json(ARTIFACTS / 'cloud-compatibility.json', {
    'date': '2026-10-18', 'reason': 'POSIX feature paths and Python security-patch compatibility; exact library pins retained',
    'changed_sources': sorted(changed), 'before_code_hash': state['code_hash'], 'after_code_hash': code_hash(),
    'retrained': False, 'backup': snapshot.relative_to(ROOT).as_posix(), 'models': records,
})
print(json.dumps(verify_artifacts(), indent=2))
