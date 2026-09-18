"""SENTINEL optical colorimetry utility.

Public research tooling only. No formulation or proprietary material information.

Example:
    python sentinel_colorimetry.py baseline.jpg sample.jpg 100 100 300 300

ROI coordinates are x0 y0 x1 y1 in pixels and must refer to the same
physical region in both images.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000


def load_roi(path: str | Path, roi: tuple[int, int, int, int]) -> np.ndarray:
    image = Image.open(path).convert("RGB")
    arr = np.asarray(image, dtype=np.float64) / 255.0
    x0, y0, x1, y1 = roi
    if not (0 <= x0 < x1 <= arr.shape[1] and 0 <= y0 < y1 <= arr.shape[0]):
        raise ValueError(f"ROI {roi} is outside image bounds {arr.shape[1]}x{arr.shape[0]}")
    return arr[y0:y1, x0:x1]


def roi_lab_stats(rgb_roi: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    lab = rgb2lab(rgb_roi)
    pixels = lab.reshape(-1, 3)
    return pixels.mean(axis=0), pixels.std(axis=0, ddof=1)


def delta_e00(mean_lab_a: np.ndarray, mean_lab_b: np.ndarray) -> float:
    a = mean_lab_a.reshape(1, 1, 3)
    b = mean_lab_b.reshape(1, 1, 3)
    return float(deltaE_ciede2000(a, b)[0, 0])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline")
    parser.add_argument("sample")
    parser.add_argument("x0", type=int)
    parser.add_argument("y0", type=int)
    parser.add_argument("x1", type=int)
    parser.add_argument("y1", type=int)
    args = parser.parse_args()

    roi = (args.x0, args.y0, args.x1, args.y1)
    base = load_roi(args.baseline, roi)
    test = load_roi(args.sample, roi)

    base_mean, base_std = roi_lab_stats(base)
    test_mean, test_std = roi_lab_stats(test)
    de00 = delta_e00(base_mean, test_mean)

    np.set_printoptions(precision=4, suppress=True)
    print("Baseline mean Lab:", base_mean)
    print("Baseline std  Lab:", base_std)
    print("Sample mean Lab:  ", test_mean)
    print("Sample std  Lab:  ", test_std)
    print(f"DeltaE00: {de00:.4f}")


if __name__ == "__main__":
    main()
