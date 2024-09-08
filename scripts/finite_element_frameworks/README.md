# Comparison of Python-Based Finite Element Frameworks

## [PyFEM](https://github.com/jjcremmers/PyFEM)

- License: GPL-3.0 license
- Number of Github-stars: 217
- Number of contributors: **3** (this is very few)
- Number of commits over time: Few, occasionally
- Quality of the docs / API specification: Docs are a book you have to buy... bad idea
- Features (2D, 3D, ...): unknown

## [skikit-fem](https://github.com/kinnala/scikit-fem)

- License: BSD-3-Clause license
- Number of Github-stars: 489
- Number of contributors: 16
- Number of commits over time: Decreasing, pekaed during Covid till beginning 2022. Main developers cooled down begin 2022
- Quality of the docs / API specification: Clean, many examples, looks good from first sight
- Features: Rich, 2D, 3D, solid, fluid, heat, [hyperelasticity](https://github.com/kinnala/scikit-fem/blob/10.0.1/docs/examples/ex43.py), [3d-linear-elasticity](https://github.com/kinnala/scikit-fem/blob/10.0.1/docs/examples/ex11.py)

## [FEniCS](https://github.com/FEniCS/dolfinx)

- License: License: BSD-3-Clause license
- Number of Github-stars: 723
- Number of contributors: 94
- Number of commits over time: Peaked 2018, decreasing, steady action
- Quality of the docs / API specification: Tutorial and API-docs available . Rather academic, background elaborated, more complex than scikit-fem
- Features: Heat, linear elasticity, Navier-Stokes, Hyperelasticity, 3D example not that clear

Large community

## [sfepy](https://github.com/sfepy/sfepy)

- License: License: BSD-3-Clause license
- Number of Github-stars: 728
- Number of contributors: 29
- Number of commits over time: Steady since 2008... wow.. one main developer, second developer rising since 2021
- Quality of the docs / API specification: Many [examples](https://sfepy.org/doc-devel/examples/index.html), Can't find the APi specs... maybe not available?, Scripts seem a bit cryptic.
- Features: heat, homogenization, linear elasticity, large deformations, 1D, 2D, 3D

Looks a bit oldschool, rather messy, more engineering-focused, but [rich example collection on elasticity](https://sfepy.org/doc-devel/examples/linear_elasticity-index.html)...

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

This is the simplest (kind of real life) engineering-like application I can think of.

### Scikit-fem

#### Installation

```bash
pip install scikit-fem
pip install meshio
```

Download [Paraview](https://www.paraview.org/download/), unzip, rename top-level directory to `paraview` and execute `paraview/bin/paraview`.
This should open paraview and allow you to open the vtk-file generated from script `scikit_fem_01.py`.
