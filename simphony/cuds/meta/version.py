from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem


class Version(CUDSItem):
    """
    Version of a software tool used in a simulation
    """
    cuba_key = CUBA.VERSION

    def __init__(self, minor, patch, major, full):

        super(Version, self).__init__()
        self._init_minor(minor)
        self._init_patch(patch)
        self._init_major(major)
        self._init_full(full)

    def supported_parameters(self):
        try:
            base_params = super(Version, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.MINOR,
            CUBA.PATCH,
            CUBA.MAJOR,
            CUBA.FULL, ) + base_params

    def _init_minor(self, value):
        if value is Default:
            value = self._default_minor()

        self.minor = value

    @property
    def minor(self):
        return self.data[CUBA.MINOR]

    @minor.setter
    def minor(self, value):
        value = self._validate_minor(value)
        self.data[CUBA.MINOR] = value

    def _validate_minor(self, value):
        value = validation.cast_data_type(value, 'MINOR')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'MINOR')
        return value

    def _default_minor(self):
        raise TypeError("No default for minor")

    def _default_definition(self):
        return "Version of a software tool used in a simulation"  # noqa

    def _init_patch(self, value):
        if value is Default:
            value = self._default_patch()

        self.patch = value

    @property
    def patch(self):
        return self.data[CUBA.PATCH]

    @patch.setter
    def patch(self, value):
        value = self._validate_patch(value)
        self.data[CUBA.PATCH] = value

    def _validate_patch(self, value):
        value = validation.cast_data_type(value, 'PATCH')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'PATCH')
        return value

    def _default_patch(self):
        raise TypeError("No default for patch")

    def _init_major(self, value):
        if value is Default:
            value = self._default_major()

        self.major = value

    @property
    def major(self):
        return self.data[CUBA.MAJOR]

    @major.setter
    def major(self, value):
        value = self._validate_major(value)
        self.data[CUBA.MAJOR] = value

    def _validate_major(self, value):
        value = validation.cast_data_type(value, 'MAJOR')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'MAJOR')
        return value

    def _default_major(self):
        raise TypeError("No default for major")

    def _init_full(self, value):
        if value is Default:
            value = self._default_full()

        self.full = value

    @property
    def full(self):
        return self.data[CUBA.FULL]

    @full.setter
    def full(self, value):
        value = self._validate_full(value)
        self.data[CUBA.FULL] = value

    def _validate_full(self, value):
        value = validation.cast_data_type(value, 'FULL')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'FULL')
        return value

    def _default_full(self):
        raise TypeError("No default for full")
