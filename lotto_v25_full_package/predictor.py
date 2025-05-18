
import argparse, pandas as pd, numpy as np, json
from core_pool import build_core_pool
from optimizer import pso_ga
from wheel_generator import generate_wheel
from neural_net import load_or_train
from feature_extraction import dual_window_counts

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--history', default='data/539_history.txt')
    parser.add_argument('--draw', type=int, required=True)
    parser.add_argument('--weights', default='models/basenet_v25.h5')
    args=parser.parse_args()

    df=pd.read_csv(args.history, sep=' ', header=None,
                   names=['period','n1','n2','n3','n4','n5'])
    core_pool, scores, meta=build_core_pool(df)

    # Neural‑Net scoring demo (optional fast path)
    X=np.eye(39)[[n-1 for n in core_pool]]
    y=np.ones(len(core_pool))
    model=load_or_train(args.weights, X, y)
    nn_scores=dict(zip(core_pool, model.predict(X, verbose=0).flatten()))
    # Merge NN scores with previous scores (simple average)
    merged_scores={n:(scores[n]+nn_scores.get(n,0))/2 for n in core_pool}

    combos=pso_ga(core_pool, merged_scores)
    wheel=generate_wheel(core_pool, args.draw, n_combos=len(combos))

    report={'draw':args.draw,'core_pool':core_pool,'wheel':wheel,'meta':meta}
    with open(f'prediction_{args.draw}.json','w') as f:
        json.dump(report,f,indent=2)
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
