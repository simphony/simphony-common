from .cuds_item import CUDSItem
from . import validation
from simphony.core import Default
from simphony.core.cuba import CUBA


class CUDSComponent(CUDSItem):
    """
    Base data type for the CUDS components
    """
    cuba_key = CUBA.CUDS_COMPONENT

    def __init__(self, description=Default, name=Default, *args, **kwargs):
        super(CUDSComponent, self).__init__(*args, **kwargs)

        self._init_description(description)
        self._init_definition()
        self._init_name(name)

    def supported_parameters(self):
        try:
            base_params = super(CUDSComponent, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.DESCRIPTION,
            CUBA.NAME, ) + base_params

    def _init_description(self, value):
        if value is Default:
            value = ""

        self.description = value

    @property
    def description(self):
        return self.data[CUBA.DESCRIPTION]

    @description.setter
    def description(self, value):
        value = self._validate_description(value)
        self.data[CUBA.DESCRIPTION] = value

    def _validate_description(self, value):
        value = validation.cast_data_type(value, 'DESCRIPTION')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'DESCRIPTION')
        return value

    def _init_definition(self):
        self._definition = "Base data type for the CUDS components"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_name(self, value):
        if value is Default:
            value = ""

        self.name = value

    @property
    def name(self):
        return self.data[CUBA.NAME]

    @name.setter
    def name(self, value):
        value = self._validate_name(value)
        self.data[CUBA.NAME] = value

    def _validate_name(self, value):
        value = validation.cast_data_type(value, 'NAME')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'NAME')
        return value
