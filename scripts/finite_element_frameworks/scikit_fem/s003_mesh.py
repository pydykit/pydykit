import numpy as np
import skfem
import utils
from skfem.visuals.matplotlib import plot

mesh = skfem.MeshTri().refined(3)

ax = plot(
    mesh,
    np.ones(mesh.nelements),
)
utils.dump_plt(name="ones_elements")

random_elements = np.random.rand(mesh.nelements)

ax = plot(
    mesh,
    random_elements,
)
utils.dump_plt(name="random_elements")


ax = plot(
    mesh,
    random_elements[0 : mesh.nvertices],
)
utils.dump_plt(name="random_vertices")
