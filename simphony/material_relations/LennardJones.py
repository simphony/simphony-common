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

    def __init(
        self,
        cutoffDistance,
        energyWellDepth,
        vanDerWaalsRadius
    ):
        super(LennardJones, self).__init__(
            name="LennardJones",
            description="LennardJones",
            parameters=dc.DataContainer(),
            supported_parameters=[
                CUBA.CUTOFF_DISTANCE,
                CUBA.ENERGY_WELL_DEPTH,
                CUBA.VAN_DER_WAALS_RADIUS,
            ],
            materials=[1, 2],
            kind=CUBA.LENNARD_JONES
        )

        self.cutoffDistance = cutoffDistance
        self.energyWellDepth = energyWellDepth
        self.vanDerWaalsRadius = vanDerWaalsRadius
