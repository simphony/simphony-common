import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent


class Mesh(CUDSComponent):
    '''A mesh  # noqa
    '''

    cuba_key = CUBA.MESH

    def __init__(self, description=None, name=None, data=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._cell = None
        # This is a system-managed, read-only attribute
        self._definition = 'A mesh'  # noqa
        # This is a system-managed, read-only attribute
        self._face = None
        # This is a system-managed, read-only attribute
        self._edge = None
        # This is a system-managed, read-only attribute
        self._point = None

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
    def cell(self):
        return self._cell

    @property
    def definition(self):
        return self._definition

    @property
    def face(self):
        return self._face

    @property
    def edge(self):
        return self._edge

    @property
    def point(self):
        return self._point

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.POINT, CUBA.UUID, CUBA.FACE, CUBA.CELL,
                CUBA.EDGE, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
