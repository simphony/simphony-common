from simphony.material_relations.material-relation
import MaterialRelation


class Coulomb(MaterialRelation):

    """ Automatically generated implementation of the
    Coulomb material-relation

    Attributes
    ----------

    cutoffdistance : <type 'numpy.float64'>
        Cutoff Distance
    dielectriccontance : <type 'numpy.float64'>
        Dielectric Contance

    """

    def __init(
        self,
        cutoffdistance,
        dielectriccontance
    ):
        super({MR_NAME}, self).__init__(
            name="Coulomb"
            description="Coulomb"
            parameters=DataContainer()
            supported_parameters=[
                CUBA.CUTOFF_DISTANCE,
                CUBA.DIELECTRIC_CONTANCE,
            ]
            materials=[1, 2]
            kind=CUBA.COULOMB
        )
