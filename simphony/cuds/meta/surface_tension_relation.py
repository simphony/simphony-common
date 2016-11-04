import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation
from . import validation


class SurfaceTensionRelation(MaterialRelation):
    '''Surface tension relation between two fluids  # noqa
    '''

    cuba_key = CUBA.SURFACE_TENSION_RELATION

    def __init__(self, material, description="", name="",
                 surface_tension=0.07):

        self._data = DataContainer()

        self.material = material
        self.surface_tension = surface_tension
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Surface tension relation between two fluids'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def material(self):
        return self.data[CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'material')
            validation.check_shape(value, '(2)')
            for item in value:
                validation.validate_cuba_keyword(item, 'material')
        data = self.data
        data[CUBA.MATERIAL] = value
        self.data = data

    @property
    def surface_tension(self):
        return self.data[CUBA.SURFACE_TENSION]

    @surface_tension.setter
    def surface_tension(self, value):
        value = validation.cast_data_type(value, 'surface_tension')
        validation.validate_cuba_keyword(value, 'surface_tension')
        data = self.data
        data[CUBA.SURFACE_TENSION] = value
        self.data = data

    @property
    def models(self):
        return self._models

    @property
    def definition(self):
        return self._definition

    @property
    def variables(self):
        return self._variables

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.UUID, CUBA.SURFACE_TENSION, CUBA.DESCRIPTION,
                CUBA.MATERIAL, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
