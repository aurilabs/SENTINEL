"""Batch colorimetry for SENTINEL P0 imaging experiments.

Analyzes a fixed ROI across a folder of images and reports mean CIELAB,
channel standard deviations, and CIEDE2000 difference relative to the
first image (or a named baseline).

Example:
    python batch_analyze.py images/ --roi 100 100 300 300 --output results.csv
    python batch_analyze.py images/ --roi 100 100 300 300 --baseline baseline_01.jpg
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000

SUPPORTED = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


def load_rgb(path: Path) -> np.ndarray:
    return np.asarray(Image.open(path).convert("RGB"), dtype=np.float64) / 255.0


def crop_roi(rgb: np.ndarray, roi: tuple[int, int, int, int]) -> np.ndarray:
    x0, y0, x1, y1 = roi
    h, w = rgb.shape[:2]
    if not (0 <= x0 < x1 <= w and 0 <= y0 < y1 <= h):
        raise ValueError(f"ROI {roi} outside image bounds {w}x{h}")
    return rgb[y0:y1, x0:x1]


def lab_stats(rgb_roi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lab = rgb2lab(rgb_roi)
    pixels = lab.reshape(-1, 3)
    return pixels.mean(axis=0), pixels.std(axis=0, ddof=1)


def de00(a: np.ndarray, b: np.ndarray) -> float:
    aa = a.reshape(1, 1, 3)
    bb = b.reshape(1, 1, 3)
    return float(deltaE_ciede2000(aa, bb)[0, 0])


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("image_dir", type=Path)
    p.add_argument("--roi", nargs=4, type=int, required=True, metavar=("X0", "Y0", "X1", "Y1"))
    p.add_argument("--baseline", type=str, default=None)
    p.add_argument("--output", type=Path, default=Path("results.csv"))
    args = p.parse_args()

    images = sorted([x for x in args.image_dir.iterdir() if x.suffix.lower() in SUPPORTED])
    if not images:
        raise SystemExit("No supported images found.")

    if args.baseline:
        baseline_path = args.image_dir / args.baseline
        if baseline_path not in images:
            raise SystemExit(f"Baseline not found: {baseline_path}")
    else:
        baseline_path = images[0]

    roi = tuple(args.roi)
    baseline_mean, _ = lab_stats(crop_roi(load_rgb(baseline_path), roi))

    rows = []
    for path in images:
        mean_lab, std_lab = lab_stats(crop_roi(load_rgb(path), roi))
        rows.append({
            "file": path.name,
            "L_mean": mean_lab[0],
            "a_mean": mean_lab[1],
            "b_mean": mean_lab[2],
            "L_sd_pixels": std_lab[0],
            "a_sd_pixels": std_lab[1],
            "b_sd_pixels": std_lab[2],
            "deltaE00_vs_baseline": de00(baseline_mean, mean_lab),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    de_values = np.array([r["deltaE00_vs_baseline"] for r in rows], dtype=float)
    print(f"Images analyzed: {len(rows)}")
    print(f"Baseline: {baseline_path.name}")
    print(f"DeltaE00 mean: {de_values.mean():.4f}")
    print(f"DeltaE00 SD:   {de_values.std(ddof=1) if len(de_values) > 1 else 0.0:.4f}")
    print(f"DeltaE00 max:  {de_values.max():.4f}")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
