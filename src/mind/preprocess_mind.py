from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd

NEWS_COLS = ["news_id","category","subcategory","title","abstract","url","title_entities","abstract_entities"]
BEH_COLS  = ["impression_id","user_id","time","history","impressions"]

def read_news(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", names=NEWS_COLS, quoting=3)
    df["title"] = df["title"].fillna("")
    df["abstract"] = df["abstract"].fillna("")
    return df

def read_behaviors(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep="\t", names=BEH_COLS, quoting=3)
    df["history"] = df["history"].fillna("")
    df["impressions"] = df["impressions"].fillna("")
    return df

def build_maps(news_df: pd.DataFrame, beh_df: pd.DataFrame) -> tuple[dict, dict]:
    news2idx = {nid: i for i, nid in enumerate(news_df["news_id"].tolist())}
    # users can be sparse; map from behaviors
    users = beh_df["user_id"].fillna("").astype(str).tolist()
    user_set = sorted({u for u in users if u and u != "nan"})
    user2idx = {u: i for i, u in enumerate(user_set)}
    return news2idx, user2idx

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw_dir", type=str, required=True)     # e.g. data/raw/MINDsmall_train
    ap.add_argument("--out_dir", type=str, default="data/processed/mind_small_train")
    args = ap.parse_args()

    raw_dir = Path(args.raw_dir)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    news = read_news(raw_dir / "news.tsv")
    beh  = read_behaviors(raw_dir / "behaviors.tsv")

    news2idx, user2idx = build_maps(news, beh)

    news.to_parquet(out_dir / "news.parquet", index=False)
    beh.to_parquet(out_dir / "behaviors.parquet", index=False)

    (out_dir / "maps").mkdir(exist_ok=True)
    json.dump(news2idx, open(out_dir / "maps/news2idx.json", "w"))
    json.dump(user2idx, open(out_dir / "maps/user2idx.json", "w"))

    print(f"[ok] wrote: {out_dir}")
    print(f"  news rows: {len(news)}")
    print(f"  behaviors rows: {len(beh)}")
    print(f"  unique users: {len(user2idx)}")

if __name__ == "__main__":
    main()
