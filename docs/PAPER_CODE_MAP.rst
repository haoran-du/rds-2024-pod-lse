Paper-to-code map
=================

Paths below are DATA-relative and retained in the local archive.

2024: POD–LSE scale interaction
------------------------------

* ORIGINAL per-case block*_POD_PIV.m/cathedral_POD_PIV.m and pod3.m
  form the PIV snapshot decomposition.
* ORIGINAL HWA per-case ``*_POD_HWA_Filtered_V2.m`` forms the filtered,
  time-delayed HWA decomposition; ``*_177_6HZ_f.m`` is the higher-rate branch.
* ``PREPROCESSING/RdS_PIV_HWA_XZ_POD-LSE/XZ_POD_LSE_copy2_short.m``
  maps the saved HWA/PIV bases and exports scale fields. copy1/copy2 are
  retained variants, not deleted merely because they contain duplicate code.
* ``POSTPROCESSING/RdS_PIV_HWA_POD_LSE/`` contains statistics, mode-energy,
  integral-scale and cross-correlation plotting branches.
* The verified 7.4-Hz projection is algebraically X B B^T, where X is the
  centered PIV signal and B contains the 105 orthonormal HWA temporal modes.
  This is equivalent to the full-rank PIV POD expression in the script and
  avoids storing/recomputing its complete 10,000-mode SVD.
* ``RdS_POD_LSE_Statistics.m`` computes small-scale fluctuations from each
  component's original field minus its large-scale field. The Python
  statistics workflow uses the same definition.

Python: see this repository's ``src/rds2024`` package.

