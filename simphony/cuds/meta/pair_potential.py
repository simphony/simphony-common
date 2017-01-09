from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA
from .interatomic_potential import InteratomicPotential


class PairPotential(InteratomicPotential):
    """
    Pair Interatomic Potentials Category
    """
    cuba_key = CUBA.PAIR_POTENTIAL

    def __init__(self, material, *args, **kwargs):
        super(PairPotential, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_material(material)

    def supported_parameters(self):
        try:
            base_params = super(PairPotential, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.MATERIAL, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.ATOMISTIC']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Pair Interatomic Potentials Category"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_material(self, value):
        if value is Default:
            raise TypeError("Value for material must be specified")

        self.material = value

    @property
    def material(self):
        return self.data[CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        value = self._validate_material(value)
        self.data[CUBA.MATERIAL] = value

    def _validate_material(self, value):

        value = validation.cast_data_type(value, 'MATERIAL')
        validation.check_shape(value, [2])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(container, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'MATERIAL')

        return value
