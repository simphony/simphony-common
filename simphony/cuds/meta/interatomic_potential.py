from .material_relation import MaterialRelation
from simphony.core.cuba import CUBA


class InteratomicPotential(MaterialRelation):
    """
    Interatomic Potentials Category
    """
    cuba_key = CUBA.INTERATOMIC_POTENTIAL

    def __init__(self, *args, **kwargs):

        super(InteratomicPotential, self).__init__(*args, **kwargs)
        self._init_models()
        self._init_definition()

    def supported_parameters(self):
        try:
            base_params = super(InteratomicPotential,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa    

    def _default_definition(self):
        return "Interatomic Potentials Category"  # noqa
