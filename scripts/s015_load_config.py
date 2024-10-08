from pydykit import configuration, utils

file_content = utils.load_yaml_file("./pydykit/example_files/pendulum_2d.yml")
conf = configuration.Configuration(**file_content["configuration"])

from pydykit import simulators

solver = getattr(simulators, conf.simulator.class_name)(**conf.simulator.kwargs)
