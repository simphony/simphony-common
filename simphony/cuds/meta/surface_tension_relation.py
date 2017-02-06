from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation


class SurfaceTensionRelation(MaterialRelation):
    """
    Surface tension relation between two fluids
    """
    cuba_key = CUBA.SURFACE_TENSION_RELATION

    def __init__(self,
                 material,
                 surface_tension=Default,
                 description=Default,
                 name=Default):
        super(SurfaceTensionRelation, self).__init__(
            material=material, description=description, name=name)
        self._init_surface_tension(surface_tension)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(SurfaceTensionRelation,
                                cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([
            CUBA.MATERIAL,
            CUBA.SURFACE_TENSION,
        ]) | base_params

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
        validation.check_valid_shape(value, [2], 'MATERIAL')
        validation.check_elements(value, [2], 'MATERIAL')

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
        validation.check_valid_shape(value, [1], 'SURFACE_TENSION')
        validation.validate_cuba_keyword(value, 'SURFACE_TENSION')
        return value

    def _default_surface_tension(self):
        return 0.07
