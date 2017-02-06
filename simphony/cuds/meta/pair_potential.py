from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .interatomic_potential import InteratomicPotential


class PairPotential(InteratomicPotential):
    """
    Pair Interatomic Potentials Category
    """
    cuba_key = CUBA.PAIR_POTENTIAL

    def __init__(self, material, description=Default, name=Default):
        super(PairPotential, self).__init__(
            material=material, description=description, name=name)
        self._init_material(material)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(PairPotential, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return (CUBA.MATERIAL, ) + base_params

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa

    def _default_definition(self):
        return "Pair Interatomic Potentials Category"  # noqa

    def _init_material(self, value):
        if value is Default:
            value = self._default_material()

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
        validation.check_valid_shape(value, [2], 'MATERIAL')
        validation.check_elements(value, [2], 'MATERIAL')

        return value

    def _default_material(self):
        raise TypeError("No default for material")
