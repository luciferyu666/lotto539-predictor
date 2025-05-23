"""
data_update.py
v2.8 Update – 2025‑05‑23

Utility to append latest draw results to historical dataset and
rebuild the sliding‑window training feature file.

Usage:
    python data_update.py --raw_file raw.txt --window 334
"""
import argparse, hashlib, json, os, datetime, collections, pickle

def parse_draws(file_path):
    draws=[]
    with open(file_path,'r',encoding='utf-8') as f:
        for line in f:
            parts=line.strip().split()
            if len(parts)==6:
                period=int(parts[0])
                nums=list(map(int,parts[1:]))
                draws.append({'period':period,'nums':nums})
    return draws

def sliding_window(draws, window=334):
    return draws[-window:]

def compute_features(draws_window):
    # Simple frequency feature set; extend with Dual‑Window 2.1, ColdBoost 3.0 etc.
    from collections import Counter
    freq=Counter()
    for d in draws_window:
        freq.update(d['nums'])
    total=len(draws_window)*5
    features={n:freq.get(n,0)/total for n in range(1,40)}
    return {'freq':features,'window':len(draws_window)}

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        h.update(f.read())
    return h.hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--raw_file',required=True)
    parser.add_argument('--window',type=int,default=334)
    parser.add_argument('--out',default='features.pkl')
    args=parser.parse_args()

    draws=parse_draws(args.raw_file)
    subset=sliding_window(draws,args.window)
    feats=compute_features(subset)
    meta={'generated':datetime.datetime.utcnow().isoformat(),
          'raw_sha256':sha256(args.raw_file)}
    with open(args.out,'wb') as f:
        pickle.dump({'meta':meta,'features':feats},f)
    print(f'Saved {args.out}')

if __name__=='__main__':
    main()
