import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent
from . import validation


class Node(CUDSComponent):
    '''A node on a structured grid like lattice  # noqa
    '''

    cuba_key = CUBA.NODE

    def __init__(self, index, description=None, name=None, data=None):

        self.index = index
        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._definition = 'A node on a structured grid like lattice'  # noqa

    @property
    def index(self):
        return self.data[CUBA.INDEX]

    @index.setter
    def index(self, value):
        value = validation.cast_data_type(value, 'index')
        validation.validate_cuba_keyword(value, 'index')
        self.data[CUBA.INDEX] = value

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, DataContainer):
            self._data = new_data
        else:
            self._data = DataContainer(new_data)

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
        return (CUBA.DESCRIPTION, CUBA.INDEX, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
