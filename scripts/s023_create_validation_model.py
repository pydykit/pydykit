import typing
from inspect import getfullargspec

from pydantic import create_model

import pydykit
import pydykit.systems

# ## Validate config file content

# - https://stackoverflow.com/questions/66168517/generate-dynamic-model-using-pydantic
# - https://stackoverflow.com/questions/2677185/how-can-i-read-a-functions-signature-including-default-argument-values

annotations = getfullargspec(pydykit.systems.MultiBodySystem).annotations

reformatted = {key: (val,) for key, val in annotations.items()}
typed = {key: typing.Annotated[val, key] for key, val in annotations.items()}

tmp = create_model(
    "tmp",
    # **annotations,
    # **reformatted,
    **typed,
)
