# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod


class ABCDataset(object):
    """Abstract base class for a dataset.

    Attributes
    ----------
    name : str
        name of dataset item.
    data : DataContainer
        The data associated with the container
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, iterable):  # pragma: no cover
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

        Examples
        --------
        Add a set of particles

        >>> particle_list = [Particle(), Particle()]
        >>> particles = Particles(name="foo")
        >>> uids = particles.add(particle_list)
        """

    @abstractmethod
    def update(self, iterable):  # pragma: no cover
        """Updates a set of objects from the provided iterable.

        Takes the uids of the objects and searches inside the dataset for
        those objects. If the object exists, they are replaced in the
        dataset. If any object doesn't exist, it will raise an exception.

        Parameters
        ----------

        iterable : iterable of objects
            the objects that will be replaced.

        Raises
        ------
        ValueError :
            If any object inside the iterable does not exist.

        Examples
        --------
        Given a set of objects that already exists in the dataset
        (taken with the 'get' method for example), just call the
        function passing the items as parameter.

        >>> part_container = Particles(name="foo")
        >>> ... #do whatever you want with the particles
        >>> part_container.update([part1, part2])
        """

    @abstractmethod
    def get(self, uid):  # pragma: no cover
        """Returns a copy of the object with the 'uid' id.

        Parameters
        ----------

        uid : uuid.UUID
            the uid of the object

        Raises
        ------
        KeyError :
            when the object is not in the container.

        Returns
        -------
        object :
            A copy of the internally stored info.
        """

    @abstractmethod
    def remove(self, uids):  # pragma: no cover
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
        >>> particles.remove([uid1, uid2])
        """

    @abstractmethod
    def iter(self, uids=None, item_type=None):  # pragma: no cover
        """Generator method for iterating over the objects of the container.

        It can receive any kind of sequence of uids to iterate over
        those concrete objects. If nothing is passed as parameter, it will
        iterate over all the objects.

        Parameters
        ----------
        uids : iterable of uuid.UUID, optional
            sequence containing the uids of the objects that will be
            iterated. When the uids are provided, then the objects are
            returned in the same order the uids are returned by the iterable.
            If uids is None, then all objects are returned by the iterable
            and there is no restriction on the order that they are returned.

        Yields
        ------
        object : Particle
            The object item.

        Raises
        ------
        KeyError :
            if any of the ids passed as parameters are not in the dataset.

        Examples
        --------
        It can be used with a sequence as parameter or without it:

        >>> particles = Particles(name="foo")
        >>> ...
        >>> for object in particles.iter([uid1, uid2, uid3]):
            ...  #do stuff
        >>> for object in particles.iter():
            ...  #do stuff
        """

    @abstractmethod
    def has(self, uid):  # pragma: no cover
        """Checks if an object with the given uid already exists
        in the dataset."""

    def has_type(self, item_type):
        """Checks if an object with the given uid already exists
        in the dataset."""
        return self.count_of(item_type) != 0

    @abstractmethod
    def count_of(self, item_type):  # pragma: no cover
        """ Return the count of item_type in the container.

        Parameters
        ----------
        item_type : CUDSItem
            The CUDSItem enum of the type of the items to return the count of.

        Returns
        -------
        count : int
            The number of items of item_type in the dataset.

        Raises
        ------
        ValueError :
            If the type of the item is not supported in the current
            dataset.
        """
