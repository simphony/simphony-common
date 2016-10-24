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
        data = self.data
        data[CUBA.MINOR] = value
        self.data = data

    @property
    def patch(self):
        return self.data[CUBA.PATCH]

    @patch.setter
    def patch(self, value):
        value = validation.cast_data_type(value, 'patch')
        validation.validate_cuba_keyword(value, 'patch')
        data = self.data
        data[CUBA.PATCH] = value
        self.data = data

    @property
    def major(self):
        return self.data[CUBA.MAJOR]

    @major.setter
    def major(self, value):
        value = validation.cast_data_type(value, 'major')
        validation.validate_cuba_keyword(value, 'major')
        data = self.data
        data[CUBA.MAJOR] = value
        self.data = data

    @property
    def full(self):
        return self.data[CUBA.FULL]

    @full.setter
    def full(self, value):
        value = validation.cast_data_type(value, 'full')
        validation.validate_cuba_keyword(value, 'full')
        data = self.data
        data[CUBA.FULL] = value
        self.data = data

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer.new_with_restricted_keys(
                self.supported_parameters())
            data_container = self._data

        retvalue = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        retvalue.update(data_container)

        return retvalue

    @data.setter
    def data(self, new_data):
        data = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        data.update(new_data)
        self._data = data

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
        return (CUBA.CUDS_ITEM, )
