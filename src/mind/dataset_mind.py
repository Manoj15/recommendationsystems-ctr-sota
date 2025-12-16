from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

class MindPairwiseDataset(Dataset):
    """
    Each __getitem__ returns one training instance:
      history_idxs: [H]
      candidate_idxs: [1+neg_k]   (first is positive)
      labels: [1+neg_k]
    This works for NRMS/NAML/LSTUR-style training and general ranking models.
    """
    def __init__(
        self,
        behaviors_parquet: str,
        news2idx_json: str,
        max_history: int = 50,
        neg_k: int = 4,
        seed: int = 42,
    ):
        self.beh = pd.read_parquet(behaviors_parquet)
        self.news2idx = json.load(open(news2idx_json))
        self.max_history = max_history
        self.neg_k = neg_k
        self.rng = np.random.default_rng(seed)

    def __len__(self):
        return len(self.beh)

    def _parse_history(self, s: str) -> list[int]:
        if not s:
            return []
        ids = s.split()
        idxs = [self.news2idx[n] for n in ids if n in self.news2idx]
        return idxs[-self.max_history :]

    def _parse_impressions(self, s: str) -> tuple[list[int], list[int]]:
        pos, neg = [], []
        if not s:
            return pos, neg
        for tok in s.split():
            if "-" not in tok:
                continue
            nid, lab = tok.rsplit("-", 1)
            if nid not in self.news2idx:
                continue
            (pos if lab == "1" else neg).append(self.news2idx[nid])
        return pos, neg

    def __getitem__(self, i: int):
        row = self.beh.iloc[i]
        hist = self._parse_history(str(row["history"]))
        pos, neg = self._parse_impressions(str(row["impressions"]))

        # Some rows might have no positives; return None and collate will drop
        if len(pos) == 0:
            return None

        p = pos[0]
        if len(neg) >= self.neg_k:
            n = self.rng.choice(neg, self.neg_k, replace=False).tolist()
        else:
            n = (neg + neg[: max(0, self.neg_k - len(neg))])[: self.neg_k]

        candidates = [p] + n
        labels = [1] + [0] * len(n)

        return {
            "history_idxs": torch.tensor(hist, dtype=torch.long),
            "candidate_idxs": torch.tensor(candidates, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.float32),
        }
