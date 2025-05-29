
import torch, pandas as pd
from core.neural_net import BiGRUScorer

def test_forward():
    model=BiGRUScorer(6)
    x=torch.randn(1,10,6)
    out=model(x)
    assert out.shape==torch.Size([1])
