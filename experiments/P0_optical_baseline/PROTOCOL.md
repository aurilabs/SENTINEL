# P0 — Optical Measurement-System Baseline

## Purpose

Measure how much apparent optical change is created by the imaging system itself before any smart coating is tested.

This is a metrology experiment, not a coating experiment.

## Research question

When the physical target is unchanged, how much variation in CIELAB coordinates and CIEDE2000 color difference is introduced by camera, illumination, geometry, and repeated capture?

## Materials

Use what is already available whenever possible.

Required:
- smartphone camera
- rigid support or temporary improvised mount
- stable matte colored target(s)
- neutral background
- ruler or fixed-distance spacer
- computer with Python

Preferred later:
- fixed 3D-printed camera/sample fixture
- controlled LED illumination
- calibrated color reference card

A calibrated color card is **not required for P0 repeatability**, but it will be required before making claims about absolute color accuracy.

## Camera setup

Use manual/pro mode if available.

Keep fixed where possible:
- lens
- focus
- ISO
- shutter/exposure
- white balance
- HDR/off
- filters/off
- flash/off

Do not digitally zoom.

Record the phone model and all available settings.

## Image groups

Create folders or filenames that identify these conditions.

### A — Baseline repeatability
Without moving anything, take 10 images.

Goal: estimate the natural repeatability floor of the setup.

### B — Lighting perturbation
Change illumination intensity or source position by one controlled step.

Take 10 images.

### C — Geometry perturbation
Change camera angle or camera-target distance by one controlled step.

Take 10 images.

### D — Return to baseline
Restore the original setup.

Take 10 images.

Goal: test whether the setup returns to the same optical state.

## Metadata

For every image record:
- filename
- condition
- replicate number
- date/time
- phone/camera
- ISO
- exposure/shutter if available
- white balance if available
- camera-target distance
- illumination description
- notes

## Analysis

Use the same ROI coordinates across the image series.

Run:

```bash
python analysis/optical_quantification/batch_analyze.py path/to/images \
  --roi X0 Y0 X1 Y1 \
  --baseline baseline_01.jpg \
  --output results.csv
```

Do not interpret a generic DeltaE threshold as a pass/fail criterion yet.

Instead, estimate the **empirical noise distribution** of the baseline setup.

Important quantities:
- mean L*, a*, b*
- between-image variability
- DeltaE00 distribution within baseline condition
- DeltaE00 under deliberate lighting perturbation
- DeltaE00 under deliberate geometry perturbation
- return-to-baseline error

## Gate 0 decision

**GO:** a fixed setup produces substantially less optical variation than deliberate perturbations, and return-to-baseline is reproducible.

**FIX THE SETUP:** baseline itself drifts strongly or return-to-baseline is poor.

No smart coating experiment should be interpreted quantitatively until this gate is passed.

## Deliverables

1. raw images kept locally
2. metadata CSV
3. processed results CSV
4. one plot of DeltaE00 by condition
5. short note: "What controls imaging error in our setup?"
6. fixture requirements for the first 3D-printed version
