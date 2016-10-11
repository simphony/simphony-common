import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .pair_potential import PairPotential
from . import validation


class Coulomb(PairPotential):

    '''The standard electrostatic Coulombic interaction potential between a pair of point charges  # noqa
    '''

    cuba_key = CUBA.COULOMB

    def __init__(self, material, description=None, name=None, data=None, cutoff_distance=1.0, dielectric_constant=1.0):

        self.material = material
        self.description = description
        self.name = name
        if data:
            self.data = data
        self.cutoff_distance = cutoff_distance
        self.dielectric_constant = dielectric_constant
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'The standard electrostatic Coulombic interaction potential between a pair of point charges'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, DataContainer):
            self._data = new_data
        else:
            self._data = DataContainer(new_data)

    @property
    def cutoff_distance(self):
        return self.data[CUBA.CUTOFF_DISTANCE]

    @cutoff_distance.setter
    def cutoff_distance(self, value):
        value = validation.cast_data_type(value, 'cutoff_distance')
        validation.validate_cuba_keyword(value, 'cutoff_distance')
        self.data[CUBA.CUTOFF_DISTANCE] = value

    @property
    def dielectric_constant(self):
        return self.data[CUBA.DIELECTRIC_CONSTANT]

    @dielectric_constant.setter
    def dielectric_constant(self, value):
        value = validation.cast_data_type(value, 'dielectric_constant')
        validation.validate_cuba_keyword(value, 'dielectric_constant')
        self.data[CUBA.DIELECTRIC_CONSTANT] = value

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
        return (CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.UUID, CUBA.CUTOFF_DISTANCE, CUBA.DIELECTRIC_CONSTANT, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.PAIR_POTENTIAL, CUBA.INTERATOMIC_POTENTIAL, CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
