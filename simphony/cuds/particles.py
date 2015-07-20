# -*- coding: utf-8 -*-
import uuid

from simphony.cuds.abc_particles import ABCParticles
from simphony.core.cuds_item import CUDSItem
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

        self._items_count = {
            CUDSItem.PARTICLE: lambda: self._particles,
            CUDSItem.BOND: lambda: self._bonds
        }

    @property
    def data(self):
        return DataContainer(self._data)

    @data.setter
    def data(self, new_data):
        self._data = DataContainer(new_data)

    def add_particles(self, iterable):
        """Adds a set of particles from the provided iterable
        to the container.

        If any particle have no uids, the container
        will generate a new uids for it. If the particle has
        already an uids, it won't add the particle if a particle
        with the same uid already exists. If the user wants to replace
        an existing particle in the container there is an 'update_particles'
        method for that purpose.

        Parameters
        ----------
        iterable : iterable of Particle objects
            the new set of particles that will be included in the container.

        Returns
        -------
        uids : list of uuid.UUID
            The uids of the added particles.

        Raises
        ------
        ValueError :
            when there is a particle with an uids that already exists
            in the container.

        Examples
        --------
        Add a set of particles to a Particles container.

        >>> particle_list = [Particle(), Particle()]
        >>> particles = Particles(name="foo")
        >>> uids = particles.add_particles(particle_list)

        """
        uids = []
        for particle in iterable:
            uid = self._add_element(
                self._particles, particle, clone=Particle.from_particle)
            uids.append(uid)
        return uids

    def add_bonds(self, iterable):
        """Adds a set of bonds to the container.

        Also like with particles, if any bond has a defined uid,
        it won't add the bond if a bond with the same uid already exists, and
        if the bond has no uid the particle container will generate an
        uid. If the user wants to replace an existing bond in the
        container there is an 'update_bonds' method for that purpose.

        Parameters
        ----------
        iterable : iterable of Bond objects
            the new bond that will be included in the container.

        Returns
        -------
        uuid : list of uuid.UUID
            The uuids of the added bonds.

        Raises
        ------
        ValueError :
            when there is a bond with an uuid that already exists
            in the container.

        Examples
        --------
        Add a set of bonds to a Particles container.

        >>> bonds_list = [Bond(), Bond()]
        >>> particles = Particles(name="foo")
        >>> particles.add_bond(bonds_list)

        """
        uids = []
        for bond in iterable:
            uid = self._add_element(self._bonds, bond, Bond.from_bond)
            uids.append(uid)
        return uids

    def update_particles(self, iterable):
        """Updates a set of particles from the provided iterable.

        Takes the uids of the particles and searches inside the container for
        those particles. If the particles exists, they are replaced in the
        container. If any particle doesn't exist, it will raise an exception.

        Parameters
        ----------

        iterable : iterable of Particle objects
            the particles that will be replaced.

        Raises
        ------
        ValueError :
            If any particle inside the iterable does not exist.

        Examples
        --------
        Given a set of Particle objects that already exists in the container
        (taken with the 'get_particle' method for example), just call the
        function passing the Particle items as parameter.

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> part1 = part_container.get_particle(uid1)
        >>> part2 = part_container.get_particle(uid2)
        >>> ... #do whatever you want with the particles
        >>> part_container.update_particle([part1, part2])

        """
        for particle in iterable:
            self._update_element(
                self._particles, particle, clone=Particle.from_particle)

    def update_bonds(self, iterable):
        """Updates a set of bonds from the provided iterable.

        Takes the uids of the bonds and searches inside the container for
        those bond. If the bonds exists, they are replaced in the container.
        If any bond doesn't exist, it will raise an exception.

        Parameters
        ----------
        iterable : iterable of Bond objects
            the bonds that will be replaced.

        Raises
        ------
        ValueError :
            If any bond doesn't exist.

        Examples
        --------
        Given a set of Bond objects that already exists in the container
        (taken with the 'get_bond' method for example) just call the
        function passing the set of Bond as parameter.

        >>> particles = Particles(name="foo")
        >>> ...
        >>> bond1 = particles.get_bond(uid1)
        >>> bond2 = particles.get_bond(uid2)
        >>> ... #do whatever you want with the bonds
        >>> particles.update_bond([bond1, bond2])

        """
        for bond in iterable:
            self._update_element(self._bonds, bond, clone=Bond.from_bond)

    def get_particle(self, uid):
        """Returns a copy of the particle with the 'particle_id' id.

        Parameters
        ----------

        uid : uuid.UUID
            the uid of the particle

        Raises
        ------
        KeyError :
           when the particle is not in the container.

        Returns
        -------
        particle : Particle
            A copy of the internally stored particle info.

        """
        particle = self._particles[uid]
        return Particle.from_particle(particle)

    def get_bond(self, uid):
        """Returns a copy of the bond with the 'bond_id' id.

        Parameters
        ----------
        uid : uuid.UUID
            the uid of the bond

        Raises
        ------
        KeyError :
           when the bond is not in the container.

        Returns
        -------
        bond : Bond
            A copy of the internally stored bond info.

        """
        bond = self._bonds[uid]
        return Bond.from_bond(bond)

    def remove_particles(self, uids):
        """Remove the particles with the provided uids from the container.

        The uids inside the iterable should exists in the container. Otherwise
        an exception will be raised.

        Parameters
        ----------
        uid : uuid.UUID
            the uid of the particle to be removed.

        Raises
        ------
        KeyError :
           If any particle doesn't exist.


        Examples
        --------
        Having a set of uids of existing particles, pass it to the method.

        >>> particles = Particles(name="foo")
        >>> ...
        >>> particle1 = particles.get_particle(uid1)
        >>> particle2 = particles.get_particle(uid2)
        >>> ...
        >>> particles.remove_particle([part1.uid, part2.uid)
        or directly
        >>> particles.remove_particle([uid1, uid2])

        """
        for uid in uids:
            del self._particles[uid]

    def remove_bonds(self, uids):
        """Remove the bonds with the provided uids.

        The uids passed as parameter should exists in the container. If
        any uid doesn't exist, an exception will be raised.

        Parameters
        ----------
        uids : uuid.UUID
            the uid of the bond to be removed.

        Examples
        --------
        Having a set of uids of existing bonds, pass it to the method.

        >>> particles = Particles(name="foo")
        >>> ...
        >>> bond1 = particles.get_bond(uid1)
        >>> bond2 = particles.get_bond(uid2)
        >>> ...
        >>> particles.remove_bonds([bond1.uid, bond2.uid])
        or
        >>> particles.remove_bond([uid1, uid2])

        """
        for uid in uids:
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
            The Particle item.

        Raises
        ------
        KeyError :
            if any of the ids passed as parameters are not in the container.

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
        bond : Bond
           The next Bond item

        Raises
        ------
        KeyError :
            if any of the ids passed as parameters are not in the container.

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
        """Checks if a particle with the given uid already exists
        in the container."""
        return uid in self._particles

    def has_bond(self, uid):
        """Checks if a bond with the given uid already exists
        in the container."""
        return uid in self._bonds

    def count_of(self, item_type):
        """ Return the count of item_type in the container.

        Parameters
        ----------
        item_type : CUDSItem
            The CUDSItem enum of the type of the items to return the count of.

        Returns
        -------
        count : int
            The number of items of item_type in the container.

        Raises
        ------
        ValueError :
            If the type of the item is not supported in the current
            container.

        """
        try:
            return len(self._items_count[item_type]())
        except KeyError:
            error_str = "Trying to obtain count a of non-supported item: {}"
            raise ValueError(error_str.format(item_type))

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
