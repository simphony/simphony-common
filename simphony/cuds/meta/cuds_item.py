from simphony.core.data_container import DataContainer
from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
import uuid


class CUDSItem(object):
    """
    Root of all CUDS types
    """
    cuba_key = CUBA.CUDS_ITEM

    def __init__(self):
        super(CUDSItem, self).__init__()
        self._init_definition()
        self._init_data()
        self._init_uid()

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(CUDSItem, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((CUBA.UID, ) + base_params))

    @classmethod
    def parents(cls):
        return tuple(c.cuba_key for c in cls.__mro__[1:]
                     if hasattr(c, "cuba_key"))

    def _init_definition(self):
        self._definition = self._default_definition()  # noqa

    @property
    def definition(self):
        return self._definition

    def _default_definition(self):
        return "Root of all CUDS types"  # noqa

    def _init_data(self):
        self._data = DataContainer()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    def _init_uid(self):
        self.data[CUBA.UID] = uuid.uuid4()

    @property
    def uid(self):
        return self.data[CUBA.UID]
