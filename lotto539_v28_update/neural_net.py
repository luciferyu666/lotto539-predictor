"""BiGRU + Attention neural net, v2.8 warm-fit compatible"""
import torch
import torch.nn as nn
COLD_FLAG_LEVELS = 3
INPUT_DIM = 10
HIDDEN = 64
class BiGRUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.gru = nn.GRU(INPUT_DIM, HIDDEN, num_layers=3, bidirectional=True, batch_first=True)
        self.attn_w = nn.Linear(HIDDEN*2, 1)
        self.fc = nn.Linear(HIDDEN*2, 1)
    def forward(self, x):
        h,_ = self.gru(x)
        a = torch.softmax(self.attn_w(h), dim=1)
        context = (a * h).sum(dim=1)
        return torch.sigmoid(self.fc(context))
