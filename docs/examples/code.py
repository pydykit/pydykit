from markdown import markdown

from pydykit import examples

keys = examples.ExampleManager().examples.keys()
html = markdown(f"# greeting from python \n {keys}")
print(html)
