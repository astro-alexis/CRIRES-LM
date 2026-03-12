#!/bin/bash
set -euo pipefail

ls -d */flats.sof | sed 's|/flats.sof||' \
| parallel -j16 --bar \
    'cd {} && esorex --recipe-config=../../cr2res_cal_flat.rc cr2res_cal_flat flats.sof 2>&1 > esorex.log'
