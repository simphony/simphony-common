import abc
import textwrap

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
        out.write(
            utils.indent(
                """
                class {class_name}({parent_class_name}):
                    \"\"\"
                    {docstring}
                    \"\"\"

                    cuba_key = {qualified_cuba_key}
                """.format(
                        class_name=self.class_name,
                        parent_class_name=parent_class_name,
                        docstring=self.docstring,
                        qualified_cuba_key=utils.with_cuba_prefix(self.cuba_key)  # noqa
                    ),
                indent_level
            )
        )

        out.write(utils.indent(self._render_init_method(), indent_level+1))

        for method in self.methods:
            method.render(out, indent_level=indent_level+1)

        for prop in self.properties:
            prop.render(out, indent_level=indent_level+1)

    def _render_init_method(self):
        init_args = []
        for prop in self.properties:
            if isinstance(prop, VariableProperty):
                init_args.append(prop.name)

        init_args_str = ""
        if len(init_args):
            init_args_str = (
                ", ".join([
                    "{}=Default".format(arg)
                    for arg in init_args])
                            )+', '

        s = textwrap.dedent("""
            def __init__(self, {init_args_str}*args, **kwargs):
                super({class_name}, self).__init__(*args, **kwargs)
            """.format(
                class_name=self.class_name,
                init_args_str=init_args_str)
        )

        for prop in self.properties:
            if isinstance(prop, FixedProperty):
                s += utils.indent(
                    textwrap.dedent("""
                    self._init_{prop_name}()
                    """.format(prop_name=prop.name)))
            else:
                s += utils.indent(
                    textwrap.dedent("""
                    self._init_{prop_name}({prop_name})
                    """.format(prop_name=prop.name)))

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

    def render(self, out, indent_level=0):
        s = self._render_init()
        s += self._render_getter()
        s += self._render_setter()
        s += self._render_validation()

        out.write(utils.indent(s, indent_level))


class Property(ABCProperty):
    def import_required(self):
        return [ShortcutImport("Default")]

    def __init__(self, name, default=None, docstring=""):
        super(Property, self).__init__(name)
        self.default = default
        self.docstring = docstring

    def _render_setter(self):
        return textwrap.dedent("""
            @{name}.setter
            def {name}(self, value):
                \"\"\"
                {docstring}
                \"\"\"
                self._validate_{name}(value)
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
            if value == Default:
                value = {default}

            self.{name} = value

        """).format(name=self.name,
                    default=utils.quoted_if_string(self.default))

    def _render_validation(self):
        return textwrap.dedent("""
        def _validate_{name}(value):
            pass
        """).format(name=self.name)


class FixedProperty(Property):
    def _render_init(self):
        return textwrap.dedent("""
        def _init_{name}(self):
            self._{name} = {default}

        """).format(name=self.name,
                    default=utils.quoted_if_string(self.default))

    def _render_setter(self):
        return ""

    def _render_validation(self):
        return ""


class VariableProperty(Property):
    def import_required(self):
        return [ShortcutImport("validation")]

    def __init__(self, qual_cuba_key):
        prop_name = utils.cuba_key_to_property_name(qual_cuba_key)
        super(VariableProperty, self).__init__(name=prop_name)
        self.qual_cuba_key = qual_cuba_key

    def _render_setter(self):
        return textwrap.dedent("""
            @{prop_name}.setter
            def {prop_name}(self, value):
                self._validate_{prop_name}(value)
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
        return textwrap.dedent("""
            def _validate_{prop_name}(self, value):
                pass
        """.format(prop_name=self.name))
        # value = validation.cast_data_type(value, {!r})


class DataProperty(ABCProperty):
    """Special data property is handled slightly different"""
    def __init__(self):
        super(DataProperty, self).__init__("data")

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
            def _init_data(self, new_data):
                self._data = DataContainer()
        """)

    def _render_validation(self):
        return ""


class UUIDProperty(ABCProperty):
    def __init__(self):
        super(UUIDProperty, self).__init__("uuid")

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
