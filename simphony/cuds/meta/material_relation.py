from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .model_equation import ModelEquation


class MaterialRelation(ModelEquation):
    """
    Material relation which together with the Physics equation
    gives the model equation
    """
    cuba_key = CUBA.MATERIAL_RELATION

    def __init__(self, material, description=Default, name=Default):

        super(MaterialRelation, self).__init__(
            description=description, name=name)
        self._init_material(material)

    def supported_parameters(self):
        try:
            base_params = super(MaterialRelation, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.MATERIAL, ) + base_params

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
        value = validation.cast_data_type(value, 'MATERIAL')
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'MATERIAL')

        return value

    def _default_material(self):
        raise TypeError("No default for material")
