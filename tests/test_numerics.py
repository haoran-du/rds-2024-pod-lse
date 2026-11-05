import numpy as np
import pytest
from rds2024.decomposition import pod, third_order_split, lse_fit, lse_predict

def test_pod_reconstruction():
    x = np.random.default_rng(9).normal(size=(25, 4, 3))
    p = pod(x)
    np.testing.assert_allclose(np.einsum("pcm,tm->tpc", p.modes, p.coefficients)+p.mean, x, atol=1e-12)


def test_lse_rank_deficiency_and_offset():
    b = np.random.default_rng(7).normal(size=(50, 3))
    b[:, 2] = b[:, 1]
    a = b@np.array([[1, 2], [3, 4], [5, 6]])+7
    model = lse_fit(b, a)
    assert model["rank"] == 2
    np.testing.assert_allclose(lse_predict(model, b), a, atol=1e-12)


def test_third_moment_closure():
    l, s = np.random.default_rng(8).normal(size=(2, 100, 8))
    np.testing.assert_allclose(third_order_split(l, s).sum(0), np.mean((l+s)**3, axis=0), atol=1e-14)
