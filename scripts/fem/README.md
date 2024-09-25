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

We try to answer the question
"What is the interface to combine `pydykit` with FEM codes?".

There are multiple options, outlined below including sub steps:

- Option 01:
  1. Within a class from `pydykit.systems` we could use a FEM code to assemble a `tangent` and a `residuum`,
     i.e., `A` and `b` in common pattern `A x = b`.
  2. `tangent` and `residuum` might then be used to solve for the next state within `pydikit`.
  3. Afterwards, the new state can be used to update FEM fields within the instance of a `pydykit.systems`-class from step 1.
  4. Postprocessing option of the FEM code could be utilized from within `pydykit`.
- Option 02:
  1. Define the variational forma and constraints in FEM-framework
  2. Use the FEM-framework solver
  3. Use the FEM-framework postprocessing

FEM codes, such as

Vocabulary:

- monolithic
  - https://en.wikipedia.org/wiki/Fluid%E2%80%93structure_interaction#Analysis
  - https://fenicsproject.org/pub/tutorial/html/._ftut1010.html#ftut1:reactionsystem
- ## Variational formulation
  - https://fenicsproject.org/pub/tutorial/html/._ftut1010.html#ftut1:reactionsystem

References:

- [Fenics example elastodynamics](https://fenicsproject.org/olddocs/dolfin/2019.1.0/python/demos/elastodynamics/demo_elastodynamics.py.html)
- [Fenics tutorial advection-diffusion-reaction](https://fenicsproject.org/pub/tutorial/html/._ftut1010.html#ftut1:reactionsystem)
- [Fenics course dynamic hyperelasticty](https://fenicsproject.org/pub/course/lectures/2016-04-11-alnaes-simula/lecture_07_dynamic_hyperelasticity.pdf)
- [scikit-fem multiple fields, pressure and velocity](https://github.com/kinnala/scikit-fem/blob/10.0.1/docs/examples/ex18.py)

## Proof of Concept: Euler-Bernoulli-Beam

References:

- [Wikipedia](https://en.wikipedia.org/wiki/Euler%E2%80%93Bernoulli_beam_theory)

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

From ["JOSS: scikit-fem: A Python package for finite element assembly"](file:///home/julian/Downloads/gustafsson2020scikit-fem.pdf)

"In contrast to NGSolve (Schöberl, 2014), FEniCS (Alnæs et al., 2015), Firedrake (Rathgeber et
al., 2016), SfePy (Cimrman, Lukeš, & Rohan, 2019), and GetFEM (Renard & Poulios, 2020),
scikit-fem contains no compiled code making the installation quick and straightforward.
We specifically target **finite element assembly** instead of encapsulating the entire finite element
analysis from pre- to postprocessing into a single framework. As a consequence, we cannot
provide an end-to-end experience when it comes to, e.g., specific physical models or distributed
computing. Our aim is to be generic in terms of PDEs and, hence, support a variety of finite
element schemes. Currently scikit-fem includes basic support for H1-, H(div)-, H(curl)-,
and H2-conforming problems as well as various nonconforming schemes.
scikit-fem accepts **weak forms that depend on** the values and the derivatives of the trial and
the test functions, their high-order derivatives, the local mesh parameter, nonuniform material
or coefficient fields defined at the quadrature points, or any existing finite element solutions.
Iterations related to, e.g., nonlinear problems (Newton’s method and the variants, parameter
continuation) or adaptive mesh refinement (evaluation of functionals and the marking strategy)
should be implemented by the user although we provide basic tools such as interpolation
routines and conforming mesh refinement, and examples by using them. The same applies to
boundary conditions: the linear system (A, b) is provided as such and eliminating or penalizing
the correct degrees-of-freedom, implementing inhomogeneous or periodic boundary conditions
should be done separately either by using the various helper routines of scikit-fem or by
other means. scikit-fem has **no explicit support for distributed computing** although it could
be used as a building block in parallel computations such as parameter sweeps or domain
decomposition techniques.
"

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
