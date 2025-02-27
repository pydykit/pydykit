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
  - name: Philipp Lothar Kinon
    orcid: 0000-0002-4128-5124
    affiliation: "1"
  - name: Julian Karl Bauer^[corresponding author]
    orcid: 0000-0002-4931-5869
    affiliation: "2" # (Multiple affiliations must be quoted)
  # - name: Peter Betsch
  #   orcid: 0000-0002-0596-2503
  #   affiliation: "1"
affiliations:
  - name: Independent Researcher, Karlsruhe, Germany
    index: 2
  - name: Institute of Mechanics, Karlsruhe Institute of Technology (KIT), Karlsruhe, Germany
    index: 1
date: 09 February 2025
bibliography: paper.bib
---

# Summary

Simulating dynamical systems is crucial in many scientific and engineering disciplines.
Discrete dynamical systems are typically governed by ordinary differential or
differential-algebraic equations (DAEs),
which describe the evolution of the unknown quantities in a finite-dimensional state space.
Combined with
initial conditions,
these equations form an initial value problem (IVP).

Solving IVPs
numerically requires discretization techniques
which translate the problem into a computationally feasible form.
The open-source Python package `pydykit`
is a tool for academic researchers to study and
develop discretization methods
for the simulation of discrete dynamical systems.
The package is designed to be modular and extensible.
Existing implementations focus
on geometric integration methods [@hairer_geometric_2006], energy-momentum schemes using _discrete gradients_ (see, e.g. [@gonzalez_time_1996])
and _variational integrators_ [@lew2016brief].

# Statement of Need

Existing research codes within the discipline

- TODO: List existing codes

TODO: List drawbacks

# Features

`pydykit` is a flexible framework for simulating a wide range of dynamical systems governed by ordinary differential equations (ODEs) and differential-algebraic equations (DAEs). Thus `pydykit` is open for users from a plethora of application fields. It supports the implementation of

1. General quasilinear DAEs of the form $E(x) \dot{x} = f(x)$,
   where $E(x)$ may be singular, allowing for broad applicability in constrained dynamics.

2. Port-Hamiltonian DAE systems governed by $E(x) \dot{x} = (J(x)- R(x)) z(x) + B(x) u$
   which appear in various physical modeling contexts [@duindam_modeling_2009], also cover open control systems and follow an energy-based modelling approach.

3. Multibody systems formulated as index-3 DAEs with holonomic positional constraints $g(q)$. Beyond standard multibody dynamics, pydykit supports rigid body dynamics using unit quaternions [@betsch_2009_rigid], a powerful approach for modeling rotational motion. The software is also well-suited for Hamiltonian dynamics, with or without constraints [@leimkuhler_simulating_2005], making it an effective tool for structure-preserving simulations.

These formulations make pydykit a versatile tool for researchers across disciplines, from robotics and biomechanics to electrical and thermodynamic systems.

![Current system classes covered by `pydykit` \label{fig:systems}](./figures/sample.png){width=70%}

TODO: Define terminology:

- Klasse / abstrakte Basisklasse
- System / Systembestandteil
- Konifgurationsdatei

TODO: Formulate the following:

1. pydykit definiert eine Struktur in die weitere Systembestandteilen (Integratoren, Simulatoren etc.) eingebunden werden können.
   Umgesetzt ist diese Strukture in Form von abstrakten Basisklassen.
2. Konkrete Parametrisierung von Systembestandteilen erfolgt durch Konfigurationsdatei...

## Code Structure

TODO: Liste welche Systembestandteile existieren.
TODO: Liste welche konkreten Implementierungen existieren.

![Code structure 01 \label{fig:code_structure_pdydkit}](./figures/code_structure/pydykit.pdf){width=100%}
![Code structure 02 \label{fig:code_structure_systems}](./figures/code_structure/systems.pdf){width=100%}
![Code structure 03 \label{fig:code_structure_integrators}](./figures/code_structure/integrators.pdf){width=100%}

## Usage

TODO: Add pendulum example from https://pydykit.github.io/pydykit/latest/examples/pendulum_3d/

## Usage so far

`pydykit` has been recently used in the authors work TODO where discrete gradient based methods have been discussed for the class of port-Hamiltonian systems governed by differential-algebraic equations. Its predecessor `metis` has been used in three major contributions [@kinon_ggl_2023],[@kinon_structure_2023],[@kinon_2024_conserving] dealing with the simulation of rigid and multibody systems, focussing on structure-preserving integration, e.g. variational and energy-momentum integrators.

# Acknowledgements

PLK gratefully acknowledges financial support by the German Research Foundation (DFG) – project number TODO XX.

<!-- - and by the Research Travel Grant of the Karlsruhe House of Young Scientists (KYHS) -->

# References
