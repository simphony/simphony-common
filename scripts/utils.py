import re
import shutil
import tempfile
import textwrap

from contextlib import contextmanager


class NoDefault(object):
    pass


@contextmanager
def make_temporary_directory():
    ''' Context Manager for creating a temporary directory
    and remove the tree on exit

    Yields
    ------
    temp_dir : str
        absolute path to temporary directory
    '''
    try:
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


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


def indent(text, level=1):
    """Indents a body of text of a given amount of levels, where each level
    is the standard indentation space of 4 spaces.
    """
    dedent_text = textwrap.dedent(text)
    spaces = 4 * level * " "
    return "\n".join((spaces + line) for line in dedent_text.splitlines())


def with_cuba_prefix(string):
    """Adds the CUBA. prefix to the string if not there."""
    if is_cuba_key(string):
        return string

    return "CUBA." + string


def without_cuba_prefix(string):
    """Removes the CUBA. prefix to the string if there."""
    if is_cuba_key(string):
        return string[5:]

    return string


def is_cuba_key(value):
    return isinstance(value, (str, unicode)) and value.startswith("CUBA.")


def cuba_key_to_meta_class_name(string):
    return to_camel_case(without_cuba_prefix(string))


def cuba_key_to_meta_class_module_name(string):
    return without_cuba_prefix(string).lower()


def cuba_key_to_property_name(string):
    return without_cuba_prefix(string).lower()


def meta_class_name_to_module_name(string, special={"CUDS": "Cuds"}):
    for search, replace in special.items():
        string = re.sub(search, replace, string)

    def replace_func(matched):
        word = matched.group(0).strip("_")
        res = "_"+word.lower()
        return res

    return re.sub(r'([A-Z]+)', replace_func, string).lstrip("_")


def quoted_if_string(value):
    """
    returns the same value if not a string, otherwise adds quotes before
    and after.
    """
    if isinstance(value, (str, unicode)):
        return '"{}"'.format(value)

    return value


def parse_shape(shape_spec):
    if shape_spec is None:
        return [1]

    elif isinstance(shape_spec, (str, unicode)):
        shape_spec = shape_spec.strip()
        if shape_spec[0] not in "[(" or shape_spec[-1] not in "])":
            raise ValueError("Shape specification {} not "
                             "compliant to required format".format(shape_spec))

        elems = shape_spec[1:-1].split(",")

        def transform(el):
            el = el.strip()
            if el == ':':
                return None
            else:
                return int(el)

        shape = map(transform, elems)
    else:
        shape = shape_spec

    if not isinstance(shape, list):
        raise TypeError(
            "Shape not compliant with required type. Got {}".format(
                shape_spec
            ))

    if not all([x is None or x > 0 for x in shape]):
        raise ValueError("shape must be a list of positive or None values. "
                         "Got {}".format(shape))

    return shape


def format_docstring(docstring):
    lines = docstring.splitlines()

    out_lines = []
    for line in lines:
        out_lines.extend(textwrap.wrap(line.strip(), 60))

    out_lines = ['"""'] + out_lines + ['"""']
    return "\n".join(out_lines)
