from .model_equation import ModelEquation
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class MaterialRelation(ModelEquation):
    """
    Material relation which together with the Physics equation
    gives the model equation
    """
    cuba_key = CUBA.MATERIAL_RELATION

    def __init__(self, material, *args, **kwargs):
        super(MaterialRelation, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_material(material)

    def supported_parameters(self):
        try:
            base_params = super(MaterialRelation, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.MATERIAL, ) + base_params

    def _init_definition(self):
        self._definition = "Material relation which together with the Physics equation gives the model equation"  # noqa

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
        import itertools
        value = validation.cast_data_type(value, 'CUBA.MATERIAL')
        validation.check_shape(value, [None])
        for tuple_ in itertools.product(*[range(x) for x in [None]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.MATERIAL')

        return value
