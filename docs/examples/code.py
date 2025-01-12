from markdown import markdown

from pydykit import examples

example_manager = examples.ExampleManager()
keys = example_manager.examples.keys()


html = markdown(
    "\n".join(
        [
            f"- {item} [config file]({example_manager.BASE_URL_EXAMPLE_FILES}{item}.yml)"
            for item in keys
        ]
    )
)
print(html)
