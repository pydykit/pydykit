# Getting Started

A `pydykit`-simulation contains several building blocks,
which are at least a `system`, `integrator`, `simulator` and a `time_stepper`.
These building blocks are defined within a config file.

## Config File

A `pydykit`-config file configures a simulation devided into several building blocks.
Each building blocks consists of parameters and methods.
Example config files can be found in [pydykit/example_files][source_pydykit_examples]
and some of them are discussed in more detail in the section [examples](examples/pendulum_3d.md).

## System

The `system` defines the system of ordinary differential equations (ODEs)
or differential algebraic equations (DAEs), to be solved.
`Pydykit` covers three system families,
which are:

1. Multibody systems
2. Port-Hamiltonian systems
3. Quasilinear DAEs

Lets briefly introduce them one by one.

#### 1. Multibody system (MBS) dynamics <a name="mbs"></a>

This family covers DAEs belonging to mechanical systems composed of multiple rigid bodies, governed by

$$
\begin{align}
\dot q &= M^{-1} p \\
\dot p &= -\nabla V(q) - D(q) M^{-1} p - \nabla g(q)^{\mathrm{T}} \lambda \\
0 &= g(q)
\end{align}
$$

where $q$ and $p$ are generalized coordinates and momenta, respectively,
$M$ is the mass matrix, $V$ is the potential energy,
$D$ is the Rayleigh dissipation matrix and $g$ are independent,
holonomic constraint functions enforced by Lagrange multipliers $\lambda$.
One example can be studied in more detail, the [3D pendulum](examples/pendulum_3d.md).

<!-- TODO: include -->
<!-- References: ... -->

#### 2. Port-Hamiltonian systems (PHS)

Port-Hamiltonian systems are an extension of classical Hamiltonian dyamics
with respect to dissipative effects and interconnection terms from the environment.
This energy-based approach combines dynamics from various physical disciplines in one formalism
and emerges from control systems theory.
The dynamics follow

$$
\begin{align}
E(x) \dot x &= \left( J(x) -R(x) \right) z(x)  + B(x)u \\
E(x)^{\mathrm{T}} z(x) &= \nabla H(x) \\
y &= B(x)^{\mathrm{T}} z(x)
\end{align}
$$

with state $x$, co-state function $z$, possibly singular descriptor matrix $E$,
structure matrix $J=-J^{\mathrm{T}}$, positive semi-definite dissipatrix matrix $R=R^{\mathrm{T}}$,
input matrix $B$, control input $u$ with collocated output $y$ and Hamiltonian $H$.

<!-- TODO: include -->
<!-- References: ... -->

#### 3. Quasilinear DAEs

This last framework is an even more general one.
It comprises all DAEs of the general form

$$
E(x) \dot x = f(x,t)
$$

where $E$ is a possibly singular descriptor matrix,
$x$ are the unknowns/states and $f$ denotes an arbitrary right-hand side function.
Examples that can be studied in more detail, are the [Lorenz attractor](examples/lorenz.md)
and the [chemical reactor](examples/reactor.md).

## Integrator

The `integrator` defines the numerical integration scheme
to be used for the system at hand.
As the integration scheme defines whether a numerical procedure preserves the underlying structure of the problem,
`pydykit` places particular emphasis on integrator classed.
Although a system may fit into even two or three of the abovementioned framework,
the user might want to introduce specialized integrators to capture as much of the underlying structure as possible,
e.g. exactly preserve the constraint functions of the MBS or the skew-symmetry of the structure matrix of a PHS.

## Simulator

The `simulator` defines the solution procedure to be used.
This includes the equation solver to be used,
e.g. Newton's method and its characeteristics such as accuracy.

## Time Stepper

The `time_stepper` defines the discrete temporal grid,
where approximative solutions are computed.
Currently, `pydykit` supports one-step methods only,
i.e. for a known solution at one time-instance `pydykit` computes the solution at the next time instance on the specified grid.

[source_pydykit_examples]: https://github.com/pydykit/pydykit/blob/main/pydykit/example_files
