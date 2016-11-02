import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA


class CUDSItem(object):
    '''Root of all CUDS types  # noqa
    '''

    cuba_key = CUBA.CUDS_ITEM

    def __init__(self, data=None):

        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._definition = 'Root of all CUDS types'  # noqa

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            data_container = self._data

        return DataContainer(data_container)

    @data.setter
    def data(self, new_data):
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
        return (CUBA.UUID, )

    @classmethod
    def parents(cls):
        return ()
