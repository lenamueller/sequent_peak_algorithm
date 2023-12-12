![CI](https://github.com/lenamueller/sequent_peak_algorithm/actions/workflows/python-package-conda.yml/badge.svg)
![license - MIT](https://img.shields.io/badge/license-MIT-ffe05c?logo=github&logoColor=4685b7)
[![field of application - hydrology](https://img.shields.io/badge/field_of_application-hydrology-blue)](https://)

# sequent-peak-algorithm

Python implementation of the Sequent Peak Algorithm for the design and simulation of water reservoirs in hydrology.

# Installation with requirements

```
pip install sequent-peak-algorithm==0.0.5
```

# Usage example

```python 
# 0. Create random input data
q_in = np.random.rand(100) * 10
q_out = np.random.rand(100) * 10

# 1. Run sequent peak algorithm
res_cap = spa.spa(q_in=q_in, q_out=q_out)
print("Capacity: ", res_cap.capacity)

# 2. Plot results from sequent peak algorithm
fig_cap = spa.spa_plot(res_cap)
plt.savefig("example_2_spa.png", dpi=300)

# 3. Run storage simulation and explore results
res_sim = spa.sim(
    q_in=q_in,
    q_out=q_out,
    initial_storage=0.0,
    capacity=res_cap.capacity
)

# Plot results from storage simulation
fig_sim = spa.sim_plot(res_sim)
plt.savefig("example_2_sim.png", dpi=300)
```
For further explanations see the [examples/](examples/) folder.

#### Sequent Peak Algorithm Visualization
![examples/example_2_spa.png](examples/example_2_spa.png)

#### Simulation Visualization
![examples/example_2_sim.png](examples/example_2_sim.png)

# Documentation

## `spa`
#### Parameters
- `q_in: list[float]` : discharge input values
- `q_out: list[float]`: discharge output values

#### Returns
- `Result: collections.namedtuple`: Result of the sequent peak algorithm with the following attributes:
    - `q_in: list[float]`: discharge input values
    - `q_out: list[float]`: discharge output values
    - `storage: list[float]`: storage values, calculated with `_storage`
    - `cumulative_storage: list[float]`: cumulative storage values, calculated with `_cumulative_storage` 
    - `max_vals: list[float]`: discharge values of the maxima, calculated with `_maxima`
    - `max_indices: list[int]`: indices of the maxima, calculated with `_maxima`
    - `min_vals: list[float]`: discharge values of the minima, calculated with `_minima`
    - `min_indices: list[int]`: indices of the minima, calculated with `_minima`
    - `capacity: list[float]`: capacity, calculated with `_capacity`
    - `capacity_indices: list[int]`: indices of the capacity (multiple positions possible), calculated with `_capacity`
    - `capacity_max_vals: list[float]`: preceeding maxima of the capacity, calculated with `_capacity`
    - `capacity_max_indices: list[int]`: indices of the preceeding maxima of the capacity, calculated with `_capacity`
    - `capacity_min_vals: list[float]`: succeeding minima of the capacity, calculated with `_capacity`
    - `capacity_min_indices: list[int]`: indices of the succeeding minima of the capacity, calculated with `_capacity`

## `sim`
#### Parameters
- `q_in: list[float]` : discharge input values
- `q_out: list[float]`: discharge output values
- `initial_storage: float`: initial storage value, chosen by the user
- `capacity: float`: capacity values, calculated with `spa` or chosen by the user

#### Returns
- `Result: collections.namedtuple`: Result of the sequent peak algorithm with the following attributes:
    - `q_in: list[float]` : discharge input values
    - `q_out: list[float]`: discharge output values
    - `initial_storage: float`: initial storage value, chosen by the user
    - `capacity: list[float]`: capacity values, calculated with `spa` or chosen by the user
    - `q_out_real: list[float]`: real discharge output accounting for the capacity (deficit and overflow situations)
    - `storage: list[float]`: storage values
    - `deficit: list[float]`: deficit values
    - `overflow: list[float]`: overflow values

## `spa_plot`
#### Parameters
- `Result: collections.namedtuple`: Result of the sequent peak algorithm
#### Returns
- `fig: matplotlib.figure.Figure`: Figure object of the plot

## `sim_plot`
#### Parameters
- `Result: collections.namedtuple`: Result of the storage simulation
#### Returns
- `fig: matplotlib.figure.Figure`: Figure object of the plot
