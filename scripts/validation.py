import warnings
import re

import numpy


def to_camel_case(text, special={'cuds': 'CUDS'}):
    """ Convert text to CamelCase (for class name)

    Parameters
    ----------
    text : str
        The text to be converted

    special : dict
        If any substring of text (lower case) matches a key of `special`,
        the substring is replaced by the value

    Returns
    -------
    result : str
    """

    def replace_func(matched):
        # word should be lower case already
        word = matched.group(0).strip("_")
        if word in special:
            # Handle special case
            return special[word]
        else:
            # Capitalise the first character
            return word[0].upper()+word[1:]

    return re.sub(r'(_?[a-zA-Z]+)', replace_func, text.lower())


def decode_shape(shape_code):
    """ Decode the 'shape' attribute in the metadata schema

    Parameters
    ----------
    shape_code : str

    Returns
    -------
    tuple

    Examples
    --------
    >>> decode_shape("(1:)")
    ((1, inf),)

    >>> decode_shape("(:, :10)")
    ((-inf, inf), (-inf, 10))
    """
    matched = re.finditer(
        r'([0-9+]):([0-9]+)|([0-9]+):|:([0-9]+)|([0-9]+)|[^0-9](:)[^0-9]',
        shape_code)

    shapes = []

    for code in matched:
        min_size = code.group(1) or code.group(3) or code.group(5)
        min_size = int(min_size) if min_size else -numpy.inf
        max_size = code.group(2) or code.group(4) or code.group(5)
        max_size = int(max_size) if max_size else numpy.inf
        shapes.append((min_size, max_size))
    return tuple(shapes)


def check_shape(value, shape):
    """ Check if `value` is a sequence that comply with `shape`

    Parameters
    ----------
    shape : str

    Returns
    -------
    None

    Raises
    ------
    ValueError
        if the `value` does not comply with the required `shape`
    """
    decoded_shape = decode_shape(shape)
    if len(decoded_shape) == 0:
        # Any shape is allowed
        return

    # FIXME: cuba.yml uses [1] to mean a single value with no shape
    value_shape = numpy.asarray(value).shape or (1,)

    msg_fmt = ("value has a shape of {value_shape}, "
               "which does not comply with shape: {shape}")
    error_message = msg_fmt.format(value_shape=value_shape,
                                   shape=shape)

    if len(decoded_shape) != len(value_shape):
        raise ValueError(error_message)

    for (min_size, max_size), size in zip(decoded_shape, value_shape):
        if not (size >= min_size and size <= max_size):
            raise ValueError(error_message)


def validate_cuba_keyword(value, key):
    ''' Validate the given `value` against `key` such that
    shape and type of value matches what was specified

    Parameters
    ----------
    value : object
       any value

    key : str
       CUBA key, can be stripped of 'CUBA.'

    Returns
    -------
    None

    Raises
    ------
    TypeError
        - if key is a CUBA keyword with shape and the value's shape
          or type does not match
        - if key corresponds to a class defined by the meta data and
          the value is not an instance of that class
    '''
    from . import api
    from simphony.core.keywords import KEYWORDS


    # Sanitising, although generated code already did
    key = key.replace('CUBA.', '')

    # Class name, e.g. cuds_item -> CUDSItem
    class_name = to_camel_case(key)

    # The corresponding class in the metadata
    api_class = getattr(api, class_name, None)

    # Keyword name in KEYWORDS
    keyword_name = key.upper()

    if api_class:
        if not isinstance(value, api_class):
            message = '{0!r} is not an instance of {1}'
            raise TypeError(message.format(value, api_class))
    elif keyword_name in KEYWORDS:
        keyword = KEYWORDS[keyword_name]

        # Check type
        value_arr = numpy.asarray(value)

        if not numpy.issubdtype(value_arr.dtype, keyword.dtype):
            message = ('value has dtype {dtype1} while {key} '
                       'needs to be a {dtype2}')
            raise TypeError(message.format(dtype1=value_arr.dtype,
                                           key=key,
                                           dtype2=keyword.dtype))
        # FIXME: STRING
        # cuba.yml gives a fix length for the shape of string
        # It actually means the maximum length of the string
        # We will skip checking validating it for now
        if keyword.dtype is str and value_arr.dtype.char[0] in ('S', 'U'):
            warnings.warn('Value is a string, its shape is not validated. '
                          'Please fix the cuba.yml shape syntax.')
            return

        # Check shape, keyword.shape needs to be converted
        # to our shape syntax
        shape = '({})'.format(str(keyword.shape).strip('[]'))
        check_shape(value, shape)
    else:
        message = '{} is not defined in CUBA keyword or meta data'
        warnings.warn(message.format(key.upper()))


def cast_data_type(value, key):
    ''' Safely cast the value according to the type specified by
    KEYWORDS[key].

    Parameters
    ----------
    value : any
        Value to be casted

    key : str
        Name of the keyword

    Returns
    -------
    new_value : any
        If key is in KEYWORDS, new_value has the same data type as the
        type especified in KEYWORDS[key]
        If key is not in KEYWORDS, the original value is returned

    Raises
    ------
    ValueError
        If casting is not possible

    TypeError
        If casting would be unsafe
    '''
    from simphony.core.keywords import KEYWORDS

    keyword_name = key.upper()

    if keyword_name in KEYWORDS:
        target_type = KEYWORDS[keyword_name].dtype

        # Check if target is cuds instance
        if not target_type:
            # No casting for CUDS instances
            return value

        # If safe casting is not possible,
        # this will raise a ValueError/TypeError
        new_value = numpy.asarray(value).astype(target_type,
                                                casting='same_kind')

        if isinstance(value, (list, tuple)):
            return type(value)(new_value)

        if new_value.shape == ():
            return numpy.asscalar(new_value)

        return new_value

    else:
        return value
