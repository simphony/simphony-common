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
    def add_particle(self, particle):
        """Adds the particle to the container.

        If the new particle has no uid, the particle container
        will generate a new uid for it. If the particle has
        already an uid, it won't add the particle if a particle
        with the same uid already exists. If the user wants to replace
        an existing particle in the container there is an 'update_particle'
        method for that purpose.

        Parameters
        ----------
        particle : Particle
            the new particle that will be included in the container.

        Returns
        -------
        uid : uuid.UUID
            The uid of the added particle.

        Raises
        ------
        ValueError :
            when the new particle already exists in the container.

        Examples
        --------
        Having a Particle and a ParticleContainer just call the function
        passing the Particle as parameter.

        >>> part = Particle()
        >>> part_container = Particles(name="foo")
        >>> part_container.add_particle(part)

        """

    @abstractmethod
    def add_bond(self, bond):
        """Adds the bond to the container.

        Also like with particles, if the bond has a defined uid,
        it won't add the bond if a bond with the same uid already exists, and
        if the bond has no uid the particle container will generate an
        uid. If the user wants to replace an existing bond in the
        container there is an 'update_bond' method for that purpose.

        Parameters
        ----------
        new_bond : Bond
            the new bond that will be included in the container.

        Returns
        -------
        uid : uuid.UID
            The uid of the added bond.

        Raises
        ------
        ValueError :
            When the new particle already exists in the container.

        Examples
        --------
        Having a Bond and a ParticleContainer just call the function
        passing the Bond as parameter.

        >>> bond = Bond()
        >>> part_container = Particles(name="foo")
        >>> part_container.add_bond(bond)

        """

    @abstractmethod
    def update_particle(self, particle):
        """Replaces an existing particle.

        Takes the uid of 'particle' and searches inside the container for
        that particle. If the particle exists, it is replaced with the new
        particle passed as parameter. If the particle doesn't exist, it will
        raise an exception.

        Parameters
        ----------

        particle : Particle
            the particle that will be replaced.

        Raises
        ------
        ValueError :
            If the particle does not exist.

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

    @abstractmethod
    def update_bond(self, bond):
        """Replaces an existing bond.

        Takes the uid of 'bond' and searchs inside the container for
        that bond. If the bond exists, it is replaced with the new
        bond passed as parameter. If the bond doesn't exist, it will
        raise an exception.

        Parameters
        ----------
        bond : Bond
            the bond that will be replaced.

        Raises
        ------
        ValueError :
            If the bond doesn't exist.

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
    def remove_particle(self, uid):
        """Removes the particle with uid from the container.

        The uid passed as parameter should exists in the container. Otherwise
        an expcetion will be raised.

        Parameters
        ----------
        uid : uuid.UUID
            the uid of the particle to be removed.

        Raises
        ------
        KeyError :
           If the particle doesn't exist.


        Examples
        --------
        Having an uid of an existing particle, pass it to the function.

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> part = part_container.get_particle(uid)
        >>> ...
        >>> part_container.remove_particle(part.uid)
        or directly
        >>> part_container.remove_particle(uid)

        """

    @abstractmethod
    def remove_bond(self, uid):
        """Removes the bond with the uid from the container.

        The uid passed as parameter should exists in the container. If
        it doesn't exists, nothing will happen.

        Parameters
        ----------
        uid : uuid.UUID
            the uid of the bond to be removed.

        Examples
        --------
        Having an uid of an existing bond, pass it to the function.

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> bond = part_container.get_bond(id)
        >>> ...
        >>> part_container.remove_bond(bond.uid)
        or directly
        >>> part_container.remove_bond(id)

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

    @abstractmethod
    def has_particle(self, uid):
        """Checks if a particle with the given uid already exists
        in the container."""
        pass

    @abstractmethod
    def has_bond(self, uid):
        """Checks if a bond with the given uid already exists
        in the container."""
        pass
