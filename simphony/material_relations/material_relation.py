from simphony.core.data_container import DataContainer
from simphony.core.material_relations_information import (
    MATERIAL_RELATIONSHIP_INFORMATION)


class MaterialRelation(object):
    """ Class represents relationships between materials

    MaterialRelation provides a general interface for describing the
    (physics/chemistry) relations between different materials

    Attributes
    ----------
    kind: CUDSMaterialRelation
        Describes the kind of the MaterialRelation

    name : str
        name of the material-relation

    materials: list of uids
        materials where this relation applies

    parameters: DataContainer
        the required parameters

    description: str
        user-defined description of the material-relation

    supported_parameters: list of CUBA
        CUBA values required/allowed for the parameters

    allowed_number_materials : list of int
        list with all possible configurations of avaliable
        number of materials in the relation

    """

    def __init__(self, name, kind, materials, parameters, description=""):

        info = MATERIAL_RELATIONSHIP_INFORMATION[kind]
        self._allowed_number_materials = info.allowed_number_materials
        self._supported_parameters = [
            parameter.cuba_key for parameter in info.supported_parameters]

        self._name = name
        self._kind = kind
        self._description = description

        self.materials = materials
        self.parameters = parameters

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, basestring):
            self._name = value
        else:
            message = 'Expected string but received {!r}'
            raise TypeError(message.format(type(basestring)))

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if isinstance(value, basestring):
            self._description = value
        else:
            message = 'Expected string but received {!r}'
            raise TypeError(message.format(type(value)))

    @property
    def supported_parameters(self):
        return set(self._supported_parameters)

    @property
    def materials(self):
        return list(self._materials)

    @materials.setter
    def materials(self, value):
        self._check_materials(value)
        self._materials = value

    def _check_materials(self, value):
        if(len(value) not in self._allowed_number_materials):
            error_str = "Incorrect number of materials, expected: {}"
            raise ValueError(
                error_str.format(
                    len(value),
                    self._allowed_number_materials
                )
            )

    @property
    def parameters(self):
        return DataContainer(self._parameters)

    @parameters.setter
    def parameters(self, value):
        self._check_parameters(value)
        self._parameters = DataContainer(value)

    def _check_parameters(self, value):
        if (set(self._supported_parameters) != set(value.keys())):
            raise ValueError("Unsupported parameters")

    @property
    def allowed_number_materials(self):
        return self._allowed_number_materials

    @property
    def kind(self):
        return self._kind
