Effect of Urban Morphology and an Upstream Tall Building on the Scale Interaction Between the Overlying Boundary Layer and a Street Canyon
==========================================================================================================================================

Authors: Haoran Du, Laurent Perret, and Eric Savory

Affiliations:

* Haoran Du and Eric Savory: Department of Mechanical and Materials Engineering,
  University of Western Ontario, London, Ontario, Canada.
* Laurent Perret: Nantes Universite, Ecole Centrale de Nantes, CNRS, LHEEA,
  UMR 6598, Nantes, France.

Corresponding author: Haoran Du, hdu59@uwo.ca

Published in Boundary-Layer Meteorology (2024).
Article: https://doi.org/10.1007/s10546-023-00844-8

Code Repository
---------------

This repository contains Python routines for the POD–LSE analysis of the
Rue des Suisses (RdS) street canyon. The workflow uses the saved hot-wire
temporal basis to recover large-scale PIV velocity fluctuations and compute
scale-separated variances and third-order moments.

This is a code-only release. Experimental data, processed arrays and
generated figures are supplied or produced separately.

Repository layout
-----------------

* ``src/rds2024/analysis.py``: large-scale reconstruction and scale-separated statistics.
* ``src/rds2024/decomposition.py``: POD, linear stochastic estimation and third-order moments.
* ``src/rds2024/io.py``: measurement-file readers and array conventions.
* ``data/README.rst``: expected inputs and directory layout.
* ``tests/``: automated tests for the Python routines.
* ``docs/``: implementation and processing notes.

Setup
-----

Use Python 3.10 or later. From the repository directory::

    python -m venv .venv

Activate the environment on Linux/macOS::

    source .venv/bin/activate

Or in Windows PowerShell::

    .\.venv\Scripts\Activate.ps1

Then install the package::

    python -m pip install -e .

Run order
---------

1. Obtain the external velocity fields and hot-wire temporal bases listed in
   ``data/README.rst``. Keep their original directory layout.
2. Compute the scale-separated statistics for all five configurations::

       rds2024 reproduce --data-root "/path/to/DATA" --output outputs/lse

3. To process B6h only::

       rds2024 reproduce --data-root "/path/to/DATA" --output outputs/lse_6b --cases 6b

The earlier command name ``rds2024 validate`` remains supported.

All generated files are written to the selected output directory. ``outputs/``
is ignored by Git. ``python -m rds2024.cli`` is an alternative to ``rds2024``.

Processing scope
----------------

The workflow uses the 7.4-Hz PIV fields and the saved orthonormal hot-wire
temporal basis. Small-scale fluctuations are calculated as the original
fluctuation minus its corresponding large-scale component, following the
paper's main statistics script.

Outputs include scale variances, the four third-order contributions and a
centreline comparison plot. Raw hot-wire filtering, delay embedding, the
177.6-Hz reconstruction and the complete set of paper figures are not yet
included in this Python workflow.

Data and citation
-----------------

Input files are external to this repository; their expected layout is given
in ``data/README.rst``. Please cite the article linked above when using this
code. Citation metadata are also provided in ``CITATION.cff``.
