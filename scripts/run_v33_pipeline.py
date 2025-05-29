import json
from core.backtest_mc import monte_carlo
from core.wheel_generator import gen_wheels
from core.core_pool import build_core_pool
import numpy as np
core = build_core_pool(list(np.arange(39)),0.4)
wheels = gen_wheels(core)
kpi = monte_carlo(core,wheels)
with open('outputs/result.json','w') as f: json.dump({'core':core,'wheels':wheels,'kpi':kpi},f)
print('Done')
