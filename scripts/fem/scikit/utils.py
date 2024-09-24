import inspect
from pathlib import Path

import matplotlib.pyplot as plt


class Dumper:
    def __init__(self, path_base):
        # Define directory
        self.path_base = path_base
        self.out_dir = self.path_base.joinpath("plots")
        self.out_dir.mkdir(parents=True, exist_ok=True)

        # Get name of calling script
        previous_frame = inspect.currentframe().f_back

        (
            filename,
            line_number,
            function_name,
            lines,
            index,
        ) = inspect.getframeinfo(previous_frame)

        calling_script = Path(filename).stem

        # Define prefix
        index = calling_script[0:4]
        self.pattern = str(self.out_dir.joinpath(f"{index}_" + "{name}" + ".png"))

    def dump_plt(self, name):

        plt.savefig(self.pattern.format(name=name))
