from .cuds_item import CUDSItem
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class SoftwareTool(CUDSItem):
    """
    Represents a software tool which is used to solve the model
    or in pre/post processing
    """
    cuba_key = CUBA.SOFTWARE_TOOL

    def __init__(self, version):

        super(SoftwareTool, self).__init__()
        self._init_version(version)

    def supported_parameters(self):
        try:
            base_params = super(SoftwareTool, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (CUBA.VERSION, ) + base_params

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'VERSION')
        return value

    def _default_version(self):
        return None
