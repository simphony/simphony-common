from simphony.material_relations.material_relation import (
    MaterialRelation)
from simphony.core.cuba import CUBA
import simphony.core.data_container as dc


class LennardJones(MaterialRelation):

    """ Automatically generated implementation of the
    LennardJones material-relation

    Attributes
    ----------

    cutoffdistance : <type 'numpy.float64'>
        Cutoff Distance
    energywelldepth : <type 'numpy.float64'>
        Energy Well Depth
    vanderwaalsradius : <type 'numpy.float64'>
        Van Der Waals Radius

    """

    def __init__(
        self,
        name="LennardJones",
        materials=None,
        cutoff_distance=1.0,
        energy_well_depth=1.0,
        van_der_waals_radius=1.0
    ):
        super(LennardJones, self).__init__(
            name=name,
            description="Lennard Jones material relation",  # noqa
            parameters=dc.DataContainer(),
            supported_parameters=[
                CUBA.CUTOFF_DISTANCE,
                CUBA.ENERGY_WELL_DEPTH,
                CUBA.VAN_DER_WAALS_RADIUS,
            ],
            materials=materials,
            num_materials=[1, 2],
            kind=CUBA.LENNARD_JONES
        )

    @property
    def cutoff_distance(self):
        return self.parameters[CUBA.CUTOFF_DISTANCE]

    @cutoff_distance.setter
    def cutoff_distance(self, value):
        self.parameters[CUBA.CUTOFF_DISTANCE] = value

    @property
    def energy_well_depth(self):
        return self.parameters[CUBA.ENERGY_WELL_DEPTH]

    @energy_well_depth.setter
    def energy_well_depth(self, value):
        self.parameters[CUBA.ENERGY_WELL_DEPTH] = value

    @property
    def van_der_waals_radius(self):
        return self.parameters[CUBA.VAN_DER_WAALS_RADIUS]

    @van_der_waals_radius.setter
    def van_der_waals_radius(self, value):
        self.parameters[CUBA.VAN_DER_WAALS_RADIUS] = value
