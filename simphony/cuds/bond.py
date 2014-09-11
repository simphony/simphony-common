class Bond(object):
    """
    Bond entity
    """
    def __init__(self, id, particles, data=None):
        self.id = id
        self.particles = particles
        if data is None:
            self.data = {}
        else:
            self.data = data

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.id == other.id and
                    self.particles == other.particles and
                    self.data == self.data)
        else:
            return False

    def __ne__(self, other):
        return not self == other
