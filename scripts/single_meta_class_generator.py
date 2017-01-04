from __future__ import print_function

from . import templates
from . import utils


class SingleMetaClassGenerator(object):
    def __init__(self, cuba_key, class_data):
        self.cuba_key = cuba_key
        self.class_data = class_data

    def generate(self, out):
        print("Generating for {}".format(self.cuba_key))

        parent_class_key = self.class_data.get('parent', None)

        if parent_class_key is None:
            self._generate_hierarchy_root(out)
        else:
            self._generate_descendant(out)

    def _generate_descendant(self, out):
        f = templates.File()
        f.imports.append(templates.ShortcutImport("CUBA"))

        parent_class_key = self.class_data["parent"]

        if not parent_class_key.startswith('CUBA.'):
            message = "'parent' should be either empty " \
                      "or a CUBA value, got {}".format(parent_class_key)
            raise ValueError(message)

        parent_class_name = utils.cuba_key_to_meta_class_name(
            parent_class_key)

        class_ = templates.Class(
            utils.cuba_key_to_meta_class_name(self.cuba_key),
            self.cuba_key,
            parent_class_name,
            docstring=self.class_data["definition"])

        f.classes.append(class_)

        f.render(out)

    def _generate_hierarchy_root(self, out):
        f = templates.File()
        f.imports.append(templates.ShortcutImport("CUBA"))

        parent_class_name = None

        class_ = templates.Class(
            utils.cuba_key_to_meta_class_name(self.cuba_key),
            self.cuba_key,
            parent_class_name,
            docstring=self.class_data["definition"]
        )
        class_.methods.append(templates.MetaAPIMethods())
        class_.properties.append(templates.UUIDProperty())
        class_.properties.append(templates.DataProperty())
        f.classes.append(class_)
        f.render(out)
