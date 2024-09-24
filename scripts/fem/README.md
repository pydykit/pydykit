# Comparison of Python-Based Finite Element Frameworks

- [PyFEM](https://github.com/jjcremmers/PyFEM)
- [skikit-fem](https://github.com/kinnala/scikit-fem)
- [FEniCS](https://github.com/FEniCS/dolfinx)
- [sfepy](https://github.com/sfepy/sfepy)

## Assessment

From my perspective, only FEniCS and scikit-fem are real options for us.
I would recommend to create small proof of concepts (POC) for both.

The content of these POCs could be:

- 2D or 3D tension test
  - displacement-controlled tension test
  - with straight rectangular specimen
  - of isotropic material and
  - prohibited lateral displacement within the clamping area
  - assuming small deformation.

This is the simplest (kind of real life) mechanical-engineering-like example I can think of.

### Scikit-fem

#### Installation

```bash
pip install scikit-fem
pip install meshio
```

Download [Paraview](https://www.paraview.org/download/), unzip, rename top-level directory to `paraview` and execute `paraview/bin/paraview`.
This should open paraview and allow you to open the vtk-file generated from script `scikit_fem_01.py`.

#### Run Scikit-fem Scripts

```bash
cd scripts/finite_elements_frameworks/scikit_fem/
ipython
# % run s0xx....
```
