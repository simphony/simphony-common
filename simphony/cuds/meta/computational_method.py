import uuid
from simphony.core import data_container as dc
from simphony.core import cuba as cb
from .cuds_component import CUDSComponent


class ComputationalMethod(CUDSComponent):

    '''A computational method according to the RoMM  # noqa
    '''

    cuba_key = cb.CUBA.COMPUTATIONAL_METHOD

    def __init__(self, description=None, name=None, data=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._physics_equation = []
        # This is a system-managed, read-only attribute
        self._definition = 'A computational method according to the RoMM'  # noqa

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = dc.DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, dc.DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, dc.DataContainer):
            self._data = new_data
        else:
            self._data = dc.DataContainer(new_data)

    @property
    def physics_equation(self):
        return self._physics_equation

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
        return (cb.CUBA.DESCRIPTION, cb.CUBA.PHYSICS_EQUATION, cb.CUBA.UUID, cb.CUBA.NAME)

    @classmethod
    def parents(cls):
        return (cb.CUBA.CUDS_COMPONENT, cb.CUBA.CUDS_ITEM)
