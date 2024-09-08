r"""Linear elasticity.

This example solves the linear elasticity problem using trilinear elements.

"""

import skfem
from skfem.helpers import ddot, eye, sym_grad, trace
from skfem.models.elasticity import lame_parameters

m = skfem.MeshHex().refined(3).with_defaults()
e = skfem.ElementVector(skfem.ElementHex1())
basis = skfem.Basis(
    m,
    e,
    intorder=3,
)

# calculate Lamé parameters from Young's modulus and Poisson ratio
lam, mu = lame_parameters(
    E=1e3,
    nu=0.3,
)


def C(T):
    return 2.0 * mu * T + lam * eye(
        trace(T),
        T.shape[0],
    )


@skfem.BilinearForm
def stiffness(u, v, w):
    return ddot(
        C(sym_grad(u)),
        sym_grad(v),
    )


K = stiffness.assemble(basis)

u = basis.zeros()
u[basis.get_dofs("right").nodal["u^1"]] = 0.3

u = skfem.solve(
    *skfem.condense(
        K,
        x=u,
        D=basis.get_dofs({"left", "right"}),
    ),
)

sf = 1.0
m = m.translated(
    sf * u[basis.nodal_dofs],
)

if __name__ == "__main__":
    from os.path import splitext
    from sys import argv

    # save to VTK for visualization in Paraview
    m.save(splitext(argv[0])[0] + ".vtk")
