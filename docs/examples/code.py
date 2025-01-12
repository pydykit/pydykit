from markdown import markdown

from pydykit import examples


def to_markdown_list(llist):
    return "\n".join(
        [
            f"- [{item}](https://github.com/pydykit/pydykit/tree/main/pydykit/example_files/{item}.yml)"
            for item in llist
        ]
    )


keys = examples.ExampleManager().examples.keys()
html = markdown(
    f"""
{to_markdown_list(llist=keys)}
"""
)
print(html)
