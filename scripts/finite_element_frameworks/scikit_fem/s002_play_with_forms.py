import skfem
from skfem.helpers import dot, grad


@skfem.BilinearForm
def integrand(u, v, w):
    import pdb

    pdb.set_trace()  # breakpoint
    return dot(grad(u), grad(v))


skfem.asm(
    integrand,
    skfem.Basis(
        skfem.MeshTri(),
        skfem.ElementTriP1(),
    ),
)

# After running this scrip, you created an skfem-assembly and
# your started a Python debugger at the breakpoint in line 9
#
# Therefore, you are able to inspect the local namespace at line 9 during execution.
