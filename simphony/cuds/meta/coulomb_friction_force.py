import uuid
from simphony.core import data_container as dc
from simphony.core import cuba as cb
from .material_relation import MaterialRelation
from . import validation


class CoulombFrictionForce(MaterialRelation):

    '''Shear force accounting for the tangential displacement between contacting particles  # noqa
    '''

    cuba_key = cb.CUBA.COULOMB_FRICTION_FORCE

    def __init__(self, material, description=None, name=None, data=None, friction_coefficient=0.0):

        self.material = material
        self.description = description
        self.name = name
        if data:
            self.data = data
        self.friction_coefficient = friction_coefficient
        # This is a system-managed, read-only attribute
        self._models = [cb.CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'Shear force accounting for the tangential displacement between contacting particles'  # noqa
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
    def friction_coefficient(self):
        return self.data[cb.CUBA.FRICTION_COEFFICIENT]

    @friction_coefficient.setter
    def friction_coefficient(self, value):
        value = validation.cast_data_type(value, 'friction_coefficient')
        validation.validate_cuba_keyword(value, 'friction_coefficient')
        self.data[cb.CUBA.FRICTION_COEFFICIENT] = value

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
        return (cb.CUBA.FRICTION_COEFFICIENT, cb.CUBA.DESCRIPTION, cb.CUBA.MATERIAL, cb.CUBA.UUID, cb.CUBA.NAME)

    @classmethod
    def parents(cls):
        return (cb.CUBA.MATERIAL_RELATION, cb.CUBA.MODEL_EQUATION, cb.CUBA.CUDS_COMPONENT, cb.CUBA.CUDS_ITEM)
