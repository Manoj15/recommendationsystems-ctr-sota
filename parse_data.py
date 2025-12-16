import pandas as pd
from pathlib import Path

def read_news_tsv(path: str) -> pd.DataFrame:
    cols = ["news_id","category","subcategory","title","abstract","url","title_entities","abstract_entities"]
    df = pd.read_csv(path, sep="\t", names=cols, quoting=3)
    df["title"] = df["title"].fillna("")
    df["abstract"] = df["abstract"].fillna("")
    return df

def read_behaviors_tsv(path: str) -> pd.DataFrame:
    cols = ["impression_id","user_id","time","history","impressions"]
    df = pd.read_csv(path, sep="\t", names=cols, quoting=3)
    df["history"] = df["history"].fillna("")  # space-separated news_ids
    df["impressions"] = df["impressions"].fillna("")  # "N1-1 N2-0 ..."
    return df

raw_train = Path("data/MINDsmall_train")
news = read_news_tsv(raw_train/"news.tsv")
beh = read_behaviors_tsv(raw_train/"behaviors.tsv")

Path("data/processed").mkdir(parents=True, exist_ok=True)
news.to_parquet("data/processed/news.parquet", index=False)
beh.to_parquet("data/processed/behaviors.parquet", index=False)
