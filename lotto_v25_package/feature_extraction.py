import numpy as np, pandas as pd

def dual_window_counts(df, short=334, long=1500):
    recent_short=df.tail(short)
    recent_long=df.tail(long)
    counts_short=recent_short.iloc[:,1:].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    counts_long=recent_long.iloc[:,1:].apply(pd.Series.value_counts).fillna(0).sum(axis=1)
    fused=0.6*counts_short + 0.4*counts_long
    # Mid-Boost
    for n in range(21,31):
        fused.loc[n]*=1.3
    return fused
def compute_features(df):
    fused=dual_window_counts(df)
    rates=fused / fused.sum()
    sigma_h=float(rates.std())
    return rates.to_dict(), sigma_h
