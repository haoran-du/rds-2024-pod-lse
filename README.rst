RdS 2024: POD–LSE scale interaction
==================================

Independent Python tools for Du, Perret & Savory (2024), Boundary-Layer
Meteorology, https://doi.org/10.1007/s10546-023-00844-8.
No MATLAB runtime or installation of another RdS repository is required.

Install and run
---------------

From this repository directory, with Python 3.10 or newer::

    python -m venv .venv
    # Linux/macOS: source .venv/bin/activate
    # Windows PowerShell: .venv\Scripts\Activate.ps1
    python -m pip install -e ".[test]"
    python -m pytest -q
    rds2024 validate --data-root "/path/to/DATA" --output outputs/lse

For one case, add ``--cases 6b``. ``python -m rds2024.cli`` is an equivalent
entry point. Inputs remain external and read-only, in their original DATA
directory layout.

Scope and limitations
---------------------

This is a partial, explicitly audited reproduction, not a claim that all
2024 figures have been independently rebuilt.

* Reprojects all three 7.4-Hz PIV components in five cases using the saved
  HWA temporal basis. The projection is algebraically equivalent to the
  full-rank PIV POD–LSE expression without another giant PIV SVD.
* Computes scale variances and third-order terms using corresponding-
  component residuals, as the main MATLAB statistics script already does.
* Retains checks on old wS/vS caches. Those caches do not contain the named
  component residuals, but the main statistics script does not use them.
  This is not evidence that the paper's actual statistics are wrong.
* Supplies independent POD, centered least-squares and third-moment kernels.

The retained baseline has 35 passing checks and 10 failed legacy-cache
closures. Ten of the passes diagnose the cache substitution; they are not
ten additional scientific validations. The validation command therefore
returns status 1 even when the independently reprojected large scales match.
See ``docs/AUDIT_FINDINGS.rst`` and ``docs/validation_summary.json``.

Raw HWA filtering, delay embedding, 177.6-Hz reconstruction and all final
figure paths are not yet independently reproduced. The diagnostic figure
is not an exact recreation of a publication figure.

Contents and provenance
-----------------------

``src/rds2024`` contains only the POD–LSE workflow and its local helpers.
It does not import the 2023 plotting package or the 2025 SPOD package.
``tests`` is data-independent; ``docs/SPLIT_VERIFICATION.rst`` distinguishes
new extraction tests from inherited experimental-data validation.

MATLAB originals are retained unchanged in the local ``archive/matlab``;
the public hash index is in ``docs``. Neither original arrays nor MATLAB
source is uploaded. See ``THIRD_PARTY.rst`` and ``CITATION.cff``.
