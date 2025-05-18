# lotto_v25_predictor

Implementation of v2.5 prediction pipeline for Taiwan Lotto 539.

## Key Updates
* Dual-Window (334 + 1500) heat trend fusion
* Mid‑Segment Boost (21–30) weight 1.3 in neural features
* PPO reward updated with `mid_segment_hit` & `segment_cov_bonus = 0.25`
* Fitness v2.5 adds `MidBoostScore` weight
* Adaptive-Core 2.5 with σₕ dual-stage expansion
* Dual-Extreme Guard (#03 low, #35/#38 high rotation)

## CLI
```bash
python predictor.py --draw 114122
```
