from simphony.core import Default  # noqa
from .data_set import DataSet
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class Mesh(DataSet):
    """
    A mesh
    """
    cuba_key = CUBA.MESH

    def __init__(self,
                 cell,
                 edge,
                 face,
                 point,
                 description=Default,
                 name=Default):
        super(Mesh, self).__init__(description=description, name=name)
        self._init_point(point)
        self._init_edge(edge)
        self._init_cell(cell)
        self._init_face(face)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Mesh, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((
                CUBA.POINT,
                CUBA.EDGE,
                CUBA.CELL,
                CUBA.FACE, ) + base_params))

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
        value = meta_validation.cast_data_type(value, 'POINT')
        meta_validation.check_valid_shape(value, [None], 'POINT')
        meta_validation.check_elements(value, [None], 'POINT')

        return value

    def _default_point(self):
        raise TypeError("No default for point")

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
        value = meta_validation.cast_data_type(value, 'EDGE')
        meta_validation.check_valid_shape(value, [None], 'EDGE')
        meta_validation.check_elements(value, [None], 'EDGE')

        return value

    def _default_edge(self):
        raise TypeError("No default for edge")

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
        value = meta_validation.cast_data_type(value, 'CELL')
        meta_validation.check_valid_shape(value, [None], 'CELL')
        meta_validation.check_elements(value, [None], 'CELL')

        return value

    def _default_cell(self):
        raise TypeError("No default for cell")

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
        value = meta_validation.cast_data_type(value, 'FACE')
        meta_validation.check_valid_shape(value, [None], 'FACE')
        meta_validation.check_elements(value, [None], 'FACE')

        return value

    def _default_face(self):
        raise TypeError("No default for face")
