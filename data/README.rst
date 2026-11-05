Expected inputs
===============

Pass the original DATA directory to ``--data-root``. For each selected case:

* ``PREPROCESSING/RdS_PIV_HWA_XZ_POD-LSE/V_POD_HWA_<case>_Filtered_econ.mat``:
  the saved orthonormal hot-wire temporal basis (snapshots by modes).
* ``POSTPROCESSING/RdS_PIV_HWA_POD_LSE/RdS_POD_LSE_Computed_Values/``:
  ``<component>_org_7d4_<case>.mat`` and ``<component>L_7d4_<case>.mat``
  for components ``u``, ``w`` and ``v``. Each velocity array has MATLAB
  dimensions (154, 37, 10000), ordered as (z, x, time).
* ``POSTPROCESSING/RdS_PIV_XZ_STATISTICS/RdS_PIV_XZ_STATISTICS_PROFILES/PIV_z.mat``:
  the vertical coordinates for the centreline plots.

The case identifiers are ``1b``, ``2b``, ``3b``, ``6b`` and ``ca``.
Small-scale fields are computed directly from each component's original and
large-scale fields; no separately saved small-scale array is required.
Inputs are read-only. Output paths must be outside the input data tree.
