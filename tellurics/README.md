# tellurics/

One telluric-standard AB pair per wavelength setting (16 settings, L3244–M4519), reduced with `cr2res_obs_nodding` and then fit with `vipere` to derive the wavelength solution and slit tilt that populate the per-setting `../{setting}_tw.fits` used by the main science reduction.

## Workflow

1. **Reduce each setting's AB pair** with esorex:
   `cd {setting} && esorex cr2res_obs_nodding nodd.sof`

2. **Fit tellurics with vipere** on extractedA and extractedB separately. This produces `telluric{A,B}.par.dat` (per-order wavelength + continuum + atmosphere coefficients) and residuals.

3. **Measure the true nod throw** — `measure_nod_throw.py`
   Double-Gaussian fits to `|combinedA|` spatial profiles; writes `nod_throw_measurements.json`. Needed to convert A−B wavelength differences into a slit tilt.

4. **Per-order tilt from A−B wavelength offsets** — `fit_tilt.py`
   Uses the vipere A vs B wavelength solutions and the measured nod throw.

5. **Global linear tilt(wavelength) per band** — `fit_tilt_linear.py`
   Iterative 3σ-clipped linear fit, one for L band, one for M band. Output: `tilt_linear_fit.json`.

6. **Write SlitPolyB into `_tw.fits`** — `set_slit_tilt.py`
   For every trace, `SlitPolyB = [tilt(wl_center), 0, 0]` from the linear fit.

7. **Write Wavelength polynomials into `_tw.fits`** — `set_wavelength.py`
   Converts vipere's (Angstrom, xcen-centered) polynomial to the `_tw.fits` convention (nm, pixel 0). Quality-filtered; rejected traces keep the pipeline solution.

8. **Provenance table** — `make_tw_origin.py` generates `tw_origin.md`, recording whether each trace's wavelength and tilt came from vipere or the pipeline.

## Paper figure

- `plot_tilt_paper.py` — renders the tilt-vs-wavelength figure for the paper; not part of the calibration pipeline.
