import uuid

from simphony.core import DataContainer


class Particle(object):
    """Class representing a particle.

    Attributes
    ----------
    uid : uuid.UUID
        the uid of the particle
    coordinates : list / tuple
        x,y,z coordinates of the particle
    data : DataContainer
        DataContainer to store the attributes of the particle

    """

    def __init__(self, coordinates=(0.0, 0.0, 0.0), uid=None, data=None):
        """ Create a Particle.

        Parameters
        ----------
        coordinates : list / tuple
            x,y,z coordinates of the particle (Default: [0, 0, 0])
        uid : uuid.UID
            the id, None as default (the particle container will generate it)
        data : DataContainer
            the data, the particle will have a copy of this
        """

        self.uid = uid
        self.coordinates = tuple(coordinates)
        if data is None:
            self.data = DataContainer()
        else:
            self.data = DataContainer(data)

    @classmethod
    def from_particle(cls, particle):
        return cls(
            uid=uuid.UUID(bytes=particle.uid.bytes),
            coordinates=particle.coordinates,
            data=DataContainer(particle.data))

    def __str__(self):
        template = "uid:{0.uid}\ncoordinates:{0.coordinates}\ndata:{0.data}"
        return template.format(self)


class Bond(object):
    """Class representing a bond.

    Attributes
    ----------
    uid : uuid.UUID
        the uid of the bond
    particles : tuple
        tuple of uids of the particles that are participating in the bond.
    data : DataContainer
        DataContainer to store the attributes of the bond

    """

    def __init__(self, particles, uid=None, data=None):
        """ Create a Bond.

        Parameters
        ----------
        particles : sequence
            list of particles of the bond. It can not be empty.
        uid : uuid.UUID
            the id, None as default (the particle container will generate it)
        data : DataContainer
            DataContainer to store the attributes of the bond

        """
        self.uid = uid
        if particles is not None and len(particles) > 0:
            self.particles = tuple(particles)
        else:
            message = 'particles list {} is not valid'
            raise ValueError(message.format(particles))

        if data is None:
            self.data = DataContainer()
        else:
            self.data = DataContainer(data)

    @classmethod
    def from_bond(cls, bond):
        return cls(
            particles=bond.particles,
            uid=uuid.UUID(bytes=bond.uid.bytes),
            data=DataContainer(bond.data))

    def __str__(self):
        total_str = "{0}_{1}".format(self.uid, self.particles)
        return total_str
