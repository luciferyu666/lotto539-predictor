
import pandas as pd, numpy as np
from util.constants import LONG_WINDOW, SHORT_WINDOW, MID_SEGMENT

def dual_window_counts(df, short=SHORT_WINDOW, long=LONG_WINDOW):
    short_df=df.tail(short)
    long_df=df.tail(long)
    counts_short=short_df.iloc[:,1:].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    counts_long=long_df.iloc[:,1:].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    fused=0.6*counts_short + 0.4*counts_long
    # Mid‑segment boost
    for n in MID_SEGMENT:
        if n in fused:
            fused.loc[n]*=1.3
    fused=fused.reindex(range(1,40)).fillna(0)
    return fused

def compute_sigma_h(rates):
    return float(np.std(rates.values))

def hit2_score(df, n, last=50):
    recent=df.tail(last)
    cnt=0
    for row in recent.itertuples(index=False):
        nums=row[1:]
        if n in nums:
            cnt+=1
    return cnt/last
