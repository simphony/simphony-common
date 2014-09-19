class Bond(object):
    """
    Bond entity
    """
    def __init__(self, particles, data=None, id=None):
        self.id = id
        self.particles = particles
        if data is None:
            self.data = {}
        else:
            self.data = data
