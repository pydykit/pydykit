<p align="center">
  <a href="https://github.com/pydykit/pydykit"><img alt="pydykit" src="docs/assets/banner.png" width="50%"></a>
</p>

# `pydykit`: A *Py*thon-based *dy*namics simulation tool*kit*

`pydykit` provides a basic framework for the simulation of dynamical systems.
The package is based on time stepping methods,
which are discrete versions of the corresponding dynamics equations - either ordinary differential equations (ODEs) or differential-algebraic equations (DAEs).

## How to start

1. Starting on a new machine, create a new virtual environment and activate it. We recommend using `venv`:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the local python package `pydykit` in editable-/develoment-mode:

   ```bash
   pip install --editable .
   ```

3. Run your first script, e.g.

   ```bash
   python scripts/s*.py
   ```

## Reproducibilty of published results

`pydykit` can and has been used to tackle scientific questions. The scripts, input-files and results of previous simulations run by this package can be found in the folders contained in [./test/publications](./test/publications) using the naming convention `YEAR_author1_author2_*_journalabbreviation`.

## Running tests against installed code

See [test/README.md](./test/README.md)
