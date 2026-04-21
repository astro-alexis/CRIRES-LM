#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Single-panel tilt vs wavelength figure for the paper."""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path

BASE = Path(__file__).parent

with open(BASE / 'tilt_fits.json') as f:
    data = json.load(f)

with open(BASE / 'tilt_linear_fit.json') as f:
    fits = json.load(f)

measurements = data['measurements']

wl = np.array([m['wl_nm'] for m in measurements])
tilt = np.array([m['tilt'] for m in measurements])
chips = np.array([m['chip'] for m in measurements])
bands = np.array([m['band'] for m in measurements])

# sigma clip per band (same as fit_tilt_linear.py)
mask = np.ones(len(wl), dtype=bool)
for band in ['L', 'M']:
    sel = bands == band
    c = [fits[band]['slope'], fits[band]['intercept']]
    res = tilt[sel] - np.polyval(c, wl[sel])
    sigma = fits[band]['rms']
    mask[sel] = np.abs(res) < 3 * sigma

chip_colors = {1: 'C0', 2: 'C1', 3: 'C2'}
chip_markers = {1: 'o', 2: 's', 3: 'D'}

fig, ax = plt.subplots(figsize=(7, 3.5))

for chip in [1, 2, 3]:
    sel = (chips == chip) & mask
    ax.plot(wl[sel], tilt[sel],
            marker=chip_markers[chip], color=chip_colors[chip],
            ms=2, lw=0, alpha=0.4, label=f'CHIP{chip}')
    rej = (chips == chip) & ~mask
    if rej.any():
        ax.plot(wl[rej], tilt[rej],
                marker=chip_markers[chip], color='gray',
                ms=1.5, lw=0, alpha=0.15)

# linear fits
for band, ls in [('L', '-'), ('M', '--')]:
    f = fits[band]
    c = [f['slope'], f['intercept']]
    wl_range = np.linspace(f['wl_min'], f['wl_max'], 200)
    ax.plot(wl_range, np.polyval(c, wl_range), 'k', ls=ls, lw=1.5,
            label=f'{band} fit (RMS={f["rms"]:.004f})')

ax.axhline(0, color='gray', ls=':', lw=0.5)
ax.set_ylim(-0.15, 0.06)
ax.set_xlabel('wavelength [nm]')
ax.set_ylabel('slit tilt (dx/dy)')
ax.legend(fontsize=7, loc='lower left', ncol=2)

fig.tight_layout()
outpath = BASE.parent / 'paper' / 'figs' / 'slit_tilt.png'
fig.savefig(outpath, dpi=150, bbox_inches='tight')
fig.savefig(outpath.with_suffix('.pdf'), bbox_inches='tight')
print(f'Saved {outpath}')
