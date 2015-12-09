from abc import ABCMeta, abstractmethod


class ABCMaterialRelation(object):
    """Abstract base class for material-relations.

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

    __metaclass__ = ABCMeta
