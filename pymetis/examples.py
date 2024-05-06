from importlib.resources import files

import yaml


def load_examples():
    """Load content of all examples_files which have been shipped with package pymetis"""
    examples = {}
    for path in files("pymetis.example_files").iterdir():
        with open(path, "r") as file:
            content = yaml.safe_load(file)
        examples[content["name"]] = content
    return examples


examples = load_examples()


def get(name):
    return examples[name]
