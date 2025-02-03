# Chemical Reactor

Let's use the system class `pydykit.systems_dae.ChemicalReactor`
to represent a chemical reactor in terms of a differential-algebraic system and solve it's behavior in time.
This system is modelled as quasilinear differential-algebraic equations.
<!-- TODO: insert link -->

```python exec="true" source="tabbed-right"
--8<-- "snippets/run_reactor.py"
```

## Config File

The configuration file of this simulation reads as

```yaml
--8<-- "reactor.yml"
```

For details on the usage of `class_name`-variable, see the example [`Pendulum 3D`](./pendulum_3d.md).
