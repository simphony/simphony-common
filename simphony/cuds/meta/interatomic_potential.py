from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation


class InteratomicPotential(MaterialRelation):
    """
    Interatomic Potentials Category
    """
    cuba_key = CUBA.INTERATOMIC_POTENTIAL

    def __init__(self, material=Default, description=Default, name=Default):
        super(InteratomicPotential, self).__init__(
            material=material, description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(InteratomicPotential,
                                cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([]) | base_params

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa

    def _default_definition(self):
        return "Interatomic Potentials Category"  # noqa
