
import argparse, json, os, numpy as np, random, yaml, hashlib, sys

def monte_carlo(core, wheels, n=50000):
    core_set=set(core)
    draws=np.random.randint(0,39,(n,5))
    core_hits=((draws[...,None]==np.array(list(core_set))).any(-1)).sum(-1)
    k1=(core_hits>=1).mean()
    k2=(core_hits>=2).mean()
    k3=(core_hits>=3).mean()
    roi=k2*25+k3*250-50
    return {'Hit@Core':float(k1),'Hit2':float(k2),'Hit3+':float(k3),'ROI':float(roi)}

def kpi_pass(kpi, gate):
    return all([kpi['Hit@Core']>=gate['hit_core'],
                kpi['Hit2']>=gate['hit2'],
                kpi['Hit3+']>=gate['hit3_plus'],
                kpi['ROI']>gate['roi']])

def main(issue):
    random.seed(42); np.random.seed(42)
    scores=np.random.rand(39)
    ranking=list(np.argsort(scores)[::-1])
    core_pool=list(map(int,sorted(ranking[:15])))
    high=core_pool[:len(core_pool)//2]; low=core_pool[len(core_pool)//2:]
    wheels=[list(map(int,sorted(random.sample(high,5)))) for _ in range(6)]+[list(map(int,sorted(random.sample(high,3)+random.sample(low,2)))) for _ in range(4)]
    gate=yaml.safe_load(open('configs/monitor.yaml'))
    kpi=monte_carlo(core_pool, wheels)
    status='PASS' if kpi_pass(kpi, gate) else 'FAIL'
    os.makedirs('outputs', exist_ok=True)
    output={'issue':issue,'core_pool':core_pool,'wheels':wheels,'kpi':kpi,'status':status}
    with open(f'outputs/{issue}_result.json','w') as f: json.dump(output,f,indent=2)
    # simple txt report
    with open(f'outputs/{issue}_report.txt','w',encoding='utf-8') as f:
        f.write(f"核心池: {core_pool}\n")
        for i,w in enumerate(wheels,1):
            f.write(f"W{i:02d}: {w}\n")
        f.write(str(kpi)+'\n狀態:'+status+'\n')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--issue',type=int,required=True)
    args=ap.parse_args()
    main(args.issue)
