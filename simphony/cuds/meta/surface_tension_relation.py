from .material_relation import MaterialRelation
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class SurfaceTensionRelation(MaterialRelation):
    """
    Surface tension relation between two fluids
    """
    cuba_key = CUBA.SURFACE_TENSION_RELATION

    def __init__(self, material, surface_tension=Default, *args, **kwargs):
        super(SurfaceTensionRelation, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_material(material)
        self._init_surface_tension(surface_tension)

    def supported_parameters(self):
        try:
            base_params = super(SurfaceTensionRelation,
                                self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.MATERIAL,
            CUBA.SURFACE_TENSION, ) + base_params

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Surface tension relation between two fluids"  # noqa

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
        validation.check_shape(value, [2])
        for tuple_ in itertools.product(*[range(x) for x in [2]]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.MATERIAL')

        return value

    def _init_surface_tension(self, value):
        if value is Default:
            value = 0.07

        self.surface_tension = value

    @property
    def surface_tension(self):
        return self.data[CUBA.SURFACE_TENSION]

    @surface_tension.setter
    def surface_tension(self, value):
        value = self._validate_surface_tension(value)
        self.data[CUBA.SURFACE_TENSION] = value

    def _validate_surface_tension(self, value):
        value = validation.cast_data_type(value, 'CUBA.SURFACE_TENSION')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'CUBA.SURFACE_TENSION')
        return value
