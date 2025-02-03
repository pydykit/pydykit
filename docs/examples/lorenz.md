# Lorenz System

Let's use the system class `pydykit.systems_dae.Lorenz`
to simulate the famous [Lorenz attractor][wiki_lorenz],
which is modelled in terms a quasilinear differential algebraic equations.
<!-- TODO: insert link -->

```python exec="true" source="tabbed-right"
--8<-- "snippets/run_lorenz.py"
```

## Config File

The configuration file of this simulation reads as

```yaml
--8<-- "lorenz.yml"
```

For details on the usage of `class_name`-variable, see the example [`Pendulum 3D`](./pendulum_3d.md).

[wiki_lorenz]: https://en.wikipedia.org/wiki/Lorenz_system
