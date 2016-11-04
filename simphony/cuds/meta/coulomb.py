import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .pair_potential import PairPotential
from . import validation


class Coulomb(PairPotential):
    '''The standard electrostatic Coulombic interaction potential between a pair of point charges  # noqa
    '''

    cuba_key = CUBA.COULOMB

    def __init__(self,
                 material,
                 description="",
                 name="",
                 cutoff_distance=1.0,
                 dielectric_constant=1.0):

        self._data = DataContainer()

        self.material = material
        self.dielectric_constant = dielectric_constant
        self.cutoff_distance = cutoff_distance
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'The standard electrostatic Coulombic interaction potential between a pair of point charges'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def dielectric_constant(self):
        return self.data[CUBA.DIELECTRIC_CONSTANT]

    @dielectric_constant.setter
    def dielectric_constant(self, value):
        value = validation.cast_data_type(value, 'dielectric_constant')
        validation.validate_cuba_keyword(value, 'dielectric_constant')
        data = self.data
        data[CUBA.DIELECTRIC_CONSTANT] = value
        self.data = data

    @property
    def cutoff_distance(self):
        return self.data[CUBA.CUTOFF_DISTANCE]

    @cutoff_distance.setter
    def cutoff_distance(self, value):
        value = validation.cast_data_type(value, 'cutoff_distance')
        validation.validate_cuba_keyword(value, 'cutoff_distance')
        data = self.data
        data[CUBA.CUTOFF_DISTANCE] = value
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
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.DIELECTRIC_CONSTANT,
                CUBA.CUTOFF_DISTANCE, CUBA.MATERIAL, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.PAIR_POTENTIAL, CUBA.INTERATOMIC_POTENTIAL,
                CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
