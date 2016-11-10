import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .material_relation import MaterialRelation
from . import validation


class DissipationForce(MaterialRelation):
    '''Viscous normal force describing the inelasticity of particle collisions  # noqa
    '''

    cuba_key = CUBA.DISSIPATION_FORCE

    def __init__(self,
                 material,
                 description="",
                 name="",
                 restitution_coefficient=1.0):

        self._data = DataContainer()

        self.material = material
        self.restitution_coefficient = restitution_coefficient
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'Viscous normal force describing the inelasticity of particle collisions'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def restitution_coefficient(self):
        return self.data[CUBA.RESTITUTION_COEFFICIENT]

    @restitution_coefficient.setter
    def restitution_coefficient(self, value):
        value = validation.cast_data_type(value, 'restitution_coefficient')
        validation.validate_cuba_keyword(value, 'restitution_coefficient')
        data = self.data
        data[CUBA.RESTITUTION_COEFFICIENT] = value
        self.data = data

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
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.NAME,
                CUBA.RESTITUTION_COEFFICIENT, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
