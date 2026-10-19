"""Reconcile imported artifact metadata after applying cloud-only compatibility changes."""
import json,subprocess
import joblib
import pandas as pd
from agrocebada.common import ROOT,ARTIFACTS,code_hash,sha256,write_json
from agrocebada.inference import Predictor,verify_artifacts

snapshot=ARTIFACTS/'versions/upstream-sync-89b2f67'
state=json.loads((snapshot/'source.json').read_text(encoding='utf-8'))
current={p.name:sha256(p) for p in (ROOT/'src/agrocebada').glob('*.py')}
assert current.keys()==state['source_hashes'].keys()
changed=sorted(k for k in current if current[k]!=state['source_hashes'][k])
assert changed==['cli.py','inference.py'],changed
records={}
for name in ['selected','official']:
    model_path=ARTIFACTS/f'model_{name}.joblib'
    contract_path=ARTIFACTS/f'contract_{name}.json'
    contract=json.loads(contract_path.read_text(encoding='utf-8'))
    source_embedded_code_hash=joblib.load(snapshot/f'model_{name}.joblib')['contract'].get('code_hash')
    if sha256(model_path)==state['models'][name]:
        assert contract['code_hash']==state['code_hash']
        bundle=joblib.load(model_path)
        bundle['contract']['code_hash']=code_hash()
        contract['code_hash']=code_hash()
        joblib.dump(bundle,model_path)
        contract['model_hash']=sha256(model_path)
        write_json(contract_path,contract)
    else:
        # A previous interrupted run may already have reconciled this route.
        assert contract['code_hash']==code_hash()
        assert contract['model_hash']==sha256(model_path)
    predictor=Predictor(name)
    actual=predictor.predict(predictor.master.ID_POLIGONO.tolist())
    expected=pd.read_parquet(snapshot/f'predictions_{name}.parquet')
    pd.testing.assert_frame_equal(actual,expected,check_exact=True)
    records[name]={'source_model_hash':state['models'][name],'cloud_model_hash':contract['model_hash'],'source_embedded_code_hash':source_embedded_code_hash,'parcels_compared':len(actual),'predictions_and_intervals_exactly_equal':True}
source_commit=subprocess.check_output(['git','-C',str(ROOT/'Reto-Cebada'),'rev-parse','HEAD'],text=True).strip()
write_json(ARTIFACTS/'upstream-cloud-compatibility.json',{'date':'2026-10-18','source_repository':'https://github.com/Elypsoon/Reto-Cebada','source_branch':state['source_branch'],'source_commit':source_commit,'source_code_hash':state['code_hash'],'cloud_code_hash':code_hash(),'cloud_changed_source_files':changed,'retrained':False,'models':records,'selected_model':'R08; precomputed estimates for the official parcels','included_research':['estratificacion-pyr-20261018','fisiologia-siniestros-20261018']})
print(json.dumps(verify_artifacts(),indent=2))
