from pathlib import Path
import numpy as np
import pytest
from rds2024 import analysis


def test_scale_statistics_match_component_residual():
    rng = np.random.default_rng(25)
    original = rng.normal(size=(4, 3, 17))
    large = rng.normal(size=original.shape)
    small = original-large
    variance, variance_large, terms, closure = analysis.scale_statistics(original, large, batch_size=5)
    expected = np.stack([np.mean(large**3, axis=2),
                         3*np.mean(large**2*small, axis=2),
                         3*np.mean(large*small**2, axis=2),
                         np.mean(small**3, axis=2)])
    np.testing.assert_allclose(variance, np.mean(original**2, axis=2))
    np.testing.assert_allclose(variance_large, np.mean(large**2, axis=2))
    np.testing.assert_allclose(terms, expected, atol=1e-14)
    np.testing.assert_allclose(terms.sum(axis=0), np.mean(original**3, axis=2), atol=1e-14)
    assert closure < 1e-14


@pytest.mark.parametrize("error", [0.0, 1e-3, np.nan])
def test_workflow_uses_only_original_and_large_fields(tmp_path, monkeypatch, error):
    root = tmp_path/'DATA'
    root.mkdir()
    rng = np.random.default_rng(26)
    basis = np.linalg.qr(rng.normal(size=(40, 3)))[0]
    arrays = {}
    for component in 'uwv':
        original = rng.normal(size=(4, 19, 40))
        flat = original.reshape(-1, 40, order='F').T
        projected = (basis@(flat.T@basis).T).T.reshape(original.shape, order='F')
        arrays[f'{component}_org_7d4_6b.mat'] = original
        arrays[f'{component}L_7d4_6b.mat'] = projected + (error if component == 'w' else 0)
    loaded = []
    def load(path):
        loaded.append(path.name)
        assert path.name in arrays, 'Unexpected dependency on a saved small-scale field'
        return arrays[path.name]
    monkeypatch.setattr(analysis, 'load_velocity', load)
    monkeypatch.setattr(analysis, 'one_mat', lambda p: np.arange(4)*.01 if p.name == 'PIV_z.mat' else basis)
    result = analysis.validate_lse(root, tmp_path/'out', ['6b'])
    assert set(loaded) == set(arrays) and len(loaded) == 6
    if error == 0:
        assert result['failed'] == []
    else:
        assert any(c['name'] == '6b/w/LSE-direct-projection' for c in result['failed'])
    for component in 'uwv':
        with np.load(tmp_path/'out'/f'6b_{component}_scale_statistics.npz') as saved:
            original = arrays[f'{component}_org_7d4_6b.mat']
            if component != 'w' or np.isfinite(error):
                np.testing.assert_allclose(saved['third_order_terms'].sum(0), np.mean(original**3, axis=2), atol=1e-12)
