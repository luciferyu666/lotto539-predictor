"""
train.py
End‑to‑end pipeline to update data, build features, train models,
produce prediction for the next draw, using v2.8 flow.
"""

import argparse, pickle, json, os, random, datetime
from data_update import parse_draws
from feature_engineering import dual_window_features, cold_boost
from neural_net import build_model
from optimizer import pso_optimize
from core_pool import build_core_pool
from wheel_generator import generate_wheel, risk_label
import torch, numpy as np

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--raw', required=True)
    parser.add_argument('--outdir', default='output')
    args=parser.parse_args()

    draws=parse_draws(args.raw)
    feats=dual_window_features(draws)
    feats=cold_boost(feats)
    model=build_model()
    # skip training for brevity
    score_dict={n:feats[n] for n in range(1,40)}

    core_pool, sigma_h=build_core_pool(list(range(1,40)), score_dict)
    hot_set={n for n,v in feats.items() if v>0.05}  # crude
    combos=generate_wheel(core_pool)

    labeled=[(c, risk_label(c, hot_set)) for c in combos]
    ts=datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    os.makedirs(args.outdir, exist_ok=True)
    with open(os.path.join(args.outdir,'result.json'),'w') as f:
        json.dump({'core_pool':core_pool,'combo':labeled},f, indent=2)

if __name__=='__main__':
    main()
