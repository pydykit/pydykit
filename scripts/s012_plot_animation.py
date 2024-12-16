import numpy as np
import pandas as pd
import plotly.graph_objects as go

import pydykit
import pydykit.postprocessors as postprocessors

# name = "particle_system_01"
name = "particle_system_02"
manager = pydykit.managers.Manager()

manager.configure_from_path(path=f"./pydykit/example_files/{name}.yml")


df = pd.read_csv(f"test/reference_results/{name}.csv")

x = df["position_x0"]
y = df["position_y0"]
z = df["position_z0"]

postprocessor = postprocessors.Postprocessor(manager, state_results_df=df)


# Frames
frames = []
for k in range(len(x) - 1):

    data = []
    traces = []
    for index_python in range(manager.system.nbr_particles):
        index = index_python

        data.append(
            postprocessor.get_trace_3d_trajectory(
                x_components=df[f"position_x{index}"][: k + 1],
                y_components=df[f"position_y{index}"][: k + 1],
                z_components=df[f"position_z{index}"][: k + 1],
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
    index = index_python
    index_time = 0
    postprocessor.add_3d_annotation(
        figure=fig,
        x=df[f"position_x{index}"][index_time],
        y=df[f"position_y{index}"][index_time],
        z=df[f"position_z{index}"][index_time],
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


postprocessor.fix_scene_bounds_to_extrema(figure=fig, df=df)

fig.update_layout(sliders=sliders)
fig.show()
