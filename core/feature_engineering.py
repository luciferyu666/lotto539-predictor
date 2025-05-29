import pandas as pd
import numpy as np

def load_history(csv_path): return pd.read_csv(csv_path)
def tri_layer_features(df):
    mat = np.zeros((len(df),39))
    for i,row in enumerate(df[['n1','n2','n3','n4','n5']].values): mat[i, row-1] = 1
    short = pd.DataFrame(mat).rolling(200,min_periods=1).mean()
    short.columns = [f"s_{i+1}" for i in range(39)]
    return short.fillna(0)
