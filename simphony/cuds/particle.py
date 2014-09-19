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
