# Solving Partial Differential Equations (PDEs) with `pydykit`

## Motivation

The package `pydykit` focuses on the energy-consistent time integration
of ordinary differential equations (ODEs).
Such ODEs occur in the field of mechanics, for example, when simulating the motion of multi-body systems,
which may consist of, e.g., mass points or rigid bodies.
Each body has certain degrees of freedom, whose temporal evolution can be described by ODEs that can be integrated numerically.
`pydykit` provides methods to perform this integration in an energy-consistent manner.

However, many applications in the field of engineering mechanics involve
structural bodies, such as beams, plates or continua.
The motion of these structures is governed by partial differential equations (PDEs),
which in the case of dynamic problems contain both spatial and temporal gradients.
The standard tool for solving PDEs is the finite element method (FEM).

The aim of the present study is to combine existing FEM codes
for the representation of spatial structures and spatial gradients
with the methods for the temporal integration of `pydykit`.

## Outline

## Comparison of Python-Based Finite Element Frameworks

- [PyFEM](https://github.com/jjcremmers/PyFEM)
- [skikit-fem](https://github.com/kinnala/scikit-fem)
- [FEniCS](https://github.com/FEniCS/dolfinx)
- [sfepy](https://github.com/sfepy/sfepy)

### Assessment

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

#### Scikit-fem

##### Installation

```bash
pip install scikit-fem
pip install meshio
```

Download [Paraview](https://www.paraview.org/download/), unzip, rename top-level directory to `paraview` and execute `paraview/bin/paraview`.
This should open paraview and allow you to open the vtk-file generated from script `scikit_fem_01.py`.

##### Run Scikit-fem Scripts

```bash
cd scripts/finite_elements_frameworks/scikit_fem/
ipython
# % run s0xx....
```
