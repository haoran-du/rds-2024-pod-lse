2024 paper: conventions and audit findings
=================================================

1. Coordinate/component conventions
----------------------------------

XZ Dantec U,V,W columns map to physical U,W,-V; the vertical calibration
offset is +155 mm. YZ columns map to physical V,W,U, with +175 mm offset.
Python arrays use (time,z,horizontal[,component]) and physical U,V,W order.
MATLAB v7.3/HDF5 storage dimensions are reversed; explicit transposes are
tested. The YZ coordinate named x_contour in old files is physically y.

2. One-column discrepancy, verified from original snapshots
---------------------------------------------------------

Published-profile and flux scripts retain MATLAB horizontal columns 7:43.
Contour scripts retain 8:44. The 1b instantaneous MAT matches 7:43;
2b/3b/6b/ca instantaneous MATs match 8:44, despite old per-case source
scripts showing 7:43. All original TXT snapshots therefore provide the
authoritative input for legacy flux reconstruction. The two MAT crops
must not be averaged or relabelled as the same coordinates.

5. 2024 residual caches versus the main statistical calculation
--------------------------------------------------------------

The main statistics script computes the corresponding-component residuals
correctly and does not load wS/vS. The following finding concerns legacy
cache reuse, NOT evidence that the paper's statistical calculation was wrong.

Source: ``PREPROCESSING/RdS_PIV_HWA_XZ_POD-LSE/XZ_POD_LSE_copy2_short.m``,
lines 207–209. The u residual uses the correct component. The w and v
residuals use U_org_u as their minuend. Across all five cases, the saved
wS and vS fail corresponding-component closure and instead close against
the u original. All three large-scale LSE projections themselves match.

The naming-only explanation was checked against original B6h TXT frames
0,150,5000,9999: saved u_org/w_org/v_org each matches its physical component
up to a time-independent mean, within 2.6e-14 m/s, using MATLAB crop 7:43.
At those frames, wL+wS and vL+vS match u_org within 4.5e-16 m/s, not the
corresponding w_org/v_org. The cache content difference is therefore not
resolved by merely renaming the three original-component variables.

New Python small-scale moments are computed from the corresponding
original component minus its large scale. Failed legacy checks remain
visible. No original MATLAB or MAT file is patched.

This is NOT evidence that the 2024 paper's main statistics are wrong:
``RdS_POD_LSE_Statistics.m`` recomputes the correct component residuals.
See lines 66,89,111 and 404–406 for variance, shear stress and scale terms.
The highf2/177Hz contour scripts load vS, but the identified subsequent
vS calculations are commented out. Final figure provenance still needs
checking before any claim about the published conclusions.

