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


def get_numerical_tangent(func, incrementing_state, incrementation_factor=1e-10):

    state = incrementing_state.copy()

    state_dimension = len(state)
    numerical_tangent = np.zeros((state_dimension, state_dimension))

    for index in range(state_dimension):

        saved_state_entry = state[index]

        increment = incrementation_factor * (1.0 + abs(saved_state_entry))
        state[index] = saved_state_entry + increment

        forward_incremented_function = func(
            state=state,
        )

        state[index] = saved_state_entry - increment

        backward_incremented_function = func(
            state=state,
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


def shift_index_python_to_literature(index):
    return index + 1


def shift_index_iterature_to_python(index):
    return index - 1


def sort_list_of_dicts_based_on_special_value(my_list, key):
    return sorted(my_list, key=lambda d: d[key])


def get_flat_list_of_list_attributes(items, key):
    return np.array([item[key] for item in items]).flatten()


def get_nbr_elements_dict_list(my_list: list[dict,]):
    return sum(map(len, my_list.values()))


def get_keys_dict_list(my_list: list[dict,]):
    return list(my_list.keys())


def row_array_from_df(df, index):
    row = df.iloc[index]
    row = row.drop("time")
    return row.to_numpy()


def compare_string_lists(list1, list2):
    # TODO: Use the "Assert"-statement instead of implementing custom logic
    if list1 == list2:
        pass
    else:
        raise PydykitException(f"{list1} does not match {list2}")


def get_system_copies_with_desired_states(
    system: abstract_base_classes.System,
    states: list[npt.ArrayLike],
):
    return map(
        lambda state: system.copy(state=state),
        states,
    )
