from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .stress_model import StressModel


class MesoscopicStressModel(StressModel):
    """
    Stress model from meso scopic to use in mixture model
    """
    cuba_key = CUBA.MESOSCOPIC_STRESS_MODEL

    def __init__(self, description=Default, name=Default):
        super(MesoscopicStressModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(MesoscopicStressModel,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Stress model from meso scopic to use in mixture model"  # noqa
