class Particle(object):
    """
    Particle entity
    """
    def __init__(self, coordinates, data=None, id=None):
        self.id = id
        self.coordinates = coordinates
        if data is None:
            self.data = {}
        else:
            self.data = data

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.id == other.id and
                    self.coordinates == other.coordinates and
                    self.data == self.data)
        else:
            return False

    def __ne__(self, other):
        return not self == other
