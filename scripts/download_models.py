"""Download the trained vision models from the GitHub release into models/.

    python scripts/download_models.py            # both models
    python scripts/download_models.py --only vision_yolo11n.pt

The sensor model (models/sensor_xgb.json) is small and already in the repo.
"""
import argparse
import hashlib
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RELEASE = "https://github.com/manoj291205/Multimodal-Federated-Fire-Detection-System/releases/download/v2.0.0"
FILES = {
    # name: sha256 of the released file
    "vision_yolo11n.pt": "0c091706373f04fc54106748483aefc3de50bfab8ef0838f51fa39d42e0d1b62",
    "vision_yolo11n_fedavg.pt": "e0a3e6bb3b8bc7bfd8824789c3afe4b6f564023f0bb4ca1f259649e0a4e0119e",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", choices=list(FILES))
    args = ap.parse_args()

    out_dir = ROOT / "models"
    out_dir.mkdir(exist_ok=True)
    for name, digest in FILES.items():
        if args.only and name != args.only:
            continue
        dest = out_dir / name
        if dest.exists() and (digest is None or sha256(dest) == digest):
            print(f"{name}: already present")
            continue
        print(f"{name}: downloading")
        tmp = dest.with_suffix(".part")
        urllib.request.urlretrieve(f"{RELEASE}/{name}", tmp)
        if digest and sha256(tmp) != digest:
            tmp.unlink()
            raise SystemExit(f"{name}: checksum mismatch, download discarded")
        tmp.replace(dest)
        print(f"{name}: saved to {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
