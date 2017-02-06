import re
import shutil
import tempfile
import textwrap
from collections import OrderedDict

from contextlib import contextmanager

from simphony_metaparser.utils import without_cuba_prefix


@contextmanager
def make_temporary_directory():
    """Context Manager for creating a temporary directory
    and remove the tree on exit

    Yields
    ------
    temp_dir : str
        absolute path to temporary directory
    """
    temp_dir = None
    try:
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
    finally:
        if temp_dir is not None:
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

    out_lines = []
    for src_line in dedent_text.splitlines(True):
        if len(src_line.strip()) == 0:
            out_lines.append('\n')
        else:
            out_lines.append(spaces + src_line)

    return "".join(out_lines)


def is_cuba_key(value):
    """True if value is a qualified cuba key"""
    return isinstance(value, (str, unicode)) and value.startswith("CUBA.")


def cuba_key_to_meta_class_name(string):
    """Converts a cuba key in the associated class name."""
    return to_camel_case(without_cuba_prefix(string))


def cuba_key_to_meta_class_module_name(string):
    """Converts a cuba key in the associated python module name"""
    return without_cuba_prefix(string).lower()


def meta_class_name_to_module_name(string, special={"CUDS": "Cuds"}):
    """Converts a class name to an appropriate module name"""
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
    """Parses the shape as specified in the yaml file.
    Note that the colon notation e.g. (3, :) maps to a None e.g. (3, None).

    If shape is None, it will return the default [1].
    """
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
    """Formats a docstring appropriately"""
    lines = docstring.splitlines()

    out_lines = []
    for line in lines:
        out_lines.extend(textwrap.wrap(line.strip(), 60))

    out_lines = ['"""'] + out_lines + ['"""']
    return "\n".join(out_lines)


def deduplicate(list_):
    """Removes duplicates from a list, even when not contiguous.
    Returns a list without duplicates. Only the leftmost element stays."""
    o = OrderedDict()
    for l in list_:
        o[l] = l
    return o.keys()


def cuba_key_to_instantiation(cuba_key):
    """Given a cuba key, creates an "instantiation string" for the associated
    class."""
    if is_cuba_key(cuba_key):
        return "{cuba_meta_class_name}()".format(
            cuba_meta_class_name=cuba_key_to_meta_class_name(cuba_key)
        )
    else:
        raise ValueError("{} is not a cuba_key".format(cuba_key))
