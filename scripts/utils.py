import re
import shutil
import tempfile
import textwrap

from contextlib import contextmanager


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
    if string.startswith("CUBA."):
        return string

    return "CUBA." + string


def without_cuba_prefix(string):
    """Removes the CUBA. prefix to the string if there."""
    if string.startswith("CUBA."):
        return string[5:]

    return string


def cuba_key_to_meta_class_name(string):
    return to_camel_case(without_cuba_prefix(string))


def cuba_key_to_meta_class_module_name(string):
    return without_cuba_prefix(string).lower()


def meta_class_name_to_module_name(string):
    def replace_func(matched):
        word = matched.group(0).strip("_")
        res = "_"+word.lower()
        return res

    return re.sub(r'([A-Z]+)', replace_func, string).lstrip("_")
