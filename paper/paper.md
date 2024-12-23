---
title: "pydykit: A Python-based dynamics simulation toolkit"
tags:
  - Python
  - Dynamics
  - Finite-dimensional systems
  - Simulation
  - Numerical methods
  - Structure-preserving discretization
authors:
  - name: Julian Karl Bauer^[corresponding author]
    orcid: 0000-0002-4931-5869
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Philipp Lothar Kinon
    orcid: 0000-0002-4128-5124
    affiliation: "2"
  # - name: Peter Betsch
  #   orcid: 0000-0002-0596-2503
  #   affiliation: "1"
affiliations:
  - name: Institute of Mechanics, Karlsruhe Institute of Technology (KIT), Karlsruhe, Germany
    index: 2
  - name: Independent Researcher, Karlsruhe, Germany
    index: 1
date: 23 Dezember 2024
bibliography: paper.bib
---

# Summary

`pydykit` is an open-source Python package stating a framework for the numerical computation of dynamical systems.
These dynamic systems are, for example, particle systems, rigid body systems or chemical reactions,
encoded in terms of multibody dynamics with holonomic constraints or port Hamiltonian systems.

As the successor to the MATLAB package `metis`, `pydykit` inherits and builds upon its core features, offering a robust,
object-oriented framework suitable for solving differential-algebraic equations (DAEs).
With a focus on usability and modularity, `pydykit` integrates seamlessly with the Python ecosystem and
supports a variety of numerical integration schemes and postprocessing tools.

Structure of the summary:

- High-level functionality
  - Setting the scene: Mechanics and integration
    - Mechanical system
    - Differential equations
    - Initial-boundary-value-problem
    - Numerical solution based on discretization
- Purpose of the software for a diverse, non-specialist audience.
  - (Do not yet talk solely about content (integrators), but why you intent to distribute metis)
  - Support papers
  - Increase reproducibility
  - Basis for object oriented integration code in cooperations and teaching
  - Lower the barrier for students to contribute in the fields of ...
  - Share research view on ...
  - Close gap on state-of-the-art structure-preserving ....
- Decision for Python
  - Pros and cons
  - Alternatives

# Statement of Need

The analysis and simulation of constrained dynamical systems are integral to many fields,
including robotics, electric circuits, chemical engineering, biomechanics, mechanical and civil engineering and much more .

- General introduction
- Classification of numerical time integrators:
  - _Geometric_ or _structure-preserving_ integration [@hairer_geometric_2006].
  - _Energy-momentum_ (EM) methods using _discrete gradients_ (see, e.g. [@gonzalez_time_1996])
    or variational integrators [@lew2016brief], [@marsden_discrete_2001],
    which have been extended to DAEs in [@leyendecker_variational_2008].
- List alternative packages and highlight what they lack, i.e., which gap is closed by `pydykit`.

# Features

- System classification:
  - Hamiltonian dynamics with or without constraints [@leimkuhler_simulating_2005], also systems governed by differential-algebraic equations (DAEs) [@kunkel_differential-algebraic_2006] are feasible.
  - Rigid body dynamics in terms of _directors_ [@betsch2001constrained].
  - Simulation of _port-Hamiltonian_ systems [@duindam_modeling_2009].

`pydykit` provides:

- A Python-native implementation for optimal accessibility.
- Enhanced modularity and flexibility for custom applications.
- Tools for postprocessing, including animations and data export.
- Extensibility for
  - Systems
  - Simulator including solver
  - Integrator and
  - Time stepper

## Input Configuration

Simulations are defined in terms of configuration files in combination with `pydykit`-classes.
Within the configuration file, `pydykit`-classes are referenced
alongside a set of parameters.
On simulation start, `pydykit` passes these parameters to the `pydykit`-classes.
Dependencies are injected in terms of a central manager class which represents shared state among the building blocks system, simulator, integrator and time stepper.

Users can encode new systems, integrators, timesteppers, and solvers by defining them based on the provided interface descriptions.
Newly added objects can then be registered and referenced within configuration files.
This flexibility allows users to extend `pydykit`’s functionality and tailor it to specific applications.
Each simulation is defined by a combination of the configuration file and the Python.

## Simulation Workflow

1. Initialization: The input file is loaded, creating objects for the specified problem.
2. Computation: Numerical integration is performed using methods such as direct methods, variational integrators, or energy-momentum schemes. The results are stored in terms of a dataframe.
3. Postprocessing: Results are calculated on requested temporal resolution and can be visualized through plots and animations.

## Code structure

![an image's alt text \label{fig:structure_image}](./figures/image.png){ width=70% }

# Theoretical Background

pydykit supports the simulation of a broad range of dynamical systems governed by both ordinary differential equations (ODEs) and differential-algebraic equations (DAEs). This includes
1. Very general systems can be implemented such as quasilinear DAEs of type
`E(x) \dot{x} = f(x)`, where `E` is a possibly singular coefficient matrix and $f$ is a general function of the unknowns `x`.
2. DAEs with a port-Hamiltonian structure, i.e. `E(x) \dot{x} = (J(x)- R(x)) z(x) + B(x) u`, see e.g. TODO
3. Mechanical (typically multibody) systems `\dot{q} = v`, `\dot{p} = - \nabla V(q) - D(q) v - G(q)^T \lambda`, `g(q)=0`

Many dynamical systems from various physical disciplines fit into the first two frameworks and thus pydykit is open for users from a plethora of application fields.

Key theoretical concepts include:

- Hamiltonian Dynamics: Leveraging Hamiltonian mechanics for constrained systems.
- Numerical Integration: Supporting structure-preserving algorithms, including variational integrators and energy-momentum schemes.

## Usage so far

`pydykit` has been recently used in the authors work TODO where discrete gradient based methods have been discussed for the class of port-Hamiltonian systems governed by differential-algebraic equations. Its predecessor `metis` has been used in three major contributions dealing with the simulation of rigid and multibody systems, focussing on structure-preserving integration, e.g. variational and energy-momentum integrators.

# Acknowledgements

PLK gratefully acknowledges financial support by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – project numbers TODO XX and TODO YY.

# References
