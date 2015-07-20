# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class ABCParticles(object):
    """Abstract base class for a container of particles items.

    Attributes
    ----------
    name : str
        name of particles item.
    data : DataContainer
        The data associated with the container

    """
    __metaclass__ = ABCMeta

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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
        >>> particles.update_bonds([bond1, bond2])

        """

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
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

        >>> particles = Particles(name="foo")
        >>> ...
        >>> for particle in particles.iter_particles([uid1, uid2, uid3]):
                ...  #do stuff
                #take the particle back to the container so it will be updated
                #in case we need it
                part_container.update_particle(particle)

        >>> for particle in particles.iter_particles():
                ...  #do stuff; it will iterate over all the particles
                #take the particle back to the container so it will be updated
                #in case we need it
                particles.update_particle(particle)

        """

    @abstractmethod
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

        >>> particles = Particles(name="foo")
        >>> ...
        >>> for bond in particles.iter_bonds([id1, id2, id3]):
                ...  #do stuff

        >>> for bond in particles.iter_bond():
                ...  #do stuff; it will iterate over all the bond
        """

    @abstractmethod
    def has_particle(self, uid):
        """Checks if a particle with the given uid already exists
        in the container."""

    @abstractmethod
    def has_bond(self, uid):
        """Checks if a bond with the given uid already exists
        in the container."""

    @abstractmethod
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
