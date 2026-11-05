import numpy as np
import pytest
from scipy.io import savemat
from rds2024.io import one_mat

def test_one_mat_rejects_ambiguous_variables(tmp_path):
    p = tmp_path/"v5.mat"
    savemat(p, {"a": np.ones(2), "b": np.zeros(3)})
    with pytest.raises(ValueError):
        one_mat(p)


def test_mat_numeric_read(tmp_path):
    p=tmp_path/"small.mat"
    a=np.arange(12.).reshape(3,4)
    savemat(p,{"velocity":a})
    np.testing.assert_array_equal(one_mat(p),a)
