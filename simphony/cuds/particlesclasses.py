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


# from abc import ABCMeta, abstractmethod
# import bisect
import copy
import random
import numpy as np
# custom imports:
from abstractparticles import ABCParticleContainer, ElementsCommon
import pcexceptions as PCE
# import bisectservice as BS
# import DataContainers ?¿?¿?


class ParticleContainer(ABCParticleContainer):
    """Class that represents a container of particles and bonds. It can
       add particles and bonds, remove them and update them.

       Internally uses a dictionary to keep particles and another one for
       bonds.
       Also there is another dictionary for aditional data
       (not implemented yet).

       Parameters: ---

       Attributes:

       Attributes
       ----------
        _particles : dictionary
            data structure for particles storage
        _bonds : dictionary
            data structure for bonds storage
        data : DataContainer
            data attributes of the element (not implemented yet)
    """
    def __init__(self):
        self._particles = {}
        self._bonds = {}
        # When ready:
        # self._data = DataContainer()

# ================================================================

    # overriden methods of the ABC

# ================================================================

    def add_particle(self, new_particle):
        r"""Adds the 'new_particle' particle to the container.

        Since the particle has it's own id, it won't add the particle if a
        particle with the same id already exists. If the user wants to replace
        an existing particle in the container there is an 'update_particle'
        method for that purpose.

        Parameters
        ----------

        new_particle : Particle
            the new particle that will be included in the container.

        Returns
        -------
        None

        Other parameters
        ----------------

        Raises
        ------
        None (for the moment)

        See Also
        --------
        update_particle, remove_particle

        Notes
        -----

        References
        ----------

        Examples
        --------
        Having a Particle and a ParticleContainer just call the function
        passing the Particle as parameter.

        >>> part = Particle()
        >>> part_container = ParticleContainer()
        >>> part_container.add_particle(part)
        """

        if isinstance(new_particle, Particle):
            self.__add_element__(self._particles, new_particle)
        else:
            raise TypeError

    def add_bond(self, new_bond):
        r"""Adds the 'new_bond' bond to the container.

        Also like with particles, since the bond has it's own id, it won't add
        the bond if a bond with the same id already exists. If the user wants
        to replace an existing bond in the container there is an 'update_bond'
        method for that purpose.

        Parameters
        ----------

        new_bond : Bond
            the new bond that will be included in the container.

        Returns
        -------
        None

        Other parameters
        ----------------

        Raises
        ------
        None (for the moment)

        See Also
        --------
        update_bond, remove_bond

        Notes
        -----

        References
        ----------

        Examples
        --------
        Having a Bond and a ParticleContainer just call the function
        passing the Bond as parameter.

        >>> bond = Bond()
        >>> part_container = ParticleContainer()
        >>> part_container.add_bond(bond)
        """

        if isinstance(new_bond, Bond):
            self.__add_element__(self._bonds, new_bond)
        else:
            raise TypeError

    def update_particle(self, particle):
        r"""Replaces an existing particle with the 'particle' new particle.

        Takes the id of 'particle' and searchs inside the container for
        that particle. If the particle exists, it is replaced with the new
        particle passed as parameter. If the particle doesn't exist, nothing
        will happen.

        Parameters
        ----------

        particle : Particle
            the particle that will be replaced.

        Returns
        -------
        None

        Other parameters
        ----------------

        Raises
        ------
        None (for the moment)

        See Also
        --------
        add_particle, remove_particle

        Notes
        -----

        References
        ----------

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

        if isinstance(particle, Particle):
            self.__update_element__(self._particles, particle)
        else:
            raise TypeError

    def update_bond(self, bond):
        r"""Replaces an existing bond with the 'bond' new bond.

        Takes the id of 'bond' and searchs inside the container for
        that bond. If the bond exists, it is replaced with the new
        bond passed as parameter. If the bond doesn't exist, nothing
        will happen.

        Parameters
        ----------

        bond : Bond
            the bond that will be replaced.

        Returns
        -------
        None

        Other parameters
        ----------------

        Raises
        ------
        None (for the moment)

        See Also
        --------
        add_bond, remove_bond

        Notes
        -----

        References
        ----------

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
        if isinstance(bond, Bond):
            self.__update_element__(self._bonds, bond)
        else:
            raise TypeError

    def get_particle(self, particle_id):
        """Returns a copy of the particle with the 'particle_id' id.

        If the particle doesn't exists in the container, it will return 'None'.
        """

        try:
            cur_particle = copy.deepcopy(self._particles[particle_id])
            return cur_particle
        except KeyError:
            print "Error: particle not found!: ", str(particle_id)
            return None

    def get_bond(self, bond_id):
        """Returns a copy of the bond with the 'bond_id' id.

        If the bond doesn't exists in the container, it will return 'None'.
        """

        try:
            cur_bond = copy.deepcopy(self._bonds[bond_id])
            return cur_bond
        except KeyError:
            print "Error: bond not found! ", str(bond_id)
            return None

    def remove_particle(self, particle_id):
        r"""Removes the particle with the 'particle_id' id from the container.

        The id passed as parameter should exists in the container. If it
        doesn't exists, nothing will happen.

        Parameters
        ----------

        particle_id : Particle
            the id of the particle to be removed.

        Returns
        -------
        None

        Other parameters
        ----------------

        Raises
        ------
        None (for the moment)

        See Also
        --------
        add_particle, update_particle

        Notes
        -----

        References
        ----------

        Examples
        --------
        Having an id of an existing particle, pass it to the function.

        >>> part_container = ParticleContainer()
        >>> ...
        >>> part = part_container.get_particle(id)
        >>> ...
        >>> part_container.remove_particle(part.get_id())
        or directly
        >>> part_container.remove_particle(id)
        """

        if isinstance(particle_id, Particle):
            self.__remove_element__(self._particles, particle_id)
        else:
            raise TypeError

    def remove_bond(self, bond_id):
        r"""Removes the bond with the 'bond_id' id from the container.

        The id passed as parameter should exists in the container. If
        it doesn't exists, nothing will happen.

        Parameters
        ----------

        bond_id : Particle
            the id of the bond to be removed.

        Returns
        -------
        None

        Other parameters
        ----------------

        Raises
        ------
        None (for the moment)

        See Also
        --------
        add_bond, update_bond

        Notes
        -----

        References
        ----------

        Examples
        --------
        Having an id of an existing bond, pass it to the function.

        >>> part_container = ParticleContainer()
        >>> ...
        >>> bond = part_container.get_bond(id)
        >>> ...
        >>> part_container.remove_bond(bond.get_id())
        or directly
        >>> part_container.remove_bond(id)
        """

        if isinstance(bond_id, Bond):
            self.__remove_element__(self._bonds, bond_id)
        else:
            raise TypeError

    def iter_particles(self, particle_ids=None):
        r"""Generator method for iterating over the particles of the container.

        It can recieve any kind of sequence of particle ids to iterate over
        those concrete particles. If nothing is passed as parameter, it will
        iterate over all the particles.

        Parameters
        ----------

        particle_ids : array_like
            sequence containing the id's of the particles that will be
            iterated.

        Returns
        -------
        Yields each particle to be used.

        Other parameters
        ----------------

        Raises
        ------
        None (for the moment)

        See Also
        --------
        iter_bonds, add_particle, remove_particle, update_particle

        Notes
        -----

        References
        ----------

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
            return self.__iter_elements__(self._particles, particle_ids)
        else:
            return self.__iter_all__(self._particles)

    def iter_bonds(self, bond_ids=None):
        r"""Generator method for iterating over the bonds of the container.

        It can recieve any kind of sequence of bond ids to iterate over
        those concrete bond. If nothing is passed as parameter, it will
        iterate over all the bond.

        Parameters
        ----------

        bond_ids : array_like
            sequence containing the id's of the bond that will be iterated.

        Returns
        -------
        Yields each bond to be used.

        Other parameters
        ----------------

        Raises
        ------
        None (for the moment)

        See Also
        --------
        iter_particles, add_bond, remove_bond, update_bond

        Notes
        -----

        References
        ----------

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
            return self.__iter_elements__(self._bonds, bond_ids)
        else:
            return self.__iter_all__(self._bonds)


# ================================================================

    # private methods to make the code more readable and compact

# ================================================================

    def __iter_elements__(self, cur_dict, cur_ids):
        for cur_id in cur_ids:
            if cur_id in cur_dict:
                yield copy.deepcopy(cur_dict[cur_id])
            else:
                """this point can be discussed: if one of the ids is not in the
                dictionary, should we stop the iteration and raise an
                Exception? If we return 'None', the iteration can continue,
                but whoever is using the method to iterate will have to check
                if the returned object is valid or not;
                otherwise the script will fail."""
                yield None

    def __iter_all__(self, cur_dict):
        for cur_element in cur_dict.values():
            yield copy.deepcopy(cur_element)

    def __add_element__(self, cur_dict, element):
        # We check if the current dictionary has the element
        cur_id = element.get_id()
        if cur_id is None:
            cur_id = self.__generate_unique_id__(cur_dict)
            element.id = cur_id
            cur_dict[cur_id] = copy.deepcopy(element)
        else:
            if cur_id not in cur_dict:
                # Means the element is not in the dict - hence we can add it
                cur_dict[cur_id] = copy.deepcopy(element)
            else:
                raise PCE.PC_DuplicatedValueError(cur_id)

    def __update_element__(self, cur_dict, element):
        # We use the bisect module to optimize the lists
        cur_id = element.get_id()
        if cur_id in cur_dict:
            # This means the element IS in the current dictionary
            # (this should be the standard case...), so we proceed
            cur_dict[cur_id] = copy.deepcopy(element)
        else:
            raise PCE.PC_UnknownValueError(cur_id)

    def __remove_element__(self, cur_dict, element):
        cur_id = element.get_id()
        if cur_id in cur_dict:
            # Element IS in dict, we proceed
            del cur_dict[cur_id]
        else:
            raise PCE.PC_UnknownValueError(cur_id)

    def __generate_unique_id__(self, cur_dict, number_tries=1000):
        max_int = np.iinfo(np.uint32).max
        for n in xrange(number_tries):
            cur_id = random.randint(0, max_int)
            if cur_id not in cur_dict:
                return cur_id
        raise PCE.PC_IdNotGeneratedError()

# ==========================================================================

    # Additional methods that we maybe need

# ==========================================================================

    def get_n_particles(self):
        return len(self._particles)

    def get_n_bonds(self):
        return len(self._bonds)

    def __contains__(self, item):
        if isinstance(item, Particle):
            return item.get_id() in self._particles
        elif isinstance(item, Bond):
            return item.get_id() in self._bonds
        else:
            raise TypeError
            return False


class Particle(ElementsCommon):
    """Class representing a particle.

    It has an id (private) and coordinates. Also has a dictionary containing
    attributes of the particle (not implemented yet).

    Attributes:

    Attributes
    ----------
        coordinates : list / tuple
            x,y,z coordinates of the particle

    Parameters:

    Parameters
    ----------
        coordinates : list / tuple
            x,y,z coordinates of the particle (Default: [0, 0, 0])
    """

    def __init__(self, ext_coordinates=None, id=None):
        super(Particle, self).__init__(id)
        if ext_coordinates:
            self.coordinates = ext_coordinates
        else:
            self.coordinates = [0.0, 0.0, 0.0]

    def __eq__(self, other):
        return (self._id == other.get_id() and
                self.coordinates == other.coordinates)

    def __str__(self):
        total_str = "{0}_{1}".format(self.get_id(), self.coordinates)
        # return str(self.get_id())
        return total_str


class Bond(ElementsCommon):
    """Class reprensenting a bond.

    It counts with a list of particle id's that compounds the bond.
    We understand a bond as any kind of interaction that needs to be
    represented (for example a chemical bond).

    Attributes:

    Attributes
    ----------
        particles : list
            list of particles / elements of the bond

    Parameters:

    Parameters
    ----------
       particles_list : list
            list of particles of the bond. It can not be empty (Defaul: (1,))
    """

    def __init__(self, particles_list=None, id=None):
        super(Bond, self).__init__(id)
        if particles_list is not None:
            self.particles = particles_list
        else:
            self.particles.append(1)
            raise PCE.B_IncorrectTupleError()

    def __eq__(self, other):
        return (self._id == other.get_id() and
                self.particles == other.particles)

    def __str__(self):
        total_str = "{0}_{1}".format(self.get_id(), self.particles)
        # return str(self.get_id())
        return total_str

# Just an information message of the module


def main():
    print """
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
           """

if __name__ == '__main__':
    main()
