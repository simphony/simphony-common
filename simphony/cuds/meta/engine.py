import uuid
from simphony.core.data_container import create_data_container
from simphony.core.cuba import CUBA
from .software_tool import SoftwareTool

_RestrictedDataContainer = create_data_container(
    (CUBA.VERSION, CUBA.UUID, CUBA.ENGINE_FEATURE),
    class_name="_RestrictedDataContainer")


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
            self._data = _RestrictedDataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, _RestrictedDataContainer):
                raise TypeError("data is not a RestrictedDataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, _RestrictedDataContainer):
            self._data = new_data
        else:
            self._data = _RestrictedDataContainer(new_data)

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
