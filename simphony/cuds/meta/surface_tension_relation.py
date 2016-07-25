import uuid
from simphony.core.data_container import create_data_container
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation
from . import validation

_RestrictedDataContainer = create_data_container(
    (CUBA.UUID, CUBA.SURFACE_TENSION, CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.NAME),
    class_name="_RestrictedDataContainer")


class SurfaceTensionRelation(MaterialRelation):

    '''Surface tension relation between two fluids  # noqa
    '''

    cuba_key = CUBA.SURFACE_TENSION_RELATION

    def __init__(self, material, description=None, name=None, data=None, surface_tension=0.07):

        self.material = material
        self.description = description
        self.name = name
        if data:
            self.data = data
        self.surface_tension = surface_tension
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Surface tension relation between two fluids'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

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
        self.data[CUBA.MATERIAL] = value

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = _RestrictedDataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, _RestrictedDataContainer):
                raise TypeError("data is not a RestrictedDataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, _RestrictedDataContainer):
            self._data = new_data
        else:
            self._data = _RestrictedDataContainer(new_data)

    @property
    def surface_tension(self):
        return self.data[CUBA.SURFACE_TENSION]

    @surface_tension.setter
    def surface_tension(self, value):
        value = validation.cast_data_type(value, 'surface_tension')
        validation.validate_cuba_keyword(value, 'surface_tension')
        self.data[CUBA.SURFACE_TENSION] = value

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
        return (CUBA.UUID, CUBA.SURFACE_TENSION, CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
