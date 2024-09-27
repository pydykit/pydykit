from pydykit import configuration, utils

file_content = utils.load_yaml_file("./pydykit/example_files/pendulum_2d.yml")
conf = configuration.Configuration(**file_content["configuration"])

from pydykit import solvers

solver = getattr(solvers, conf.solver.class_name)(**conf.solver.kwargs)
