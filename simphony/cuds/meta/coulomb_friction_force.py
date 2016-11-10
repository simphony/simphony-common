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
                 data=None,
                 description="",
                 name="",
                 friction_coefficient=0.0):

        self.material = material
        self.friction_coefficient = friction_coefficient
        self.name = name
        self.description = description
        if data:
            internal_data = self.data
            internal_data.update(data)
            self.data = internal_data

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
        return (CUBA.DESCRIPTION, CUBA.FRICTION_COEFFICIENT, CUBA.MATERIAL,
                CUBA.NAME, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
