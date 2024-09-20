import pydykit

manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/rigidbodyrotatingquaternion.yml"
)
manager.system.initialize()

results = manager.manage()
