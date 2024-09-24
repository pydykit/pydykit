from pathlib import Path

import numpy as np
import skfem
import utils
from skfem.visuals.matplotlib import plot

dumper = utils.Dumper(
    path_base=Path(__file__).parent,
)

mesh = skfem.MeshTri().refined(3)

ax = plot(
    mesh,
    np.ones(mesh.nelements),
)
dumper.dump_plt(name="ones_elements")

random_elements = np.random.rand(mesh.nelements)

ax = plot(
    mesh,
    random_elements,
)
dumper.dump_plt(name="random_elements")


ax = plot(
    mesh,
    random_elements[0 : mesh.nvertices],
)
dumper.dump_plt(name="random_vertices")
