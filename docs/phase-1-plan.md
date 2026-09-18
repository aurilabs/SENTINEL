# Phase 1 — Reliability-First Optical Diagnostics

## Working question

Can a protective interface identify electrochemically active corrosion while rejecting benign coating damage and environmental false positives?

## Why this is Phase 1

Simple color-changing corrosion indicators, dual-stimulus systems, self-reporting/self-healing coatings, and damage-vs-corrosion visual separation already exist in the literature. The Phase 1 contribution is therefore not "make a coating change color." The target is diagnostic reliability.

## Measurement model

Optical response is treated as a sensor output, not as proof of corrosion.

Primary outputs:
- CIELAB color coordinates and CIEDE2000 color difference
- fluorescence intensity when UV channels are introduced
- spatial response around defined regions of interest
- response time and persistence

Independent ground truth will later include electrochemical measurements such as EIS and/or polarization through institutional or external laboratory access.

## Confounder classes

The first test matrix will separate:
1. intact + dry control
2. intact + humid/wet
3. mechanically damaged without deliberate corrosive exposure
4. chloride/water exposure without visible rust
5. electrochemically active corrosion
6. temperature and illumination variation as measurement-system confounders

Later matrices may include UV ageing and wet/dry cycling.

## Performance metrics

- repeatability
- sensitivity
- specificity
- false-positive rate
- response time
- calibration error
- between-sample variability
- barrier-performance penalty

## P0 before chemistry

Before evaluating any smart coating, quantify how much the imaging system itself can create an apparent color change.

This prevents camera/lighting drift from being mistaken for a material response.

See `analysis/optical_quantification/`.
