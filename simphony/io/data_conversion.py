import uuid

from ..core.keywords import KEYWORDS
from ..core import CUBA


def convert_to_file_type(value, cuba):
    """ Covert value to type to be stored in file.

    This method is used to convert a CUBA value to a
    type suitable for storage.

    Parameters
    ----------
    value :
        value
    cuba : CUBA
        the CUBA key of the value

    Returns
    -------
    value :
        The value in a form suitable for storage

    """
    if KEYWORDS[CUBA(cuba).name].dtype is uuid.UUID:
        return value.hex
    else:
        return value


def convert_from_file_type(file_value, cuba):
    """ Converts value from a value stored in file

    This method is used to convert a value from a type suitable for
    storage back to the type given in its CUBA definition.

    Parameters
    ----------
    file_value :
        value in a form suitable for storage
    cuba : CUBA
        the CUBA key of the value

    Returns
    -------
    value :
        The value which has the type as described in CUBA

    """
    if KEYWORDS[CUBA(cuba).name].dtype is uuid.UUID:
        return uuid.UUID(hex=file_value, version=4)
    else:
        return file_value
