from __future__ import print_function

from simphony_metaparser.utils import traverse

from scripts.utils import cuba_key_to_meta_class_module_name, \
    cuba_key_to_meta_class_name


class APIGenerator(object):
    def generate(self, ontology, output):
        """
        Generates the api.py with the appropriate imports.
        The imports are alphabetically ordered.

        ontology: Ontology
            The node of the ontology

        output: file
            The file on which to write the result
        """

        lines = []
        for cuds_item, _ in traverse(ontology.root_cuds_item):
            lines.append('from .{} import {}   # noqa\n'.format(
                    cuba_key_to_meta_class_module_name(cuds_item.name),
                    cuba_key_to_meta_class_name(cuds_item.name)
                )
            )

        for line in sorted(lines):
            output.write(line)
