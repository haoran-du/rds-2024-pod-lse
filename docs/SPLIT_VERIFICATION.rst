Paper workflow verification
===========================

2026-11-05. The independent Python 3.12 environment passes 15 automated
tests, including corresponding-component scale statistics, operation with
only original/large-scale inputs, and nonzero exit status for an actual
projection mismatch or non-finite projection.

The current workflow was rerun for all five configurations. Saved HWA
bases and large-scale PIV fields agree with the direct projections. The
computed residuals also satisfy internal algebraic closure; this is not
an additional independent experimental validation.

All 45 output arrays (three components, five cases, and three arrays per
file) are element-for-element identical to the earlier computed variances,
large-scale variances and third-order contributions. The detailed current
record is in ``split_validation.json`` and ``validation_summary.json``.

The command-line workflow now requires only the inputs used by the main
statistics calculation. Earlier development records are retained locally
and in Git history. No raw data or original source was modified.

The processing scope remains 7.4-Hz saved-basis projection and scale
statistics, not a complete rerun of all paper figures. The Actions tab
shows the independent Linux/Windows/macOS test results for each commit.
