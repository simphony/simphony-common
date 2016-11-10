import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .model_equation import ModelEquation
from . import validation


class MaterialRelation(ModelEquation):
    '''Material relation  # noqa
    '''

    cuba_key = CUBA.MATERIAL_RELATION

    def __init__(self, material, description="", name=""):

        self._data = DataContainer()

        self.material = material
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'Material relation'  # noqa
        # This is a system-managed, read-only attribute
        self._models = []
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def material(self):
        return self.data[CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'material')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'material')
        data = self.data
        data[CUBA.MATERIAL] = value
        self.data = data

    @property
    def definition(self):
        return self._definition

    @property
    def models(self):
        return self._models

    @property
    def variables(self):
        return self._variables

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.NAME, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
