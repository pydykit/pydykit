import numpy as np
import plotly.graph_objects as go
import yaml


def load_yaml_file(path):
    with open(path, "r") as file:
        content = yaml.safe_load(file)
    return content


class PydykitException(Exception):
    pass


def get_numerical_tangent(func, state_1, state_2, epsilon=1e-10):

    state_1 = state_1.copy()
    state_2 = state_2.copy()

    N = len(state_2)
    tang_num = np.zeros((N, N))

    for j in range(N):

        xsave = state_2[j]

        delp = epsilon * (1.0 + abs(xsave))
        state_2[j] = xsave + delp

        R1 = func(
            state_n=state_1,
            state_n1=state_2,
        )

        state_2[j] = xsave - delp

        R2 = func(
            state_n=state_1,
            state_n1=state_2,
        )

        state_2[j] = xsave

        tang_num[:, j] = (R1 - R2) / (2.0 * delp)

    return tang_num


def print_current_step(step):

    print(
        "****** ",
        f"time = {step.time:.8},",
        f" step index {step.index}",
        " ******",
    )


def print_residual_norm(value):

    print(f"residual norm = {value:.4E}")


def plot_three_dimensional_trajectory(
    figure, x_components, y_components, z_components, time
):
    figure.add_trace(
        go.Scatter3d(
            x=x_components,
            y=y_components,
            z=z_components,
            marker=dict(
                size=3,
                color=time,
                colorscale="Viridis",
                colorbar=dict(
                    thickness=20,
                    title="time",
                ),
            ),
            line=dict(
                color="darkblue",
                width=3,
            ),
            showlegend=False,
        )
    )


def shift_index_python_to_literature(index):
    return index + 1


def shift_index_iterature_to_python(index):
    return index - 1
