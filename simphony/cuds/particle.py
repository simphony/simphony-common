class Particle(object):
    """
    Particle entity
    """
    def __init__(self, id, coordinates, data={}):
        self.id = id
        self.coordinates = coordinates
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
