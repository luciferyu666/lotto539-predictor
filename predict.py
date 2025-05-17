
import argparse, random
from pathlib import Path
from lotto_v24_predictor import data_loader, feature_extractor, neural_net, rl_agent, optimizer, wheel_builder

def main(dataset_path: str, period: str):
    draws = data_loader.load_draws(dataset_path)
    feats = feature_extractor.extract_features(draws)
    scorer = neural_net.SimpleHeuristicScorer(feats)

    scores = {n: scorer.score(n) for n in range(1, 40)}
    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Adaptive-Core sizing
    sigma_h = feats['z'][1] * 0  # use dummy variance, already computed below
    freq_vals = list(feats['freq'].values())
    sigma_h = (max(freq_vals) - min(freq_vals)) / max(freq_vals)
    K = 16 if sigma_h < 0.20 else 15
    core_pool = [n for n, _ in ranking[:K]]

    # Guards
    cold_low = min(range(1, 9), key=lambda n: feats['cold_gap'][n])
    hot_high = max(range(34, 40), key=lambda n: feats['freq'][n])
    core_pool = list(set(core_pool + [cold_low, hot_high]))

    # Evolution search
    elites = optimizer.pso_ga_search(core_pool, [hot_high], [cold_low])

    wheels = wheel_builder.build_wheels(elites, cold_low, hot_high)

    print(f"Core Pool (K={len(core_pool)}):", sorted(core_pool))
    print("10 Wheels:")
    for w in wheels:
        print(' '.join(f"{n:02d}" for n in w))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', required=True)
    ap.add_argument('--period', required=True)
    args = ap.parse_args()
    main(args.data, args.period)
