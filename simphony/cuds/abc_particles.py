# -*- coding: utf-8 -*-
from abc import abstractmethod
import itertools

from ..core.cuds_item import CUDSItem
from .particles_items import Particle, Bond
from .abc_dataset import ABCDataset
from .utils import deprecated


class ABCParticles(ABCDataset):
    """Abstract base class for a container of particles items.

    Attributes
    ----------
    name : str
        name of particles item.
    data : DataContainer
        The data associated with the container

    """

    def add(self, iterable):
        """Adds a set of objects from the provided iterable
        to the dataset.

        If any object has no uids, the dataset will generate a new
        uid for it. If the object has already an uid, it won't add the
        object if an object with the same type uid already exists.
        If the user wants to replace an existing object in the container
        there is an 'update' method for that purpose.

        Parameters
        ----------
        iterable : iterable of objects
            the new set of objects that will be included in the container.

        Returns
        -------
        uids : list of uuid.UUID
            The uids of the added objects.

        Raises
        ------
        ValueError :
            when there is an object with an uids that already exists
            in the dataset.
        """
        uids = []
        for item in iterable:
            if isinstance(item, Particle):
                uids.extend(self._add_particles([item]))
            elif isinstance(item, Bond):
                uids.extend(self._add_bonds([item]))
            else:
                raise TypeError("Unrecognised item type {!r}".format(item))

        return uids

    def update(self, iterable):
        """Updates objects from the provided iterable.

        Takes the uids of the objects and searches inside the container for
        those objects. If they exists, they are replaced in the
        container. If any object doesn't exist, it will raise an exception.

        Parameters
        ----------

        iterable : iterable
            the objects (Particle or Bond) that will be replaced.

        Raises
        ------
        ValueError :
            If any object inside the iterable does not exist.

        Examples
        --------
        Given a set of objects that already exists in the container
        (taken with the 'get_particle' method for example), just call the
        function passing the Particle items as parameter.

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> part1 = part_container.get(uid1)
        >>> part2 = part_container.get(uid2)
        >>> ... #do whatever you want with the particles
        >>> part_container.update([part1, part2])
        """
        for item in iterable:
            if isinstance(item, Particle):
                self._update_particles([item])
            elif isinstance(item, Bond):
                self._update_bonds([item])
            else:
                raise TypeError("Unrecognised item type")

    def get(self, uid):
        """Returns a copy of the object with the specified uid

        Parameters
        ----------
        uid : uuid.UUID
            the uid of the bond

        Raises
        ------
        KeyError :
           when the object is not in the container.

        Returns
        -------
        object : Particle or Bond
            A copy of the internally stored object.
        """
        try:
            return self._get_particle(uid)
        except KeyError:
            pass

        try:
            return self._get_bond(uid)
        except KeyError:
            pass

        raise KeyError("Unknown uid {}".format(uid))

    def remove(self, uids):
        """Remove the object with the provided uids from the container.

        The uids inside the iterable should exists in the container. Otherwise
        an exception will be raised.

        Parameters
        ----------
        uids : iterable of uuid.UUID
            the uids of the objects to be removed.

        Raises
        ------
        KeyError :
           If any object doesn't exist.

        Examples
        --------
        Having a set of uids of existing objects, pass it to the method.

        >>> particles = Particles(name="foo")
        >>> ...
        >>> particle1 = particles.get(uid1)
        >>> particle2 = particles.get(uid2)
        >>> ...
        >>> particles.remove([part1.uid, part2.uid)
        or directly
        >>> particles.remove([uid1, uid2])
        """
        for uid in uids:
            try:
                self._remove_particles([uid])
                continue
            except KeyError:
                pass

            try:
                self._remove_bonds([uid])
                continue
            except KeyError:
                pass

            raise KeyError("uid {} not found".format(uid))

    def iter(self, uids=None, item_type=None):
        """Generator method for iterating over the objects of the container.

        It can receive any kind of sequence of uids to iterate over
        those concrete objects. If nothing is passed as parameter, it will
        iterate over all the objects in undefined order.

        Parameters
        ----------
        uids : iterable of uuid.UUID, optional
            sequence containing the uids of the objects that will be
            iterated. When the uids are provided, then the objects are
            returned in the same order the uids are returned by the iterable.
            If uids is None, then all particles are returned by the iterable
            and there is no restriction on the order that they are returned.

        item_type: CUDSItem enum
            Restricts iteration only to the specified item type.
            e.g. CUDSItem.PARTICLE will only iterate over particles.

        Yields
        ------
        object : Particle or Bond
            The Particle or Bond item.

        Raises
        ------
        KeyError :
            if any of the ids passed as parameters are not in the container.

        Examples
        --------
        It can be used with a sequence as parameter or without it:

        >>> part_container = Particles(name="foo")
        >>> ...
        >>> for particle in part_container.iter([uid1, uid2, uid3]):
                ...  #do stuff
                #take the particle back to the container so it will be updated
                #in case we need it
                part_container.update([particle])

        >>> for particle in part_container.iter():
                ...  #do stuff; it will iterate over all the particles
                #take the particle back to the container so it will be updated
                #in case we need it
                part_container.update([particle])
        """

        if item_type == CUDSItem.PARTICLE:
            return self._iter_particles(uids)
        elif item_type == CUDSItem.BOND:
            return self._iter_bonds(uids)
        else:
            if uids is None:
                return itertools.chain(
                    self._iter_particles(),
                    self._iter_bonds())
            else:
                return self._iter_uids(uids)

    def has(self, uid):
        """Checks if an object with the given uid already exists
        in the dataset.

        Parameters
        ----------
        uid : uuid.UUID
            the uid of the object

        Returns
        -------
        True if the uid is found, False otherwise.
        """
        return self._has_particle(uid) or self._has_bond(uid)

    def has_type(self, item_type):
        """Checks if the specified CUDSItem type is present
        in the dataset.

        Parameters
        ----------
        item_type : CUDSItem
            The CUDSItem enum of the type of the items to return the count of.

        Returns
        -------
        True if the type is present, False otherwise.
        """
        raise NotImplementedError()

    def __len__(self):
        """Returns the total number of items in the container.

        Returns
        -------
        count : int
            The number of items in the dataset.
        """
        return sum(map(lambda x: self.count_of(x),
                       [CUDSItem.PARTICLE, CUDSItem.BOND]))

    # Deprecated API. Will go away. Uses the generic API instead of direct
    # call to the internal methods to guarantee the behavior is unchanged
    # through the generic interface.

    @deprecated
    def add_particles(self, iterable):  # pragma: no cover
        """
        Deprecated. Use add() instead.

        Adds a set of particles from the provided iterable
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
        return self.add(iterable)

    @deprecated
    def add_bonds(self, iterable):  # pragma: no cover
        """
        Deprecated. Use add() instead.

        Adds a set of bonds to the container.

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
        >>> particles.add_bonds(bonds_list)

        """
        return self.add(iterable)

    @deprecated
    def update_particles(self, iterable):  # pragma: no cover
        """
        Deprecated. use update() instead.

        Updates a set of particles from the provided iterable.

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
        >>> ... #do whatever you want with the particles
        >>> part_container.update_particles([part1, part2])

        """
        self.update(iterable)

    @deprecated
    def update_bonds(self, iterable):  # pragma: no cover
        """Deprecated. use update() instead.

        Updates a set of bonds from the provided iterable.

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
        self.update(iterable)

    @deprecated
    def get_particle(self, uid):  # pragma: no cover
        """
        Deprecated. use get() instead.

        Returns a copy of the particle with the 'particle_id' id.

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
        return self.get(uid)

    @deprecated
    def get_bond(self, uid):  # pragma: no cover
        """
        Deprecated. Use uid instead.

        Returns a copy of the bond with the 'bond_id' id.

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
        return self.get(uid)

    @deprecated
    def remove_particles(self, uids):  # pragma: no cover
        """
        Deprecated. use remove() instead.

        Remove the particles with the provided uids from the container.

        The uids inside the iterable should exists in the container. Otherwise
        an exception will be raised.

        Parameters
        ----------
        uids : iterable of uuid.UUID
            the uids of the particles to be removed.

        Raises
        ------
        KeyError :
            If any particle doesn't exist.

        Examples
        --------
        Having a set of uids of existing particles, pass it to the method.

        >>> particles = Particles(name="foo")
        >>> ...
        >>> particles.remove_particles([uid1, uid2])
        """
        self.remove(uids)

    @deprecated
    def remove_bonds(self, uids):  # pragma: no cover
        """
        Deprecated. use remove() instead.

        Remove the bonds with the provided uids.

        The uids passed as parameter should exists in the container. If
        any uid doesn't exist, an exception will be raised.

        Parameters
        ----------
        uids : iterable of uuid.UUID
            the uids of the bond to be removed.

        Raises
        ------
        KeyError :
            If any bond doesn't exist.

        Examples
        --------
        Having a set of uids of existing bonds, pass it to the method.

        >>> particles = Particles(name="foo")
        >>> ...
        >>> particles.remove_bonds([uid1, uid2])
        """
        self.remove(uids)

    @deprecated
    def iter_particles(self, uids=None):  # pragma: no cover
        """
        Deprecated. use iter() instead.

        Generator method for iterating over the particles of the container.

        It can receive any kind of sequence of particle uids to iterate over
        those concrete particles. If nothing is passed as parameter, it will
        iterate over all the particles.

        Parameters
        ----------
        uids : iterable of uuid.UUID, optional
            sequence containing the uids of the particles that will be
            iterated. When the uids are provided, then the particles are
            returned in the same order the uids are returned by the iterable.
            If uids is None, then all particles are returned by the iterable
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
        >>> for particle in particles.iter_particles():
            ...  #do stuff
        """
        return self.iter(uids, item_type=CUDSItem.PARTICLE)

    @deprecated
    def iter_bonds(self, uids=None):  # pragma: no cover
        """
        Deprecated. use iter() instead.

        Generator method for iterating over the bonds of the container.

        It can receive any kind of sequence of bond ids to iterate over
        those concrete bond. If nothing is passed as parameter, it will
        iterate over all the bonds.

        Parameters
        ----------

        uids : iterable of uuid.UUID, optional
            sequence containing the id's of the bond that will be iterated.
            When the uids are provided, then the bonds are returned in
            the same order the uids are returned by the iterable. If uids is
            None, then all bonds are returned by the iterable and there
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
        return self.iter(uids, item_type=CUDSItem.BOND)

    @deprecated
    def has_particle(self, uid):  # pragma: no cover
        """Deprecated. use has() instead.

        Checks if a particle with the given uid already exists
        in the container."""
        return self.has(uid)

    @deprecated
    def has_bond(self, uid):  # pragma: no cover
        """Deprecated. Use has() instead.

        Checks if a bond with the given uid already exists
        in the container."""
        return self.has(uid)

    # Internal per-type implementation. Mirrors the above but must be
    # reimplemented by subclasses.

    @abstractmethod
    def _add_particles(self, iterable):  # pragma: no cover
        pass

    @abstractmethod
    def _add_bonds(self, iterable):  # pragma: no cover
        pass

    @abstractmethod
    def _update_particles(self, iterable):  # pragma: no cover
        pass

    @abstractmethod
    def _update_bonds(self, iterable):  # pragma: no cover
        pass

    @abstractmethod
    def _get_particle(self, uid):  # pragma: no cover
        pass

    @abstractmethod
    def _get_bond(self, uid):  # pragma: no cover
        pass

    @abstractmethod
    def _remove_particles(self, uids):  # pragma: no cover
        pass

    @abstractmethod
    def _remove_bonds(self, uids):  # pragma: no cover
        pass

    @abstractmethod
    def _iter_particles(self, uids=None):  # pragma: no cover
        pass

    @abstractmethod
    def _iter_bonds(self, uids=None):  # pragma: no cover
        pass

    @abstractmethod
    def _has_particle(self, uid):  # pragma: no cover
        pass

    @abstractmethod
    def _has_bond(self, uid):  # pragma: no cover
        pass

    # Private implementation

    def _iter_uids(self, uids):
        """Iterates over a series of uids

        Parameters
        ----------
        uids: iterable
            iterable with the uids to return

        Yields
        ------
        The items corresponding to the uids.
        """
        for uid in uids:
            yield self.get(uid)
