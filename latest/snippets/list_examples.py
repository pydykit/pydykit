from markdown import markdown

from pydykit import examples

example_manager = examples.ExampleManager()
keys = example_manager.examples.keys()

base_url = example_manager.BASE_URL_EXAMPLE_FILES
html = markdown(
    "\n".join([f"- {item} [config file]({base_url}{item}.yml)" for item in keys])
)
print(html)
