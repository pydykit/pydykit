import pydykit

manager = pydykit.Manager(
    path_config_file="./pydykit/example_files/porthamiltonianfourparticlesystem.yml"
)
manager.system.initialize()
