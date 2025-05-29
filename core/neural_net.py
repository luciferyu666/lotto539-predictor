import torch, torch.nn as nn, math
class BiGRUScorer(nn.Module):
    def __init__(self, feat_dim=39):
        super().__init__()
        self.gru = nn.GRU(feat_dim,64,1,bidirectional=True,batch_first=True)
        self.fc = nn.Linear(128,39)
    def forward(self,x):
        h,_ = self.gru(x)
        return torch.sigmoid(self.fc(h.mean(1)))
