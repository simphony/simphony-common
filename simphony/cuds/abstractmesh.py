from abc import ABCMeta, abstractmethod


class ABCMesh(object):
    """Abstract base class for mesh.

    Attributes
    ----------
    name : str
        name of mesh

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_point(self, uid):
        pass

    @abstractmethod
    def get_edge(self, uid):
        pass

    @abstractmethod
    def get_face(self, uid):
        pass

    @abstractmethod
    def get_cell(self, uid):
        pass

    @abstractmethod
    def add_points(self, points):
        pass

    @abstractmethod
    def add_edges(self, edges):
        pass

    @abstractmethod
    def add_faces(self, faces):
        pass

    @abstractmethod
    def add_cells(self, cells):
        pass

    @abstractmethod
    def update_points(self, points):
        pass

    @abstractmethod
    def update_edges(self, edges):
        pass

    @abstractmethod
    def update_faces(self, faces):
        pass

    @abstractmethod
    def update_cells(self, cells):
        pass

    @abstractmethod
    def iter_points(self, uids=None):
        pass

    @abstractmethod
    def iter_edges(self, uids=None):
        pass

    @abstractmethod
    def iter_faces(self, uids=None):
        pass

    @abstractmethod
    def iter_cells(self, uids=None):
        pass

    @abstractmethod
    def has_edges(self):
        pass

    @abstractmethod
    def has_faces(self):
        pass

    @abstractmethod
    def has_cells(self):
        pass
