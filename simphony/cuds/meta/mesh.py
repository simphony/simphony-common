from simphony.core import Default  # noqa
from . import validation
from .data_set import DataSet
from simphony.core.cuba import CUBA


class Mesh(DataSet):
    """
    A mesh
    """
    cuba_key = CUBA.MESH

    def __init__(self,
                 point=Default,
                 face=Default,
                 cell=Default,
                 edge=Default,
                 description=Default,
                 name=Default):

        super(Mesh, self).__init__(description=description, name=name)
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

    def _default_definition(self):
        return "A mesh"  # noqa

    def _init_point(self, value):
        if value is Default:
            value = self._default_point()

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

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'POINT')

        return value

    def _default_point(self):
        raise TypeError("No default for point")

    def _init_face(self, value):
        if value is Default:
            value = self._default_face()

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

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'FACE')

        return value

    def _default_face(self):
        raise TypeError("No default for face")

    def _init_cell(self, value):
        if value is Default:
            value = self._default_cell()

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

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'CELL')

        return value

    def _default_cell(self):
        raise TypeError("No default for cell")

    def _init_edge(self, value):
        if value is Default:
            value = self._default_edge()

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

        if hasattr(value, "flatten"):
            flat_array = value.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'EDGE')

        return value

    def _default_edge(self):
        raise TypeError("No default for edge")
