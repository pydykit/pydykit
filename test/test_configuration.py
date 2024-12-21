import pytest
from pydantic import ValidationError

from pydykit.configuration import Integrator, System


class TestConfiguration:
    def test_invalid_class_name(self):
        with pytest.raises(ValidationError) as excinfo:
            System(class_name="my_class", kwargs={})
        assert "Input should be" in str(excinfo.value)

    def test_empty_dict_kwargs(self):
        conf = System(class_name="Lorenz", kwargs={})
        assert conf.kwargs.model_dump() == {}

    def test_invalid_kwargs(self):
        with pytest.raises(ValidationError) as excinfo:
            System(
                class_name="Lorenz",
                kwargs=None,
            )
        assert "Input should be a valid dictionary" in str(excinfo.value)


class TestIntegratorConfig:
    def test_valid_keys(self):
        for key in [
            "MidpointMultibody",
            "MidpointPH",
            "MidpointDAE",
        ]:
            Integrator(class_name=key, kwargs={})
