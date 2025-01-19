from importlib.resources import files
from typing import Dict, List

from . import utils


class ExampleManager:
    """
    A manager for handling example files included in the `pydykit` package.

    Provides functionality to load, list, and retrieve example files.

    Attributes:
        BASE_URL_EXAMPLE_FILES (str): URL pointing to the repository location of the example files.
        examples (Dict[str, dict]): A dictionary storing the loaded example files with their names as keys.
    """

    BASE_URL_EXAMPLE_FILES = (
        "https://github.com/pydykit/pydykit/tree/main/pydykit/example_files/"
    )

    def __init__(self):
        """
        Initialize the ExampleManager instance.

        Loads all examples from package resources.
        """

        self.examples = self.load_examples()

    def load_examples(self) -> Dict[str, dict]:
        """
        Load the content of all example files.

        Example files are expected to be in YAML format and located in the
        `pydykit/example_files` directory. The content of each file is loaded
        and stored in a dictionary, where the key is the `name` field specified
        in the file, and the value is the parsed YAML content.

        Returns:
            dict: A dictionary containing the loaded example files, keyed by their names.
        """
        examples = {}
        for path in files("pydykit.example_files").iterdir():
            content = utils.load_yaml_file(path=path)
            examples[content["name"]] = content
        return examples

    def list_examples(self) -> List[str]:
        """
        List the names of all example files shipped with the `pydykit` package.

        Returns:
            list: A list of example file names.
        """
        return list(self.examples.keys())

    def get_example(self, name) -> Dict:
        """
        Retrieve the content of a specific example file by its name.

        Args:
            name (str): The name of the example file to retrieve.

        Returns:
            dict: The parsed content of the requested example file.

        Raises:
            KeyError: If the requested example name does not exist in the loaded examples.
        """
        return self.examples[name]
