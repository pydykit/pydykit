import pydykit

manager = pydykit.managers.Manager()
name = "rigid_body_rotating_quaternion"
path_config_file = f"./pydykit/example_files/{name}.yml"
manager.configure_from_path(path=path_config_file)
result = pydykit.results.Result(manager=manager)
result = manager.manage(result=result)
