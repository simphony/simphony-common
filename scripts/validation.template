# This file is copied and renamed in simphony/cuds/meta/ to support the
# meta classes in performing validation
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


def without_cuba_prefix(string):
    """Removes the CUBA. prefix to the string if there."""
    if is_cuba_key(string):
        return string[5:]

    return string


def is_cuba_key(value):
    """True if value is a qualified cuba key"""
    return isinstance(value, (str, unicode)) and value.startswith("CUBA.")


def check_valid_shape(value, shape, cuba_key):
    """ Check if `value` is a sequence that comply with `shape`.
    Note that the cuba data dimensionality is also taken into account.

    Parameters
    ----------
    value :
        The value to check
    shape : list or tuple
        The expected shape
    cuba_key:
        The key of the data expected to be contained.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        if the `value` does not comply with the required `shape`
    """
    # FIXME: cuba.yml uses [1] to mean a single value with no shape
    from simphony.core.keywords import KEYWORDS

    keyword = KEYWORDS[without_cuba_prefix(cuba_key)]

    expected_shape = []
    if list(shape) != [1]:
        expected_shape += list(shape)

    if list(keyword.shape) != [1]:
        expected_shape += list(keyword.shape)

    if expected_shape == []:
        expected_shape = [1]

    value_shape = numpy.asarray(value).shape or [1]

    if len(expected_shape) != len(value_shape):
        msg_fmt = ("Value shape of {value_shape}, "
                   "not comply with shape: {expected_shape}. "
                   "len(expected_shape) = {len_expected}, "
                   "len(value_shape) = {len_value}")
        error_message = msg_fmt.format(value_shape=value_shape,
                                       expected_shape=expected_shape,
                                       len_expected=len(expected_shape),
                                       len_value=len(value_shape))
        raise ValueError(error_message)

    for s1, s2 in zip(expected_shape, value_shape):
        if s1 is None:
            continue
        if s1 != s2:
            raise ValueError(("Incongruent shapes."
                              "Value shape of {value_shape}, "
                              "not compliant with expected shape: "
                              "{expected_shape}. ").format(
                                  expected_shape=expected_shape,
                                  value_shape=value_shape))


def check_cuba_shape(value, cuba_key):
    """ Check if `value` is a sequence that comply with the cuba shape

    Parameters
    ----------
    value:
        the value to check
    cuba_key: cuba key
        the cuba key of the data

    Returns
    -------
    None

    Raises
    ------
    ValueError
        if the `value` does not comply with the required cuba shape
    """
    # FIXME: cuba.yml uses [1] to mean a single value with no shape
    from simphony.core.keywords import KEYWORDS

    keyword = KEYWORDS[without_cuba_prefix(cuba_key)]
    expected_shape = list(keyword.shape)
    value_shape = list(numpy.asarray(value).shape or [1])

    if expected_shape != value_shape:
        raise ValueError(("Incongruent shapes."
                          "Value shape of {value_shape}, "
                          "not compliant with expected CUBA shape "
                          "{expected_shape}. ").format(
                              expected_shape=expected_shape,
                              value_shape=value_shape))

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

        check_cuba_shape(value, keyword_name)
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


def check_elements(value, shape, cuba_key):
    """Check each individual element of value to see if it matches the
    expected shape for a given cuba key
    """
    for entry in flatten_to_shape(value, shape):
        validate_cuba_keyword(entry, cuba_key)


def flatten_to_shape(container, shape):
    """Flatten an array, but only partially, so that higher dimensionality
    arrays can remain if required.
    """
    if not isinstance(container, (list, tuple)):
        raise TypeError("container must be iterable")

    if len(shape) == 1:
        for i in container:
            yield i
    else:
        for i in container:
            for value in flatten_to_shape(i, shape[1:]):
                yield value
