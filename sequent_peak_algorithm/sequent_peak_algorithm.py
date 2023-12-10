import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt

    
def _storage(q_in: list[float], q_out: list[float]) -> list[float]:
    """Calculate the storage as the difference between inflow and outflow."""
    return [x-y for x, y in zip(q_in, q_out)]
    
def _cumulative_storage(storage: list[float]) -> list[float]:
    """Calculate the cumulative storage."""
    return [sum(storage[:i]) for i in range(1, len(storage)+1)]
    
def _maxima(cum_storage: list[float]) -> tuple[list[float], list[int]]:
    """
    A maximum is a value greater than its predecessor and 
    its successor and all following maxima must be greater 
    than the previous one.
    """
    assert cum_storage != [], "Cumulative storage is empty!"
    
    max_vals: list[float] = []
    max_indices: list[int] = []
    for i in range(1, len(cum_storage)-1):
        if cum_storage[i-1] < cum_storage[i] and cum_storage[i] > cum_storage[i+1]:
            if len(max_vals) == 0:
                max_vals.append(cum_storage[i])
                max_indices.append(i)
            else:
                if cum_storage[i] > max_vals[-1]:
                    max_vals.append(cum_storage[i])
                    max_indices.append(i)
    return max_vals, max_indices
    
def _minima(
        cum_storage: list[float],
        max_indices: list[int]
        ) -> tuple[list[float], list[int]]:  
    """
    A minimum is the smallest value between two maxima which
    locations are given as max_indices.
    """
    assert cum_storage != [], "Cumulative storage is empty!"
    assert max_indices != [], "Maxima indices are empty!"
    
    min_vals: list[float] = []
    min_indices: list[int] = []
    for i in range(len(max_indices)-1):
        min_val = min(cum_storage[max_indices[i]:max_indices[i+1]])
        print(min_val)
        min_vals.append(min_val)
        min_index = np.argmin(cum_storage[max_indices[i]:max_indices[i+1]]) + max_indices[i]
        min_indices.append(min_index.astype(int))
    return min_vals, min_indices
    
def _capacity(
        max_vals: list[float],
        max_indices: list[int],
        min_vals: list[float],
        min_indices: list[int]
        ) -> tuple[float, list[float], list[int], list[float], list[int]]:
    """Calculate capacity and its location."""
    
    assert max_vals != [], "Maxima values are empty!"
    assert max_indices != [], "Maxima indices are empty!"
    assert min_vals != [], "Minima values are empty!"
    assert min_indices != [], "Minima indices are empty!"
    
    # Remove last maximum because no minimum can follow.
    max_vals = max_vals[:-1]
    max_indices = max_indices[:-1]
    
    # Calculate storage differences between consecutive maxima and minima.
    diff: list[float] = [i-j for i, j in zip(max_vals, min_vals)]

    # Get maximum difference and its location.
    cap: float = max(diff)
    cap_indices: list[int] = [i for i, j in enumerate(diff) if j == cap]
    
    # Get corresponding minima and maxima and their locations.
    cap_min_vals: list[float] = [min_vals[i] for i in cap_indices]
    cap_min_indices: list[int] = [min_indices[i] for i in cap_indices]
    cap_max_vals: list[float] = [max_vals[i] for i in cap_indices]
    cap_max_indices: list[int] = [max_indices[i] for i in cap_indices]
    return cap, cap_min_vals, cap_min_indices, cap_max_vals, cap_max_indices

def spa(
        q_in: list[float],
        q_out: list[float]
        ):
    
    assert len(q_in) == len(q_out), "Inflow and outflow must have the same length!"
    assert len(q_in) != 0, "Inflow is empty!"
    assert len(q_out) != 0, "Outflow is empty!"
    
    # Calculate storage.
    storage = _storage(
        q_in=q_in,
        q_out=q_out
        )
    
    # Calculate cumulative storage.
    cum_storage = _cumulative_storage(
        storage=storage
    )
    
    # Get maxima and their locations.
    max_vals, max_indices = _maxima(
        cum_storage=cum_storage
        )
    
    # Get minima and their locations.
    min_vals, min_indices = _minima(
        cum_storage=cum_storage,
        max_indices=max_indices
        )
    
    # Get capacity and its location.
    cap, cap_min_vals, cap_min_indices, cap_max_vals, cap_max_indices = _capacity(
        max_vals=max_vals,
        max_indices=max_indices,
        min_vals=min_vals,
        min_indices=min_indices
        )
    
    Result = namedtuple("Result", [
        "q_in", 
        "q_out",
        "storage",
        "cumulative_storage",
        "max_vals", "max_indices",
        "min_vals", "min_indices",
        "capacity", "capacity_indices",
        "capacity_max_vals", "capacity_max_indices",
        "capacity_min_vals", "capacity_min_indices",
        ]
    )
    
    return Result(
        q_in=q_in,
        q_out=q_out,
        storage=storage,
        cumulative_storage=cum_storage,
        max_vals=max_vals,
        max_indices=max_indices,
        min_vals=min_vals,
        min_indices=min_indices,
        capacity=cap,
        capacity_indices=cap_min_indices,
        capacity_max_vals=cap_max_vals,
        capacity_max_indices=cap_max_indices,
        capacity_min_vals=cap_min_vals,
        capacity_min_indices=cap_min_indices,
        )

def sim(
        q_in: list[float],
        q_out: list[float],
        initial_storage: float,
        capacity: float,
        ):
    """Run storage simulation."""
    
    assert len(q_in) == len(q_out), "Inflow and outflow must have the same length!"
    assert len(q_in) != 0, "Inflow is empty!"
    assert len(q_out) != 0, "Outflow is empty!"
    assert initial_storage >= 0, "Initial storage must be greater or equal to zero!"
    assert capacity > 0, "Capacity must be greater than zero!"
    
    q_out_real = []
    storage = []
    deficit = []
    overflow = []    
    
    # Initial storage    
    current_storage = initial_storage
    
    # Start simulation
    for i in range(len(q_in)):
        
        # Add netto inflow to current storage
        current_storage += q_in[i] - q_out[i]
        
        # Empty storage
        if current_storage < 0:
            storage.append(0)
            deficit.append(current_storage)
            overflow.append(0)
            q_out_real.append(q_out[i]+current_storage)
            current_storage = 0

        # Full storage
        elif current_storage > capacity:
            
            storage.append(capacity)
            deficit.append(0)
            overflow.append(current_storage-capacity)
            q_out_real.append(q_out[i]+current_storage-capacity)
            current_storage = capacity

        # Normal storage
        else:
            if current_storage < 0:
                raise ValueError("Negative storage!")
            else:
                storage.append(current_storage)
                deficit.append(0)
                overflow.append(0)
                q_out_real.append(q_out[i])
    
    Result = namedtuple("Result", [
        "q_in",
        "q_out",
        "capacity",
        "inital_storage",
        "q_out_real",
        "storage",
        "deficit",
        "overflow",
        ])

    return Result(
        q_in=q_in,
        q_out=q_out,
        capacity=capacity, 
        inital_storage=initial_storage,
        q_out_real=q_out_real,
        storage=storage,
        deficit=deficit,
        overflow=overflow
        )


scatter_kwargs = {
    "s": 60,
    "zorder": 2,
    "alpha": 0.75,
    "marker": "."
}
title_kwargs = {
    "fontsize": 10,
    "fontweight": "bold",
    "color": "grey",
    "loc": "left",
}
colors = {
    "blue": "#4B77BE",
    "red": "#d11149",
    "green": "#55a630",
}

def spa_plot(res):
    """Plot the results of the sequent peak algorithm."""
    
    fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(10, 8), sharex=True, 
                           gridspec_kw={'hspace': 0.4})
    
    titles = ["A. Inflow", "B. Outflow", "C. Storage", "D. Cumulative storage"]
    
    ax[0].bar(range(len(res.q_in)), res.q_in, color=colors["blue"])
    ax[1].bar(range(len(res.q_out)), res.q_out, color=colors["blue"])
    ax[2].bar(range(len(res.storage)), res.storage, color=colors["blue"])
    ax[3].plot(res.cumulative_storage, color=colors["blue"], lw=1.0)
    ax[3].scatter(res.max_indices, res.max_vals, label="Max", 
                  color=colors["red"], **scatter_kwargs)
    ax[3].scatter(res.min_indices, res.min_vals, label="Min", 
                  color=colors["green"], **scatter_kwargs)

    for i in range(len(res.capacity_indices)):
        line_vert = [
            (res.capacity_min_indices[i], res.capacity_min_vals[i]),
            (res.capacity_min_indices[i], res.capacity_max_vals[i])
            ]
        line_horiz = [
            (res.capacity_min_indices[i], res.capacity_max_vals[i]),
            (res.capacity_max_indices[i], res.capacity_max_vals[i])
            ]
        ax[3].plot(*zip(*line_vert), 
                   color="black", linestyle="--", linewidth=1.0)
        ax[3].plot(*zip(*line_horiz), 
                   color="black", linestyle="--", linewidth=1.0)
    
    for i in range(4):
        ax[i].grid(True, color="grey", alpha=0.3)
        ax[i].set_title(titles[i], **title_kwargs)
    for i in [0, 1, 2]:
        ax[i].set_ylim(top=max(max(res.q_in), max(res.q_out), max(res.storage)*1.3))
    ax[3].legend(loc="upper left", fontsize=10, frameon=False)
    
    return fig
    
def sim_plot(res):
    """Plot the results from the storage simulation."""
    
    fig, ax = plt.subplots(nrows=5, ncols=1, figsize=(10, 10), sharex=True, 
                           gridspec_kw={'hspace': 0.4})
    
    titles = ["A. Inflow", "B. Outflow", "C. Real outflow",
              f"D. Storage (Capacity: {round(res.capacity, 3)}", 
              "E. Deficit/ Overflow"]
    
    ax[0].bar(range(len(res.q_in)), res.q_in, color=colors["blue"])
    ax[1].bar(range(len(res.q_out)), res.q_out, color=colors["blue"])
    ax[2].bar(range(len(res.q_out_real)), res.q_out_real, color=colors["blue"])
    ax[3].bar(range(len(res.storage)), res.storage, color=colors["blue"])
    
    deviation = [x+y for x, y in zip(res.deficit, res.overflow)]
    ax[4].plot(range(len(deviation)), [0]*len(deviation), color="grey", lw=0.5)
    ax[4].bar(range(len(res.deficit)), res.deficit, color=colors["red"])
    ax[4].bar(range(len(res.overflow)), res.overflow, color=colors["green"])
    
    for i in range(5):
        ax[i].set_title(titles[i], **title_kwargs)
        ax[i].grid(True, color="grey", alpha=0.3)
    for i in range(3):
        ax[i].set_ylim(top=max(max(res.q_in), max(res.q_out), max(res.q_out_real)*1.3))
    
    return fig