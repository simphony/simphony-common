from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
import uuid


class CUDSItem(object):
    """
    Root of all CUDS types
    """
    cuba_key = CUBA.CUDS_ITEM

    def __init__(self, *args, **kwargs):
        super(CUDSItem, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_data()
        self._init_uuid()

    def supported_parameters(self):
        try:
            base_params = super(CUDSItem, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.UUID, ) + base_params

    @classmethod
    def parents(cls):
        return tuple(c.cuba_key for c in cls.__mro__[1:]
                     if hasattr(c, "cuba_key"))

    def _init_definition(self):
        self._definition = "Root of all CUDS types"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_data(self):
        self._data = DataContainer()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    def _init_uuid(self):
        self.data[CUBA.UUID] = uuid.uuid4()

    @property
    def uuid(self):
        return self.data[CUBA.UUID]
