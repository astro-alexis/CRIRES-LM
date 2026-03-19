# CRIRES-LM arXiv Paper Plan

## Goal

Short (4–6 page) paper on astro-ph.IM describing the reprocessed CRIRES+ L/M-band
data archive. Primary purpose: create a citable bibcode in ADS. Not intended for
journal submission (but use A&A template so it looks right and keeps that option open).

## Setup

- Download `aa-package.zip` from <http://ftp.edpsciences.org/pub/aa/>
- Need `aa.cls`, `aa.bst` in the project directory
- `\documentclass{aa}` with `\usepackage{txfonts}` and `\usepackage{graphicx}`
- Submit to arXiv under astro-ph.IM

## Paper structure

### 1. Introduction (~0.5 page)
- CRIRES+ is a cross-dispersed high-res IR spectrograph at the VLT (cite Dorn+2023 A&A instrument paper)
- L/M bands (2.8–5.5 µm) are scientifically important but underserved:
  the standard cr2res pipeline does not handle slit tilt in L/M, and
  ESO's own phase 3 data release explicitly excludes L- and M-band observations
- This paper presents a bulk reprocessing of all public CRIRES+ L/M science data with
  improved calibration and telluric correction, served as a browsable/downloadable archive

### 2. Data (~0.5 page)
- All public L/M science data from ESO archive, 2021-01 to 2025-02
- 16 wavelength settings (L3244–L3426, M4187–M4519), 5–7 orders per chip, 3 chips
- 11,135 raw frames → 5,237 AB nod pairs across 412 observing sequences
- 233 flat field epochs

### 3. Method (~1.5 pages)
#### 3.1 Slit tilt calibration from telluric standards
- For each setting: reduce one hot star (B/O) observed at nod A and B
- vipere fits forward model of telluric absorption + wavelength solution independently per nod
- A vs B wavelength difference at each pixel → slit tilt measurement
- Fit linear tilt(wavelength) per band, interpolating across CO2 gap at 4.2–4.5 µm
- Written into SlitPolyB column of tracing tables

#### 3.2 Wavelength calibration
- vipere polynomials replace pipeline solution for 72% of traces
- Remaining traces (weak/no telluric features) keep pipeline wavelengths

#### 3.3 Science reduction
- Trace adjustment per observation: cross-correlate spatial profile against reference
  to measure Y-shift from instrument flexure (typically 5–10 px, up to ~50)
- esorex cr2res_obs_nodding with adjusted tracing tables + nearest flat/blaze
- Telluric correction: vipere on each extracted spectrum
- Wavelength update: fitted orders get vipere polynomial; unfitted orders get
  wavelengths interpolated from 2D polynomial surface

### 4. The archive (~0.5 page)
- Web app at https://neon.physics.uu.se/crires-lm/
- Browsable by target, setting, programme
- Per-observation: combined spectrum (interactive plot), diagnostic plots, FITS downloads
- Individual AB pair reductions also accessible
- Code at https://github.com/ivh/CRIRES-LM

### 5. Summary (~0.25 page)
- Keep it short, restate what's available and how to cite

## Figures to include
1. Example spectrum before/after telluric correction (one L-band, one M-band)
2. Slit tilt measurement: A vs B wavelength difference for one setting
3. Flexure correction: histogram of Y-shifts across all observations
4. Screenshot or example output from the web app (optional, could be cut)

## References (key ones)
- Dorn+2023 (CRIRES+ instrument paper, A&A)
- viper/vipere (Zechmeister+ and the Lavail fork)
- cr2res pipeline (ESO reference)
- ESO phase 3 data release announcement (for the L/M exclusion)

## Post-submission checklist
- Add `CITATION.cff` to the GitHub repo with the arXiv bibcode
- Add "How to cite" section to the webapp and README
- Register code with ASCL (optional but free and gets another bibcode)
