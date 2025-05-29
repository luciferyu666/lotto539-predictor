
import argparse, json, os, numpy as np
from core.core_pool import build_core_pool
from core.wheel_generator import gen_wheels
from scripts.backtest_mc import monte_carlo_eval
from core.kpi_monitor import kpi_pass
from core.rebalancer import re_balance, meta_pso

def main(issue:int):
    np.random.seed(42)
    scores = np.random.rand(39)
    ranking = list(np.argsort(scores)[::-1])
    core_pool = build_core_pool(ranking, scores)
    wheels = gen_wheels(core_pool)
    kpi = monte_carlo_eval(core_pool, wheels)
    if not kpi_pass(kpi):
        wheels = re_balance(wheels, scores)
        wheels = meta_pso(wheels, scores)
        kpi = monte_carlo_eval(core_pool, wheels)
    status = 'PASS' if kpi_pass(kpi) else 'FAIL'
    os.makedirs('outputs', exist_ok=True)
    json.dump({'issue':issue,'core_pool':core_pool,'wheels':wheels,'kpi':kpi,'status':status},
              open(f'outputs/{issue}_m6_output.json','w'), ensure_ascii=False, indent=2)
    print('Final KPI', kpi, status)

if __name__=='__main__':
    import sys
    ap=argparse.ArgumentParser()
    ap.add_argument('--issue',type=int,required=True)
    args=ap.parse_args()
    main(args.issue)
