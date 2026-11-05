Extraction provenance
=====================

This independent 2024 repository was extracted from the validated combined
workbench at commit 2bd418759368bdb305697ea354e62e99f257242f.
``extraction_provenance.json`` records the source hashes and the original
extraction-time comparison of computational function/class bodies. Package imports, the
command-line interface and the paper-specific documentation were separated.

Small helpers are deliberately present locally, not imported from another
paper package. Each repository can be installed alone. Package namespaces
rds2023, rds2024 and rds2025 also permit installation together without a
shared ``rds`` namespace collision. No fourth shared-code repository is
required. Future shared numerical changes should be tested in each consumer.

The original workbench and its complete archive remain preserved. New
idealised-campaign work stays there rather than being represented as part
of this published paper. Experimental data have not been copied to GitHub.

Subsequent paper-workflow update (2026-11-05)
-------------------------------------------

The default analysis now reads only the original and large-scale fields
used by the main statistics script. The existing component-wise moment
calculation was factored into ``scale_statistics`` without changing its
numerical definitions. The CLI offers ``reproduce`` with ``validate`` as
a compatible alias. Actual projection failures still produce a nonzero
exit code. Full-array regression against the previous computed outputs
is recorded in SPLIT_VERIFICATION.rst.
