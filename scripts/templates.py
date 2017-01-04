import textwrap

from . import utils


class File(object):
    def __init__(self):
        self.imports = []
        self.classes = []
        self.methods = []

    def render(self, out, indent_level=0):
        imports = self.imports
        for cls in self.classes:
            imports += cls.import_required()

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
        'uuid': 'import uuid'
    }

    def __init__(self, module_shortcut):
        self.module_shortcut = module_shortcut

    def render(self, out, indent_level=0):
        out.write(
            utils.indent(
                self.IMPORT_PATHS[self.module_shortcut],
                indent_level
            )+'\n'
        )


class MetaClassImport(object):
    def __init__(self, meta_class_name):
        self.meta_class_name = meta_class_name

    def render(self, out, indent_level=0):
        out.write(
            utils.indent(
                "from .{meta_class_module_name} import {meta_class_name}".format(  # noqa
                    meta_class_module_name=utils.meta_class_name_to_module_name(  # noqa
                    self.meta_class_name
                    ),
                meta_class_name=self.meta_class_name
                ),
                indent_level
            ) + '\n'
        )


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
            required = [MetaClassImport(self.parent_class_name)]

        return required + sum(
            (prop.import_required() for prop in self.properties),
            [])

    def render(self, out, indent_level=0):
        init_args = []
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

        init_args_str = ""
        if len(init_args):
            init_args_str = (", ".join(init_args))+', '

        out.write(
            utils.indent(
                """
                def __init__(self, {init_args_str}*args, **kwargs):
                    super({class_name}, self).__init__(*args, **kwargs)
                """.format(
                        class_name=self.class_name,
                        init_args_str=init_args_str
                    ),
                indent_level+1
            )
        )

        for method in self.methods:
            method.render(out, indent_level=indent_level+1)

        for prop in self.properties:
            prop.render(out, indent_level=indent_level+1)


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


class Property(object):
    def import_required(self):
        return []

    def __init__(self, name, docstring=""):
        self.name = name
        self.docstring = docstring

    def render(self, out, indent_level=0):
        s = self._render_init()
        s += self._render_setter()
        s += self._render_getter()
        s += self._render_validation()

        out.write(utils.indent(s, indent_level))

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
        def _init_{name}(value):
            pass
        """).format(name=self.name)

    def _render_validation(self):
        return textwrap.dedent("""
        def _validate_{name}(value):
            pass
        """).format(name=self.name)


class VariableProperty(Property):
    def import_required(self):
        return [ShortcutImport("validation")]

    def __init__(self,
                 qual_cuba_key,
                 shape,
                 allow_none):
        self.qual_cuba_key = qual_cuba_key
        self.shape = shape
        self.allow_none = allow_none

    def _render_setter(self):
        lowercase_cuba_key = (self.qual_cuba_key.split(".")[1]).lower()
        return textwrap.dedent("""
            @{lowercase_cuba_key}.setter
                def {lowercase_cuba_key}(self, value):
                self._validate_{lowercase_cuba_key}(value)
                self.data[{qual_cuba_key}] = value
        """).format(
            lowercase_cuba_key=lowercase_cuba_key,
            qual_cuba_key=self.qual_cuba_key)

    def _render_getter(self):
        pass

    def _render_validation(self):
        return textwrap.dedent("""
            def _validate_{lowercase_cuba_key}(self, value):
                value = validation.cast_data_type(value, {!r})

        """)


class DataProperty(Property):
    """Special data property is handled slightly different"""

    def import_required(self):
        return [ShortcutImport("DataContainer")]

    def __init__(self):
        super(DataProperty, self).__init__("data")

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
            @data.setter
            def _init_data(self, new_data):
                self._data = DataContainer()
        """)


class UUIDProperty(Property):
    def import_required(self):
        return [ShortcutImport('uuid')]

    def __init__(self):
        super(UUIDProperty, self).__init__("uuid")

    def _render_init(self):
        return textwrap.dedent("""
            @property
            def _init_uuid(self):
                self._uuid = uuid.uuid4()
        """)
