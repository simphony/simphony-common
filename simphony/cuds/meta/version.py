import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem
from . import validation


class Version(CUDSItem):

    '''Version of a software tool used in a simulation  # noqa
    '''

    cuba_key = CUBA.VERSION

    def __init__(self, minor, patch, major, full, data=None):

        self.minor = minor
        self.patch = patch
        self.major = major
        self.full = full
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._definition = 'Version of a software tool used in a simulation'  # noqa

    @property
    def minor(self):
        return self.data[CUBA.MINOR]

    @minor.setter
    def minor(self, value):
        value = validation.cast_data_type(value, 'minor')
        validation.validate_cuba_keyword(value, 'minor')
        self.data[CUBA.MINOR] = value

    @property
    def patch(self):
        return self.data[CUBA.PATCH]

    @patch.setter
    def patch(self, value):
        value = validation.cast_data_type(value, 'patch')
        validation.validate_cuba_keyword(value, 'patch')
        self.data[CUBA.PATCH] = value

    @property
    def major(self):
        return self.data[CUBA.MAJOR]

    @major.setter
    def major(self, value):
        value = validation.cast_data_type(value, 'major')
        validation.validate_cuba_keyword(value, 'major')
        self.data[CUBA.MAJOR] = value

    @property
    def full(self):
        return self.data[CUBA.FULL]

    @full.setter
    def full(self, value):
        value = validation.cast_data_type(value, 'full')
        validation.validate_cuba_keyword(value, 'full')
        self.data[CUBA.FULL] = value

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
        return (CUBA.MAJOR, CUBA.FULL, CUBA.UUID, CUBA.MINOR, CUBA.PATCH)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_ITEM,)
