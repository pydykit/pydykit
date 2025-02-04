# Welcome to `pydykit`


## What is `pydykit`?

`pydykit` is a *Py*thon-based *dy*namics simulation tool*kit* for dynamical systems. The package is based on time stepping methods, which are discrete versions of the corresponding dynamics equations - either ordinary differential equations (ODEs) or differential-algebraic equations (DAEs).

## How to install?

Directly install from
[the Python Package Index (PyPI)](https://pypi.org/project/pydykit/)
with

```bash linenums="0"
pip install pydykit
```

or clone the repository and install the package locally, following these steps:

1. Create a new virtual environment and activate it.
   We recommend using `venv`:
   ```bash linenums="0"
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
2. Clone the repository
3. Install in editable- / development-mode:
   ```bash linenums="0"
   pip install --editable .
   ```
4. Run your first script, e.g.
   ```bash linenums="0"
   python scripts/s*.py
   ```

## How to use?

Check out the
[getting started](getting_started.md) to familiarize yourself with `pydykit`
and
[examples](examples/pendulum_3d.md) for more details.


## Who are we?

- **Julian K. Bauer** - _Code architect_ - [@JulianKarlBauer](https://github.com/JulianKarlBauer)
- **Philipp L. Kinon** - _Core developer_ - [@plkinon](https://github.com/plkinon)
