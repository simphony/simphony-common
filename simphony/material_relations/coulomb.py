from simphony.material_relations.material_relation import (
    MaterialRelation)
from simphony.core.cuba import CUBA
from simphony.core.data_container import DataContainer


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

    def __init__(
        self,
        name="Coulomb",
        materials=None,
        cutoff_distance=1.0,
        dielectric_contance=1.0
    ):
        super(Coulomb, self).__init__(
            name=name,
            description="Coulomb material relation",  # noqa
            parameters=DataContainer({
                CUBA.CUTOFF_DISTANCE: cutoff_distance,
                CUBA.DIELECTRIC_CONTANCE: dielectric_contance,
            }),
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
        return self._parameters[CUBA.CUTOFF_DISTANCE]

    @cutoff_distance.setter
    def cutoff_distance(self, value):
        updated_parameters = self._parameters
        updated_parameters[CUBA.CUTOFF_DISTANCE] = value
        self._parameters = updated_parameters

    @property
    def dielectric_contance(self):
        return self._parameters[CUBA.DIELECTRIC_CONTANCE]

    @dielectric_contance.setter
    def dielectric_contance(self, value):
        updated_parameters = self._parameters
        updated_parameters[CUBA.DIELECTRIC_CONTANCE] = value
        self._parameters = updated_parameters
