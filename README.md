# Genetic Algorithm Traveling Salesman Problem (TSP)

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A genetic algorithm for the traveling salesman problem.

| Unsolved Instance | Genetic Algorithm's Tour |
| --- | --- |
| ![Unsolved instance](docs/single_tour_kroA100_run1_nodes.png) | ![Genetic algorithm's tour](docs/single_tour_kroA100_run1_elite.png) |

| Optimal Tour | Percent Error per Generation |
| --- | --- |
| ![Optimal tour](docs/single_tour_kroA100_run1_optimal.png) | ![Percent error per generation](docs/single_convergence_kroA100_run1.png) |



<br>



## Table of Contents

1. [Rationale](#rationale)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Build](#build)
6. [Usage and Example](#usage-and-example)
7. [Plotting](#plotting)
8. [References and Sources](#references-and-sources)



<br>



## Rationale

The traveling salesman problem is an NP-hard problem with no single, fast algorithmic solutions. However, John Holland's schema theorem provides a theoretical foundation for stochastic heuristics. Subsequently, I seek to measure the effectiveness of a genetic algorithm implementation in finding optimal solutions to the Euclidean two-dimensional traveling salesman problem.



<br>



## Features

* Genetic algorithm
    * Tournament selection
    * Order crossover
    * Swap mutation
    * Elitism
    * 2-opt
        * Neighbor lists
        * Don't-look bits
* Parallel offspring generation with OpenMP
* Precomputed distance matrix
* TSPLIB95 known optimal values
* Stops at optimum, after stagnation, or generation limit
* Per-run output files (summary, per-generation history, and elite tour)
* Python plotting tools
* No dependencies

***INSERT RESULTS DOCUMENTATION HERE***



<br>



## Prerequisites

* [Git](https://git-scm.com/)
* C++20 compiler with OpenMP support
    * Must accept GCC-style flags
    * Commands below use [GCC](https://gcc.gnu.org/)
* [Python](https://www.python.org/) 3.10 or newer (only for plotting)



<br>



## Installation

```
git clone https://github.com/kevinn-jie/genetic-algorithm-tsp.git
cd genetic-algorithm-tsp
```

For plotting, also install the Python packages.

```
pip install -r requirements.txt
```



<br>



## Build

Run the build command from the project root.

```bash
g++ -std=c++20 -O3 -march=native -flto=auto -fopenmp -fno-math-errno -fstack-protector-strong -D_FORTIFY_SOURCE=3 -D_GLIBCXX_ASSERTIONS -Wall -Wextra -Wpedantic -static ./src/*.cpp -o ./build/tsp.exe
```

Tested with GCC 16.2.0. `-march=native` optimizes for the building machine's CPU; the executable may not run on older CPUs. To build an executable for other machines, replace it with `-march=x86-64-v3`.



<br>



## Usage and Example

Choose instances by uncommenting their names in `INSTANCES_TO_RUN` in [src/main.cpp](src/main.cpp), and set the number of runs per instance with `RUNS_PER_INSTANCE`. Then rebuild and run the executable.

```
./build/tsp.exe
```

The executable must stay in `build/`; it locates `res/` and `stdout/` relative to its own folder. Each run is written to `stdout/runs/<instance>/run<n>.txt`, overwriting any previous file of the same name.

Algorithm parameters (population size, crossover rate, generation limits, etc.) are in [src/algorithm.h](src/algorithm.h).



<br>



### Example

With `INSTANCES_TO_RUN = { "eil51", "kroA100" }` and `RUNS_PER_INSTANCE = 3`, the console shows:

```
eil51 (dimension 51, load time 0.001)
    run 1 / 3: percent error 0.000, compute time 0.002
    run 2 / 3: percent error 0.000, compute time 0.001
    run 3 / 3: percent error 0.000, compute time 0.001
kroA100 (dimension 100, load time 0.001)
    run 1 / 3: percent error 0.000, compute time 0.002
    run 2 / 3: percent error 0.000, compute time 0.002
    run 3 / 3: percent error 0.000, compute time 0.003
```

Each run file contains a summary, then one line per generation (generation, generation time in seconds, elite tour length, percent error), then the elite tour as TSPLIB node numbers. For example, `stdout/runs/eil51/run1.txt`:

```
instance: eil51
dimension: 51
optimal: 426
elite: 426
compute time: 0.001
percent error: 0.000

generations:
0, 0.000065, 1335, 213.380
1, 0.000526, 428, 0.469
2, 0.000191, 427, 0.235
3, 0.000150, 426, 0.000

tour:
41
40
19
...
```



<br>



## Plotting

Run commands from the project root. Plots are saved to `stdout/plots/`.

| Script | Plot |
| --- | --- |
| `python tools/plot_single_tour.py <run_file>` | Nodes, elite tour, and optimal tour of one run |
| `python tools/plot_single_convergence.py <run_file>` | Percent error per generation of one run |
| `python tools/plot_error_v_dimension.py` | Percent error vs. number of nodes |
| `python tools/plot_error_fit_v_dimension.py` | Percent error vs. number of nodes, with fitted curve |
| `python tools/plot_time_v_dimension.py` | Compute time vs. number of nodes |
| `python tools/plot_time_fit_v_dimension.py` | Compute time vs. number of nodes, with fitted curve |
| `python tools/plot_error_v_generation.py` | Percent error vs. generation |
| `python tools/plot_error_v_time.py` | Percent error vs. compute time |

For example, `python tools/plot_single_tour.py stdout/runs/kroA100/run1.txt` produces images like the tour images at the top of this README. Plots of all runs read every run in `stdout/runs/`.



<br>



## References and Sources

* [TSPLIB95](http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/)
* [Concorde TSP Solver](https://www.math.uwaterloo.ca/tsp/concorde.html)
* [tsplib95 (Python)](https://github.com/rhgrant10/tsplib95)
* [C++ reference](https://cppreference.com/)
* [OpenMP](https://www.openmp.org/)
* John H. Holland, *Adaptation in Natural and Artificial Systems* (1975)
