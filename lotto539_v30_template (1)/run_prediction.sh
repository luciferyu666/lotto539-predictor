#!/usr/bin/env bash
# Run full v3.0 prediction pipeline for Lotto 539 — period 114128
set -euo pipefail

export PYTHONPATH=$(pwd)

python scripts/update_dataset.py --input data/clean_539_3251.txt --latest 114127
python scripts/recompute_features.py --config config.yaml
python scripts/neural_net.py --config config.yaml --mode infer
python scripts/rl_agent.py --config config.yaml --train
python scripts/optimizer.py --config config.yaml
python scripts/core_pool.py --config config.yaml
python scripts/wheel_generator.py --config config.yaml
python scripts/monte_carlo_kpi.py --config config.yaml
python scripts/package_results.py --config config.yaml --period 114128

echo "Prediction run complete. Check the output/package directory for deliverables."