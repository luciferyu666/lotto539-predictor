
import pandas as pd, json, pathlib, subprocess, sys, os

def test_predictor_runs(tmp_path):
    sample_history=str(pathlib.Path(__file__).parent/'../data/sample_history.txt')
    if not os.path.exists(sample_history):
        # generate tiny sample
        with open(sample_history,'w') as f:
            for i in range(1,101):
                nums=[f"{(i+j)%39+1:02d}" for j in range(5)]
                f.write(f"{100000+i} "+" ".join(nums)+"\n")
    out_json=tmp_path/'out.json'
    cmd=[sys.executable,'../predictor.py','--history',sample_history,'--draw','114122']
    subprocess.check_call(cmd,cwd=pathlib.Path(__file__).parent/'..')
    assert (pathlib.Path(__file__).parent/'../prediction_114122.json').exists()
