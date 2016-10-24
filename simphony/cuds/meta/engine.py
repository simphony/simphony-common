import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .software_tool import SoftwareTool


class Engine(SoftwareTool):

    '''Represents a software tool which is used to solve the physics equation  # noqa
    '''

    cuba_key = CUBA.ENGINE

    def __init__(self, version=None, data=None):

        self.version = version
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._definition = 'Represents a software tool which is used to solve the physics equation'  # noqa
        # This is a system-managed, read-only attribute
        self._engine_feature = None

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer.new_with_restricted_keys(
                self.supported_parameters())
            data_container = self._data

        retvalue = DataContainer.new_with_restricted_keys(
            self.supported_parameters()
            )
        retvalue.update(data_container)

        return retvalue

    @data.setter
    def data(self, new_data):
        data = DataContainer.new_with_restricted_keys(
            self.supported_parameters()
            )
        data.update(new_data)
        self._data = data

    @property
    def definition(self):
        return self._definition

    @property
    def engine_feature(self):
        return self.data[CUBA.ENGINE_FEATURE]

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.VERSION, CUBA.UUID, CUBA.ENGINE_FEATURE)

    @classmethod
    def parents(cls):
        return (CUBA.SOFTWARE_TOOL, CUBA.CUDS_ITEM)
