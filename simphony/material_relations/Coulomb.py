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
        materials,
        cutoff_distance,
        dielectric_contance
    ):
        super(Coulomb, self).__init__(
            name="Coulomb",
            description="Coulomb material relation",  # noqa
            parameters=dc.DataContainer(),
            supported_parameters=[
                CUBA.CUTOFF_DISTANCE,
                CUBA.DIELECTRIC_CONTANCE,
            ],
            materials=materials,
            num_materials=[1, 2],
            kind=CUBA.COULOMB
        )

    @property
    def cutoff_distance(self):
        return self.parameters[CUBA.CUTOFF_DISTANCE]

    @cutoff_distance.setter
    def cutoff_distance(self, value):
        self.parameters[CUBA.CUTOFF_DISTANCE] = value

    @property
    def dielectric_contance(self):
        return self.parameters[CUBA.DIELECTRIC_CONTANCE]

    @dielectric_contance.setter
    def dielectric_contance(self, value):
        self.parameters[CUBA.DIELECTRIC_CONTANCE] = value

