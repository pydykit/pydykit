import inspect
from pathlib import Path

import matplotlib.pyplot as plt


def dump_plt(name):
    previous_frame = inspect.currentframe().f_back

    (
        filename,
        line_number,
        function_name,
        lines,
        index,
    ) = inspect.getframeinfo(previous_frame)

    calling_script = Path(filename).stem
    index = calling_script[0:4]

    out_dir = Path("plots")

    out_file = out_dir.joinpath(
        index + "_" + name + ".png",
    )

    plt.savefig(out_file)
