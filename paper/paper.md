---
title: "pydykit: A Python-based dynamics simulation toolkit"
tags:
  - Python
  - Dynamics
  - Ordinary differential equations
  - Differential algebraic equations
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
  - name: Independent Researcher, Karlsruhe, Germany
    index: 1
  - name: Institute of Mechanics, Karlsruhe Institute of Technology (KIT), Karlsruhe, Germany
    index: 2
date: 09 February 2025
bibliography: paper.bib
---

# Summary

Understanding and simulating the behavior of dynamical systems is a fundamental challenge in many scientific and engineering disciplines.
These systems are typically described by ordinary differential and differential-algebraic equations that form an initial-boundary-value problem.
Solving such problems numerically requires discretization techniques that translate continuous equations into a computationally feasible form.
Our open-source Python package `pydykit` is designed to facilitate this process by providing a general, accessible and well-structured framework for the numerical treatment of dynamical systems.

As the successor to the MATLAB package `metis`, `pydykit` inherits and builds upon its core features, offering a robust,
object-oriented framework suitable for solving differential-algebraic equations (DAEs).
With a focus on usability and modularity, `pydykit` integrates seamlessly with the Python ecosystem and
supports a variety of numerical integration schemes and postprocessing tools.

# Statement of Need

The motivation behind `pydykit` extends beyond its immediate functionality.
We aim to support research publications by ensuring the reproducibility of computational experiments, thereby enhancing the transparency and credibility of numerical results.
Moreover, `pydykit` serves as a foundation for object-oriented integration methods, fostering collaborations in research and teaching.
By lowering the barrier for students and early-career researchers to contribute to the field,
the software encourages engagement with structure-preserving methods and modern computational approaches.
Additionally, we wish to share our perspective on the numerical treatment of dynamical systems and help bridge gaps in state-of-the-art structure-preserving techniques.
This is why `pydykit` and its predecessor `metis` focus on geometric integration methods [@hairer_geometric_2006], be it energy-momentum schemes using _discrete gradients_ (see, e.g. [@gonzalez_time_1996]), _variational integrators_ [@lew2016brief] or others.

A key decision in the development of `pydykit` was the choice of programming language.
Python was selected due to its accessibility, widespread adoption, and extensive ecosystem of scientific computing libraries.
Its high-level syntax facilitates ease of use, making it an attractive option for researchers, industry applicants and students.
However, Python also presents performance limitations compared to lower-level languages like C++ or Fortran, particularly for computationally intensive tasks.
Alternative frameworks exist in other languages, but we find that Python strikes a balance between usability and extensibility, allowing for seamless integration with high-performance libraries when needed.

# Features

`pydykit` is a flexible framework for simulating a wide range of dynamical systems governed by ordinary differential equations (ODEs) and differential-algebraic equations (DAEs). Thus `pydykit` is open for users from a plethora of application fields. It supports the implementation of

1. General quasilinear DAEs of the form $E(x) \dot{x} = f(x)$,
   where $E(x)$ may be singular, allowing for broad applicability in constrained dynamics.

2. Port-Hamiltonian DAE systems governed by $E(x) \dot{x} = (J(x)- R(x)) z(x) + B(x) u$
   which appear in various physical modeling contexts [@duindam_modeling_2009], also cover open control systems and follow an energy-based modelling approach.

3. Multibody systems formulated as index-3 DAEs with holonomic positional constraints $g(q)$. Beyond standard multibody dynamics, pydykit supports rigid body dynamics using unit quaternions [@betsch_2009_rigid], a powerful approach for modeling rotational motion. The software is also well-suited for Hamiltonian dynamics, with or without constraints [@leimkuhler_simulating_2005], making it an effective tool for structure-preserving simulations. An extension to directors-based formulations [@betsch2001constrained] will be straightforward as it is already implemented in the predecessor framework `metis`.

These formulations make pydykit a versatile tool for researchers across disciplines, from robotics and biomechanics to electrical and thermodynamic systems. The framework incorporates key theoretical concepts, including Hamiltonian dynamics and structure-preserving numerical integration techniques. By providing a unified and extensible approach to modeling and simulation, `pydykit` enables efficient and reproducible research in computational mechanics and beyond.

![Current system classes covered by `pydykit` \label{fig:systems}](./figures/sample.png){width=70%}

`pydykit` is a Python-native framework offering an accessible and modular approach,
and enabling users to define and solve DAEs with ease.
The software provides enhanced flexibility for custom applications, allowing researchers and developers to tailor simulations to their specific needs.
Built-in postprocessing tools, including animation and data export capabilities, facilitate result analysis and visualization.
Furthermore, `pydykit` is highly extensible, supporting modifications at multiple levels, including system definitions,
the simulator and solver, integration schemes, and time-stepping methods.
By combining ease of use with advanced customization options, `pydykit` serves as a versatile platform for research, teaching, and collaborative development in computational mechanics.

## Input Configuration

Simulations are defined in terms of configuration files in combination with `pydykit`-classes.
Within the configuration file, `pydykit`-classes are referenced
alongside a set of parameters.
On simulation start, `pydykit` passes these parameters to the `pydykit`-classes.
Dependencies are injected in terms of a central manager class which represents shared state among the building blocks system, simulator, integrator and time stepper.

Users can encode new systems, integrators, timesteppers, and solvers by defining them based on the provided interface descriptions.
Newly added objects can then be registered and referenced within configuration files.
This flexibility allows users to extend `pydykit`’s functionality and tailor it to specific applications.

## Simulation Workflow

1. Initialization: The input file is loaded, creating objects for the specified problem.
2. Computation: Numerical integration is performed using time-stepping methods. The results are stored in terms of a dataframe.
3. Postprocessing: Results are calculated on requested temporal resolution and can be visualized through plots and animations.

## Code structure

![an image's alt text \label{fig:structure_image}](./figures/image.png){ width=80% }

## Usage so far

`pydykit` has been recently used in the authors work TODO where discrete gradient based methods have been discussed for the class of port-Hamiltonian systems governed by differential-algebraic equations. Its predecessor `metis` has been used in three major contributions [@kinon_ggl_2023],[@kinon_structure_2023],[@kinon_2024_conserving] dealing with the simulation of rigid and multibody systems, focussing on structure-preserving integration, e.g. variational and energy-momentum integrators.

# Acknowledgements

PLK gratefully acknowledges financial support by the German Research Foundation (DFG) – project number TODO XX.

<!-- - and by the Research Travel Grant of the Karlsruhe House of Young Scientists (KYHS) -->

# References
