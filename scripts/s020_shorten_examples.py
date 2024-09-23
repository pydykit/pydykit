from pathlib import Path

from scipy import io

PATH_TEST_DIRECTORY = Path(__file__).parent.parent.absolute().joinpath("test")
PATH_REFERENCE_RESULTS = PATH_TEST_DIRECTORY.joinpath("reference_results")


example_names = [
    "pendulum3dcartesian_full_time",
    "rigidbodyrotatingquaternion",
    "fourparticlesystem",
    "porthamiltonianfourparticlesystem",
]

examples = [dict(name=val) for val in example_names]

paths_old = [
    PATH_REFERENCE_RESULTS.joinpath(
        "metis",
        f"{example_name}.mat",
    )
    for example_name in example_names
]

for example, path in zip(examples, paths_old):
    example["path_old"] = path


def load_result_of_metis_simulation(path):
    import scipy.io

    mat = scipy.io.loadmat(path)
    return mat


for example in examples:
    path_old = example["path_old"]
    old = load_result_of_metis_simulation(path=path_old)

    new = dict()
    for key in [key for key in old.keys() if not key.startswith("__")]:
        new[key] = old[key][0:20, ...]

    print(example["name"])
    print(new["time"][-1])

    io.savemat(path_old.parent.joinpath(example["name"] + "_new_.mat"), new)
