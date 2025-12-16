from __future__ import annotations
import torch
from torch.utils.data import DataLoader

def mind_collate_fn(batch):
    batch = [b for b in batch if b is not None]
    if len(batch) == 0:
        return None

    max_h = max(x["history_idxs"].numel() for x in batch)
    B = len(batch)

    history = torch.zeros(B, max_h, dtype=torch.long)
    history_mask = torch.zeros(B, max_h, dtype=torch.bool)

    for i, x in enumerate(batch):
        h = x["history_idxs"]
        if h.numel() > 0:
            history[i, -h.numel():] = h
            history_mask[i, -h.numel():] = True

    candidates = torch.stack([x["candidate_idxs"] for x in batch], dim=0)  # [B, K]
    labels = torch.stack([x["labels"] for x in batch], dim=0)              # [B, K]

    return {
        "history_idxs": history,
        "history_mask": history_mask,
        "candidate_idxs": candidates,
        "labels": labels,
    }

def make_loader(dataset, batch_size=64, shuffle=True, num_workers=2, pin_memory=True):
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=pin_memory,
        collate_fn=mind_collate_fn,
        drop_last=False,
    )
