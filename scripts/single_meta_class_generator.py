from __future__ import print_function

from simphony_metaparser.nodes import FixedPropertyEntry, VariablePropertyEntry

from simphony_metaparser.utils import (
    without_cuba_prefix, traverse_to_root)

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

    def generate(self, ontology, item, output):
        """Generates the meta class content, and writes them
        to the out file handler.

        Parameters
        ----------
        ontology: Ontology
            The ontology

        item: CUDSItem
            The item to render.

        out: file
            File handler where to write the content.
        """
        print("Generating for {}".format(item.name))

        f = templates.File()
        f.imports.add(templates.ShortcutImport("CUBA"))

        if item.parent is None:
            print ("  Hierarchy root")
        else:
            print ("  Descendant of {}".format(item.parent.name))

        hierarchy_properties = []
        for parent in traverse_to_root(item):
            hierarchy_properties += self._create_property_templates(parent)

        class_ = templates.Class(
            utils.cuba_key_to_meta_class_name(item.name),
            item.name,
            item.parent.name,
            hierarchy_properties,
            docstring=""
        )

        if item.parent is None:
            class_.methods.append(templates.MetaAPIMethods())

        class_.properties = self._create_property_templates(item)

        f.classes.append(class_)
        f.render(output)

    def _create_property_templates(self, item):
        """Helper method. Extracts all the properties from a given
        class.

        Parameters
        ----------
        class_data: dict
            the data of the CUDS entry, as from yaml parsed dict.

        parent_keys: list
            the list of parent cuba keys

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
                            reimplemented=is_variable_reimplemented(
                                prop.name,
                                item
                            )
                        )
                    )

            elif isinstance(prop, VariablePropertyEntry):
                properties.append(
                    templates.VariableProperty(
                        prop.name,
                        default=prop.default,
                        shape=prop.shape,
                        reimplemented=is_variable_reimplemented(
                            prop.name,
                            item,
                        )
                    ),
                )
            else:
                raise ValueError("Unrecognized property {}, item {} "
                                 .format(prop, item.name))

        return properties


def is_variable_reimplemented(prop_key, parent_keys):
    """Checks if a given variable is reimplemented from a base parent class.

    Parameters
    ----------
    prop_key: str
        The key of the property
    parent_keys: list
        a list of all the parent classes, from top to bottom (None)
    simphony_metadata_dict: dict
        the full yaml parsed dictionary

    Returns
    -------
    True or False
    """
    for parent_key in parent_keys:
        if parent_key is None:
            return False

        if prop_key in simphony_metadata_dict["CUDS_KEYS"][
                without_cuba_prefix(parent_key)]:
            return True


