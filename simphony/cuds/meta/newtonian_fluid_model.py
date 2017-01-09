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

    def supported_parameters(self):
        try:
            base_params = super(NewtonianFluidModel,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Newtonian fluid model assuming the viscous stresses are proportional to the rates of deformation"  # noqa
