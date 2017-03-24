from simphony.core import Default  # noqa
from .condition import Condition
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class Dirichlet(Condition):
    """
    Dirichlet boundary condition to specify the value the
    solutions takes on the boundary of the domain.
    """
    cuba_key = CUBA.DIRICHLET

    def __init__(self, material, description=Default, name=Default):
        super(Dirichlet, self).__init__(description=description, name=name)
        self._init_material(material)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Dirichlet, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.MATERIAL, ) + base_params))

    def _default_definition(self):
        return "Dirichlet boundary condition to specify the value the solutions takes on the boundary of the domain."  # noqa

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
        value = meta_validation.cast_data_type(value, 'MATERIAL')
        meta_validation.check_valid_shape(value, [1], 'MATERIAL')
        meta_validation.validate_cuba_keyword(value, 'MATERIAL')
        return value

    def _default_material(self):
        raise TypeError("No default for material")
