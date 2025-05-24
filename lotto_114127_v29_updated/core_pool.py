
"""
core_pool.py
~~~~~~~~~~~~
Generate Elastic‑K 核心號碼池 (v2.9).

規則摘要
--------
* Dual‐Window 統計：長窗 1500、短窗 300
* 冷熱分段：Hot > μ + 0.5σ、Cold < μ − 0.5σ
* Guard：{3, 35, 38, 32|34(動態)}
* Elastic‑K：12 ≤ K ≤ 16，Mid‑Cold Retention ≥ 15 %
"""

from __future__ import annotations
import collections, statistics, typing, random, pathlib, re

# ==============================
# 公用
# ==============================
HISTORY_PATTERN = re.compile(r"^(\d{6})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})\s+(\d{2})")

def load_history(path: str) -> list[tuple[str, list[int]]]:
    """讀取清洗後歷史檔，回傳 (period, [5 numbers]) 列表。"""
    records: list[tuple[str, list[int]]] = []
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            m = HISTORY_PATTERN.match(line.strip())
            if not m:
                continue
            period = m.group(1)
            nums = [int(m.group(i)) for i in range(2, 7)]
            records.append((period, nums))
    if not records:
        raise ValueError("History file empty or wrong format")
    return records

# ==============================
# 主要 API
# ==============================
def generate_core_pool(records: list[tuple[str, list[int]]],
                       k_target: int = 14,
                       guard_floating: int = 34) -> list[int]:
    """產出核心號碼池。"""
    long_win, short_win = 1500, 300
    if len(records) < long_win:
        long_win = len(records)
    # -------
    def _freq(window: int) -> dict[int, float]:
        cnt = collections.Counter()
        for _, nums in records[-window:]:
            cnt.update(nums)
        total = window * 5
        return {n: cnt[n] / total for n in range(1, 40)}
    freq_long = _freq(long_win)
    μ = sum(freq_long.values()) / 39
    σ = statistics.stdev(freq_long.values())
    hot = {n for n, f in freq_long.items() if f > μ + 0.5 * σ}
    cold = {n for n, f in freq_long.items() if f < μ - 0.5 * σ}
    mid_cold = set(range(1, 40)) - hot - cold
    # -------
    guards = {3, 35, 38, guard_floating}
    pool = set(guards)
    # Hot：取前 4
    pool.update(sorted(hot, key=lambda n: -freq_long[n])[:4])
    # Mid‑Cold：取低頻 6
    pool.update(sorted(mid_cold, key=lambda n: freq_long[n])[:6])
    # Cold：取低頻 3
    pool.update(sorted(cold, key=lambda n: freq_long[n])[:3])
    # 補齊
    for n in range(1, 40):
        if len(pool) >= k_target:
            break
        pool.add(n)
    core = sorted(pool)[:k_target]
    # 驗證 Mid‑Cold Retention
    mid_ratio = len([n for n in core if n in mid_cold]) / len(core)
    if mid_ratio < 0.15:
        raise RuntimeError("Mid‑Cold retention below threshold")
    return core

if __name__ == "__main__":
    import argparse, json
    ap = argparse.ArgumentParser()
    ap.add_argument("history", help="清洗後歷史檔路徑")
    ap.add_argument("-k", type=int, default=14)
    args = ap.parse_args()
    recs = load_history(args.history)
    core = generate_core_pool(recs, k_target=args.k)
    print(json.dumps({"core_pool": core}, ensure_ascii=False, indent=2))
