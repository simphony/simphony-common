from simphony.core import Default  # noqa
from .relative_velocity_model import RelativeVelocityModel
from simphony.core.cuba import CUBA


class MesoscopicRelativeVelocityModel(RelativeVelocityModel):
    """
    Relative velocity taken from meso scopic model
    """
    cuba_key = CUBA.MESOSCOPIC_RELATIVE_VELOCITY_MODEL

    def __init__(self, description=Default, name=Default):
        super(MesoscopicRelativeVelocityModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(MesoscopicRelativeVelocityModel,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Relative velocity taken from meso scopic model"  # noqa
