import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .condition import Condition


class Free(Condition):

    '''Free boundary condition  # noqa
    '''

    cuba_key = CUBA.FREE

    def __init__(self, data=None, description=None, name=None):

        if data:
            self.data = data
        self.description = description
        self.name = name
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ELECTRONIC, CUBA.ATOMISTIC, CUBA.MESOSCOPIC, CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Free boundary condition'  # noqa

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer.new_with_restricted_keys(
                self.supported_parameters())
            data_container = self._data

        # One more check in case the
        # property setter is by-passed
        if not isinstance(data_container, DataContainer):
            raise TypeError("data is not a DataContainer. "
                            "data.setter is by-passed.")

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
    def models(self):
        return self._models

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
        return (CUBA.DESCRIPTION, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CONDITION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
