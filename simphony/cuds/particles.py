# -*- coding: utf-8 -*-
import uuid

from simphony.cuds.abstractparticles import ABCParticles
import simphony.cuds.pcexceptions as pce
from simphony.core.data_container import DataContainer


class Particles(ABCParticles):
    """Class that represents a container of particles and bonds.

    Class provides methods to add particles and bonds, remove them and update
    them.

    Attributes
    ----------
    name : str
        name of the particle container
    _particles : dict
        data structure for particles storage
    _bonds : dict
        data structure for bonds storage
    data : DataContainer
        data attributes of the element

    """
    def __init__(self, name):
        """ Constructor

        Parameters
        ----------
        name : str
            name of the particle container
        """
        self._particles = {}
        self._bonds = {}
        self._data = DataContainer()
        self.name = name

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    def add_particle(self, particle):
        """Adds the particle to the container.

        If the new particle has no id, the particle container
        will generate a new unique id for it. If the particle has
        already an id (user set), it won't add the particle if a particle
        with the same id already exists. If the user wants to replace
        an existing particle in the container there is an 'update_particle'
        method for that purpose.

        Parameters
        ----------
        particle : Particle
            the new particle that will be included in the container.

        Returns
        -------
        uid : uuid.UUID
            The id of the added particle.

        Raises
        ------
        ValueError when the new particle already exists in the container.

        Examples
        --------
        Having a Particle and a ParticleContainer just call the function
        passing the Particle as parameter.

        >>> part = Particle()
        >>> part_container = Particles(name="foo")
        >>> part_container.add_particle(part)
        """
        return self._add_element(
            self._particles, particle, clone=Particle.from_particle)

    def add_bond(self, bond):
        """Adds the bond to the container.

        Also like with particles, if the bond has an user defined id,
        it won't add the bond if a bond with the same id already exists, and
        if the bond has no id the particle container will generate an
        unique id. If the user wants to replace an existing bond in the
        container there is an 'update_bond' method for that purpose.

        Parameters
        ----------
        new_bond : Bond
            the new bond that will be included in the container.

        Returns
        -------
        uid : uuid.UID
            The id of the added bond.

        Raises
        ------
        ValueError when the new particle already exists in the container.

        Examples
        --------
        Having a Bond and a ParticleContainer just call the function
        passing the Bond as parameter.

        >>> bond = Bond()
        >>> part_container = Particles(name="foo")
        >>> part_container.add_bond(bond)
        """
        return self._add_element(self._bonds, bond, Bond.from_bond)

    def update_particle(self, particle):
        """Replaces an existing particle.

        Takes the id of 'particle' and searchs inside the container for
        that particle. If the particle exists, it is replaced with the new
        particle passed as parameter. If the particle doesn't exist, it will
        raise an exception.

        Parameters
        ----------

        particle : Particle
            the particle that will be replaced.

        Raises
        ------
        ValueError exception if the particle does not exists.

        Examples
        --------
        Having a Particle that already exists in the container (taken with the
        'get_particle' method for example) and a ParticleContainer just call
        the function passing the Particle as parameter.

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> part = part_container.get_particle(uid)
        >>> ... #do whatever you want with the particle
        >>> part_container.update_particle(part)
        """
        self._update_element(
            self._particles, particle, clone=Particle.from_particle)

    def update_bond(self, bond):
        """Replaces an existing bond.

        Takes the id of 'bond' and searchs inside the container for
        that bond. If the bond exists, it is replaced with the new
        bond passed as parameter. If the bond doesn't exist, it will
        raise an exception.

        Parameters
        ----------

        bond : Bond
            the bond that will be replaced.

        Raises
        ------
        ValueError exception if the bond doesn't exists.

        Examples
        --------
        Having a Bond that already exists in the container (taken with the
        'get_bond' method for example) and a Particles just call the
        function passing the Bond as parameter.

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> bond = part_container.get_bond(uid)
        >>> ... #do whatever you want with the bond
        >>> part_container.update_bond(bond)
        """
        self._update_element(self._bonds, bond, clone=Bond.from_bond)

    def get_particle(self, uid):
        """Returns a copy of the particle with the 'particle_id' id.

        Parameters
        ----------

        uid : uuid.UUID
            the id of the particle

        Raises
        ------
        KeyError :
           when the particle is not in the container.

        Returns
        -------
        A copy of the particle
        """
        particle = self._particles[uid]
        return Particle.from_particle(particle)

    def get_bond(self, uid):
        """Returns a copy of the bond with the 'bond_id' id.

        Parameters
        ----------
        uid : uuid.UUID
            the id of the bond

        Raises
        ------
        KeyError :
           when the bond is not in the container.

        Returns
        -------
        A copy of the bond
        """
        bond = self._bonds[uid]
        return Bond.from_bond(bond)

    def remove_particle(self, uid):
        """Removes the particle with uid from the container.

        The id passed as parameter should exists in the container. Otherwise
        an expcetion will be raised.

        Parameters
        ----------
        uid : uuid.UUID
            the id of the particle to be removed.

        Raises
        ------
        KeyError exception if the particle doesn't exist.


        Examples
        --------
        Having an id of an existing particle, pass it to the function.

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> part = part_container.get_particle(uid)
        >>> ...
        >>> part_container.remove_particle(part.uid)
        or directly
        >>> part_container.remove_particle(uid)
        """
        del self._particles[uid]

    def remove_bond(self, uid):
        """Removes the bond with the uid from the container.

        The id passed as parameter should exists in the container. If
        it doesn't exists, nothing will happen.

        Parameters
        ----------
        uid : uuid.UUID
            the id of the bond to be removed.

        Examples
        --------
        Having an id of an existing bond, pass it to the function.

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> bond = part_container.get_bond(id)
        >>> ...
        >>> part_container.remove_bond(bond.uid)
        or directly
        >>> part_container.remove_bond(id)
        """
        del self._bonds[uid]

    def iter_particles(self, uids=None):
        """Generator method for iterating over the particles of the container.

        It can receive any kind of sequence of particle uids to iterate over
        those concrete particles. If nothing is passed as parameter, it will
        iterate over all the particles.

        Parameters
        ----------

        uids : iterable of uuid.UUID, optional
            sequence containing the uids of the particles that will be
            iterated. When the uids are provided, then the particles are
            returned in the same order the uids are returned by the iterable.
            If uids is None, then all particles are returned by the interable
            and there is no restriction on the order that they are returned.

        Yields
        ------
        particle : Particle
            Yields each particle to be used.

        Raises
        ------
        KeyError exception if any of the ids passed as parameters are not
        in the container.

        Examples
        --------
        It can be used with a sequence as parameter or without it:

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> for particle in part_container.iter_particles([uid1, uid2, uid3]):
                ...  #do stuff
                #take the particle back to the container so it will be updated
                #in case we need it
                part_container.update_particle(particle)

        >>> for particle in part_container.iter_particles():
                ...  #do stuff; it will iterate over all the particles
                #take the particle back to the container so it will be updated
                #in case we need it
                part_container.update_particle(particle)
        """
        if uids is None:
            return self._iter_all(
                self._particles, clone=Particle.from_particle)
        else:
            return self._iter_elements(
                self._particles, uids, clone=Particle.from_particle)

    def iter_bonds(self, uids=None):
        """Generator method for iterating over the bonds of the container.

        It can receive any kind of sequence of bond ids to iterate over
        those concrete bond. If nothing is passed as parameter, it will
        iterate over all the bonds.

        Parameters
        ----------

        uids : iterable of uuid.UUID, optional
            sequence containing the id's of the bond that will be iterated.
            When the uids are provided, then the bonds are returned in
            the same order the uids are returned by the iterable. If uids is
            None, then all bonds are returned by the interable and there
            is no restriction on the order that they are returned.

        Yields
        ------
        Yields each bond to be used.

        Raises
        ------
        KeyError exception if any of the ids passed as parameters are not
        in the container.

        Examples
        --------
        It can be used with a sequence as parameter or without it:

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> for bond in part_container.iter_bonds([id1, id2, id3]):
                ...  #do stuff
                #take the bond back to the container so it will be updated
                #in case we need it
                part_container.update_bond(bond)

        >>> for bond in part_container.iter_bond():
                ...  #do stuff; it will iterate over all the bond
                #take the bond back to the container so it will be updated
                #in case we need it
                part_container.update_bond(bond)
        """

        if uids is None:
            return self._iter_all(self._bonds, clone=Bond.from_bond)
        else:
            return self._iter_elements(
                self._bonds, uids, clone=Bond.from_bond)

    def has_particle(self, uid):
        """Checks if a particle with the given id already exists
        in the container."""
        return uid in self._particles

    def has_bond(self, uid):
        """Checks if a bond with the given id already exists
        in the container."""
        return uid in self._bonds

    # Utility methods ########################################################

    def _iter_elements(self, cur_dict, cur_ids, clone):
        for cur_id in cur_ids:
            item = cur_dict[cur_id]
            yield clone(item)

    def _iter_all(self, cur_dict, clone):
        for cur_element in cur_dict.itervalues():
            yield clone(cur_element)

    def _add_element(self, cur_dict, element, clone):
        # We check if the current dictionary has the element
        cur_id = element.uid
        if cur_id is None:
            cur_id = uuid.uuid4()
            element.uid = cur_id
            cur_dict[cur_id] = clone(element)
        else:
            if cur_id not in cur_dict:
                # Means the element is not in the dict - hence we can add it
                cur_dict[cur_id] = clone(element)
            else:
                message = "Item with id:{} already exists"
                raise ValueError(message.format(element))
        return cur_id

    def _update_element(self, cur_dict, element, clone):
        uid = element.uid
        if uid in cur_dict:
            cur_dict[uid] = clone(element)
        else:
            raise ValueError('id: {} does not exist'.format(uid))


class Particle(object):
    """Class representing a particle.

    Attributes
    ----------
    uid : uuid.UUID
        the unique id of the particle
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
    """Class reprensenting a bond.

    Attributes
    ----------
    uid : uuid.UUID
        the unique id of the bond
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
            raise Exception(pce._PC_errors['IncorrectParticlesTuple'])

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
