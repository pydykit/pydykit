import numpy as np
import pandas as pd
import plotly.graph_objects as go

import pydykit

# name = "particle_system_01"
name = "particle_system_02"
manager = pydykit.Manager(path_config_file=f"./pydykit/example_files/{name}.yml")
manager.system.initialize()

df = pd.read_csv(f"test/reference_results/{name}.csv")

x = df["x1"]
y = df["y1"]
z = df["z1"]


# Frames
frames = []
for k in range(len(x) - 1):

    data = []
    traces = []
    for index_python in range(manager.system.nbr_particles):
        index = pydykit.utils.shift_index_python_to_literature(index_python)

        data.append(
            pydykit.plotting.get_trace_3d_trajectory(
                x_components=df[f"x{index}"][: k + 1],
                y_components=df[f"y{index}"][: k + 1],
                z_components=df[f"z{index}"][: k + 1],
                time=df["time"],
            )
        )
        traces.append(index_python)

    frames.append(
        go.Frame(
            data=data,
            traces=traces,
            name=f"frame{k}",
        )
    )

# Create figure
fig = go.Figure(data=[go.Scatter3d() for trace in frames[0]])

fig.update(frames=frames)

for index_python in range(manager.system.nbr_particles):
    index = pydykit.utils.shift_index_python_to_literature(index_python)

    index_time = 0
    pydykit.plotting.add_3d_annotation(
        figure=fig,
        x=df[f"x{index}"][index_time],
        y=df[f"y{index}"][index_time],
        z=df[f"z{index}"][index_time],
        text=str(index),
    )


def frame_args(duration):
    return {
        "frame": {"duration": duration},
        "mode": "immediate",
        "fromcurrent": True,
        "transition": {"duration": duration, "easing": "linear"},
    }


sliders = [
    {
        "pad": {"b": 10, "t": 60},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": [
            {
                "args": [[f.name], frame_args(0)],
                "label": str(k),
                "method": "animate",
            }
            for k, f in enumerate(fig.frames)
        ],
    }
]

fig.update_layout(
    updatemenus=[
        {
            "buttons": [
                {
                    "args": [None, frame_args(50)],
                    "label": "Play",
                    "method": "animate",
                },
                {
                    "args": [[None], frame_args(0)],
                    "label": "Pause",
                    "method": "animate",
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 70},
            "type": "buttons",
            "x": 0.1,
            "y": 0,
        }
    ],
    sliders=sliders,
)


pydykit.plotting.fix_scene_bounds_to_extrema(figure=fig, df=df)

fig.update_layout(sliders=sliders)
fig.show()
