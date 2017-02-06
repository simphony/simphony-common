import abc
import textwrap

from simphony_metaparser.flags import NoDefault

from simphony_metaparser.utils import with_cuba_prefix, \
    cuba_key_to_property_name, without_cuba_prefix

from . import utils


class File(object):
    def __init__(self):
        self.imports = set()
        self.classes = []
        self.methods = []

    def render(self, out, indent_level=0):
        imports = set(self.imports)
        for cls in self.classes:
            for imp in cls.import_required():
                imports.add(imp)

        for imp in imports:
            imp.render(out, indent_level)

        for cls in self.classes:
            cls.render(out, indent_level)

        for meth in self.methods:
            meth.render(out, indent_level)


class ShortcutImport(object):
    IMPORT_PATHS = {
        'CUBA': 'from simphony.core.cuba import CUBA',
        'DataContainer': 'from simphony.core.data_container import DataContainer',  # noqa
        'create_data_container': 'from simphony.core.data_container import create_data_container',  # noqa
        'KEYWORDS': 'from simphony.core.keywords import KEYWORDS',
        'validation': 'from . import validation',
        'uuid': 'import uuid',
        'Default': 'from simphony.core import Default  # noqa'
    }

    def __init__(self, module_shortcut):
        self.module_shortcut = module_shortcut

    def render(self, out, indent_level=0):
        out.write(
            utils.indent(
                self._render_import(),
                indent_level
            )+'\n'
        )

    def _render_import(self):
        return self.IMPORT_PATHS[self.module_shortcut]

    def __hash__(self):
        return hash(self._render_import())

    def __eq__(self, other):
        return hash(other) == hash(self)


class MetaClassImport(object):
    def __init__(self, meta_class_name):
        self.meta_class_name = meta_class_name

    def render(self, out, indent_level=0):
        out.write(
            utils.indent(
                self._render_import(),
                indent_level
            ) + '\n'
        )

    def _render_import(self):
        return "from .{meta_class_module_name} import {meta_class_name}".format(  # noqa
                    meta_class_module_name=utils.meta_class_name_to_module_name(  # noqa
                        self.meta_class_name
                    ),
                    meta_class_name=self.meta_class_name
                )

    def __hash__(self):
        return hash(self._render_import())

    def __eq__(self, other):
        return hash(other) == hash(self)


class Class(object):
    def __init__(self,
                 class_name,
                 cuba_key,
                 parent_class_name,
                 hierarchy_properties,
                 docstring=""):

        self.class_name = class_name
        self.cuba_key = cuba_key
        self.parent_class_name = parent_class_name
        self.hierarchy_properties = hierarchy_properties
        self.docstring = docstring
        self.methods = []
        self.properties = []

    def import_required(self):
        required = [ShortcutImport("Default")]
        if self.parent_class_name is not None:
            required += [
                MetaClassImport(self.parent_class_name)
            ]

        return required + sum(
            (prop.import_required() for prop in self.properties),
            [])

    def render(self, out, indent_level=0):
        parent_class_name = (self.parent_class_name
                             if self.parent_class_name is not None
                             else "object")

        s = "class {class_name}({parent_class_name}):\n".format(
            class_name=self.class_name,
            parent_class_name=parent_class_name,
        )
        s += utils.indent(utils.format_docstring(self.docstring))+'\n'
        s += utils.indent("cuba_key = {qualified_cuba_key}\n".format(
            qualified_cuba_key=with_cuba_prefix(self.cuba_key)))

        out.write(utils.indent(s, indent_level))

        out.write(utils.indent(self._render_init_method(),
                               indent_level+1))
        out.write(utils.indent(self._render_supported_parameters(),
                               indent_level+1))

        for method in self.methods:
            method.render(out, indent_level=indent_level+1)

        for prop in self.properties:
            prop.render(out, indent_level=indent_level+1)

    def _render_init_method(self):

        # We have various types of properties.
        # with/without default = optional/mandatory
        # reimplemented/not reimplemented.
        # We need to take care of the combinations
        # so that the init is well behaved

        mandatory, optional, pass_down = self._compute_init_args_info()
        init_args = []
        super_init_args = []

        for arg in mandatory:
            init_args.append("{}".format(arg))

        for arg in optional:
            init_args.append("{}=Default".format(arg))

        for arg in pass_down:
            super_init_args.append("{}={}".format(arg, arg))

        s = textwrap.dedent("""def __init__({init_args_str}):""".format(
            init_args_str=", ".join(init_args))+'\n'
        )

        s += utils.indent(textwrap.dedent("""super({class_name}, self).__init__({super_init_args_str})""".format(  # noqa
                class_name=self.class_name,
                super_init_args_str=", ".join(super_init_args))
        ))+'\n'

        for prop in self.properties:
            if prop.reimplemented:
                continue

            if isinstance(prop, VariableProperty):
                s += utils.indent(
                    textwrap.dedent(
                        """self._init_{prop_name}({prop_name})""".format(  # noqa
                            prop_name=prop.name)))+'\n'
            else:
                s += utils.indent(
                    textwrap.dedent(
                        """self._init_{prop_name}()""".format(
                            prop_name=prop.name)))+'\n'

        return s

    def _compute_init_args_info(self):
        hierarchy_mandatory = []
        hierarchy_optional = []
        pass_down = []

        for prop_group in self.hierarchy_properties:
            for prop in sorted(
                    [p for p in prop_group if isinstance(p, VariableProperty)],
                    key=lambda x: x.name):
                if (prop.name in hierarchy_mandatory or
                        prop.name in hierarchy_optional):
                    continue

                if prop.default is NoDefault:
                    hierarchy_mandatory.append(prop.name)
                else:
                    hierarchy_optional.append(prop.name)

                pass_down.append(prop.name)

        cur_class_mandatory = []
        cur_class_optional = []
        for prop in sorted(
                [p for p in self.properties
                 if isinstance(p, VariableProperty)],
                key=lambda x: x.name):
            if (prop.name in hierarchy_mandatory and
                    prop.default is not NoDefault):
                # A property that was mandatory now has a default.
                hierarchy_mandatory.remove(prop.name)
                cur_class_optional.append(prop.name)

            elif (prop.name in hierarchy_optional and
                  prop.default is NoDefault):
                # A property that was optional has been reimplemented
                # without default
                hierarchy_optional.remove(prop.name)
                cur_class_mandatory.append(prop.name)
            else:
                if prop.default is NoDefault:
                    cur_class_mandatory.append(prop.name)
                else:
                    cur_class_optional.append(prop.name)

        return (['self'] +
                utils.deduplicate(cur_class_mandatory + hierarchy_mandatory),
                utils.deduplicate(cur_class_optional + hierarchy_optional),
                utils.deduplicate(pass_down))

    def _render_supported_parameters(self):
        params = []
        for prop in self.properties:
            if isinstance(prop, VariableProperty):
                params.append(prop.source_key)
            elif isinstance(prop, UIDProperty):
                params.append("CUBA.UID")

        s = textwrap.dedent("""
            @classmethod
            def supported_parameters(cls):
                try:
                    base_params = super(
                        {class_name},
                        cls).supported_parameters()
                except AttributeError:
                    base_params = ()
                return tuple(set(({params}) + base_params))
                """.format(
                    class_name=self.class_name,
                    params="".join([p+", " for p in params]))
        )

        return s


class MetaAPIMethods(object):
    """These methods go only in the base class (whose parent is empty)"""
    def render(self, out, indent_level=0):
        out.write(
            utils.indent(textwrap.dedent(
                """
                @classmethod
                def parents(cls):
                    return tuple(
                        c.cuba_key
                        for c in cls.__mro__[1:]
                        if hasattr(c, "cuba_key"))
                """),
                indent_level)
        )


class ABCProperty(object):
    """Describes a template for a generic python property.
    It's an abstract class. Derived classes must reimplement the
    appropriate methods for rendering"""
    __metaclass__ = abc.ABCMeta

    def __init__(self, name, default=NoDefault, docstring=""):
        self.name = name
        self.default = default
        self.docstring = docstring

    @abc.abstractmethod
    def import_required(self):
        """Must return the import required to make the property work,
        as a list of ShortcutImport or MetaClassImport"""

    @abc.abstractmethod
    def _render_init(self):
        """Renders the initialization routine. This is called
        by the class __init__ method.
        Must return a string containing the rendered data."""

    @abc.abstractmethod
    def _render_setter(self):
        """Renders the setter method.
        Must return a string containing the rendered data."""

    @abc.abstractmethod
    def _render_getter(self):
        """Renders the getter method.
        Must return a string containing the rendered data.
        """

    @abc.abstractmethod
    def _render_validation(self):
        """Renders the validation method.
        Must return a string containing the rendered data.
        """

    @abc.abstractmethod
    def _render_default(self):
        """Renders a routine that returns the appropriate default.
        Must return a string containing the rendered data.
        """
        pass

    def render(self, out, indent_level=0):
        """Triggers the rendering

        out: file-like
            Where to write the rendering

        indent_level: int
            used to indent the rendering of a given level amount.
        """
        s = self._render_init()
        s += self._render_getter()
        s += self._render_setter()
        s += self._render_validation()
        s += self._render_default()

        out.write(utils.indent(s, indent_level))


class FixedProperty(ABCProperty):
    """Describes a fixed property template."""

    def __init__(self, source_key, default, reimplemented):
        """Defines a fixed property"""
        super(FixedProperty, self).__init__(source_key, default)

        # This is the original name as it comes from the ontology tree.
        # the template "property name" is the actual name that goes in the
        # python code.
        self.source_key = source_key

        # True if the property is reimplemented on the base class, hence
        # its rendering must keep this into account for appropriate
        # initialization
        self.reimplemented = reimplemented

    def _render_init(self):
        if self.reimplemented:
            return ""
        return textwrap.dedent("""
        def _init_{name}(self):
            self._{name} = self._default_{name}()  # noqa
            """).format(
            name=self.name)

    def _render_default(self):
        return textwrap.dedent("""
        def _default_{name}(self):
            return {default}  # noqa
        """).format(name=self.name,
                    default=utils.quoted_if_string(self.default))

    def _render_setter(self):
        return ""

    def _render_validation(self):
        return ""

    def _render_getter(self):
        if self.reimplemented:
            return ""
        return textwrap.dedent("""
            @property
            def {name}(self):
                return self._{name}
        """).format(name=self.name)

    def import_required(self):
        imp = []
        return imp


class VariableProperty(ABCProperty):
    """Describes a variable (CUBA) property template."""

    def import_required(self):
        imp = [ShortcutImport("Default")]
        imp += [ShortcutImport("validation")]

        if utils.is_cuba_key(self.default):
            imp.append(
                MetaClassImport(
                    meta_class_name=utils.cuba_key_to_meta_class_name(
                        self.default)
                )
            )
        elif isinstance(self.default, (list, tuple)):
            default = '{}'.format(self.default)
            if 'CUBA.' in default:
                for elem in self.default:
                    if utils.is_cuba_key(elem):
                        imp.append(
                            MetaClassImport(
                                meta_class_name=utils.cuba_key_to_meta_class_name(elem)))  # noqa

        return imp

    def __init__(self, qual_cuba_key, default, shape, reimplemented):
        if shape is None:
            raise ValueError("shape cannot be None")

        self.source_key = qual_cuba_key
        prop_name = cuba_key_to_property_name(qual_cuba_key)
        super(VariableProperty, self).__init__(
            name=prop_name,
            default=default)
        self.shape = shape
        self.reimplemented = reimplemented

    def _render_init(self):
        return textwrap.dedent("""
        def _init_{name}(self, value):
            if value is Default:
                value = self._default_{name}()

            self.{name} = value
        """).format(name=self.name)

    def _render_setter(self):
        return textwrap.dedent("""
            @{prop_name}.setter
            def {prop_name}(self, value):
                value = self._validate_{prop_name}(value)
                self.data[{qual_cuba_key}] = value
        """).format(
            prop_name=self.name,
            qual_cuba_key=self.source_key)

    def _render_getter(self):
        return textwrap.dedent("""
            @property
            def {prop_name}(self):
                return self.data[{qual_cuba_key}]
        """).format(
            prop_name=self.name,
            qual_cuba_key=self.source_key)

    def _render_validation(self):
        cuba_key = without_cuba_prefix(self.source_key)
        if self.shape == [1]:
            return textwrap.dedent("""
            def _validate_{prop_name}(self, value):
                value = validation.cast_data_type(value, '{cuba_key}')
                validation.check_valid_shape(value, {shape}, '{cuba_key}')
                validation.validate_cuba_keyword(value, '{cuba_key}')
                return value
            """.format(prop_name=self.name,
                       cuba_key=cuba_key,
                       shape=self.shape))
        else:
            return textwrap.dedent("""
            def _validate_{prop_name}(self, value):
                value = validation.cast_data_type(value, '{cuba_key}')
                validation.check_valid_shape(value, {shape}, '{cuba_key}')
                validation.check_elements(value, {shape}, '{cuba_key}')

                return value
            """.format(prop_name=self.name,
                       cuba_key=cuba_key,
                       shape=self.shape))

    def _render_default(self):
        if self.default == NoDefault:
            return textwrap.dedent("""
            def _default_{name}(self):
                raise TypeError("No default for {name}")
            """).format(name=self.name)

        if utils.is_cuba_key(self.default):
            default = utils.cuba_key_to_instantiation(self.default)
        elif isinstance(self.default, (list, tuple)):
            default = '{}'.format(self.default)
            if 'CUBA.' in default:
                elements = []
                for elem in self.default:
                    if utils.is_cuba_key(elem):
                        elem = utils.cuba_key_to_instantiation(elem)
                    elements.append(elem)

                default = '[' + ", ".join(elements) + ']'
        else:
            default = utils.quoted_if_string(self.default)

        return textwrap.dedent("""
        def _default_{name}(self):
            return {default}
        """).format(name=self.name,
                    default=default)


class DataProperty(FixedProperty):
    """Special data property is handled slightly different.
    It is a fixed property, but the value does not come from
    a hardcoded value in its default."""
    def __init__(self):
        super(DataProperty, self).__init__("data", None, False)
        self.source_key = "data"

    def import_required(self):
        return [ShortcutImport("DataContainer")]

    def _render_getter(self):
        return textwrap.dedent("""
            @property
            def data(self):
                return self._data
        """)

    def _render_setter(self):
        return textwrap.dedent("""
            @data.setter
            def data(self, new_data):
                self._data = DataContainer(new_data)
        """)

    def _render_init(self):
        return textwrap.dedent("""
            def _init_data(self):
                self._data = DataContainer()
        """)

    def _render_validation(self):
        return ""

    def _render_default(self):
        return ""


class UIDProperty(FixedProperty):
    """Special property that handles the special case of CUBA.UID.
    It behaves like a fixed property, but it has a CUBA qualified key.
    """
    def __init__(self):
        super(UIDProperty, self).__init__("uid", None, False)
        self.source_key = "uid"

    def import_required(self):
        return [ShortcutImport('uuid')]

    def _render_init(self):
        return textwrap.dedent("""
            def _init_uid(self):
                self.data[CUBA.UID] = uuid.uuid4()
        """)

    def _render_getter(self):
        return textwrap.dedent("""
            @property
            def uid(self):
                return self.data[CUBA.UID]
        """)

    def _render_setter(self):
        return ""

    def _render_validation(self):
        return ""

    def _render_default(self):
        return ""
