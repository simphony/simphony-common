import uuid
from simphony.core import data_container as dc
from simphony.core import cuba as cb
from .pair_potential import PairPotential
from . import validation


class LennardJones_6_12(PairPotential):

    '''A Lennard-Jones 6-12 Potential  # noqa
    '''

    cuba_key = cb.CUBA.LENNARD_JONES_6_12

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
        self._models = [cb.CUBA.ATOMISTIC]
        # This is a system-managed, read-only attribute
        self._definition = 'A Lennard-Jones 6-12 Potential'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = [cb.CUBA.POSITION, cb.CUBA.POTENTIAL_ENERGY]

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
    def van_der_waals_radius(self):
        return self.data[cb.CUBA.VAN_DER_WAALS_RADIUS]

    @van_der_waals_radius.setter
    def van_der_waals_radius(self, value):
        value = validation.cast_data_type(value, 'van_der_waals_radius')
        validation.validate_cuba_keyword(value, 'van_der_waals_radius')
        self.data[cb.CUBA.VAN_DER_WAALS_RADIUS] = value

    @property
    def cutoff_distance(self):
        return self.data[cb.CUBA.CUTOFF_DISTANCE]

    @cutoff_distance.setter
    def cutoff_distance(self, value):
        value = validation.cast_data_type(value, 'cutoff_distance')
        validation.validate_cuba_keyword(value, 'cutoff_distance')
        self.data[cb.CUBA.CUTOFF_DISTANCE] = value

    @property
    def energy_well_depth(self):
        return self.data[cb.CUBA.ENERGY_WELL_DEPTH]

    @energy_well_depth.setter
    def energy_well_depth(self, value):
        value = validation.cast_data_type(value, 'energy_well_depth')
        validation.validate_cuba_keyword(value, 'energy_well_depth')
        self.data[cb.CUBA.ENERGY_WELL_DEPTH] = value

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
        return (cb.CUBA.DESCRIPTION, cb.CUBA.ENERGY_WELL_DEPTH, cb.CUBA.MATERIAL, cb.CUBA.UUID, cb.CUBA.CUTOFF_DISTANCE, cb.CUBA.VAN_DER_WAALS_RADIUS, cb.CUBA.NAME)

    @classmethod
    def parents(cls):
        return (cb.CUBA.PAIR_POTENTIAL, cb.CUBA.INTERATOMIC_POTENTIAL, cb.CUBA.MATERIAL_RELATION, cb.CUBA.MODEL_EQUATION, cb.CUBA.CUDS_COMPONENT, cb.CUBA.CUDS_ITEM)
