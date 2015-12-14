from simphony.material_relations.abc_material_relation import (
    ABCMaterialRelation)
import simphony.core.data_container as dc


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

        self._name = name
        self._description = description
        self._parameters = parameters
        self._supported_parameters = supported_parameters
        self._materials = materials
        self._kind = kind

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, string):
            self._name = value
        else:
            message = 'Expected string but received {!r}'
            raise TypeError(message.format(type(string)))

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, string):
            self._description = value
        else:
            message = 'Expected string but received {!r}'
            raise TypeError(message.format(type(string)))

    @property
    def supported_parameters(self):
        return set(self._supported_parameters)

    @property
    def materials(self):
        return list(self._materials)

    @materials.setter
    def materials(self, value):
        self._materials = value

    @property
    def parameters(self):
        return dc.DataContainer(self._parameters)

    @parameters.setter
    def parameters(self, value):
        self._parameters = dc.DataContainer(value)

    @property
    def num_materials(self):
        return self._num_materials

    @num_materials.setter
    def num_materials(self, value):
        self._num_materials = value

    @property
    def kind(self):
        return self._kind
