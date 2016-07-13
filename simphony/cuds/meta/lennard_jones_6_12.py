import uuid
from simphony.core.data_container import create_data_container
from simphony.core.cuba import CUBA
from .pair_potential import PairPotential
from . import validation

_RestrictedDataContainer = create_data_container(
    (CUBA.DESCRIPTION, CUBA.ENERGY_WELL_DEPTH, CUBA.MATERIAL, CUBA.UUID, CUBA.CUTOFF_DISTANCE, CUBA.VAN_DER_WAALS_RADIUS, CUBA.NAME),
    class_name="_RestrictedDataContainer")


class LennardJones_6_12(PairPotential):

    '''A Lennard-Jones 6-12 Potential  # noqa
    '''

    cuba_key = CUBA.LENNARD_JONES_6_12

    def __init__(self, material, description=None, name=None, data=None, van_der_waals_radius=1.0, cutoff_distance=1.0, energy_well_depth=1.0):

        self.material = material
        self.description = description
        self.name = name
        if data:
            self.data = data
        self.van_der_waals_radius = van_der_waals_radius
        self.cutoff_distance = cutoff_distance
        self.energy_well_depth = energy_well_depth
        # This is a system-managed, read-only attribute
        self._models = [CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'A Lennard-Jones 6-12 Potential'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = [CUBA.POSITION, CUBA.POTENTIAL_ENERGY]

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = _RestrictedDataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, _RestrictedDataContainer):
                raise TypeError("data is not a RestrictedDataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, _RestrictedDataContainer):
            self._data = new_data
        else:
            self._data = _RestrictedDataContainer(new_data)

    @property
    def van_der_waals_radius(self):
        return self.data[CUBA.VAN_DER_WAALS_RADIUS]

    @van_der_waals_radius.setter
    def van_der_waals_radius(self, value):
        value = validation.cast_data_type(value, 'van_der_waals_radius')
        validation.validate_cuba_keyword(value, 'van_der_waals_radius')
        self.data[CUBA.VAN_DER_WAALS_RADIUS] = value

    @property
    def cutoff_distance(self):
        return self.data[CUBA.CUTOFF_DISTANCE]

    @cutoff_distance.setter
    def cutoff_distance(self, value):
        value = validation.cast_data_type(value, 'cutoff_distance')
        validation.validate_cuba_keyword(value, 'cutoff_distance')
        self.data[CUBA.CUTOFF_DISTANCE] = value

    @property
    def energy_well_depth(self):
        return self.data[CUBA.ENERGY_WELL_DEPTH]

    @energy_well_depth.setter
    def energy_well_depth(self, value):
        value = validation.cast_data_type(value, 'energy_well_depth')
        validation.validate_cuba_keyword(value, 'energy_well_depth')
        self.data[CUBA.ENERGY_WELL_DEPTH] = value

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
        return (CUBA.DESCRIPTION, CUBA.ENERGY_WELL_DEPTH, CUBA.MATERIAL, CUBA.UUID, CUBA.CUTOFF_DISTANCE, CUBA.VAN_DER_WAALS_RADIUS, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.PAIR_POTENTIAL, CUBA.INTERATOMIC_POTENTIAL, CUBA.MATERIAL_RELATION, CUBA.MODEL_EQUATION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
