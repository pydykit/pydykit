# Visualize the Code Structure

Following this [stackoverflow contribution](https://stackoverflow.com/a/7554457/8935243)
we can use
[`pyreverse`](https://pylint.readthedocs.io/en/stable/pyreverse.html)
which ships with `pylint`. Additionally we will need `graphviz` to create png-files.

```bash
conda install pylint graphviz
```

to visualize our package `pydykit`.
Therefore, we navigate into the package

```bash
cd pydykit
```

and execute

```bash
pyreverse -p pydykit .
```

to generate a graphviz-dot-file which represents the structure of both the package and it's classes.

A dot-file can be used to generate a visualization (I did not yet succeed in finding a way to create mermaid-code from a graphviz-dot-file).
Example:

```bash
pyreverse -o png -p pydykit .
```

![alt text](assets/classes_pydykit.png "Generated from pyreverse -o png -p pydykit .")

A subset of a package, composed out of selected modules can be visualized by, e.g.,

```bash
pyreverse -o png -p MySubset integrators.py managers.py simulators.py solvers.py systems_dae.py systems_multi_body.py systems_port_hamiltonian.py systems.py
```

# Structure

```mermaid
---
title: pydykit
---
classDiagram
    class System{
        +double mass
        +array mass_matrix
        +array ext_acceleration
        +int dimension
        +int nbr_degrees_of_freedom
        +int nbr_constraints
        +int nbr_bodies
        +int nbr_lagrange_multipliers
        +array geometric_properties
        +int nbr_potential_invariants
        +int nbr_position_constraint_invariants
        +int nbr_velocity_constraint_invariants
        +array dissipation_matrix
        +bool is_cyclic_coordinate
        +int nbr_mixed_quantities
        +int nbr_kinetic_invariants
        +dict special_properties
        +get_mass_matrix()
        +kinetic_energy_gradient_from_momentum()
        +kinetic_energy_gradient_from_velocity()
        +external_potential()
        +external_potential_gradient()
        +external_potential_hessian()
        +internal_potential()
        +internal_potential_gradient()
        +internal_potential_hessian()
        +constraint()
        +constraint_gradient()
        +constraint_hessian()
        +potential_invariant()
        +potential_invariant_gradient()
        +vConstraint_invariant()
        +vConstraint_invariant_gradient_q()
        +vConstraint_invariant_gradient_p()
        +vConstraint_invariant_hessian_qp()
        +Vconstraint_from_invariant()
        +Vconstraint_gradient_from_invariant()
        +constraint_invariant()
        +constraint_invariant_gradient()
        +constraint_invariant_hessian()
        +constraint_from_invariant()
        +constraint_gradient_from_invariant()
        +hconvergence_set()
        +hconvergence_reference()
    }
    class Simulation{
        +
    }
    class Integrator{
    }
```
