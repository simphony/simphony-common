from simphony.material_relations.material-relation import MaterialRelation


class {MR_NAME}(MaterialRelation):
    """ MaterialRelation provides a general interface for describing the
    (physics/chemistry) relations between different materials

    Attributes
    ----------
    {ATTR_DESC_BLOCK}
    """

    def __init__(
        self,
        name,
        description,
        parameters,
        supported_parameters,
        materials,
        kind,
        {ATTR_DESC}
    ):
        super({MR_NAME}, self).__init__(
            name=name,
            description=description,
            parameters=parameters,
            supported_parameters=supported_parameters,
            materials=materials,
            kind={MR_KIND}
        )

        {ATTR_ASSIGN_BLOCK}

    @property
    def data(self):
        return dc.DataContainer(self._data)

    @data.setter
    def data(self, value):
        self._data = dc.DataContainer(value)
