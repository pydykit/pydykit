import skfem
from skfem.visuals import matplotlib as mplt

mesh = skfem.MeshTri()

ax = mplt.plot(mesh, [0, 1, 2, 3])

ax.show()
