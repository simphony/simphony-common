from __future__ import print_function

import warnings

from . import templates
from . import utils

# A list of the known values for fixed property.
# It does not include parent and data, as they are handled in a special way
KNOWN_FIXED_PROPERTIES = [
    "definition", "models", "variables", "physics_equations"
]


class SingleMetaClassGenerator(object):
    def __init__(self, cuba_key, simphony_metadata_dict):
        self.cuba_key = cuba_key
        self.simphony_metadata_dict = simphony_metadata_dict

    def generate(self, out):
        print("Generating for {}".format(self.cuba_key))

        # Catch inconsistent definitions that would choke the generator
        parent_keys = list(
            all_parent_keys(
                self.cuba_key,
                self.simphony_metadata_dict))

        parent_class_key = parent_keys[0]
        if (parent_class_key and parent_class_key.replace('CUBA.', '')
                not in self.simphony_metadata_dict['CUDS_KEYS']):
            raise ValueError(
                'parent {parent} of {cuba_key} '
                'is not defined in CUDS_KEYS'.format(parent=parent_class_key,
                                                     cuba_key=self.cuba_key)
            )

        if self.cuba_key.lower() in ('validation', 'api'):
            raise ValueError(
                'Name clashes with utility modules: '+self.cuba_key.lower()
            )

        class_data = self.simphony_metadata_dict["CUDS_KEYS"][self.cuba_key]

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
            docstring=class_data["definition"]
        )

        if parent_class_key is None:
            class_.methods.append(templates.MetaAPIMethods())

        for prop_key in [p for p in class_data.keys()]:
            if prop_key == "parent":
                continue
            if prop_key == "data":
                print ("  Adding data property")
                class_.properties.append(templates.DataProperty())
            elif prop_key == "CUBA.UUID":
                print ("  Adding UUID property")
                class_.properties.append(templates.UUIDProperty())
            elif prop_key in KNOWN_FIXED_PROPERTIES:
                print ("  Adding fixed property {}".format(prop_key))
                if prop_key in class_data:
                    class_.properties.append(
                        templates.FixedProperty(
                            prop_key,
                            default=class_data[prop_key]
                        )
                    )

            elif prop_key.startswith("CUBA."):
                print ("  Adding variable property {}".format(prop_key))
                property_entry = class_data[prop_key]
                if property_entry is None:
                    property_entry = {}
                class_.properties.append(
                    templates.VariableProperty(
                        prop_key,
                        default=property_entry.get("default", utils.NoDefault),
                        shape=utils.parse_shape(property_entry.get("shape")),
                        reimplemented=is_variable_reimplemented(
                            prop_key,
                            parent_keys,
                            self.simphony_metadata_dict
                        )
                    ),
                )
            else:
                raise ValueError("Unrecognized property {}".format(prop_key))

        f.classes.append(class_)
        f.render(out)


def is_variable_reimplemented(prop_key, parent_keys, simphony_metadata_dict):
    for parent_key in parent_keys:
        if parent_key is None:
            return False

        if prop_key in simphony_metadata_dict["CUDS_KEYS"][
                utils.without_cuba_prefix(parent_key)]:
            return True


def all_parent_keys(key, simphony_metadata_dict):
    cur_key = key

    while cur_key is not None:
        class_data = simphony_metadata_dict["CUDS_KEYS"][cur_key]
        parent_key = utils.without_cuba_prefix(class_data['parent'])
        yield (utils.with_cuba_prefix(parent_key)
               if parent_key is not None else None)
        cur_key = parent_key
