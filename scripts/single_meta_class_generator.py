from __future__ import print_function

from simphony_metaparser.nodes import FixedProperty, VariableProperty

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

        properties = self._extract_properties(item)

        try:
            definition = item.properties["definition"].default
        except KeyError:
            definition = ""

        class_ = templates.Class(
            utils.cuba_key_to_meta_class_name(item.name),
            item.name,
            (utils.cuba_key_to_meta_class_name(item.parent.name)
             if item.parent is not None else None),
            properties[1:],
            docstring=definition
        )

        if item.parent is None:
            class_.methods.append(templates.MetaAPIMethods())

        class_.properties = properties[0]

        f.classes.append(class_)
        f.render(output)

    def _extract_properties(self, item):
        """Extracts the properties from the entity.
        Returns a list of lists, each list being the properties of the
        associated object in the traversal, the first element being associated
        to root, the last being associated to item.
        """
        properties = []
        reimplemented_keys = set()

        # We reverse the traversal, so that we can build up the
        # reimplemented keys from the root of the hierarchy as we descend
        # the tree. Traverse to root walks in the opposite direction.

        for item in reversed(list(traverse_to_root(item))):
            item_props = self._create_property_templates(item,
                                                         reimplemented_keys)
            properties.append(item_props)
            for p in item_props:
                reimplemented_keys.add(p.source_key)

        # We reverse them again, so that they are in the same order as
        # in a item to root traversal
        return list(reversed(properties))

    def _create_property_templates(self, item, reimplemented_keys):
        """Helper method. Extracts all the properties from a given
        class.

        Parameters
        ----------
        item: CUDSItem
            the item of the CUDS entry.

        reimplemented_keys: set
            A set containing the identifying key of the properties that
            are already defined in a base class.

        Return
        ------
        list
            A list of templates Properties
        """
        properties = []
        for prop in item.properties.values():
            if prop.name == "data":
                properties.append(templates.DataProperty())
            elif prop.name == "CUBA.UID":
                properties.append(templates.UIDProperty())
            elif isinstance(prop, FixedProperty):
                properties.append(
                    templates.FixedProperty(
                        prop.name,
                        default=prop.default,
                        reimplemented=(prop.name in reimplemented_keys)
                    )
                )

            elif isinstance(prop, VariableProperty):
                properties.append(
                    templates.VariableProperty(
                        qual_cuba_key=prop.name,
                        default=prop.default,
                        shape=prop.shape,
                        reimplemented=(prop.name in reimplemented_keys)
                    ),
                )
            else:
                raise ValueError("Unrecognized property {}, item {} "
                                 .format(prop, item.name))

        return properties
