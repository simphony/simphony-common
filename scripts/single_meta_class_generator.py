from __future__ import print_function

from simphony_metaparser.nodes import FixedPropertyEntry, VariablePropertyEntry

from simphony_metaparser.utils import (
    traverse_to_root)

from . import templates
from . import utils

# A list of the known values for fixed property.
# It does not include parent and data, as they are handled in a special way
KNOWN_FIXED_PROPERTIES = [
    "definition", "models", "variables", "physics_equations"
]


class SingleMetaClassGenerator(object):
    """Generator for a single meta class file.
    """

    def generate(self, item, output):
        """Generates the meta class content, and writes them
        to the out file handler.

        Parameters
        ----------
        item: CUDSItem
            The item to render.

        output: file
            File handler where to write the content.
        """
        print("Generating for {}".format(item.name))

        f = templates.File()
        f.imports.add(templates.ShortcutImport("CUBA"))

        if item.parent is None:
            print ("  Hierarchy root")
        else:
            print ("  Descendant of {}".format(item.parent.name))

        hierarchy_properties, object_properties = self._extract_properties(
            item)

        class_ = templates.Class(
            utils.cuba_key_to_meta_class_name(item.name),
            item.name,
            item.parent.name if item.parent is not None else None,
            hierarchy_properties,
            docstring=""
        )

        if item.parent is None:
            class_.methods.append(templates.MetaAPIMethods())

        f.classes.append(class_)
        f.render(output)

    def _extract_properties(self, item):
        base_properties = []
        reimplemented_keys = set()

        traversal = list(reversed(list(traverse_to_root(item))))[:-1]

        for parent in traversal:
            base_properties += self._create_property_templates(
                parent,
                reimplemented_keys)
            reimplemented_keys.add([p.name for p in base_properties])

        object_properties = self._create_property_templates(
            item,
            reimplemented_keys)

        return base_properties, object_properties

    def _create_property_templates(self, item, reimplemented_keys):
        """Helper method. Extracts all the properties from a given
        class.

        Parameters
        ----------
        item: CUDSItem
            the item of the CUDS entry.

        Return
        ------
        list
            A list of templates Properties
        """
        properties = []
        for prop in item.property_entries.values():
            if prop.name == "data":
                properties.append(templates.DataProperty())
            elif prop.name == "CUBA.UID":
                properties.append(templates.UIDProperty())
            elif isinstance(prop, FixedPropertyEntry):
                properties.append(
                    templates.FixedProperty(
                        prop.name,
                        default=prop.default,
                        reimplemented=(prop.name in reimplemented_keys)
                    )
                )

            elif isinstance(prop, VariablePropertyEntry):
                properties.append(
                    templates.VariableProperty(
                        prop.name,
                        default=prop.default,
                        shape=prop.shape,
                        reimplemented=(prop.name in reimplemented_keys)
                    ),
                )
            else:
                raise ValueError("Unrecognized property {}, item {} "
                                 .format(prop, item.name))

        return properties


def is_variable_reimplemented(prop_key, item):
    """Checks if a given variable is reimplemented from a base parent class.

    Parameters
    ----------
    prop_key: str
        The key of the property
    item: the current item
        a list of all the parent classes, from top to bottom (None)

    Returns
    -------
    True or False
    """
    for parent in traverse_to_root(item)[1:]:
        if prop_key in parent.property_entries:
            return True

    return False
