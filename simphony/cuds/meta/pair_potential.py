import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .interatomic_potential import InteratomicPotential
from . import validation


class PairPotential(InteratomicPotential):
    '''Pair Interatomic Potentials Category  # noqa
    '''

    cuba_key = CUBA.PAIR_POTENTIAL

    def __init__(self, material, data=None, description=None, name=None):

        self.material = material
        if data:
            self.data = data
        self.description = description
        self.name = name
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
            self._data = DataContainer.new_with_restricted_keys(
                self.supported_parameters())
            data_container = self._data

        # One more check in case the
        # property setter is by-passed
        if not isinstance(data_container, DataContainer):
            raise TypeError("data is not a DataContainer. "
                            "data.setter is by-passed.")

        retvalue = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        retvalue.update(data_container)

        return retvalue

    @data.setter
    def data(self, new_data):
        data = DataContainer.new_with_restricted_keys(
            self.supported_parameters())
        data.update(new_data)
        self._data = data

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
        return (CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.INTERATOMIC_POTENTIAL, CUBA.MATERIAL_RELATION,
                CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
