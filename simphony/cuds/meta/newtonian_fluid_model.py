from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .rheology_model import RheologyModel


class NewtonianFluidModel(RheologyModel):
    """
    Newtonian fluid model assuming the viscous stresses are
    proportional to the rates of deformation
    """
    cuba_key = CUBA.NEWTONIAN_FLUID_MODEL

    def __init__(self, description=Default, name=Default):

        super(NewtonianFluidModel, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(NewtonianFluidModel,
                                cls).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Newtonian fluid model assuming the viscous stresses are proportional to the rates of deformation"  # noqa
