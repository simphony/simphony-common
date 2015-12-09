from simphony.material_relations.material-relation
import MaterialRelation


class LennardJones(MaterialRelation):

    """ Automatically generated implementation of the
    LennardJones material-relation

    Attributes
    ----------

    position : <type 'numpy.float64'>
        Position of a point or node or atom
    velocity : <type 'numpy.float64'>
        Velocity of a point or node
    deltadisplacement : <type 'numpy.float64'>
        Displacement during the last time step

    """

    def __init(
        self,
        position,
        velocity,
        deltadisplacement
    ):
        super({MR_NAME}, self).__init__(
            name=LennardJones
            description=LennardJones
            parameters=DataContainer()
            supported_parameters=[
                CUBA.POSITION,
                CUBA.VELOCITY,
                CUBA.DELTA_DISPLACEMENT,
            ]
            materials=[1, 2]
            kind=CUBA.LENNARD_JONES
        )
