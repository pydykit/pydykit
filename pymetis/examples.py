from importlib.resources import files

from . import utils


def load_examples():
    """Load content of all examples_files which have been shipped with package pymetis"""
    examples = {}
    for path in files("pymetis.example_files").iterdir():
        content = utils.load_yaml_file(path=path)
        examples[content["name"]] = content
    return examples


examples = load_examples()


def get(name):
    return examples[name]
