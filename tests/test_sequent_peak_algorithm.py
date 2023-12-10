import pytest

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

def test_storage_empty(q_in_sample: list[float], q_out_sample: list[float]) -> None:
    assert _storage(q_in=[], q_out=[]) == []
    assert _storage(q_in=[], q_out=q_out_sample) == []
    assert _storage(q_in=q_in_sample, q_out=[]) == []
    
# --------------------------------------------------
# Test _cumulative_storage
# --------------------------------------------------

def test_cumulative_storage(storage_sample: list[float]) -> None:
    print(_cumulative_storage(storage=storage_sample))
    assert _cumulative_storage(storage=storage_sample) == [1.0, 3.0, 6.0, 7.0, 9.0, 14.0, 18.0]

def test_cumulative_storage_empty() -> None:
    assert _cumulative_storage(storage=[]) == []

# --------------------------------------------------
# Test _maxima
# --------------------------------------------------

def test_maxima(cum_storage_sample: list[float]) -> None:
    assert _maxima(cum_storage=cum_storage_sample)[0] == [3.0, 6.0]
    assert _maxima(cum_storage=cum_storage_sample)[1] == [1, 5]

def test_maxima_empty() -> None:
    with pytest.raises(AssertionError):
        _maxima(cum_storage=[])

# --------------------------------------------------
# Test _minima
# --------------------------------------------------

def test_minima(cum_storage_sample: list[float]) -> None:
    assert _minima(cum_storage=cum_storage_sample, max_indices=[1, 5])[0] == [1.0]
    assert _minima(cum_storage=cum_storage_sample, max_indices=[1, 5])[1] == [4]

def test_minima_empty(cum_storage_sample: list[float]) -> None:
    with pytest.raises(AssertionError):
        _minima(cum_storage=cum_storage_sample, max_indices=[])
    with pytest.raises(AssertionError):
        _minima(cum_storage=[], max_indices=[1, 5])
    
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

def test_capacity_empty() -> None:
    with pytest.raises(AssertionError):
        _capacity(max_vals=[], max_indices=[1, 5], min_vals=[1.0], min_indices=[4])
    with pytest.raises(AssertionError):
        _capacity(max_vals=[3.0, 6.0], max_indices=[], min_vals=[1.0], min_indices=[4])
    with pytest.raises(AssertionError):
        _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=[], min_indices=[4])
    with pytest.raises(AssertionError):
        _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=[1.0], min_indices=[])
    with pytest.raises(AssertionError):
        _capacity(max_vals=[], max_indices=[], min_vals=[1.0], min_indices=[4])
    with pytest.raises(AssertionError):
        _capacity(max_vals=[3.0, 6.0], max_indices=[1, 5], min_vals=[], min_indices=[])
    with pytest.raises(AssertionError):
        _capacity(max_vals=[], max_indices=[], min_vals=[], min_indices=[])
        
# --------------------------------------------------
# Test spa
# --------------------------------------------------

def test_spa() -> None:
    res = spa(
        q_in=[1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 5.0, 2.0],
        q_out=[1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 4.0]
        )
    assert res.q_in ==                  [1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 5.0, 2.0]
    assert res.q_out ==                 [1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 4.0]
    assert res.storage ==               [0.0, 1.0, 2.0, -3.0, 1.0, 2.0, 4.0, -2.0]
    assert res.cumulative_storage ==    [0.0, 1.0, 3.0, 0.0, 1.0, 3.0, 7.0, 5.0]
    assert res.max_vals ==              [3.0, 7.0]
    assert res.max_indices ==           [2, 6]
    assert res.min_vals ==              [0.0]
    assert res.min_indices ==           [3]
    assert res.capacity ==              3.0
    assert res.capacity_indices ==      [3]
    assert res.capacity_max_vals ==     [3.0]
    assert res.capacity_max_indices ==  [2]
    assert res.capacity_min_vals ==     [0.0]
    assert res.capacity_min_indices ==  [3]
    
# --------------------------------------------------
# Test sim
# --------------------------------------------------

def test_sim() -> None:
    res = sim(
        q_in=                           [1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 5.0, 2.0],
        q_out=                          [1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 4.0],
        initial_storage=                0.0,
        capacity=                       7.0
        )

    assert res.q_in ==                  [1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 5.0, 2.0]
    assert res.q_out ==                 [1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 4.0]
    assert res.capacity ==              7.0
    assert res.inital_storage ==        0.0
    assert res.q_out_real ==            [1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 4.0]
    assert res.storage ==               [0.0, 1.0, 3.0, 0.0, 1.0, 3.0, 7.0, 5.0]
    assert res.deficit ==               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert res.overflow ==              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

def test_sim_overflow() -> None:
    res = sim(
        q_in=                           [1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 5.0, 2.0],
        q_out=                          [1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 4.0],
        initial_storage=                0.0,
        capacity=                       5.0
        )

    assert res.q_in ==                  [1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 5.0, 2.0]
    assert res.q_out ==                 [1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 4.0]
    assert res.capacity ==              5.0
    assert res.inital_storage ==        0.0
    assert res.q_out_real ==            [1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 3.0, 4.0]
    assert res.storage ==               [0.0, 1.0, 3.0, 0.0, 1.0, 3.0, 5.0, 3.0]
    assert res.deficit ==               [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert res.overflow ==              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 0.0]

def test_sim_deficit() -> None:
    res = sim(
        q_in=                           [1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 5.0, 2.0],
        q_out=                          [1.0, 1.0, 1.0, 5.0, 1.0, 1.0, 1.0, 4.0],
        initial_storage=                0.0,
        capacity=                       7.0
        )

    assert res.q_in ==                  [1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 5.0, 2.0]
    assert res.q_out ==                 [1.0, 1.0, 1.0, 5.0, 1.0, 1.0, 1.0, 4.0]
    assert res.capacity ==              7.0
    assert res.inital_storage ==        0.0
    assert res.q_out_real ==            [1.0, 1.0, 1.0, 4.0, 1.0, 1.0, 1.0, 4.0]
    assert res.storage ==               [0.0, 1.0, 3.0, 0.0, 1.0, 3.0, 7.0, 5.0]
    assert res.deficit ==               [0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0]
    assert res.overflow ==              [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]