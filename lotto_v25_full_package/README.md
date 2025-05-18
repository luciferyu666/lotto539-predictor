
# lotto_v25_predictor (Full Spec)

> **第 114122 期今彩 539 – v2.5 完整實作**

此版本依《v2.5 執行版本》與一致性檢核缺口全面補強：

* **BaseNet + Mid‑Boost**：TensorFlow Keras 建構，可自動偵測 `.h5` 權重；若不存在則自動訓練 3 個 epoch 以利快速產生範例權重 (示範)。
* **PPO 強化學習**：自訂 `reward_fn` 含 `mid_segment_hit` 與 `segment_cov_bonus`。
* **Fitness v2.5**：PSO × GA 雙演化器，加入 `MidBoostScore` 權重。
* **Wheel 2‑Stage**：Mid Coverage → Dual‑Guard (#03 固定；#35/#38 依期數奇偶切換)，並標記 `risk_level` (low/med/high)。
* **Hit₂ 指標**：最近 50 期中兩球覆蓋率，用於核心池排序。
* **pytest**：`tests/` 內含 smoke‑test，CI 可於 30 秒內跑完。

## Quick‑Start

```bash
pip install -r requirements.txt
python predictor.py --draw 114122
pytest -q
```
