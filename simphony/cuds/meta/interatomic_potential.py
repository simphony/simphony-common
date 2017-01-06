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

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC']

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Interatomic Potentials Category"

    @property
    def definition(self):
        return self._definition
