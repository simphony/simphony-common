import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent
from . import validation


class Basis(CUDSComponent):
    '''Space basis vectors (row wise)  # noqa
    '''

    cuba_key = CUBA.BASIS

    def __init__(self, vector=None, description=None, name=None, data=None):

        if vector is None:
            self.vector = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._definition = 'Space basis vectors (row wise)'  # noqa

    @property
    def vector(self):
        return self.data[CUBA.VECTOR]

    @vector.setter
    def vector(self, value):
        value = validation.cast_data_type(value, 'vector')
        validation.check_shape(value, '(3, 3)')
        for item in value:
            validation.validate_cuba_keyword(item, 'vector')
        data = self.data
        data[CUBA.VECTOR] = value
        self.data = data

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer.new_with_restricted_keys(
                self.supported_parameters())
            data_container = self._data

        retvalue = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        retvalue.update(data_container)

        return retvalue

    @data.setter
    def data(self, new_data):
        data = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        data.update(new_data)
        self._data = data

    @property
    def definition(self):
        return self._definition

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.VECTOR, CUBA.DESCRIPTION, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
