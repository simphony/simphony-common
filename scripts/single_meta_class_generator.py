from __future__ import print_function

import re
import warnings
from collections import OrderedDict, MutableSequence
from itertools import chain

from scripts.utils import to_camel_case

# May be 'simphony.meta', we can make this as a command-line attribute
PATH_TO_CLASSES = ''

IMPORT_PATHS = {
    'CUBA': 'from simphony.core.cuba import CUBA',
    'DataContainer': 'from simphony.core.data_container import DataContainer',
    'create_data_container': 'from simphony.core.data_container import create_data_container',  # noqa
    'KEYWORDS': 'from simphony.core.keywords import KEYWORDS',
    'validation': 'from . import validation'
    }

# Excludes these keys in the `supported_parameters` property
# FIXME: These are excluded because they are not defined CUBA keys
EXCLUDE_SUPPORTED_PARAMETERS = ('definition', 'models', 'variables', 'data',)

# keywords that are excludes from DataContainers
CUBA_DATA_CONTAINER_EXCLUDE = ['Id', 'Position']


class SingleMetaClassGenerator(object):
    """ Generator for SimPhoNy Metadata classes

    On initialisation, the generator will identify which attributes
    are managed by the system etc. (i.e. `system_variables`,
    `required_user_defined`, `optional_user_defined`).

    Then, if the generated class should inherit from other generated
    classes, `collect_parents_to_mro`, `collect_attributes_from_parents`
    should be called, which populates the dictionaries containing
    inherited attributes (`inherited_required`, `inherited_optional`,
    `inherited_sys_vars`).

    Then, a number of `populate_` methods populate the code (`imports`,
    `init_boby`, `methods`).

    At last, the code is written to a file by a number of `generate_*`
    methods.

    For convenience, the `generate` method is included and it calls
    the `populate_*` and `generate_*` methods in the right order.

    Examples
    --------
    >>> gen = SingleMetaClassGenerator(key, class_data)

    >>> # if class should inherit other classes
    >>> # you should call `collect_parents_to_mro`
    >>> # and `collect_attributes_from_parents` here

    >>> with open('output.py', 'wb') as file_out:
            gen.generate(file_out)


    Attributes
    ----------
    original_key : str
        Name of the CUBA key

    class_data : dict
        All the meta data of the class

    system_variables: OrderedDict
        Attributes that are system-managed.
        key is the name of the attribute;
        value is a dictionary of metadata for the attributes

    required_user_defined: OrderedDict
        Attributes that required user's definition.
        key is the name of the attribute;
        value is a dictionary of metadata for the attributes

    optional_user_defined: OrderedDict
        Attributes that have default values.
        key is the name of the attribute;
        value is a dictionary of metadata

    parent : str
        Name of the superclass

    imports : list
        Lists of import statements

    init_body: list
        Lists of code in the `__init__` body

    methods: list
        Lists of code for the class's methods and descriptors

    inherited_required: dict
       Inherited attributes that require user's definition

    inherited_optional: dict
       Inherited attributes that have default values

    inherited_sys_vars: dict
       Inherited attributes that are managed by the system

    mro: list
        List of inherited parents' names

    mro_completed : boolean
        Whether the mro is completed
    """

    def __init__(self, key, class_data):
        """ Initialisation

        Parameters
        ----------
        key : str
            CUBA key, e.g. 'CUBA.CUDS_ITEM'

        class_data : dict
            meta data of the class, generally the result from
            the pyyaml parser.  Keys are the attributes of the
            generated class
        """
        # We keep a record of the original key
        self.original_key = key

        # We keep a record of the whole class data
        self.class_data = class_data

        # This collects import statements
        self.imports = [IMPORT_PATHS['CUBA']]

        # parent is for class inheritance so it is handled separately
        # self.parent = ""; class_data.pop("parent")    # for testing
        self.parent = class_data.pop('parent', None)

        if self.parent and not self.parent.startswith('CUBA.'):
            message = "'parent' should be either empty or a CUBA value, got {}"
            raise ValueError(message.format(self.parent))

        if self.parent:
            self.parent = self.parent.replace('CUBA.', '')

            self.imports.append("from {0}.{1} import {2}".format(
                PATH_TO_CLASSES, self.parent.lower(),
                to_camel_case(self.parent)))

        else:
            self.parent = "object"

        # This collects required __init__ arguments that are defined
        # by the corresponding metadata (not inherited)
        self.required_user_defined = OrderedDict()

        # This collects the required __init__ arguments that are
        # inherited
        self.inherited_required = OrderedDict()

        # This collects optional __init__ arguments (not inherited)
        # (i.e. with default values)
        self.optional_user_defined = OrderedDict()

        # This collects optional __init__ arguments that are inherited
        self.inherited_optional = OrderedDict()

        # Readonly variables managed by the system
        self.system_variables = {}

        # This collects inherited system-managed attributes
        self.inherited_sys_vars = {}

        # module-level variables after imports and before class definition
        self.module_variables = []

        # All code at the class levels
        self.class_variables = [""]

        # All statements within __init__
        self.init_body = [""]

        # All codes for methods
        self.methods = []

        # Method Resolution Order as defined by the simphony metadata
        # Note: assumed no multi-inheritance
        self.mro = []

        # Flag for whether the MRO is completed
        self.mro_completed = False

        for original_key, contents in class_data.items():
            key = original_key.lower().replace('cuba.', '')

            if is_system_managed(original_key, contents):
                self.system_variables[key] = contents

            elif isinstance(contents, dict) and 'default' in contents:
                self.optional_user_defined[key] = contents

            else:
                self.required_user_defined[key] = contents

    def generate(self, file_out):
        """ Populate and generate the code in the right order.

        Parameters
        ----------
        file_out : file object

        """
        # Populate codes before writing
        self._setup_user_variable_code()
        self._setup_system_code()
        self._setup_module_variables()
        self._setup_class_variables()
        self._setup_meta_api()

        # Now write to the file output
        self.generate_class_import(file_out)
        self.generate_module_variables(file_out)
        self.generate_class_header(file_out)
        self.generate_class_docstring(file_out)
        self.generate_class_attributes_docstring(file_out)
        self.generate_class_variables(file_out)
        self.generate_initializer(file_out)

        # methods (including descriptors)
        print(*self.methods, sep="\n", file=file_out)

    @property
    def all_non_inherited_attributes(self):
        """ All attributes that are not inherited """
        return (set(self.system_variables) |
                set(self.optional_user_defined) |
                set(self.required_user_defined))

    @property
    def all_attributes(self):
        """ All attributes, inherited and non-inherited """
        return (self.all_non_inherited_attributes |
                set(self.inherited_required) |
                set(self.inherited_optional) |
                set(self.inherited_sys_vars))

    @property
    def supported_parameters(self):
        """ Return a tuple of supported CUBA IntEnum
        """
        # We loop over `self.all_attributes` which include
        # inherited attributes.  These attributes are lower-case
        # without 'CUBA.' in front.  If they are in the yaml-file,
        # They are not CUBA attributes and therefore not supported
        # parameter
        def get_cuba_attribute():
            for attr in sorted(self.all_attributes):
                if attr not in EXCLUDE_SUPPORTED_PARAMETERS:
                    yield 'CUBA.'+attr.upper()

        return tuple(attr for attr in get_cuba_attribute())

    def _setup_system_code(self):
        """ Populate code for system-managed (and read-only) attributes"""

        for key, contents in chain(self.system_variables.items(),
                                   self.inherited_sys_vars.items()):
            # We first search for CodeGenerator.populate_`key`
            # If the method is defined, that is used and then move on
            if hasattr(self, 'populate_'+key):
                getattr(self, 'populate_'+key)(contents)
                continue

            # Populates self.methods with getter
            self._setup_getter(key)

            # For CUBA attributes that are read-only, `content`
            # should be a dict.
            if isinstance(contents, dict):
                default = contents.get('default')
            else:
                default = contents

            # We will defined private variable so that the system
            # can modify it but the user is not supposed to
            self.init_body.extend([
                '# This is a system-managed, read-only attribute',
                'self._{0} = {1}'.format(
                    key, transform_cuba_string(repr(default)))])

            # String default values maybe too long to fulfil PEP8
            if isinstance(default, str):
                self.init_body[-1] += '  # noqa'

    def _setup_module_variables(self):
        """ Populate module-level variables """
        pass

    def _setup_class_variables(self):
        """ Populate class variables

        These variables are requested by the user, but they are not
        directly specified in the yaml file
        """

        # Add cuba_key as a class variable
        self.class_variables.append(
            'cuba_key = CUBA.{}'.format(self.original_key))

    def _setup_meta_api(self):
        """ Populate API for interoperability """

        # Add a supported_parameters as a class method
        self.methods.append(
            transform_cuba_string('''
    @classmethod
    def supported_parameters(cls):
        return {!r}'''.format(self.supported_parameters)))

        # Add parents as a class method
        self.methods.append(
            transform_cuba_string('''
    @classmethod
    def parents(cls):
        return {!r}'''.format(tuple('CUBA.{}'.format(parent)
                                    for parent in self.mro))))

    def _setup_user_variable_code(self):
        """ Populate code for user-defined attributes """

        # populate them in reverse, because we want the root base class
        # attributes filled at the very end. This is to prevent
        # data to be overwritten by the defaults
        for key, contents in chain(
                reversed(list(chain(
                    self.inherited_required.items(),
                    self.required_user_defined.items()
                    ))
                ),
                reversed(list(chain(
                    self.inherited_optional.items(),
                    self.optional_user_defined.items()
                    )),
                )):
            if hasattr(self, 'populate_'+key):
                getattr(self, 'populate_'+key)(contents)
                continue

            try:
                default = contents['default']
            except (TypeError, KeyError):
                default = None

            if isinstance(default, str) and default.startswith('CUBA.'):
                # If default value is a CUBA key, it should be an instance
                # of the corresponding meta class
                self._setup_init_body_with_cuba_default(key,
                                                        contents['default'])
            elif isinstance(default, MutableSequence):
                # The __init__ signature will replace the default with None
                self.init_body.extend(('if {key} is None:'.format(key=key),
                                       '    self.{key} = {default!r}'.format(
                                           key=key,
                                           default=default)))
            else:
                # __init__ body
                self.init_body.append('self.{key} = {key}'.format(key=key))

            # The attributes is not inherited, we need to write the getter,
            # setter and the validation code
            if (key in self.optional_user_defined or
                    key in self.required_user_defined):
                # Getter
                self._setup_getter(key)

                # Setter
                self._setup_setter_with_validation(key, contents)

    def _setup_getter(self, key, value=None, docstring=''):
        """ Populate getter descriptor

        Parameters
        ----------
        key : str
            name of the attribute

        value : object
            fixed return value of the getter

        docstring : str
            Documentation for the getter
        """
        # default property getter
        if value is None:
            # Where is the value stored
            # If the key is a CUBA key, store it in the DataContainer
            cuba_key = 'CUBA.'+key.upper()
            if cuba_key in self.class_data:
                value = 'self.data[{cuba_key}]'.format(cuba_key=cuba_key)
            else:
                value = 'self._{key}'.format(key=key)

        if docstring:
            docstring = "'''{}'''".format(docstring)

            self.methods.append('''
    @property
    def {key}(self):
        {docstring}
        return {value}'''.format(key=key, value=value,
                                 docstring=docstring))
        else:
            self.methods.append('''
    @property
    def {key}(self):
        return {value}'''.format(key=key, value=value))

    def _setup_setter(self, key, check_statements=()):
        """ Populate setter descriptor

        Parameters
        ----------
        key : str
            name of the attribute

        check_statements : sequence
            sequence of strings (code)
        """
        # Get the indentation right
        validation_code = '''
        '''.join(check_statements)

        # Where to store the value
        # If the key is a CUBA key, store it in the DataContainer
        cuba_key = 'CUBA.'+key.upper()
        if cuba_key in self.class_data:
            self.methods.append('''
    @{key}.setter
    def {key}(self, value):
        {validation_code}
        data = self.data
        data[{cuba_key}] = value
        self.data = data'''.format(key=key,
                                   cuba_key=cuba_key,
                                   validation_code=validation_code))
        else:
            target = 'self._{key}'.format(key=key)

            # default property setter
            self.methods.append('''
    @{key}.setter
    def {key}(self, value):
        {validation_code}
        {target} = value'''.format(key=key, target=target,
                                   validation_code=validation_code))

    def _setup_setter_with_validation(self, key, contents):
        """ Populate setter descriptor with validation codes

        Parameters
        ----------
        key : str
            name of the attribute

        contents : dict
            metadata of the attribute
        """
        self.imports.append(IMPORT_PATHS['validation'])

        # Validation code for the setter
        check_statements = [
            'value = validation.cast_data_type(value, {!r})'.format(key)]

        # Is `shape` defined that we need to check shape?
        check_shape = isinstance(contents, dict) and "shape" in contents

        if check_shape:
            # If `shape` is defined, the value is supposed to be a sequence
            # We check the shape of the sequence
            statement = "validation.check_shape(value, {!r})"
            check_statements.append(statement.format(contents['shape']))

        # is key defined as CUBA.* in the meta data?
        is_cuba_key = 'CUBA.'+key.upper() in self.class_data

        # If the key is also a CUBA key and `shape` is defined
        # we should check each element in the sequence
        if is_cuba_key:
            if check_shape:
                check_statements.extend([
                    'for item in value:',
                    ('    validation.validate_cuba_keyword('
                     'item, {!r})').format(key)])
            else:
                statement = ('validation.validate_cuba_keyword('
                             'value, {!r})').format(key)
                check_statements.append(statement)
        else:
            # Warn the user/developer that an attribute is not identified
            # as a CUBA keyword in the meta data (even if it is in cuba.yml)
            warnings.warn('{key} is not described as a CUBA.{upper} '
                          'in the meta data of {name}.  It will not be '
                          'validated against the CUBA keyword and it will '
                          'not be stored in the DataContainer'.format(
                              key=key, upper=key.upper(),
                              name=self.original_key))

        # Allow None?
        allow_none = (isinstance(contents, dict) and
                      contents.get('default') is None)

        if allow_none:
            check_statements.insert(0, 'if value is not None:')
            # add indentation
            check_statements[1:] = ('    '+statement
                                    for statement in check_statements[1:])

        # Populate setter
        self._setup_setter(key, check_statements)

    def _setup_init_body_with_cuba_default(self, key, default):
        """  Populate the body of `__init__` for an attribute

        Parameters
        ----------
        key : str
            name of the attribute

        default : object
            default value of the attribute.  If it is a string that
            starts with "CUBA.", the default value is understood
            as a metadata class and an instance of that class
            would be created on initialisation.  The corresponding
            import statement would be added.
        """
        default_key = default.lower().replace('cuba.', '')
        class_name = to_camel_case(default_key)
        # __init__ body
        self.init_body.append('''
        if {key}:
            self.{key} = {key}
        else:
            self.{key} = {class_name}()'''.format(key=key,
                                                  class_name=class_name))

        self.imports.append("from {0}.{1} import {2}".format(
            PATH_TO_CLASSES, default_key,
            to_camel_case(default_key)))

    # Populate methods: they handle special cases for some datatypes
    # that require non-boilerplate setup.
    def populate_uuid(self, contents):
        """Populate code for CUBA.UUID

        Parameters
        ----------
        contents : dict
            meta data of the uuid (not currently used)
        """
        self.imports.append("import uuid")

        self.methods.append('''
    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid''')

    def populate_data(self, contents):
        """Sets up the internal self.data which is the DataContainer
        storage for all non-system variables.
        """

        self.imports.append(IMPORT_PATHS['DataContainer'])

        # Put it in front because other data depend on it.
        self.init_body.insert(0, '''
        self._data = DataContainer()
        ''')

        self.methods.append('''
    @property
    def data(self):
        return self._data
        ''')

        self.methods.append('''
    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)
        ''')

    # End populate methods

    def collect_parents_to_mro(self, generators):
        """ Recursively collect all the inherited into CodeGenerator.mro
        Assume single inheritence, i.e. no multiple parents

        Parameters
        ----------
        generators : dict
            keys are the names of classes (all upper case)
            values are the cooresponding CodeGenerator objects
        """
        # If its mro is already completed, return
        if self.mro_completed:
            return

        if self.parent == 'object':
            self.mro_completed = True
            return

        # Collect all the grandparents
        parent_generator = generators[self.parent]

        # Populate MRO
        parent_generator.collect_parents_to_mro(generators)
        self.mro.append(parent_generator.original_key)
        self.mro.extend(parent_generator.mro)

        # Mark MRO as completed
        self.mro_completed = True

    def collect_attributes_from_parents(self, generators):
        """ Given the MRO is populated, collect all the
        attributes inherited from the parents and thus populate
        `inherited_required`, `inherited_optional` and `inherited_sys_vars`

        Parameters
        ----------
        generators : dict
            keys are the names of classes (all upper case)
            values are the cooresponding CodeGenerator objects

        See Also
        --------
        collect_parents_to_mro
        """
        if not self.mro_completed:
            raise RuntimeError(
                'MRO is not yet populated for {}.'.format(self.original_key))

        if not self.mro:
            return

        # Populate inherited_required and inherited_optional
        # with the ones from parents.  Make sure only add the ones
        # that are not known to the chile already
        # MRO's order goes from the closest parent
        mappings = {'inherited_required': 'required_user_defined',
                    'inherited_optional': 'optional_user_defined',
                    'inherited_sys_vars': 'system_variables'}

        for parent_name in reversed(self.mro):
            parent = generators[parent_name]

            # Update the known attribute
            known_attributes = self.all_attributes

            # populate self.to_save[key] with parent.to_get[key]
            for to_save, to_get in mappings.items():
                new_attrs = set(getattr(parent, to_get)) - known_attributes

                for key in new_attrs:
                    getattr(self, to_save)[key] = getattr(parent, to_get)[key]

    def generate_class_import(self, file_out):
        """ Print import statements to the file output

        Parameters
        ----------
        file_out : file object
        """
        # import statements
        print(*sorted(set(self.imports), reverse=True),
              sep="\n", file=file_out)

    def generate_module_variables(self, file_out):
        """ Print module-level variables to the file output

        Parameters
        ----------
        file_out : file object
        """
        if self.module_variables and len(self.module_variables) > 0:
            print("", file=file_out)
            print(*self.module_variables,
                  sep="\n", file=file_out)

    def generate_class_header(self, file_out):
        """ Print class definition to the file output

        Parameters
        ----------
        file_out : file object
        """
        # class header
        if self.parent != 'object':
            parent_class_name = to_camel_case(self.parent)
        else:
            parent_class_name = self.parent

        print('\n\nclass {name}({parent}):'.format(
            name=to_camel_case(self.original_key), parent=parent_class_name),
              file=file_out)

    def generate_class_docstring(self, file_out):
        """ Generates the description block of the generated class.

        This block does not include individual attribute documentation

        Parameters
        ----------
        file_out : File object
        """

        definition = self.class_data.get('definition', 'Missing definition')

        print('''
    \'\'\'{DOC_DESCRIPTION}  # noqa
    \'\'\''''.format(DOC_DESCRIPTION=definition), file=file_out)

    def generate_class_attributes_docstring(self, file_out):
        """ Generates the description block of the generated class.

        This block does not include individual attribute documentation

        Parameters
        ----------
        file_out : File object
        """
        # Not yet implemented
        pass

    def generate_class_variables(self, file_out):
        """ Print class-level variables

        Parameters
        ----------
        file_out : file object
        """
        # class-level variables
        print(*self.class_variables,
              sep="\n    ", file=file_out)

    def generate_initializer(self, file_out):
        """ Generate the entire __init__ method of the generated class.

        Parameters
        ----------
        file_out : File object
        """
        # __init__ keyword arguments
        kwargs = []
        for key, content in chain(
                self.inherited_optional.items(),
                self.optional_user_defined.items(),
        ):
            # Since it is optional, it must have a default entry
            # However if the default value is a CUBA key,
            # we set it to None in the init
            default = content['default']
            if isinstance(default, str):
                if default.startswith('CUBA.'):
                    kwargs.append('{key}=None'.format(key=key))
                else:
                    kwargs.append('{key}=\"{value}\"'.format(
                        key=key, value=default))
            elif isinstance(default, MutableSequence):
                # Should not use mutable in the signature
                kwargs.append('{key}=None'.format(key=key))
            else:
                kwargs.append('{key}={value}'.format(key=key, value=default))

        # __init__ signature
        signature = ["self"]
        signature.extend(self.inherited_required.keys())
        signature.extend(self.required_user_defined.keys())
        signature.extend(kwargs)

        # Print __init__ definition and signature
        print('''
    def __init__({signature}):'''.format(signature=", ".join(signature)),
              file=file_out)

        # __init__ body
        if self.init_body == [""]:
            self.init_body.append("pass")

        print(*self.init_body, sep="\n        ", file=file_out)


def transform_cuba_string(code):
    """ Tranform any \'CUBA.SOMETHING\' in a string to CUBA.SOMETHING

    Parameters
    ----------
    code : str

    Returns
    -------
    transformed_code : str
       with any \'CUBA.SOMETHING\' converted to CUBA.SOMETHING
    """
    return re.sub('\'(CUBA.\w+)\'', lambda x: x.group(0).strip("'"), code)


def is_system_managed(key, contents):
    """ Return True is `key` is a system-managed attribute

    Criteria:
    (1) the key does not start with "CUBA." OR
    (2) contents['scope'] is CUBA.SYSTEM

    Parameters
    ----------
    key : str
    """
    if isinstance(contents, dict):
        if contents.get('scope') == 'CUBA.SYSTEM':
            return True
        if contents.get('scope') == 'CUBA.USER':
            return False

    if not key.upper().startswith('CUBA.'):
        return True

    return False
