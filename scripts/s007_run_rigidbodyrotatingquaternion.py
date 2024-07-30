import matplotlib.pyplot as plt
import numpy as np

import pydykit

manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/rigidbodyrotatingquaternion.yml"
)
tmp = manager.system.get_mass_matrix(
    q=np.array(
        [
            1,
            1,
            0,
            0,
        ]
    ),
)
print(tmp)
