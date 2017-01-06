from __future__ import print_function

from . import templates
from . import utils

# A list of the known values for fixed property.
# It does not include parent and data, as they are handled in a special way
KNOWN_FIXED_PROPERTIES = [
    "definition", "models", "variables", "physics_equations"
]


class SingleMetaClassGenerator(object):
    def __init__(self, cuba_key, class_data):
        self.cuba_key = cuba_key
        self.class_data = class_data

    def generate(self, out):
        print("Generating for {}".format(self.cuba_key))

        parent_class_key = self.class_data.get('parent', None)

        f = templates.File()
        f.imports.add(templates.ShortcutImport("CUBA"))

        if parent_class_key is None:
            parent_class_name = None
            print ("  Hierarchy root")
        else:
            if not parent_class_key.startswith('CUBA.'):
                message = "'parent' should be either empty " \
                          "or a CUBA value, got {}".format(parent_class_key)
                raise ValueError(message)

            parent_class_name = utils.cuba_key_to_meta_class_name(
                parent_class_key)
            print ("  Descendant of {}".format(parent_class_name))

        class_ = templates.Class(
            utils.cuba_key_to_meta_class_name(self.cuba_key),
            self.cuba_key,
            parent_class_name,
            docstring=self.class_data["definition"]
        )

        if parent_class_key is None:
            class_.methods.append(templates.MetaAPIMethods())

        for prop_key in [p for p in self.class_data.keys()]:
            if prop_key == "parent":
                continue
            if prop_key == "data":
                print ("  Adding data property")
                class_.properties.append(templates.UUIDProperty())
            elif prop_key == "CUBA.UUID":
                print ("  Adding UUID property")
                class_.properties.append(templates.DataProperty())
            elif prop_key in KNOWN_FIXED_PROPERTIES:
                print ("  Adding fixed property {}".format(prop_key))
                if prop_key in self.class_data:
                    class_.properties.append(
                        templates.FixedProperty(
                            prop_key,
                            default=self.class_data[prop_key]
                        )
                    )

            elif prop_key.startswith("CUBA."):
                print ("  Adding variable property {}".format(prop_key))
                property_entry = self.class_data[prop_key]
                if property_entry is None:
                    property_entry = {}
                class_.properties.append(
                    templates.VariableProperty(
                        prop_key,
                        default=property_entry.get("default", utils.NoDefault),
                        shape=utils.parse_shape(property_entry.get("shape")),
                    )
                )
            else:
                raise ValueError("Unrecognized property {}".format(prop_key))

        f.classes.append(class_)
        f.render(out)
