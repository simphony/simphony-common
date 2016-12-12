import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA


class CUDSItem(object):
    '''Root of all CUDS types  # noqa
    '''

    cuba_key = CUBA.CUDS_ITEM

    def __init__(self):

        self._data = DataContainer()

        # This is a system-managed, read-only attribute
        self._definition = 'Root of all CUDS types'  # noqa

    @property
    def definition(self):
        return self._definition

    @property
    def data(self):
        return self._data

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
        return (CUBA.UUID, )

    @classmethod
    def parents(cls):
        return ()
