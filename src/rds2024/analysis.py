"""Validate saved 2024 POD-LSE projections without recomputing giant SVDs."""
from pathlib import Path
import json
import numpy as np
from scipy.io import loadmat, whosmat
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .io import CASES, one_mat
from .common import comparison, savefig, COLORS, LABELS


def load_velocity(path):
    info = whosmat(path)
    if len(info) != 1 or info[0][1] != (154, 37, 10000) or info[0][2] != "double":
        raise ValueError(f"Unexpected legacy 2024 velocity array: {path.name}: {info}")
    name = info[0][0]
    return loadmat(path, variable_names=[name])[name]


def validate_lse(root: Path, output: Path, cases=None):
    root, output = root.resolve(strict=True), output.resolve()
    if root == output or root in output.parents:
        raise ValueError("Output cannot be in source data")
    output.mkdir(parents=True, exist_ok=True)
    folder = root / "POSTPROCESSING/RdS_PIV_HWA_POD_LSE/RdS_POD_LSE_Computed_Values"
    checks, rows, profiles = [], [], {}
    for case in cases or CASES:
        b = one_mat(root / "PREPROCESSING/RdS_PIV_HWA_XZ_POD-LSE" / f"V_POD_HWA_{case}_Filtered_econ.mat")
        checks.append(comparison(f"{case}/HWA-temporal-basis-orthonormal", b.T@b, np.eye(b.shape[1])))
        case_profiles = {}
        for component in "uwv":
            original = load_velocity(folder / f"{component}_org_7d4_{case}.mat")
            # Direct projection is algebraically identical to Phi*S*(V.T*B)*B.T
            # when all PIV modes are retained. It avoids the 10000-mode SVD.
            x = original.reshape(-1, 10000, order="F").T
            coefficients = x.T @ b
            large = load_velocity(folder / f"{component}L_7d4_{case}.mat")
            stored = large.reshape(-1, 10000, order="F").T
            max_error = 0.0
            for start in range(0, len(b), 100):
                predicted = b[start:start+100]@coefficients.T
                max_error = max(max_error, float(np.max(abs(predicted-stored[start:start+100]))))
            checks.append({"name": f"{case}/{component}/LSE-direct-projection", "pass": max_error < 1e-9,
                           "max_abs_error": max_error, "atol": 1e-9})
            # Keep profiles for later use; the normalizer is local total RMS,
            # not a friction velocity or RMS of a spatially averaged signal.
            var = np.mean(original**2, axis=2)
            var_l = np.mean(large**2, axis=2)
            small = load_velocity(folder / f"{component}S_7d4_{case}.mat")
            closure = 0.0
            legacy_u_substitution_error = 0.0
            u_reference = load_velocity(folder / f"u_org_7d4_{case}.mat") if component != "u" else original
            terms = np.zeros((4, 154, 37))
            for start in range(0, 10000, 100):
                l = large[:, :, start:start+100]
                legacy_s = small[:, :, start:start+100]
                closure = max(closure, float(np.max(abs(l+legacy_s-original[:, :, start:start+100]))))
                legacy_u_substitution_error = max(legacy_u_substitution_error, float(np.max(abs(l+legacy_s-u_reference[:, :, start:start+100]))))
                # Recomputed small scales use the CORRESPONDING component.
                # Saved wS/vS fail closure: do not propagate that legacy bug.
                s = original[:, :, start:start+100]-l
                terms[0] += np.sum(l*l*l, axis=2)
                terms[1] += 3*np.sum(l*l*s, axis=2)
                terms[2] += 3*np.sum(l*s*s, axis=2)
                terms[3] += np.sum(s*s*s, axis=2)
            terms /= 10000
            checks.append({"name": f"{case}/{component}/large+small=original", "pass": closure < 1e-10, "max_abs_error": closure})
            if component != "u":
                checks.append({"name": f"{case}/{component}/legacy-small-equals-u-original-minus-large",
                               "pass": legacy_u_substitution_error < 1e-10,
                               "max_abs_error": legacy_u_substitution_error,
                               "meaning": "Diagnostic confirmation of historical cross-component substitution, NOT scientific validation"})
            np.savez_compressed(output / f"{case}_{component}_scale_statistics.npz", variance=var,
                                variance_large=var_l, third_order_terms=terms)
            if component == "u":
                normal = np.where(var > 0, var**1.5, np.nan)
                case_profiles = {"terms_center": terms[:, :, 18]/normal[:, 18],
                                 "large_variance_fraction_center": var_l[:, 18]/np.where(var[:, 18] > 0, var[:, 18], np.nan)}
            del original, x, large, stored, small, u_reference
        profiles[case] = case_profiles
        rows.append({"case": case, "predictor_modes": b.shape[1], "snapshots": b.shape[0]})
        print(f"2024 {case}: direct LSE and scale-closure checks finished", flush=True)
    fig, axes = plt.subplots(1, 2, figsize=(9, 5), layout="constrained")
    zfile = root / "POSTPROCESSING/RdS_PIV_XZ_STATISTICS/RdS_PIV_XZ_STATISTICS_PROFILES/PIV_z.mat"
    z = one_mat(zfile).ravel()[:154]/.116
    for case, p in profiles.items():
        index = list(CASES).index(case)
        color, label = COLORS[index], LABELS[index]
        axes[0].plot(p["large_variance_fraction_center"], z, color=color, label=label)
        axes[1].plot(p["terms_center"][2], z, color=color, label=label)
    axes[0].set(xlabel=r"$\overline{u_L'^2}/\overline{u'^2}$", ylabel=r"$z/h_2$", ylim=(0, 3))
    axes[1].set(xlabel=r"$3\overline{u_L'u_S'^2}/\sigma_u^3$", ylabel=r"$z/h_2$", ylim=(0, 3))
    axes[0].legend(fontsize=8)
    savefig(fig, output, "scale_interaction_centerline_diagnostic")
    report = {"status": "full 7.4-Hz saved PIV scale fields reprojected with saved HWA basis; raw HWA filter and high-rate reconstruction not rerun",
              "checks": checks, "cases": rows,
              "corrected_output_policy": "Small-scale moments recomputed as corresponding original minus corresponding large scale; archived wS/vS are diagnostic only",
              "historical_bug_source": "PREPROCESSING/RdS_PIV_HWA_XZ_POD-LSE/XZ_POD_LSE_copy2_short.m:208-209",
              "published_figure_impact": "not established; RdS_POD_LSE_Statistics.m recomputes correct small scales; highf2/177Hz contour scripts load vS and require figure-level tracing"}
    (output / "validation.json").write_text(json.dumps(report, indent=2))
    return {"passed": sum(c["pass"] for c in checks), "failed": [c for c in checks if not c["pass"]]}
