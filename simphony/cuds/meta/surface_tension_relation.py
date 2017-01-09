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

        super(SurfaceTensionRelation, self).__init__(material, *args, **kwargs)
        self._init_models()
        self._init_definition()
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

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_definition(self):
        return "Surface tension relation between two fluids"  # noqa

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
        validation.check_shape(value, [2])

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

    def _init_surface_tension(self, value):
        if value is Default:
            value = self._default_surface_tension()

        self.surface_tension = value

    @property
    def surface_tension(self):
        return self.data[CUBA.SURFACE_TENSION]

    @surface_tension.setter
    def surface_tension(self, value):
        value = self._validate_surface_tension(value)
        self.data[CUBA.SURFACE_TENSION] = value

    def _validate_surface_tension(self, value):
        value = validation.cast_data_type(value, 'SURFACE_TENSION')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'SURFACE_TENSION')
        return value

    def _default_surface_tension(self):
        return 0.07
