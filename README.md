<p align="center">
  <a href="https://github.com/pydykit/pydykit"><img alt="pydykit" src="docs/assets/banner.png" width="50%"></a>
</p>

[![Pytest](https://github.com/pydykit/pydykit/actions/workflows/pytest.yml/badge.svg)](https://github.com/pydykit/pydykit/actions/workflows/pytest.yml)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
<!-- [![PyPI](https://img.shields.io/pypi/v/pydykit?style=flat-square)](https://pypi.org/project/pydykit)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/pydykit?style=flat-square)](https://pypi.org/project/pydykit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydykit?style=flat-square)](https://pypi.org/project/pydykit) -->

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

   Dependencies are installed automatically. Detailed requirements can be found in the [requirements_dev](requirements_dev.txt).

3. Run your first script, e.g.

   ```bash
   python scripts/s*.py
   ```

## Running tests against installed code

See [test/README.md](./test/README.md)

## Built With

- [Venv](https://docs.python.org/3/library/venv.html) - virtual environments for managing dependencies and package versioning.
- [Pre-commit](https://pre-commit.com) - for styling with [black](https://github.com/psf/black) and other formatting.

## Contributing

Please read our code of conduct, fork this repo and initiate a pull request. Feel free to contact us if you have doubts.

## Main Contributors

- **Julian K. Bauer** - _Code architect_ - [@JulianKarlBauer](https://github.com/JulianKarlBauer)
- **Philipp L. Kinon** - _Core developer_ - [@plkinon](https://github.com/plkinon)

See also the list of [contributors](https://github.com/pydykit/pydykit/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<!-- ## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc -->
