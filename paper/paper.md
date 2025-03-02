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
  - name: Institute of Mechanics, Karlsruhe Institute of Technology (KIT), Karlsruhe, Germany
    index: 1
  - name: Independent Researcher, Karlsruhe, Germany
    index: 2
date: 09 February 2025
bibliography: paper.bib
---

# Summary

Simulating dynamical systems is crucial in many scientific and engineering disciplines.
Discrete dynamical systems are typically governed by ordinary differential equations (ODEs) or
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

<!-- Field of application:
Präzise wissenschaftliche Abgrenzung der verschiedenen Arten von Differentialgleichungssystemen und deren Auftreten in bestimmten Disziplinen. -->

<!-- In dem Abschnitt “Statement of need” passt durchaus ein bisschen blabla zu “foster research collaboration…” aber in den anderen Abschnitten aus meiner Sicht nicht.  -->

Reproducibility and transparency of numerical results is not yet the standard in all scientific engineering disciplines.
The goal of `pydykit` is to support research publications by ensuring the FAIR requirements for computational experiments.
Moreover, `pydykit` can serve as a foundation for the prototyping of object-oriented integration methods,
fostering collaborations in research and teaching.
The choice to use the Python environment may lower the barrier for students
and early-career researchers due to its accessibility, widespread adoption, and extensive ecosystem of scientific computing libraries.
Meanwhile, the package encourages engagement with structure-preserving methods
and could help bridge gaps in state-of-the-art numerical techniques.

Existing research codes within the discipline

- TODO: List existing codes

TODO: List drawbacks

<!-- In den vorheringen Bulletpoints, hattest du skizziert, dass wir die Verwendung von Python motivieren sollen. Ich würde das gerne beibehalten, dabei aber den Fokus legen warum Python in unserem Kontext nun das Mittel der Wahl war. Natürlich waren manche Sätze trivial in der Python-Welt aber nicht jeder arbeitet mit Python in der Wissenschaft. -->

# Features

`pydykit` is a package for simulating a wide range of dynamical systems governed by ODEs and DAEs. It supports the implementation of

1. General quasilinear DAEs of the form $E(x) \dot{x} = f(x)$,
   where $E(x)$ may be singular, allowing for broad applicability in constrained dynamics.

2. Port-Hamiltonian DAE systems governed by $E(x) \dot{x} = (J(x)- R(x)) z(x) + B(x) u$
   which appear in various physical modeling contexts [@duindam_modeling_2009], also cover open control systems and follow an energy-based modelling approach.

3. Multibody systems formulated as index-3 DAEs with holonomic positional constraints $g(q)$. Beyond standard multibody dynamics, pydykit supports rigid body dynamics using unit quaternions [@betsch_2009_rigid], a powerful approach for modeling rotational motion. The package is also well-suited for Hamiltonian dynamics, with or without constraints [@leimkuhler_simulating_2005], making it an effective tool for structure-preserving simulations.

Thus `pydykit` can be helpful for users from various application fields,
from robotics and biomechanics to electrical and thermodynamic systems.

![Current system classes covered by `pydykit` \label{fig:systems}](./figures/sample.png){width=70%}

Users may choose their favorite system description from this hierarchy depending on their goal:
They can either design numerical methods for a more general system class
or for a concrete application where additional specified requirements have to be met.

TODO: Define terminology:

- Klasse / abstrakte Basisklasse
- System / Systembestandteil
- Konifgurationsdatei
- Integratoren
- time-steppers
- Solvers

TODO: Formulate the following:

1. pydykit definiert eine Struktur in die weitere Systembestandteilen (Integratoren, Simulatoren etc.) eingebunden werden können.
   Umgesetzt ist diese Strukture in Form von abstrakten Basisklassen.
2. Konkrete Parametrisierung von Systembestandteilen erfolgt durch Konfigurationsdatei...

<!-- Built-in postprocessing tools, including animation and data export capabilities allow for a basic result analysis and visualization. JKB: nichts besonderes -->

## Code Structure and Usage

<!--
- Users describe a system in terms of code and
- Parametrize the system and solution process in terms of a configuration file.
- A simulation contains components, which are
  - a system,
  - an integrator,
  - a simulator (mostly containing a solve) and
  - a time-stepper.
- Abstract base classes exist for each component and define an interface, i.e., methods a given component implementation has to have.
- Systems encode the dynamical system to be simulated and are split into three groups:
  - DAEs
  - Port-Hamiltonian systems
  - Multibody systems, see figure 1.
- The system might be implemented generic like "particleSystem" or specific like Lorenz (DAE) or Pendulum2D (PortHamiltonianSystem)
- Combination of integrator, simulator, solver define the discretization method and solution process, whereas the time-stepper define the resolution of the solution.
- Example:
  - sperical pendulum represented in terms of particle system, parametrized with config file: `pendulum_3d.yml`
  - system class deifnes what to simulate, i.e., spherical pendulum is parametrized using class xy
-->

The Python package `pydykit` solves initial boundary value problems for dynamically solved systems.
Users of the package specify both the system to be simulated and the procedure for solving the initial boundary value problem in terms of Python classes
which can be grouped into class types `system`, `integrator`, `simulator`, and `time-stepper`.
The class type `system` defines the system to be simulated and following
Figure \ref{fig:systems}
contains three subtypes: `DAE`, `Port-Hamiltonian system`, and `Multibody system`.
The class types `integrator`, `simulator` and `times-stepper` specify the procedure for solving an initial boundary value problem of a dynamical system.
Each of these class types is defined in terms of an abstract base class, i.e., an interphase specifying the methods a given class has to have.

An overview of the existing classes, their relation and interfaces is given in
TODO: Create and add nice images.

<!-- ![Code structure 01 \label{fig:code_structure_pdydkit}](./figures/code_structure/pydykit.pdf){width=100%} -->
<!-- ![Code structure 02 \label{fig:code_structure_systems}](./figures/code_structure/systems.pdf){width=100%} -->
<!-- ![Code structure 03 \label{fig:code_structure_integrators}](./figures/code_structure/integrators.pdf){width=100%} -->

Developers can extend the functionality of pydykit by developing new Python classes within the given class types.
A particular simulation can be encoded in a configuration file.
This file specifies which Python classes should be combined with each other
and contains parameters which are passed to the classes at runtime, defining the system and the solution process.

This approach is explained using a concrete example, a spherical pendulum.
Based on the Python class `pydykit.systems_multi_body.ParticleSystem`, a single particle with concentrated mass in a three-dimensional space is simulated.
The initial position of the particle is (1,0, 0,0, 0,0) and its initial velocity points in the y-direction.
The distance of the particle to a fixed support at (0,0, 0,0, 0,0) is limited to the length 1.0 and there is a gravitational field in the negative z-direction.

The configuration file for the spherical pendulum is given in Listing \ref{lst:spherical_pendulum}.
TODO: Nutze listing Referenz

```yaml
name: pendulum_3d
system:
  class_name: ParticleSystem
  nbr_spatial_dimensions: 3
  particles:
    - index: 0
      initial_position: [1.0, 0.0, 0.0]
      initial_momentum: [0.0, 1.0, 0.0]
      mass: 1.0
  supports:
    - index: 0
      type: fixed
      position: [0.0, 0.0, 0.0]
  springs: []
  dampers: []
  constraints:
    - start:
        type: support
        index: 0
      end:
        type: particle
        index: 0
      length: 1.0
  gravity: [0.0, 0.0, -9.81]
integrator:
  class_name: MidpointMultibody
simulator:
  class_name: OneStep
  solver_name: NewtonPlainPython
  newton_epsilon: 1.e-07
  max_iterations: 40
time_stepper:
  class_name: FixedIncrementHittingEnd
  step_size: 0.08
  start: 0.0
  end: 1.3
```

Parameters listed within the `system` section are passed to the Python class `pydykit.systems_multi_body.ParticleSystem` at runtime
and specify the particle, its initial conditions and the physical properties of the spherical pendulum.
The combination of the classes `integrator`, `simulator`, and `time-stepper` parameters define the discretization method and the solution process.

## Usage so far

`pydykit` has been recently used in the authors work TODO where discrete gradient based methods have been discussed for the class of port-Hamiltonian systems governed by differential-algebraic equations.
Its predecessor `metis` has been used in three major contributions
[@kinon_ggl_2023], [@kinon_structure_2023], [@kinon_2024_conserving]
dealing with the simulation of rigid and multibody systems, focussing on structure-preserving integration, e.g. variational and energy-momentum integrators.

# Acknowledgements

PLK gratefully acknowledges financial support by the German Research Foundation (DFG) – project number TODO XX.

<!-- - and by the Research Travel Grant of the Karlsruhe House of Young Scientists (KYHS) -->

# References
