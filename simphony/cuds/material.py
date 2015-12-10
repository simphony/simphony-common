import uuid

from simphony.core.data_container import DataContainer


class Material(object):
    """A class that represents a material.

    Class describes a material and its data.

    Attributes
    ----------
    uid : uuid.UUID
        the id of the material. If None, then it is generated
    data : DataContainer
        data associated with this material
    description : str
        textual description of the material

    """
    def __init__(self, uid=None, data=None, description=""):
        self.data = data if data else DataContainer()
        self.uid = uid if uid else uuid.uuid4()
        self.description = description

    @classmethod
    def from_material(cls, material):
        return cls(
            uid=material.uid,
            description=material.description,
            data=DataContainer(material.data))