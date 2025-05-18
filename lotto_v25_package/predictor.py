import argparse, json, random, numpy as np, pandas as pd, pathlib, math

from feature_extraction import compute_features
from core_pool import build_core_pool
from wheel_generator import generate_wheel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--history', default='data/539_history.txt')
    parser.add_argument('--draw', type=int, required=True)
    args = parser.parse_args()

    df = pd.read_csv(args.history, sep=' ', header=None,
                     names=['period','n1','n2','n3','n4','n5'])
    core_pool, meta = build_core_pool(df)
    wheel = generate_wheel(core_pool)

    print('Core Pool:', core_pool)
    print('Combos:')
    for c in wheel:
        print(' '.join(f'{n:02d}' for n in c))

    report={'draw':args.draw, 'core_pool':core_pool, 'combos':wheel, 'meta':meta}
    with open(f'prediction_{args.draw}.json','w') as f:
        json.dump(report,f,indent=2)

if __name__ == '__main__':
    main()
