import numpy as np
import skfem
import utils
from skfem.visuals import matplotlib as skfem_mpl

mesh = skfem.MeshTri().refined(3)

ax = skfem_mpl.plot(mesh, np.random.rand(mesh.nelements))

utils.dump_plt(name="random")

ax = skfem_mpl.plot(mesh, np.ones(mesh.nelements))
utils.dump_plt(name="ones")
