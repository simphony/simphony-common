from simphony.material_relations.material-relation
import MaterialRelation


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
        cutoffdistance,
        energywelldepth,
        vanderwaalsradius
    ):
        super({MR_NAME}, self).__init__(
            name="LennardJones"
            description="LennardJones"
            parameters=DataContainer()
            supported_parameters=[
                CUBA.CUTOFF_DISTANCE,
                CUBA.ENERGY_WELL_DEPTH,
                CUBA.VAN_DER_WAALS_RADIUS,
            ]
            materials=[1, 2]
            kind=CUBA.LENNARD_JONES
        )
