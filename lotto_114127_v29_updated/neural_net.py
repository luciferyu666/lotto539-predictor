
"""
neural_net.py
~~~~~~~~~~~~~
簡化版號碼潛力評分模型。

* 特徵：頻率 (long / short)、最近間隔期數、Mid‑Cold flag
* 模型：LogisticRegression (可替換為 BiGRU + Attention)
"""
from __future__ import annotations
import numpy as np, collections, statistics, pandas as pd
from sklearn.linear_model import LogisticRegression

class SimpleLottoScorer:
    def __init__(self):
        self.model = LogisticRegression(max_iter=1000)
        self.label_numbers: set[int] = set()

    def _build_feature_frame(self, records: list[tuple[str, list[int]]]) -> pd.DataFrame:
        # 建立 39×N 特徵
        long_win, short_win = 1500, 300
        if len(records) < long_win:
            long_win = len(records)
        def freq(window):
            cnt=collections.Counter()
            for _,nums in records[-window:]:
                cnt.update(nums)
            total=window*5
            return {n:cnt[n]/total for n in range(1,40)}
        f_long=freq(long_win)
        f_short=freq(short_win)
        # 最近間隔
        last_seen={n:0 for n in range(1,40)}
        for idx,(p,nums) in enumerate(reversed(records),1):
            for n in nums:
                if last_seen[n]==0:
                    last_seen[n]=idx
        μ=sum(f_long.values())/39
        σ=statistics.stdev(f_long.values())
        midcold={n for n,f in f_long.items() if abs(f-μ) <=0.5*σ}
        rows=[]
        for n in range(1,40):
            rows.append({
                "num":n,
                "freq_long":f_long[n],
                "freq_short":f_short[n],
                "recency":last_seen[n],
                "midcold_flag":1 if n in midcold else 0,
            })
        return pd.DataFrame(rows).set_index("num")

    def fit(self, records: list[tuple[str, list[int]]]) -> None:
        df=self._build_feature_frame(records)
        # 標籤 = 下一期是否中獎 (滑動視窗簡易學習)
        y=[]
        for _,nums in records[-1:]:
            self.label_numbers=set(nums)
        y=[1 if n in self.label_numbers else 0 for n in df.index]
        self.model.fit(df.values,y)

    def score(self, records: list[tuple[str, list[int]]]) -> dict[int,float]:
        df=self._build_feature_frame(records)
        proba=self.model.predict_proba(df.values)[:,1]
        return {n:float(p) for n,p in zip(df.index,proba)}
