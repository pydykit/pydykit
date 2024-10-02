import numpy as np

import pydykit
import pydykit.operators

quat_position = np.array([1.0, 0.0, 0.0, 0.0])
angular_velo = np.array([10.0, 20.0, 20.0])
quat_velocity = pydykit.operators.quaternion_velocity(
    quaternion_position=quat_position, angular_velocity=angular_velo
)
print(quat_velocity)
