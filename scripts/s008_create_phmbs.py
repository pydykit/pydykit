import pydykit

manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/porthamiltonian_fourparticle_system.yml"
)
manager.system.initialize()
