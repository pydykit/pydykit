import pytest
from pydantic import ValidationError

from pydykit.configuration import Integrator, System


class TestConfiguration:

    def test_invalid_class_name(self):
        with pytest.raises(ValidationError) as excinfo:
            System(class_name="my_class", kwargs=None)
        assert "supported options for" in str(excinfo.value)

    def test_defaults(self):
        conf = System(class_name="Lorenz", kwargs=None)
        assert conf.kwargs == None  # TODO: Fix this


class TestIntegratorConfig:
    def test_valid_keys(self):
        for key in [
            "Midpoint_DAE",
            "MidpointPH",
            "MidpointODE",
        ]:
            Integrator(class_name=key, kwargs={})
