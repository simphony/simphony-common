import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation
from . import validation


class CoulombFrictionForce(MaterialRelation):
    '''Shear force accounting for the tangential displacement between contacting particles  # noqa
    '''

    cuba_key = CUBA.COULOMB_FRICTION_FORCE

    def __init__(self,
                 material,
                 friction_coefficient=0.0,
                 description=None,
                 name=None,
                 data=None):

        self.material = material
        self.friction_coefficient = friction_coefficient
        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'Shear force accounting for the tangential displacement between contacting particles'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def friction_coefficient(self):
        return self.data[CUBA.FRICTION_COEFFICIENT]

    @friction_coefficient.setter
    def friction_coefficient(self, value):
        value = validation.cast_data_type(value, 'friction_coefficient')
        validation.validate_cuba_keyword(value, 'friction_coefficient')
        data = self.data
        data[CUBA.FRICTION_COEFFICIENT] = value
        self.data = data

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            data_container = self._data

        return DataContainer(data_container)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

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
        return (CUBA.FRICTION_COEFFICIENT, CUBA.DESCRIPTION, CUBA.MATERIAL,
                CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
