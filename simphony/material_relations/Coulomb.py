from simphony.material_relations.material_relation import (
    MaterialRelation)
from simphony.core.cuba import CUBA
import simphony.core.data_container as dc


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
        super(Coulomb, self).__init__(
            name="Coulomb",
            description="Coulomb",
            parameters=dc.DataContainer(),
            supported_parameters=[
                CUBA.CUTOFF_DISTANCE,
                CUBA.DIELECTRIC_CONTANCE,
            ],
            materials=[1, 2],
            kind=CUBA.COULOMB
        )
