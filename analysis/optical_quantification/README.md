# Optical Quantification — P0 Measurement-System Study

The first SENTINEL experiment is intentionally coating-free.

## Question

How much apparent color change can be produced by the phone camera, lighting, angle, distance, and exposure settings when the physical sample has not changed?

## Why this matters

A self-reporting coating can only be trusted if the measurement system contributes less variation than the material response we intend to detect.

## P0 protocol

Use stable, non-changing colored targets. A commercial color reference card is preferred when available; until then, matte colored paper or another stable target can be used for pipeline development only.

For each target:

### Condition A — Repeatability
- fix camera position, angle, distance, and illumination
- capture at least 10 images without moving the setup

### Condition B — Illumination perturbation
- deliberately change illumination intensity or source position
- repeat the image series

### Condition C — Geometry perturbation
- change angle or distance by a controlled amount
- repeat

### Condition D — return to baseline
- restore the original geometry and illumination
- repeat

## Analysis

For a fixed ROI:
1. convert sRGB to CIELAB
2. calculate mean and standard deviation of L*, a*, b*
3. calculate CIEDE2000 color difference relative to the baseline reference
4. plot within-condition and between-condition distributions

The result is not a universal pass/fail threshold. It is a measurement-system baseline that will later be compared with the response of real SENTINEL films.

## Output

A short report should state:
- imaging device and camera settings
- illumination
- geometry
- ROI definition
- within-condition repeatability
- drift produced by each perturbation
- fixture requirements inferred from the results
