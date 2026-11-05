"""Paper-specific decomposition kernels; no MATLAB runtime."""
from dataclasses import dataclass
import numpy as np
from scipy.linalg import eigh

@dataclass
class Decomposition:
    modes: np.ndarray
    coefficients: np.ndarray
    energy: np.ndarray
    mean: np.ndarray
    mode_norm: np.ndarray


def pod(data, n_modes=None):
    """Ordinary unweighted POD: first dimension is time, other axes arbitrary."""
    x = np.asarray(data, float)
    if x.ndim < 2 or not np.isfinite(x).all():
        raise ValueError("Expected finite time-first data")
    shape, mean = x.shape, x.mean(axis=0)
    u, s, vh = np.linalg.svd((x-mean).reshape(len(x), -1), full_matrices=False)
    k = len(s) if n_modes is None else n_modes
    if not isinstance(k, int) or not 1 <= k <= len(s):
        raise ValueError("Invalid mode count")
    return Decomposition(vh[:k].T.reshape(*shape[1:], k), u[:, :k]*s[:k], s[:k]**2/len(x), mean, np.ones(k))


def lse_fit(predictors, targets, *, rcond=None):
    """Centered least-squares mapping, never explicitly invert a covariance."""
    b, a = np.asarray(predictors, float), np.asarray(targets, float)
    if b.ndim != 2 or a.ndim != 2 or len(b) != len(a) or not np.isfinite(b).all() or not np.isfinite(a).all():
        raise ValueError("Expected matching finite (time,channel) arrays")
    bmean, amean = b.mean(axis=0), a.mean(axis=0)
    mapping, _, rank, singular = np.linalg.lstsq(b-bmean, a-amean, rcond=rcond)
    return {"mapping": mapping, "predictor_mean": bmean, "target_mean": amean,
            "rank": int(rank), "singular_values": singular}


def lse_predict(model, predictors):
    return (np.asarray(predictors)-model["predictor_mean"])@model["mapping"]+model["target_mean"]


def third_order_split(large, small, axis=0):
    """u'^3 = uL^3 + 3 uL^2 uS + 3 uL uS^2 + uS^3, unnormalized."""
    large, small = np.asarray(large), np.asarray(small)
    if large.shape != small.shape:
        raise ValueError("Scale arrays must have identical shapes")
    return np.stack([np.mean(large**3, axis=axis), 3*np.mean(large**2*small, axis=axis),
                     3*np.mean(large*small**2, axis=axis), np.mean(small**3, axis=axis)])
