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

3. Scale-separated statistics
-----------------------------

The main statistics calculation uses each velocity component's original
fluctuation and reconstructed large scale. The small-scale fluctuation is
their difference. The Python workflow follows this definition for the
variances and third-order moments.

The 7.4-Hz large-scale projection uses the saved orthonormal HWA temporal
basis. Internal residual closure is an algebraic consistency condition,
not an independent comparison to a published result. Raw HWA preprocessing,
the high-rate reconstruction and the complete figure sequence remain
outside the current Python workflow.
