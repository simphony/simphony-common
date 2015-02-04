# -*- coding: utf-8 -*-
"""
    Module for Particle classes:

        ParticleContainer ------> Concrete implementation of the Particles
           Containter class for stand-alone use of the container within python.
        Particle ----------------> Concrete implementation of the class repre-
           senting the Particles and Atoms for stand-alone use.
        Bond --------------------> Concrete implementation of the class repre-
           senting the bonds between Particles or Atoms. This class should re-
           present any kind of interaction (between atoms, molecules, etc.)
"""
from __future__ import print_function
import uuid

from simphony.cuds.abstractparticles import ABCParticleContainer
import simphony.cuds.pcexceptions as pce
from simphony.core.data_container import DataContainer


class ParticleContainer(ABCParticleContainer):
    """Class that represents a container of particles and bonds.

    Class provides methods to add particles and bonds, remove them and update
    them.

    Parameters
    ----------
    name : str
        name of the particle container

    Attributes
    ----------
    name : str
        name of the particle container
    _particles : dictionary
        data structure for particles storage
    _bonds : dictionary
        data structure for bonds storage
    data : DataContainer
        data attributes of the element

    """
    def __init__(self, name):
        self._particles = {}
        self._bonds = {}
        self.data = DataContainer()
        self.name = name

# ================================================================

    # overriden methods of the ABC

# ================================================================

    def add_particle(self, new_particle):
        """Adds the 'new_particle' particle to the container.

        If the new particle has no id, the particle container
        will generate a new unique id for it. If the particle has
        already an id (user set), it won't add the particle if a particle
        with the same id already exists. If the user wants to replace
        an existing particle in the container there is an 'update_particle'
        method for that purpose.

        Parameters
        ----------
        new_particle : Particle
            the new particle that will be included in the container.

        Returns
        -------
        id : uuid.UUID
            The id of the added particle.

        Raises
        ------
        Exception when the new particle already exists in the container.

        See Also
        --------
        update_particle, remove_particle

        Examples
        --------
        Having a Particle and a ParticleContainer just call the function
        passing the Particle as parameter.

        >>> part = Particle()
        >>> part_container = ParticleContainer(name="foo")
        >>> part_container.add_particle(part)
        """
        return self._add_element(
            self._particles, new_particle, clone=Particle.from_particle)

    def add_bond(self, new_bond):
        """Adds the 'new_bond' bond to the container.

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
        id : uuid.UUID
            The id of the added bond.

        Raises
        ------
        Exception when the new particle already exists in the container.

        See Also
        --------
        update_bond, remove_bond

        Examples
        --------
        Having a Bond and a ParticleContainer just call the function
        passing the Bond as parameter.

        >>> bond = Bond()
        >>> part_container = ParticleContainer(name="foo")
        >>> part_container.add_bond(bond)
        """
        return self._add_element(self._bonds, new_bond, Bond.from_bond)

    def update_particle(self, particle):
        """Replaces an existing particle with the 'particle' new particle.

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
        KeyError exception if the particle doesn't exists.

        See Also
        --------
        add_particle, remove_particle

        Examples
        --------
        Having a Particle that already exists in the container (taken with the
        'get_particle' method for example) and a ParticleContainer just call
        the function passing the Particle as parameter.

        >>> part_container = ParticleContainer(name="foo")
        >>> ...
        >>> part = part_container.get_particle(id)
        >>> ... #do whatever you want with the particle
        >>> part_container.update_particle(part)
        """
        self._update_element(
            self._particles, particle, clone=Particle.from_particle)

    def update_bond(self, bond):
        """Replaces an existing bond with the 'bond' new bond.

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
        KeyError exception if the bond doesn't exists.

        See Also
        --------
        add_bond, remove_bond

        Examples
        --------
        Having a Bond that already exists in the container (taken with the
        'get_bond' method for example) and a ParticleContainer just call the
        function passing the Bond as parameter.

        >>> part_container = ParticleContainer(name="foo")
        >>> ...
        >>> bond = part_container.get_bond(id)
        >>> ... #do whatever you want with the bond
        >>> part_container.update_bond(bond)
        """
        self._update_element(self._bonds, bond, clone=Bond.from_bond)

    def get_particle(self, particle_id):
        """Returns a copy of the particle with the 'particle_id' id.

        Parameters
        ----------

        particle_id : uint32
            the id of the particle

        Raises
        ------
        KeyError when the particle is not in the container.

        Returns
        -------
        A copy of the particle
        """
        try:
            particle = self._particles[particle_id]
        except KeyError:
            raise KeyError(
                'Particle with id {} not found!'.format(particle_id))
        return Particle.from_particle(particle)

    def get_bond(self, bond_id):
        """Returns a copy of the bond with the 'bond_id' id.

        Parameters
        ----------

        bond_id : uint32
            the id of the bond

        Raises
        ------
        KeyError when the bond is not in the container.

        Returns
        -------
        A copy of the bond
        """
        try:
            bond = self._bonds[bond_id]
        except KeyError:
            raise KeyError(
                'Bond with id {} not found!'.format(bond_id))
        return Bond.from_bond(bond)

    def remove_particle(self, particle_id):
        """Removes the particle with the 'particle_id' id from the container.

        The id passed as parameter should exists in the container. Otherwise
        an expcetion will be raised.

        Parameters
        ----------

        particle_id : Particle
            the id of the particle to be removed.

        Raises
        ------
        KeyError exception if the particle doesn't exist.

        See Also
        --------
        add_particle, update_particle

        Examples
        --------
        Having an id of an existing particle, pass it to the function.

        >>> part_container = ParticleContainer(name="foo")
        >>> ...
        >>> part = part_container.get_particle(id)
        >>> ...
        >>> part_container.remove_particle(part.id)
        or directly
        >>> part_container.remove_particle(id)
        """

        try:
            self._remove_element(self._particles, particle_id)
        except KeyError:
            raise KeyError(
                'Particle with id { } not found!'.format(particle_id))

    def remove_bond(self, bond_id):
        """Removes the bond with the 'bond_id' id from the container.

        The id passed as parameter should exists in the container. If
        it doesn't exists, nothing will happen.

        Parameters
        ----------

        bond_id : Bond
            the id of the bond to be removed.

        See Also
        --------
        add_bond, update_bond

        Examples
        --------
        Having an id of an existing bond, pass it to the function.

        >>> part_container = ParticleContainer(name="foo")
        >>> ...
        >>> bond = part_container.get_bond(id)
        >>> ...
        >>> part_container.remove_bond(bond.id)
        or directly
        >>> part_container.remove_bond(id)
        """

        try:
            self._remove_element(self._bonds, bond_id)
        except KeyError:
            raise KeyError(
                'Bond with id { } not found!'.format(bond_id))

    def iter_particles(self, particle_ids=None):
        """Generator method for iterating over the particles of the container.

        It can recieve any kind of sequence of particle ids to iterate over
        those concrete particles. If nothing is passed as parameter, it will
        iterate over all the particles.

        Parameters
        ----------

        particle_ids : array_like
            sequence containing the id's of the particles that will be
            iterated.

        Yields
        -------
        Yields each particle to be used.

        Raises
        ------
        KeyError exception if any of the ids passed as parameters are not
        in the container.

        See Also
        --------
        iter_bonds, add_particle, remove_particle, update_particle

        Examples
        --------
        It can be used with a sequence as parameter or withouth it:

        >>> part_container = ParticleContainer(name="foo")
        >>> ...
        >>> for particle in part_container.iter_particles([id1, id2, id3]):
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
        if particle_ids is not None:
            return self._iter_elements(
                self._particles, particle_ids, clone=Particle.from_particle)
        else:
            return self._iter_all(
                self._particles, clone=Particle.from_particle)

    def iter_bonds(self, bond_ids=None):
        """Generator method for iterating over the bonds of the container.

        It can recieve any kind of sequence of bond ids to iterate over
        those concrete bond. If nothing is passed as parameter, it will
        iterate over all the bonds.

        Parameters
        ----------

        bond_ids : array_like
            sequence containing the id's of the bond that will be iterated.

        Yields
        -------
        Yields each bond to be used.

        Raises
        ------
        KeyError exception if any of the ids passed as parameters are not
        in the container.

        See Also
        --------
        iter_particles, add_bond, remove_bond, update_bond

        Examples
        --------
        It can be used with a sequence as parameter or withouth it:

        >>> part_container = ParticleContainer(name="foo")
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

        if bond_ids is not None:
            return self._iter_elements(
                self._bonds, bond_ids, clone=Bond.from_bond)
        else:
            return self._iter_all(self._bonds, clone=Bond.from_bond)

    def has_particle(self, id):
        """Checks if a particle with the given id already exists
        in the container."""
        return id in self._particles

    def has_bond(self, id):
        """Checks if a bond with the given id already exists
        in the container."""
        return id in self._bonds

# ================================================================

    # private methods to make the code more readable and compact

# ================================================================

    def _iter_elements(self, cur_dict, cur_ids, clone):
        for cur_id in cur_ids:
            try:
                yield clone(cur_dict[cur_id])
            except KeyError:
                raise KeyError('id {} not found!'.format(cur_id))

    def _iter_all(self, cur_dict, clone):
        for cur_element in cur_dict.itervalues():
            yield clone(cur_element)

    def _add_element(self, cur_dict, element, clone):
        # We check if the current dictionary has the element
        cur_id = element.id
        if cur_id is None:
            cur_id = uuid.uuid4()
            element.id = cur_id
            cur_dict[cur_id] = clone(element)
        else:
            if cur_id not in cur_dict:
                # Means the element is not in the dict - hence we can add it
                cur_dict[cur_id] = clone(element)
            else:
                raise Exception(
                    pce._PC_errors['ParticleContainer_DuplicatedValue']
                    + " id: " + str(cur_id))
        return cur_id

    def _update_element(self, cur_dict, element, clone):
        cur_id = element.id
        if cur_id in cur_dict:
            # This means the element IS in the current dictionary
            # (this should be the standard case...), so we proceed
            cur_dict[cur_id] = clone(element)
        else:
            raise KeyError(pce._PC_errors['ParticleContainer_UnknownValue']
                           + " id: " + str(cur_id))

    def _remove_element(self, cur_dict, cur_id):
        if cur_id in cur_dict:
            # Element IS in dict, we proceed
            del cur_dict[cur_id]
        else:
            raise KeyError(pce._PC_errors['ParticleContainer_UnknownValue']
                           + " id: " + str(cur_id))


class Particle(object):
    """Class representing a particle.

    Attributes
    ----------
        id : uint32
            the unique id of the particle
        coordinates : list / tuple
            x,y,z coordinates of the particle
        data : DataContainer
            DataContainer to store the attributes of the particle

    """

    def __init__(self, coordinates=(0.0, 0.0, 0.0), id=None, data=None):
        """ Create a Particle.

        Parameters
        ----------
        coordinates : list / tuple
            x,y,z coordinates of the particle (Default: [0, 0, 0])
        id : uuid.UUID
            the id, None as default (the particle container will generate it)
        data : DataContainer
            the data, the particle will have a copy of this
        """

        self.id = id
        self.coordinates = tuple(coordinates)
        if data is None:
            self.data = DataContainer()
        else:
            self.data = DataContainer(data)

    @classmethod
    def from_particle(cls, particle):
        return cls(
            id=uuid.UUID(bytes=particle.id.bytes),
            coordinates=particle.coordinates,
            data=DataContainer(particle.data))

    def __str__(self):
        total_str = "{0}_{1}".format(self.id, self.coordinates)
        return total_str


class Bond(object):
    """Class reprensenting a bond.

    Attributes
    ----------
        id : uuid
            the unique id of the bond
        particles : tuple
            tuple of uuids of the particles that are participating in the bond.
        data : DataContainer
            DataContainer to store the attributes of the bond

    """

    def __init__(self, particles, id=None, data=None):
        """ Create a Bond.

        Parameters
        ----------
        particles : sequence
            list of particles of the bond. It can not be empty.
        id : uuid.UUID
            the id, None as default (the particle container will generate it)
        data : DataContainer
            DataContainer to store the attributes of the bond

        """
        self.id = id
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
            id=uuid.UUID(bytes=bond.id.bytes),
            data=DataContainer(bond.data))

    def __str__(self):
        total_str = "{0}_{1}".format(self.id, self.particles)
        return total_str


def main():
    print("""
            Module for Particle classes:
                ParticleContainer ------> Concrete implementation of the
                    Particles Containter class for stand-alone use of the
                    container within python.
                Particle ----------------> Concrete implementation of the
                    class representing the Particles and Atoms for stand-alone
                    use.
                Bond --------------------> Concrete implementation of the class
                    representing the bonds between Particles or Atoms.
                    This class should represent any kind of interaction
                    (between atoms, molecules, etc.)
           """)

if __name__ == '__main__':
    main()
