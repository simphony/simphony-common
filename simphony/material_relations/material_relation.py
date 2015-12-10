from simphony.material_relations.abc_material_relation import (
    ABCMaterialRelation)


class MaterialRelation(ABCMaterialRelation):
    """ MaterialRelation provides a general interface for describing the
    (physics/chemistry) relations between different materials

    Attributes
    ----------
    name : str
        name of the material-relation

    description: str
        user-defined description of the material-relation

    parameters: DataContainer
        the required parameters

    supported_parameters: list of CUBA
        CUBA values required/allowed for the parameters

    materials: list of uids
        materials where this relation applies

    kind: CUBA
        Describes the kind of the MaterialRelation

    """

    def __init__(self, name, description, parameters, supported_parameters,
                 materials, kind):

        self.name = name
        self.description = {}
        self.parameters = {}
        self.supported_parameters = {}
        self.materials = {}
        self.kind = {}
