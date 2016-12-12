import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .cuds_component import CUDSComponent
from . import validation


class Mesh(CUDSComponent):
    '''A mesh  # noqa
    '''

    cuba_key = CUBA.MESH

    def __init__(self, point, face, cell, edge, description="", name=""):

        self._data = DataContainer()

        self.edge = edge
        self.cell = cell
        self.face = face
        self.point = point
        self.name = name
        self.description = description
        # This is a system-managed, read-only attribute
        self._definition = 'A mesh'  # noqa

    @property
    def edge(self):
        return self.data[CUBA.EDGE]

    @edge.setter
    def edge(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'edge')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'edge')
        data = self.data
        data[CUBA.EDGE] = value
        self.data = data

    @property
    def cell(self):
        return self.data[CUBA.CELL]

    @cell.setter
    def cell(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'cell')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'cell')
        data = self.data
        data[CUBA.CELL] = value
        self.data = data

    @property
    def face(self):
        return self.data[CUBA.FACE]

    @face.setter
    def face(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'face')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'face')
        data = self.data
        data[CUBA.FACE] = value
        self.data = data

    @property
    def point(self):
        return self.data[CUBA.POINT]

    @point.setter
    def point(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'point')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'point')
        data = self.data
        data[CUBA.POINT] = value
        self.data = data

    @property
    def definition(self):
        return self._definition

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.CELL, CUBA.DESCRIPTION, CUBA.EDGE, CUBA.FACE, CUBA.NAME,
                CUBA.POINT, CUBA.UUID)

    @classmethod
    def parents(cls):
        return (CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
