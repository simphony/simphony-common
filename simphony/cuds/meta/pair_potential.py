import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .interatomic_potential import InteratomicPotential
from . import validation


class PairPotential(InteratomicPotential):
    '''Pair Interatomic Potentials Category  # noqa
    '''

    cuba_key = CUBA.PAIR_POTENTIAL

    def __init__(self, material, data=None, description="", name=""):

        self.material = material
        self.name = name
        self.description = description
        if data:
            internal_data = self.data
            internal_data.update(data)
            self.data = internal_data

        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'Pair Interatomic Potentials Category'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = []

    @property
    def material(self):
        return self.data[CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'material')
            validation.check_shape(value, '(2)')
            for item in value:
                validation.validate_cuba_keyword(item, 'material')
        data = self.data
        data[CUBA.MATERIAL] = value
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
        return (CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.NAME, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.INTERATOMIC_POTENTIAL, CUBA.MATERIAL_RELATION,
                CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
