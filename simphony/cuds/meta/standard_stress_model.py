from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .stress_model import StressModel


class StandardStressModel(StressModel):
    """
    Standard stress model (to use in mixture model)
    """
    cuba_key = CUBA.STANDARD_STRESS_MODEL

    def __init__(self, description=Default, name=Default):
        super(StandardStressModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(StandardStressModel,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Standard stress model (to use in mixture model)"  # noqa
