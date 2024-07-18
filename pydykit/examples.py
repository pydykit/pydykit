from importlib.resources import files

from . import utils


class Manager:

    def __init__(self):
        self.examples = self.load_examples()

    def load_examples(self):
        """Load content of all examples_files which have been shipped with package pydykit"""
        examples = {}
        for path in files("pydykit.example_files").iterdir():
            content = utils.load_yaml_file(path=path)
            examples[content["name"]] = content
        return examples

    def list_examples(self):
        """List all examples_files which have been shipped with package pydykit"""
        return list(self.examples.keys())

    def get_example(self, name):
        return self.examples[name]
