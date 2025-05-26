# Lotto 539 v3.0 Deployment Template (Period 114128)

This template scaffolds the folder structure, configuration, and execution script required to reproduce the **v3.0 Reinforcement Learning × PSO** prediction workflow described in *今彩539強化學習_PSO_選號全新流程(最終整合版)_18.txt*.

## Directory Layout

```
lotto539_v30_template/
├─ config.yaml              # Full set of v3.0 hyper‑parameters
├─ run_prediction.sh        # One‑shot pipeline runner
├─ Dockerfile               # Minimal container recipe
└─ README_DEPLOY.md         # This file
```

> **Prerequisites**  
> * Python ≥ 3.10  
> * `pip install -r requirements.txt` (see main repo)  
> * The project root should be **cloned at `~/lotto539-predictor`** as per the GitHub repository.

## Quick Start

```bash
cd lotto539_v30_template
./run_prediction.sh
```

The script will:

1. **Append** draw *114127* to the historical dataset.
2. **Re‑compute** Dual‑Window 2.3 features.
3. **Infer** BiGRU × Attention NN scores (warm‑fit if no weights).
4. **Train** PPO v3.0 agent and **evolve** candidate pools via DE/GA/PSO.
5. **Consolidate** an Elastic‑K core pool (dynamic 14–16 numbers).
6. **Generate** 10 Wheel 2.6 betting sets (High/Low risk tiers).
7. **Validate** KPIs with 150 k Monte‑Carlo samples.
8. **Package** reports, model weights, and wheel outputs to `output/package/`.

## Docker Usage

```bash
docker build -t lotto539:v3 .
docker run --rm -v $(pwd):/app lotto539:v3 ./run_prediction.sh
```

The container exposes **port 8888** for optional Jupyter access.

## KPI Targets

* **Hit@Core ≥ 78 %**  
* **Hit₂ ≥ 70 %**  
* **Hit₃⁺ ≥ 42 %**  
* **Rolling ROI (12 draw) > 0 %**

Tune hyper‑parameters in `config.yaml` if any metric is below target.