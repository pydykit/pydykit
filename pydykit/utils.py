import re

import numpy as np
import numpy.typing as npt
import yaml

from . import abstract_base_classes


def update_object_from_config_file(
    obj,
    path_config_file,
    content_config_file,
):
    if (path_config_file is not None) and (content_config_file is not None):

        raise PydykitException(
            "Did receive both path_config_file and content_config_file. "
            + "Supply either path_config_file or content_config_file, not both"
        )

    elif path_config_file is not None:

        obj.path_config_file = path_config_file
        content_config_file = load_yaml_file(path=obj.path_config_file)

    elif content_config_file is not None:

        pass

    else:

        raise PydykitException(
            "Did not receive kwargs. "
            + "Supply either path_config_file or content_config_file"
        )

    obj.content_config_file = content_config_file

    obj.name = obj.content_config_file["name"]
    obj.configuration = obj.content_config_file["configuration"]


def load_yaml_file(path):
    with open(path, "r") as file:
        content = yaml.safe_load(file)
    return content


class PydykitException(Exception):
    pass


def get_numerical_tangent(func, state, incrementation_factor=1e-10):

    state_dimension = len(state)
    numerical_tangent = np.zeros((state_dimension, state_dimension))

    for index in range(state_dimension):

        saved_state_entry = state[index]

        increment = incrementation_factor * (1.0 + abs(saved_state_entry))
        state[index] = saved_state_entry + increment

        forward_incremented_function = func(
            next_state=state,
        )

        state[index] = saved_state_entry - increment

        backward_incremented_function = func(
            next_state=state,
        )

        state[index] = saved_state_entry

        numerical_tangent[:, index] = (
            forward_incremented_function - backward_incremented_function
        ) / (2.0 * increment)

    return numerical_tangent


def print_current_step(step):

    print(
        "****** ",
        f"time = {step.time:.8},",
        f" step index {step.index}",
        " ******",
    )


def print_residual_norm(value):

    print(f"residual norm = {value:.4E}")


def get_indices(my_list):
    return [item.index for item in my_list]


def sort_based_on_attribute(obj, attribute):
    return sorted(obj, key=lambda item: getattr(item, attribute))


def get_flat_list_of_list_attributes(items, key):
    return np.array([item[key] for item in items]).flatten()


def get_nbr_elements_dict_list(my_list: dict):
    return sum(map(len, my_list.values()))


def get_keys(my_list: dict):
    return list(my_list.keys())


def row_array_from_df(df, index):
    row = df.iloc[index]
    return row.to_numpy()


def get_system_copies_with_desired_states(
    system: abstract_base_classes.System,
    states: list[npt.ArrayLike],
):
    return map(
        lambda state: system.copy(state=state),
        states,
    )


def select(
    position_vectors,
    element,
    endpoint,
):
    return position_vectors[element[endpoint]["type"]][element[endpoint]["index"]]


def quadratic_length_constraint(vector, length):
    return 0.5 * (vector.T @ vector - length**2)


def add_columns_to_plot(columns_to_plot, results_df, quantity):
    """
    Adds columns matching the given quantity pattern to the columns_to_plot list.

    Parameters
    ----------
    columns_to_plot : list
        The list to which matching columns will be added.
    results_df : DataFrame
        The DataFrame containing the columns to search.
    quantity : str
        The quantity pattern to match in the column names.

    Returns
    -------
    list
        The updated columns_to_plot list.
    """
    columns_to_plot += [
        col for col in results_df.columns if re.search(rf"^{quantity}(_\d+)?$", col)
    ]
    return columns_to_plot
