from simphony.core import Default  # noqa
from simphony.cuds import meta_validation
from simphony.core.cuba import CUBA
from .model_equation import ModelEquation


class MaterialRelation(ModelEquation):
    """
    Material relation which together with the Physics equation
    gives the model equation
    """
    cuba_key = CUBA.MATERIAL_RELATION

    def __init__(self, material=Default, description=Default, name=Default):
        super(MaterialRelation, self).__init__(
            description=description, name=name)
        self._init_material(material)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(MaterialRelation, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.MATERIAL, ) + base_params))

    def _default_definition(self):
        return "Material relation which together with the Physics equation gives the model equation"  # noqa

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
        meta_validation.check_valid_shape(value, [None], 'MATERIAL')
        meta_validation.check_elements(value, [None], 'MATERIAL')

        return value

    def _default_material(self):
        return []
