import abc
import textwrap

from scripts.utils import NoDefault
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
        'Default': 'from simphony.core import Default'
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
                 docstring=""):
        self.class_name = class_name
        self.cuba_key = cuba_key
        self.parent_class_name = parent_class_name
        self.docstring = docstring
        self.methods = []
        self.properties = []

    def import_required(self):
        required = []
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
        s += utils.indent("cuba_key = {qualified_cuba_key}".format(
            qualified_cuba_key=utils.with_cuba_prefix(self.cuba_key)))+'\n'

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

        mandatory_properties = []
        optional_properties = []
        reimplemented_properties = []
        for prop in [p for p in self.properties
                     if isinstance(p, VariableProperty)]:

            if prop.default is NoDefault:
                mandatory_properties.append(prop.name)
            else:
                optional_properties.append(prop.name)

            if prop.reimplemented:
                reimplemented_properties.append(prop.name)

        init_args = ['self']
        init_args.extend(["{}".format(arg)
                          for arg in mandatory_properties])
        init_args.extend(["{}=Default".format(arg)
                          for arg in optional_properties])
        init_args.extend(['*args', '**kwargs'])

        # Those we have to pass to the super()
        super_init_args = []
        super_init_args.extend(["{}".format(arg)
                                for arg in reimplemented_properties])
        super_init_args.extend(['*args', '**kwargs'])

        s = textwrap.dedent("""
            def __init__({init_args_str}):
            """.format(
            init_args_str=", ".join(init_args))
        )

        s += utils.indent(textwrap.dedent("""
                super({class_name}, self).__init__({super_init_args_str})
            """.format(
                class_name=self.class_name,
                super_init_args_str=", ".join(super_init_args))
        ))

        for prop in self.properties:
            if prop.reimplemented:
                continue

            if isinstance(prop, VariableProperty):
                s += utils.indent(
                    textwrap.dedent("""
                    self._init_{prop_name}({prop_name})
                    """.format(prop_name=prop.name)))
            else:
                s += utils.indent(
                    textwrap.dedent("""
                    self._init_{prop_name}()
                    """.format(prop_name=prop.name)))

        return s

    def _render_supported_parameters(self):
        params = []
        for prop in self.properties:
            if isinstance(prop, VariableProperty):
                params.append(prop.qual_cuba_key)
            elif isinstance(prop, UUIDProperty):
                params.append("CUBA.UUID")

        s = textwrap.dedent("""
            def supported_parameters(self):
                try:
                    base_params = super(
                        {class_name},
                        self).supported_parameters()
                except AttributeError:
                    base_params = ()

                return ({params}) + base_params
            """.format(class_name=self.class_name,
                       params="".join([p+", " for p in params]))
        )

        return s


class MetaAPIMethods(object):
    """These methods go only in the base class (whose parent is empty)"""
    def render(self, out, indent_level=0):
        out.write(
            utils.indent(
                """
                @classmethod
                def parents(cls):
                    return tuple(
                        c.cuba_key
                        for c in cls.__mro__[1:]
                        if hasattr(c, "cuba_key"))
                """,
                indent_level)
        )


class ABCProperty(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def import_required(self):
        pass

    @abc.abstractmethod
    def _render_init(self):
        pass

    @abc.abstractmethod
    def _render_setter(self):
        pass

    @abc.abstractmethod
    def _render_getter(self):
        pass

    @abc.abstractmethod
    def _render_validation(self):
        pass

    @abc.abstractmethod
    def _render_default(self):
        pass

    def render(self, out, indent_level=0):
        s = self._render_init()
        s += self._render_getter()
        s += self._render_setter()
        s += self._render_validation()
        s += self._render_default()
        s += '\n'

        out.write(utils.indent(s, indent_level))


class Property(ABCProperty):
    def __init__(self, name, default=utils.NoDefault, docstring=""):
        super(Property, self).__init__(name)
        self.default = default
        self.docstring = docstring

    def import_required(self):
        imp = [ShortcutImport("Default")]

        return imp

    def _render_setter(self):
        return textwrap.dedent("""
            @{name}.setter
            def {name}(self, value):
                \"\"\"
                {docstring}
                \"\"\"
                value = self._validate_{name}(value)
                self._{name} = value
        """).format(name=self.name,
                    docstring=self.docstring)

    def _render_getter(self):
        return textwrap.dedent("""
            @property
            def {name}(self):
                return self._{name}
        """).format(name=self.name)

    def _render_init(self):
        return textwrap.dedent("""
        def _init_{name}(self, value):
            if value is Default:
                value = self._default_{name}()

            self.{name} = value
        """).format(name=self.name)

    def _render_validation(self):
        return textwrap.dedent("""
        def _validate_{name}(value):
            return value
        """).format(name=self.name)

    def _render_default(self):
        if self.default == utils.NoDefault:
            return textwrap.dedent("""
            def _default_{name}(self):
                raise TypeError("No default for {name}")
            """).format(name=self.name)

        if utils.is_cuba_key(self.default):
            default = "{cuba_meta_class_name}()".format(
                cuba_meta_class_name=utils.cuba_key_to_meta_class_name(
                    self.default
                )
            )
        else:
            default = utils.quoted_if_string(self.default)

        return textwrap.dedent("""
        def _default_{name}(self):
            return {default}
        """).format(name=self.name,
                    default=default)


class FixedProperty(Property):
    def __init__(self, name, default, reimplemented):
        super(FixedProperty, self).__init__(name, default)

        self.reimplemented = reimplemented

    def _render_init(self):
        if self.reimplemented:
            return ""
        return textwrap.dedent("""
        def _init_{name}(self):
            self._{name} = self._default_{name}()  # noqa
        """).format(name=self.name)

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
        return super(FixedProperty, self)._render_getter()

    def import_required(self):
        imp = []
        return imp


class VariableProperty(Property):
    def import_required(self):
        imp = super(VariableProperty, self).import_required()
        imp += [ShortcutImport("validation")]

        if utils.is_cuba_key(self.default):
            imp.append(
                MetaClassImport(
                    meta_class_name=utils.cuba_key_to_meta_class_name(
                        self.default)
                )
            )
        return imp

    def __init__(self, qual_cuba_key, default, shape, reimplemented):
        if shape is None:
            raise ValueError("shape cannot be None")

        prop_name = utils.cuba_key_to_property_name(qual_cuba_key)
        super(VariableProperty, self).__init__(
            name=prop_name,
            default=default)
        self.qual_cuba_key = qual_cuba_key
        self.shape = shape
        self.reimplemented = reimplemented

    def _render_setter(self):
        return textwrap.dedent("""
            @{prop_name}.setter
            def {prop_name}(self, value):
                value = self._validate_{prop_name}(value)
                self.data[{qual_cuba_key}] = value
        """).format(
            prop_name=self.name,
            qual_cuba_key=self.qual_cuba_key)

    def _render_getter(self):
        return textwrap.dedent("""
            @property
            def {prop_name}(self):
                return self.data[{qual_cuba_key}]
        """).format(
            prop_name=self.name,
            qual_cuba_key=self.qual_cuba_key)

    def _render_validation(self):
        cuba_key = utils.without_cuba_prefix(self.qual_cuba_key)
        if self.shape == [1]:
            return textwrap.dedent("""
            def _validate_{prop_name}(self, value):
                value = validation.cast_data_type(value, '{cuba_key}')
                validation.check_shape(value, {shape})
                validation.validate_cuba_keyword(value, '{cuba_key}')
                return value
            """.format(prop_name=self.name,
                       cuba_key=cuba_key,
                       shape=self.shape))
        else:
            return textwrap.dedent("""
            def _validate_{prop_name}(self, value):
                value = validation.cast_data_type(value, '{cuba_key}')
                validation.check_shape(value, {shape})

                def flatten(container):
                    for i in container:
                        if isinstance(i, (list,tuple)):
                            for j in flatten(i):
                                yield j
                        else:
                            yield i

                if hasattr(value, "flatten"):
                    flat_array = value.flatten()
                else:
                    flat_array = flatten(value)

                for entry in flat_array:
                    validation.validate_cuba_keyword(entry, '{cuba_key}')

                return value
            """.format(prop_name=self.name,
                       cuba_key=cuba_key,
                       shape=self.shape))


class DataProperty(FixedProperty):
    """Special data property is handled slightly different"""
    def __init__(self):
        super(DataProperty, self).__init__("data", None, False)

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


class UUIDProperty(FixedProperty):
    def __init__(self):
        super(UUIDProperty, self).__init__("uuid", None, False)

    def import_required(self):
        return [ShortcutImport('uuid')]

    def _render_init(self):
        return textwrap.dedent("""
            def _init_uuid(self):
                self.data[CUBA.UUID] = uuid.uuid4()
        """)

    def _render_getter(self):
        return textwrap.dedent("""
            @property
            def uuid(self):
                return self.data[CUBA.UUID]
        """)

    def _render_setter(self):
        return ""

    def _render_validation(self):
        return ""

    def _render_default(self):
        return ""
