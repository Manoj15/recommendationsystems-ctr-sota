from __future__ import annotations
import argparse
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

MIND_URLS = {
    "small": {
        "train": "https://huggingface.co/datasets/yjw1029/MIND/resolve/main/MINDsmall_train.zip",
        "dev":   "https://huggingface.co/datasets/yjw1029/MIND/resolve/main/MINDsmall_dev.zip",
    },
    "large": {
        "train": "https://huggingface.co/datasets/yjw1029/MIND/resolve/main/MINDlarge_train.zip",
        "dev":   "https://huggingface.co/datasets/yjw1029/MIND/resolve/main/MINDlarge_dev.zip",
    }
}

def download(url: str, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if out_path.exists():
        print(f"[skip] exists: {out_path}")
        return
    print(f"[download] {url} -> {out_path}")
    urlretrieve(url, out_path)

def unzip(zip_path: Path, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"[unzip] {zip_path} -> {out_dir}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(out_dir)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", choices=["small", "large"], default="small")
    ap.add_argument("--out", type=str, default="data/raw")
    args = ap.parse_args()

    out = Path(args.out)
    for split, url in MIND_URLS[args.size].items():
        zip_path = out / f"MIND{args.size}_{split}.zip"
        download(url, zip_path)

        # Unzip into data/raw/MINDsmall_train/ etc.
        split_dir = out / f"MIND{args.size}_{split}"
        if split_dir.exists() and any(split_dir.iterdir()):
            print(f"[skip] already extracted: {split_dir}")
        else:
            unzip(zip_path, split_dir)

if __name__ == "__main__":
    main()