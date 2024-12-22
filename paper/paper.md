---
title: "pydykit: A Python-based dynamics simulation toolkit"
tags:
  - Python
  - Mechanics
  - Dynamics
  - Numerical methods
authors:
  - name: Philipp Lothar Kinon^[corresponding author]
    orcid: 0000-0002-4128-5124
    affiliation: "1"
  - name: Julian Karl Bauer
    orcid: 0000-0002-4931-5869
    affiliation: "2" # (Multiple affiliations must be quoted)
  - name: Peter Betsch
    orcid: 0000-0002-0596-2503
    affiliation: "1"
affiliations:
  - name: Institute of Mechanics, Karlsruhe Institute of Technology (KIT), Karlsruhe, Germany
    index: 1
  - name: Independent Researcher, Karlsruhe, Germany
    index: 2
date: 22 Dezember 2024
bibliography: paper.bib
---

# Summary

The Python code framework `pydykit` is ...

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

# Statement of need

- General introduction
- Classification of numerical time integrators:
  - _Geometric_ or _structure-preserving_ integration [@hairer_geometric_2006].
  - _Energy-momentum_ (EM) methods using _discrete gradients_ (see, e.g. [@gonzalez_time_1996])
    or variational integrators [@lew2016brief], [@marsden_discrete_2001],
    which have been extended to DAEs in [@leyendecker_variational_2008].
- List alternative packages and highlight what they lack, i.e., which gap is closed by `pydykit`.

## Applicability

- System classification:
  - Hamiltonian dynamics with or without constraints [@leimkuhler_simulating_2005], also systems governed by differential-algebraic equations (DAEs) [@kunkel_differential-algebraic_2006] are feasible.
  - Rigid body dynamics in terms of _directors_ [@betsch2001constrained].
  - Simulation of _port-Hamiltonian_ systems [@duindam_modeling_2009].

## Code structure

![an image's alt text \label{fig:structure_image}](./figures/image.png){ width=70% }

## Motivation by example

## Usage so far

`pydykit` has been recently used in the authors works (among others [@kinon_ggl_2023] and [@kinon_structure_2023]),
where numerical schemes based on a mixed extension due to Livens principle [@livens_hamiltons_1919]
have been derived for systems with holonomic constraints.

# Acknowledgements

PLK and PB gratefully acknowledge financial support by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – project numbers XX and YY.

# References
