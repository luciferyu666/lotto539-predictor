"""
neural_net.py – v2.7 Bi‑GRU + Attention scorer
Author: ChatGPT auto‑generated
"""
import torch
import torch.nn as nn

class BiGRUScorer(nn.Module):
    def __init__(self, input_dim: int, hidden_dim: int = 64, n_layers: int = 3):
        super().__init__()
        self.gru = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=n_layers,
            batch_first=True,
            bidirectional=True,
        )
        self.attn = nn.MultiheadAttention(embed_dim=hidden_dim * 2, num_heads=4, batch_first=True)
        self.out = nn.Linear(hidden_dim * 2, 1)

    def forward(self, x):
        # x: [B, T, F]
        gru_out, _ = self.gru(x)          # [B, T, 2H]
        attn_out, _ = self.attn(gru_out, gru_out, gru_out)
        logits = self.out(attn_out[:, -1])  # use last step
        return logits.squeeze(-1)

# warm‑fit helper
def warm_fit(model: nn.Module, dataloader, epochs: int = 3, lr: float = 1e-3, device="cpu"):
    optim = torch.optim.AdamW(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    model.to(device)
    model.train()
    for epoch in range(epochs):
        for xb, yb in dataloader:
            xb, yb = xb.to(device), yb.to(device)
            pred = model(xb)
            loss = loss_fn(pred, yb)
            loss.backward()
            optim.step()
            optim.zero_grad()
