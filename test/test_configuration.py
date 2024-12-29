import pytest
from pydantic import ValidationError

from pydykit.configuration import Integrator, System


class TestConfiguration:
    def test_invalid_class_name(self):
        with pytest.raises(ValidationError) as excinfo:
            System(class_name="my_class")
        assert "Input should be" in str(excinfo.value)


class TestIntegratorConfig:
    def test_valid_keys(self):
        for key in [
            "MidpointMultibody",
            "MidpointPH",
            "MidpointDAE",
        ]:
            Integrator(class_name=key)
