import uuid
from simphony.core import data_container as dc
from simphony.core import cuba as cb
from .rheology_model import RheologyModel


class NewtonianFluidModel(RheologyModel):

    '''Newtonian fluid model assuming the viscous stresses are proportional to the rates of deformation  # noqa
    '''

    cuba_key = cb.CUBA.NEWTONIAN_FLUID_MODEL

    def __init__(self, description=None, name=None, data=None):

        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._models = [cb.CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Newtonian fluid model assuming the viscous stresses are proportional to the rates of deformation'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

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
    def models(self):
        return self._models

    @property
    def definition(self):
        return self._definition

    @property
    def variables(self):
        return self._variables

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (cb.CUBA.DESCRIPTION, cb.CUBA.UUID, cb.CUBA.NAME)

    @classmethod
    def parents(cls):
        return (cb.CUBA.RHEOLOGY_MODEL, cb.CUBA.PHYSICS_EQUATION, cb.CUBA.MODEL_EQUATION, cb.CUBA.CUDS_COMPONENT, cb.CUBA.CUDS_ITEM)
