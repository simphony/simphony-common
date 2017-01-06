from .cuds_item import CUDSItem
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class Version(CUDSItem):
    """
    Version of a software tool used in a simulation
    """

    cuba_key = CUBA.VERSION

    def __init__(self, minor, patch, major, full, *args, **kwargs):
        super(Version, self).__init__(*args, **kwargs)

        self._init_minor(minor)
        self._init_definition()
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
            raise TypeError("Value for minor must be specified")

        self.minor = value

    @property
    def minor(self):
        return self.data[CUBA.MINOR]

    @minor.setter
    def minor(self, value):
        value = self._validate_minor(value)
        self.data[CUBA.MINOR] = value

    def _validate_minor(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.MINOR')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.MINOR')

        return value

    def _init_definition(self):
        self._definition = "Version of a software tool used in a simulation"

    @property
    def definition(self):
        return self._definition

    def _init_patch(self, value):
        if value is Default:
            raise TypeError("Value for patch must be specified")

        self.patch = value

    @property
    def patch(self):
        return self.data[CUBA.PATCH]

    @patch.setter
    def patch(self, value):
        value = self._validate_patch(value)
        self.data[CUBA.PATCH] = value

    def _validate_patch(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.PATCH')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.PATCH')

        return value

    def _init_major(self, value):
        if value is Default:
            raise TypeError("Value for major must be specified")

        self.major = value

    @property
    def major(self):
        return self.data[CUBA.MAJOR]

    @major.setter
    def major(self, value):
        value = self._validate_major(value)
        self.data[CUBA.MAJOR] = value

    def _validate_major(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.MAJOR')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.MAJOR')

        return value

    def _init_full(self, value):
        if value is Default:
            raise TypeError("Value for full must be specified")

        self.full = value

    @property
    def full(self):
        return self.data[CUBA.FULL]

    @full.setter
    def full(self, value):
        value = self._validate_full(value)
        self.data[CUBA.FULL] = value

    def _validate_full(self, value):
        import itertools
        value = validation.cast_data_type(value, 'CUBA.FULL')
        validation.check_shape(value, None)
        for tuple_ in itertools.product(*[range(x) for x in None]):
            entry = value
            for idx in tuple_:
                entry = entry[idx]
            validation.validate_cuba_keyword(entry, 'CUBA.FULL')

        return value
