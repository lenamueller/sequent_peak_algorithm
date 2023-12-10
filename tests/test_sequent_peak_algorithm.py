import pytest
import numpy as np

from sequent_peak_algorithm.sequent_peak_algorithm import _maxima, _minima, \
    _capacity, _storage, _cumulative_storage, spa, sim


@pytest.fixture
def q_in_sample() -> list[float]:
    return [2.0, 3.0, 4.0, 2.0, 3.0, 6.0, 5.0]

@pytest.fixture
def q_out_sample() -> list[float]:
    return [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

@pytest.fixture
def storage_sample() -> list[float]:
    return [1.0, 2.0, 3.0, 1.0, 2.0, 5.0, 4.0]

@pytest.fixture
def cum_storage_sample() -> list[float]:
    return [1.0, 3.0, 2.0, 3.0, 1.0, 6.0, 5.0]

# --------------------------------------------------
# Test _storage
# --------------------------------------------------

def test_storage(q_in_sample: list[float], q_out_sample: list[float]) -> None:
    assert _storage(q_in=q_in_sample, q_out=q_out_sample) == [1.0, 2.0, 3.0, 1.0, 2.0, 5.0, 4.0]

def test_storage_empty() -> None:
    assert _storage(q_in=[], q_out=[]) == []
    
def test_storage_q_in_empty(q_out_sample: list[float]) -> None:
    assert _storage(q_in=[], q_out=q_out_sample) == []
    
def test_storage_q_out_empty(q_in_sample: list[float]) -> None:
    assert _storage(q_in=q_in_sample, q_out=[]) == []

def test_storage_nan(q_in_sample: list[float], q_out_sample: list[float]) -> None:
    nan_list = [np.nan for i in range(len(q_in_sample))]
    assert _storage(q_in=[1.0, 2.0, 3.0, 4.0, 5.0], q_out=nan_list) == None

def test_storage_q_in_not_list(q_out_sample: list[float]) -> None:
    assert _storage(q_in=1.0, q_out=q_out_sample) == None

def test_storaga_q_str_input(q_out_sample: list[float]) -> None:
    assert _storage(q_in='a', q_out=q_out_sample) == None

def test_storaga_q_str_input2(q_out_sample: list[float]) -> None:
    assert _storage(q_in=['a'], q_out=q_out_sample) == None

# --------------------------------------------------
# Test _cumulative_storage
# --------------------------------------------------

def test_cumulative_storage(storage_sample: list[float]) -> None:
    print(_cumulative_storage(storage=storage_sample))
    assert _cumulative_storage(storage=storage_sample) == [1.0, 3.0, 6.0, 7.0, 9.0, 14.0, 18.0]

def test_cumulative_storage_empty() -> None:
    assert _cumulative_storage(storage=[]) == []

def test_cumulative_storage_nan(storage_sample: list[float]) -> None:
    nan_list = [np.nan for i in range(len(storage_sample))]
    assert _cumulative_storage(storage=nan_list) == None

def test_cumulative_storage_not_list() -> None:
    assert _cumulative_storage(storage=1.0) == None
    
def test_cumulative_storage_str_input() -> None:
    assert _cumulative_storage(storage='a') == None

# --------------------------------------------------
# Test _maxima
# --------------------------------------------------

def test_maxima(cum_storage_sample: list[float]) -> None:
    assert _maxima(cum_storage=cum_storage_sample)[0] == [3.0, 6.0]
    assert _maxima(cum_storage=cum_storage_sample)[1] == [1, 5]

def test_maxima_empty() -> None:
    assert _maxima(cum_storage=[]) == ([], [])

def test_maxima_nan(cum_storage_sample: list[float]) -> None:
    nan_list = [np.nan for i in range(len(cum_storage_sample))]
    assert _maxima(cum_storage=nan_list) == None

def test_maxima_not_list() -> None:
    assert _maxima(cum_storage=1.0) == None

def test_maxima_str_input() -> None:
    assert _maxima(cum_storage='a') == None

def test_maxima_no_maxima() -> None:
    assert _maxima(cum_storage=[1.0, 2.0, 3.0, 4.0, 5.0]) == ([], [])

# --------------------------------------------------
# Test _minima
# --------------------------------------------------

def test_minima(cum_storage_sample: list[float]) -> None:
    assert _minima(cum_storage=cum_storage_sample, max_indices=[1, 5])[0] == [1.0]
    assert _minima(cum_storage=cum_storage_sample, max_indices=[1, 5])[1] == [4]

def test_minima_empty_1() -> None:
    assert _minima(cum_storage=[], max_indices=[1, 5]) == None

def test_minimum_empty_2(cum_storage_sample: list[float]) -> None:
    assert _minima(cum_storage=cum_storage_sample, max_indices=[]) == None

def test_minima_nan(cum_storage_sample: list[float]) -> None:
    nan_list = [np.nan for i in range(len(cum_storage_sample))]
    assert _minima(cum_storage=nan_list, max_indices=[1, 5]) == None

def test_minima_not_list() -> None:
    assert _minima(cum_storage=1.0, max_indices=[1, 5]) == None
    assert _minima(cum_storage=cum_storage_sample, max_indices=1.0) == None

def test_minima_str_input() -> None:
    assert _minima(cum_storage='a', max_indices=[1, 5]) == None
    assert _minima(cum_storage=cum_storage_sample, max_indices='a') == None 
    
# --------------------------------------------------
# Test _capacity
# --------------------------------------------------

def test_capacity() -> None:
    cap, cap_min_vals, cap_min_indices, cap_max_vals, cap_max_indices = _capacity(
        max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=[1.0], min_indices=[4])
    
    assert cap == 2.0
    assert cap_min_vals == [1.0]
    assert cap_min_indices == [4]
    assert cap_max_vals == [3.0]
    assert cap_max_indices == [1]

def test_capacity_no_maxima() -> None:
    assert _capacity(max_vals=[], max_indices=[], min_vals=[1.0], min_indices=[4]) == None

def test_capacity_no_minima() -> None:
    assert _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=[], min_indices=[]) == None

def test_capacity_empty() -> None:
    assert _capacity(max_vals=[], max_indices=[], min_vals=[], min_indices=[]) == None

def test_capacity_nan() -> None:
    nan_list = [np.nan for i in range(5)]
    assert _capacity(max_vals=nan_list, max_indices=[1, 5], min_vals=[1.0], min_indices=[4]) == None
    assert _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=nan_list, min_indices=[4]) == None
    assert _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=[1.0], min_indices=nan_list) == None

def test_capacity_not_list() -> None:
    assert _capacity(max_vals=1.0, max_indices=[1, 5], min_vals=[1.0], min_indices=[4]) == None
    assert _capacity(max_vals=[3.0, 6.0], max_indices=1.0, min_vals=[1.0], min_indices=[4]) == None
    assert _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=1.0, min_indices=[4]) == None
    assert _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=[1.0], min_indices=4) == None

def test_capacity_str_input():
    assert _capacity(max_vals='a', max_indices=[1, 5], min_vals=[1.0], min_indices=[4]) == None
    assert _capacity(max_vals=[3.0, 6.0], max_indices='a', min_vals=[1.0], min_indices=[4]) == None
    assert _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals='a', min_indices=[4]) == None
    assert _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=[1.0], min_indices='a') == None

# --------------------------------------------------
# Test spa
# --------------------------------------------------

# def test_spa(q_in_sample: list[float], q_out_sample: list[float]) -> None:
#     res = spa(q_in=[1.0,2.0,3.0], q_out=[1.0,1.0,1.0])
    # assert res.q_in == q_in_sample
    # assert res.q_out == q_out_sample
    # assert res.storage == [1.0, 2.0, 3.0, 1.0, 2.0, 5.0, 4.0]
    # assert res.cumulative_storage == [1.0, 3.0, 6.0, 7.0, 9.0, 14.0, 18.0]
    # assert res.max_vals == [3.0, 6.0]
    # assert res.max_indices == [1, 5]
    # assert res.min_vals == [1.0]
    # assert res.min_indices == [4]
    # assert res.capacity == 2.0
    # assert res.capacity_indices == [4]
    # assert res.capacity_max_vals == [3.0]
    # assert res.capacity_max_indices == [1]
    # assert res.capacity_min_vals == [1.0]
    # assert res.capacity_min_indices == [4]
    
# --------------------------------------------------
# Test sim
# --------------------------------------------------