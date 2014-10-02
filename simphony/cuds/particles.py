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
import copy
import random
import numpy as np
# custom imports:
from simphony.cuds.abstractparticles import ABCParticleContainer
import simphony.cuds.pcexceptions as pce
import simphony.core.data_container as dc


class ParticleContainer(ABCParticleContainer):
    """Class that represents a container of particles and bonds. It can
       add particles and bonds, remove them and update them.

       Attributes
       ----------
        _particles : dictionary
            data structure for particles storage
        _bonds : dictionary
            data structure for bonds storage
        data : DataContainer
            data attributes of the element
    """
    def __init__(self):
        self._particles = {}
        self._bonds = {}
        self._data = dc.DataContainer()

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
        >>> part_container = ParticleContainer()
        >>> part_container.add_particle(part)
        """

        try:
            self._add_element(self._particles, new_particle)
        except Exception as exc:
            raise exc

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

        Raises
        ------
        Exception when the new particle already exists in the container.

        See Also
        --------
        update_bond, remove_bond

        Notes
        -----

        Examples
        --------
        Having a Bond and a ParticleContainer just call the function
        passing the Bond as parameter.

        >>> bond = Bond()
        >>> part_container = ParticleContainer()
        >>> part_container.add_bond(bond)
        """

        try:
            self._add_element(self._bonds, new_bond)
        except Exception as exc:
            raise exc

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

        >>> part_container = ParticleContainer()
        >>> ...
        >>> part = part_container.get_particle(id)
        >>> ... #do whatever you want with the particle
        >>> part_container.update_particle(part)
        """

        try:
            self._update_element(self._particles, particle)
        except Exception as exc:
            raise exc

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

        >>> part_container = ParticleContainer()
        >>> ...
        >>> bond = part_container.get_bond(id)
        >>> ... #do whatever you want with the bond
        >>> part_container.update_bond(bond)
        """
        try:
            self._update_element(self._bonds, bond)
        except Exception as exc:
            raise exc

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
            cur_particle = self._particles[particle_id]
        except KeyError:
            raise KeyError('Particle with id { } not found!'.format(
                particle_id))
        return copy.deepcopy(cur_particle)

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
            cur_bond = self._bonds[bond_id]
        except KeyError:
            raise KeyError('Bond with id { } not found!'.format(
                bond_id))
        return copy.deepcopy(cur_bond)

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

        >>> part_container = ParticleContainer()
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
            raise KeyError('Particle with id { } not found!'.format(
                particle_id))

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

        >>> part_container = ParticleContainer()
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
            raise KeyError('Bond with id { } not found!'.format(
                bond_id))

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

        >>> part_container = ParticleContainer()
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

        if particle_ids:
            try:
                return self._iter_elements(self._particles, particle_ids)
            except KeyError as exception:
                raise exception
        else:
            return self._iter_all(self._particles)

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

        >>> part_container = ParticleContainer()
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

        if bond_ids:
            try:
                return self._iter_elements(self._bonds, bond_ids)
            except KeyError as exception:
                raise exception
        else:
            return self._iter_all(self._bonds)

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

    def _iter_elements(self, cur_dict, cur_ids):
        for cur_id in cur_ids:
            try:
                yield copy.deepcopy(cur_dict[cur_id])
            except KeyError:
                raise KeyError('id {} not found!'.format(cur_id))

    def _iter_all(self, cur_dict):
        for cur_element in cur_dict.itervalues():
            yield copy.deepcopy(cur_element)

    def _add_element(self, cur_dict, element):
        # We check if the current dictionary has the element
        cur_id = element.id
        if cur_id is None:
            cur_id = self._generate_unique_id(cur_dict)
            element.id = cur_id
            cur_dict[cur_id] = copy.deepcopy(element)
        else:
            if cur_id not in cur_dict:
                # Means the element is not in the dict - hence we can add it
                cur_dict[cur_id] = copy.deepcopy(element)
            else:
                raise Exception(
                    pce._PC_errors['ParticleContainer_DuplicatedValue']
                    + " id: " + str(cur_id))

    def _update_element(self, cur_dict, element):
        cur_id = element.id
        if cur_id in cur_dict:
            # This means the element IS in the current dictionary
            # (this should be the standard case...), so we proceed
            cur_dict[cur_id] = copy.deepcopy(element)
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

    def _generate_unique_id(self, cur_dict, number_tries=1000):
        max_int = np.iinfo(np.uint32).max
        for n in xrange(number_tries):
            cur_id = random.randint(0, max_int)
            if cur_id not in cur_dict:
                return cur_id
        raise Exception(pce._PC_errors['ParticleContainer_IdNotGenerated'])

# ==========================================================================

    # Additional methods that we maybe need

# ==========================================================================

    def get_n_particles(self):
        """Returns the total number of particles that are in the container."""
        return len(self._particles)

    def get_n_bonds(self):
        """Returns the total number of bonds that are in the container."""
        return len(self._bonds)


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

    Parameters
    ----------
        coordinates : list / tuple
            x,y,z coordinates of the particle (Default: [0, 0, 0])
        id : uint32
            the id, None as default (the particle container will generate it)
        data : DataContainer
            the data, the particle will have a copy of this
    """

    def __init__(self, coordinates=None, id=None, data=None):
        self.id = id
        if coordinates:
            self.coordinates = coordinates
        else:
            self.coordinates = [0.0, 0.0, 0.0]
        if data:
            self.data = copy.deepcopy(data)
        else:
            self.data = dc.DataContainer()

    def __str__(self):
        total_str = "{0}_{1}".format(self.id, self.coordinates)
        return total_str


class Bond(object):
    """Class reprensenting a bond.

    Attributes
    ----------
        id : uint32
            the unique id of the bond
        particles : list
            list of particles / elements of the bond
        data : DataContainer
            DataContainer to store the attributes of the bond

    Parameters
    ----------
        particles : sequence
            list of particles of the bond. It can not be empty (Defaul: (1,))
        id : uint32
            the id, None as default (the particle container will generate it)
        data : DataContainer
            DataContainer to store the attributes of the bond
    """

    def __init__(self, particles=None, id=None, data=None):
        self.id = id
        if particles is not None and len(particles) > 0:
            self.particles = particles
        else:
            raise Exception(pce._PC_errors['IncorrectParticlesTuple'])
        if data:
            self.data = copy.deepcopy(data)
        else:
            self.data = dc.DataContainer()

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
