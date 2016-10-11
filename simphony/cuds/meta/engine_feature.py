import uuid
from simphony.core import data_container as dc
from simphony.core import cuba as cb
from .cuds_item import CUDSItem


class EngineFeature(CUDSItem):

    '''Provides a physics equation and methods that engines provides to solve them  # noqa
    '''

    cuba_key = cb.CUBA.ENGINE_FEATURE

    def __init__(self, data=None):

        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._physics_equation = None
        # This is a system-managed, read-only attribute
        self._definition = 'Provides a physics equation and methods that engines provides to solve them'  # noqa
        # This is a system-managed, read-only attribute
        self._computational_method = None

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = dc.DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, dc.DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, dc.DataContainer):
            self._data = new_data
        else:
            self._data = dc.DataContainer(new_data)

    @property
    def physics_equation(self):
        return self.data[cb.CUBA.PHYSICS_EQUATION]

    @property
    def definition(self):
        return self._definition

    @property
    def computational_method(self):
        return self.data[cb.CUBA.COMPUTATIONAL_METHOD]

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (cb.CUBA.PHYSICS_EQUATION, cb.CUBA.UUID, cb.CUBA.COMPUTATIONAL_METHOD)

    @classmethod
    def parents(cls):
        return (cb.CUBA.CUDS_ITEM,)
