from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .cuds_item import CUDSItem


class SoftwareTool(CUDSItem):
    """
    Represents a software tool which is used to solve the model
    or in pre/post processing
    """
    cuba_key = CUBA.SOFTWARE_TOOL

    def __init__(self, version):
        super(SoftwareTool, self).__init__()
        self._init_version(version)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(SoftwareTool, cls).supported_parameters()
        except AttributeError:
            base_params = set()
        return set([CUBA.VERSION, ]) | base_params

    def _default_definition(self):
        return "Represents a software tool which is used to solve the model or in pre/post processing"  # noqa

    def _init_version(self, value):
        if value is Default:
            value = self._default_version()

        self.version = value

    @property
    def version(self):
        return self.data[CUBA.VERSION]

    @version.setter
    def version(self, value):
        value = self._validate_version(value)
        self.data[CUBA.VERSION] = value

    def _validate_version(self, value):
        value = validation.cast_data_type(value, 'VERSION')
        validation.check_valid_shape(value, [1], 'VERSION')
        validation.validate_cuba_keyword(value, 'VERSION')
        return value

    def _default_version(self):
        raise TypeError("No default for version")
