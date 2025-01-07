from pydykit.configuration import Integrator


class TestIntegratorConfig:
    def test_valid_keys(self):
        for key in [
            "MidpointMultibody",
            "MidpointPH",
            "MidpointDAE",
        ]:
            Integrator(class_name=key)
