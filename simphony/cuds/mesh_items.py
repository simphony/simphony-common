from ..core import data_container as dc


class Point(object):
    """ Coordinates describing a point in the space

    Set of coordinates (x,y,z) describing a point in
    the space and data about that point

    Parameters
    ----------
    uid : uuid.UUID
        uid of the point.
    coordinates : list of double
        set of coordinates (x,y,z) describing the point position.
    data : DataContainer
        object to store point data

    Attributes
    ----------
    uid : uuid.UUID
        uid of the point.
    data : DataContainer
        object to store point data
    coordinates : list of double
        set of coordinates (x,y,z) describing the point position.

    """

    def __init__(self, coordinates, uid=None, data=None):
        self.uid = uid
        self.coordinates = tuple(coordinates)

        if data:
            self.data = dc.DataContainer(data)
        else:
            self.data = dc.DataContainer()

    @classmethod
    def from_point(cls, point):
        return cls(
            point.coordinates,
            point.uid,
            point.data
        )


class Element(object):
    """ Element base class

    Element for storing geometrical objects

    Parameters
    ----------
    uid :
        uid of the edge.
    points : list of uid
        list of points uids defining the edge.
    data : DataContainer
        object to store data relative to the element

    Attributes
    ----------
    points : list of uid
        list of points uids defining the element.
    uid : uuid.UUID
        uid of the element
    data : DataContainer
        Element data

    """

    def __init__(self, points, uid=None, data=None):
        self.uid = uid
        self.points = points[:]

        if data:
            self.data = dc.DataContainer(data)
        else:
            self.data = dc.DataContainer()


class Edge(Element):
    """ Edge element

    Element for storing 1D geometrical objects

    Parameters
    ----------
    points : list of uid
        list of points uids defining the edge.
    uid : uuid.UUID
        uid of the edge.
    data : DataContainer
        object to store data relative to the edge

    """

    @classmethod
    def from_edge(cls, edge):
        return cls(
            edge.points,
            edge.uid,
            edge.data
        )


class Face(Element):
    """ Face element

    Element for storing 2D geometrical objects

    Parameters
    ----------
    points : list of uid
        list of points uids defining the face.
    uid : uuid.UUID
        uid of the face.
    data : DataContainer
        object to store data relative to the face

    """

    @classmethod
    def from_face(cls, face):
        return cls(
            face.points,
            face.uid,
            face.data
        )


class Cell(Element):
    """ Cell element

    Element for storing 3D geometrical objects

    Parameters
    ----------
    points : list of uid
        list of points uids defining the cell.
    uid : uuid.UUID
        uid of the cell.
    data : DataContainer
        object to store data relative to the cell

    """

    @classmethod
    def from_cell(cls, cell):
        return cls(
            cell.points,
            cell.uid,
            cell.data
        )
