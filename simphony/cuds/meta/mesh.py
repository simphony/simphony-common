from simphony.core import Default
from . import validation
from .data_set import DataSet
from simphony.core.cuba import CUBA


class Mesh(DataSet):
    """
    A mesh
    """
    cuba_key = CUBA.MESH

    def __init__(self, point, face, cell, edge, *args, **kwargs):
        super(Mesh, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_point(point)
        self._init_face(face)
        self._init_cell(cell)
        self._init_edge(edge)

    def supported_parameters(self):
        try:
            base_params = super(Mesh, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.POINT,
            CUBA.FACE,
            CUBA.CELL,
            CUBA.EDGE, ) + base_params

    def _init_definition(self):
        self._definition = "A mesh"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_point(self, value):
        if value is Default:
            raise TypeError("Value for point must be specified")

        self.point = value

    @property
    def point(self):
        return self.data[CUBA.POINT]

    @point.setter
    def point(self, value):
        value = self._validate_point(value)
        self.data[CUBA.POINT] = value

    def _validate_point(self, value):

        value = validation.cast_data_type(value, 'POINT')
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'POINT')

        return value

    def _init_face(self, value):
        if value is Default:
            raise TypeError("Value for face must be specified")

        self.face = value

    @property
    def face(self):
        return self.data[CUBA.FACE]

    @face.setter
    def face(self, value):
        value = self._validate_face(value)
        self.data[CUBA.FACE] = value

    def _validate_face(self, value):

        value = validation.cast_data_type(value, 'FACE')
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'FACE')

        return value

    def _init_cell(self, value):
        if value is Default:
            raise TypeError("Value for cell must be specified")

        self.cell = value

    @property
    def cell(self):
        return self.data[CUBA.CELL]

    @cell.setter
    def cell(self, value):
        value = self._validate_cell(value)
        self.data[CUBA.CELL] = value

    def _validate_cell(self, value):

        value = validation.cast_data_type(value, 'CELL')
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'CELL')

        return value

    def _init_edge(self, value):
        if value is Default:
            raise TypeError("Value for edge must be specified")

        self.edge = value

    @property
    def edge(self):
        return self.data[CUBA.EDGE]

    @edge.setter
    def edge(self, value):
        value = self._validate_edge(value)
        self.data[CUBA.EDGE] = value

    def _validate_edge(self, value):

        value = validation.cast_data_type(value, 'EDGE')
        validation.check_shape(value, [None])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'EDGE')

        return value
