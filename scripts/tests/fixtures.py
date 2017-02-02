from simphony_metaparser.nodes import Ontology, CUBADataType, CUDSItem


def trivial_ontology():
    ontology = Ontology()
    ontology.data_types.extend([
        CUBADataType(name="CUBA.CUBA_DATA_ONE",
                     type="string"),
        CUBADataType(name="CUBA.CUBA_DATA_TWO",
                     type="string")
    ])
    ontology.root_cuds_item = CUDSItem(name="CUBA.CUDS_ROOT")
    ontology.root_cuds_item.children.extend([
        CUDSItem(name="CUBA.CUDS_C1"),
        CUDSItem(name="CUBA.CUDS_C2")]
    )

    return ontology
