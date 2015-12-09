from simphony.material_relations.material-relation
import MaterialRelation


class Coulomb(MaterialRelation):

    """ Automatically generated implementation of the
    Coulomb material-relation

    Attributes
    ----------

    position : <type 'numpy.float64'>
        Position of a point or node or atom
    position : <type 'numpy.float64'>
        Position of a point or node or atom

    """

    def __init(
        self,
        position,
        position
    ):
        super({MR_NAME}, self).__init__(
            name=Coulomb
            description=Coulomb
            parameters=DataContainer()
            supported_parameters=[
                CUBA.POSITION,
                CUBA.POSITION,
            ]
            materials=[1, 2]
            kind=CUBA.COULOMB
        )
