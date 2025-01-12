from markdown import markdown

from pydykit import examples

example_manager = examples.ExampleManager()
keys = example_manager.examples.keys()
content = "\n".join(
    [
        f"- {item} [config file]({example_manager.BASE_URL_EXAMPLE_FILES}{item}.yml)"
        for item in keys
    ]
)

html = markdown(content)
print(html)
