"""
neural_net.py
BiGRU + Attention scorer for number potential.
Requires: torch >= 2.0
"""

import torch, torch.nn as nn

class BiGRUAttention(nn.Module):
    def __init__(self, input_dim=1, hidden_size=32, num_layers=2):
        super().__init__()
        self.gru=nn.GRU(input_dim, hidden_size, num_layers=num_layers,
                        bidirectional=True, batch_first=True)
        self.attn=nn.Linear(hidden_size*2, 1)
        self.fc=nn.Linear(hidden_size*2, 1)

    def forward(self, x):
        # x: (batch, seq_len, 1)
        h,_=self.gru(x)
        attn_weights=torch.softmax(self.attn(h), dim=1)
        context=(attn_weights*h).sum(dim=1)
        score=torch.sigmoid(self.fc(context))
        return score.squeeze(-1)

def build_model():
    return BiGRUAttention()

# Example usage
if __name__=='__main__':
    model=build_model()
    dummy=torch.randn(8, 50, 1)
    out=model(dummy)
    print(out.shape)
