# `pydykit`: A *py*thon-based *dy*namics simulation tool*kit*

The target of `pydykit` is to provide a basic framework for the simulation of dynamical systems. Making use of well-established python-packages like `numpy` and `pandas`, this framework should be easily accesible. It is based on time stepping methods, which are discrete versions of the corresponding dynamics equations - either ordinary differential equations (ODEs) or differential-algebraic equations (DAEs).

## How to start

1. Starting on a new machine, create a new virtual environment and activate it. We recommend using `venv`:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the requirements for `pydykit`, which can be found in the `.txt`-file:

   ```bash
   pip install -r requirements_dev.txt
   ```

3. Install the local python package `pydykit` in editable-/develoment-mode:

   ```bash
   pip install --editable .
   ```

4. Run your first script, e.g.

   ```bash
   python scripts/s<no>_<name>.py
   ```

## Running tests against installed code

See [test/README.md](./test/README.md)
