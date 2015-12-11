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

    num_materials: list of int
        list with all possible configurations of avaliable
        number of materials in the relation

    kind: CUBA
        Describes the kind of the MaterialRelation

    Raises
    ------
    ValueError :
        If the number of materials does not match with any value of
        num_materials

    """

    def __init__(self, name, description, parameters, supported_parameters,
                 materials, num_materials, kind):

        self._num_materials = num_materials

        if(materials.size() not in self._num_materials):
            error_str = "Incorrect number of materials, expected: {}"
            raise ValueError(
                error_str.format(
                    materials.size(),
                    self._num_materials
                )
            )

        self.name = name
        self.description = description
        self.parameters = parameters
        self.supported_parameters = supported_parameters
        self.materials = materials
        self.kind = kind
