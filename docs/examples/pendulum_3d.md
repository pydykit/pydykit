# Pendulum 3D

Let's use the system class `pydykit.systems_multi_body.ParticleSystem`
to simulate a single particle with concentrated mass within a three-dimensional space.

The particle's initial position is
`(1.0, 0.0, 0.0)`
and its initial velocity points into the `y`-direction.
The particle's distance to a fixed support at `(0.0, 0.0, 0.0)`
is constraint to be of length `1.0` and there is a gravitational field into negative `z`-direction.

In consequence, the particle is called a 3D pendulum
and its motion is visualized in belows `Result` tab.
The source code of leading to this viosualization is given within the `Source` tab.

```python exec="true" source="tabbed-right"
--8<-- "snippets/run_pendulum_3d.py"
```

## Config File

Let's have a closer look at the configuration file of this simulation:

```yaml
--8<-- "pendulum_3d.yml"
```

### System

The `system`-section in the above configuration file
defines the scene, aka. system, to be simulated.
This includes definition of the particle, the fixed support, the constraint and the gravitation.

The `system`-sections variable `class_name` tells `pydykit` that the
scene shall be based on the system class
[`ParticleSystem`][source_particle_system],
which belongs to the family of [MBS][mbs].
This class is known to `pydykit` as it has been
[registered][source_register_particle_system]
within the
[`SystemFactory`][source_system_factory].

### Integrator

The `integrator`-section in the above configuration file
defines the integration scheme to be used.
Here, the implicit midpoint rule will be applied
to the system which is formulated as a [MBS][mbs].

Similar to the registration pattern of the `system`,
the variable `class_name` within section `integrator` tells `pydykit`
to use the class
[`MidpointMultibody`][source_midpoint_multibody].
This class is known to `pydykit` as it has been
[registered][source_register_midpoint_multibody]
within the
[`IntegratorFactory`][source_integrator_factory].
The pattern of referencing a registered Python class in terms of `class_name`
also applies to the sections `simulator` and `time_stepper`.

### Simulator

The `simulator`-section
defines the solution procedure, aka. simulator, to be used.
The simulator uses a Newton method with
a specific accuracy for the norm of the residual `newton_epsilon`
and a maximum number of iterations per time step before the simulation procedure is stopped.

### Time Stepper

The `time_stepper`-section defines the time stepping algorithm based on settings for
start time, end time and step size.

[source_particle_system]: https://github.com/pydykit/pydykit/blob/main/pydykit/systems_multi_body.py#L192
[source_register_particle_system]: https://github.com/pydykit/pydykit/blob/main/pydykit/factories.py#L16
[source_system_factory]: https://github.com/pydykit/pydykit/blob/main/pydykit/factories.py#L52

<!--  TODO: Change the links source_particle_system and source_midpoint_multibody to point to the docs of the Python classes -->

[source_midpoint_multibody]: https://github.com/pydykit/pydykit/blob/main/pydykit/integrators.py#L200
[source_register_midpoint_multibody]: https://github.com/pydykit/pydykit/blob/main/pydykit/factories.py#L28
[source_integrator_factory]: https://github.com/pydykit/pydykit/blob/main/pydykit/factories.py#L82
[mbs]: ../getting_started.md#mbs
