import pydykit

manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/rigid_body_rotating_quaternion.yml"
)

results = manager.manage()
