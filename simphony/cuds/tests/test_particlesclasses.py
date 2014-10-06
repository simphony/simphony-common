"""
    Testing for particlesclasses module.
"""

import unittest

import simphony.cuds.particles as pc
import simphony.core.data_container as dc
from simphony.core.cuba import CUBA


class ParticleTestCase(unittest.TestCase):
    """Test case for Particle class."""

    def test_simple_particle_default(self):
        """Creation of the particle."""
        particle = pc.Particle()
        self.assertIsInstance(particle, pc.Particle, "Error: not a Particle!")
        self.assertEqual(particle.coordinates, [0, 0, 0])
        self.assertEqual(particle.id, None)
        self.assertEqual(particle.data, dc.DataContainer())

    def test_simple_particle_custom(self):
        """Creation of the particle."""
        data = dc.DataContainer()
        data[CUBA.RADIUS] = 3.0
        particle = pc.Particle([20.5, 30.5, 40.5], 33, data)
        self.assertIsInstance(particle, pc.Particle, "Error: not a Particle!")
        self.assertEqual(particle.coordinates, [20.5, 30.5, 40.5])
        self.assertEqual(particle.id, 33)
        self.assertEqual(particle.data, data)

    def test_simple_particle_print(self):
        """Conversion to str - this could change as the str method in the
        class could change also due to specifications -."""
        particle = pc.Particle()
        self.assertNotEqual(str(particle), '', "Error: empty string!")
        total_str = str(particle.id) + '_' + str(particle.coordinates)
        self.assertEqual(str(particle), total_str,
                         "Error: wrong str conversion!")


class BondTestCase(unittest.TestCase):
    """Test case for Bond class."""

    def test_simple_bond(self):
        """Creation of the bond."""
        data = dc.DataContainer()
        data[CUBA.RADIUS] = 2.0
        bond = pc.Bond((1, 2, 3), 12, data)
        self.assertIsInstance(bond, pc.Bond, "Error: not a Bond!")
        self.assertEqual(bond.particles, (1, 2, 3), "Error: wrong particles!")
        self.assertEqual(bond.id, 12)
        self.assertEqual(bond.data, data)

    def test_wrong_tuple(self):
        """Expected a exception when the constructor recives an empty tuple."""
        with self.assertRaises(Exception):
            pc.Bond(())

    def test_simple_bond_print(self):
        """Conversion to str - this could change as the str method in the
        class could change also due to specifications -."""
        bond = pc.Bond([1, 2, 3])
        self.assertNotEqual(str(bond), '', "Error: empty string!")
        total_str = str(bond.id) + '_[1, 2, 3]'
        self.assertEqual(str(bond), total_str,
                         "Error: wrong str conversion!")


class ParticleContainerParticlesTestCase1(unittest.TestCase):
    """Test case for addition of Particle to ParticleContainer."""
    def setUp(self):
        self.p_list = []
        self.b_list = []
        for i in xrange(10):
            self.p_list.append(pc.Particle([i, i*10, i*100]))
            self.b_list.append(pc.Bond([1, 2, 3]))
        self.pc = pc.ParticleContainer('Test_Pc')

    def test_has_particle_ok(self):
        """Checks that a particle already added is in the container."""
        self.pc.add_particle(self.p_list[0])
        self.assertTrue(self.pc.has_particle(self.p_list[0].id))

    def test_has_particle_wrong(self):
        """Checks that an unexisting particle is not in the container."""
        self.assertFalse(self.pc.has_particle(9876))

    def test_add_particle_ok(self):
        """Add particles to a ParticleContainer."""
        for particle in self.p_list:
            self.pc.add_particle(particle)
        for particle in self.p_list:
            self.assertTrue(self.pc.has_particle(particle.id),
                            "Error: particle not inside the container!")

    def test_add_particle_wrong_duplicated_value(self):
        """Add a particle that already exists in the container."""
        for particle in self.p_list:
            self.pc.add_particle(particle)
        with self.assertRaises(Exception):
            self.pc.add_particle(self.p_list[0])


class ParticleContainerParticlesTestCase2(unittest.TestCase):
    """Test case for updating, removing and iteration of Particle inside
    the container."""
    def setUp(self):
        self.p_list = []
        self.b_list = []
        self.pc = pc.ParticleContainer('Test_Pc')
        for i in xrange(10):
            self.p_list.append(pc.Particle([i, i*10, i*100]))
            self.b_list.append(pc.Bond([1, 2, 3]))
            self.pc.add_particle(self.p_list[i])

    def test_n_particles_ok(self):
        """Test that the particle container has correct number of particles."""
        self.assertEqual(self.pc.get_n_particles(), 10)

    def test_update_particle_ok(self):
        """Update an existing particle in a correct way."""
        particle = self.pc.get_particle(self.p_list[1].id)
        particle.coordinates = [123, 456, 789]
        part_coords = particle.coordinates
        self.pc.update_particle(particle)
        new_particle = self.pc.get_particle(particle.id)
        self.assertTrue(new_particle is not particle)
        self.assertEqual(particle.id, new_particle.id,
                         "Error: not same id!")
        self.assertEqual(part_coords, new_particle.coordinates,
                         "Error: not same coords!")
        self.assertEqual(particle.data, new_particle.data,
                         "Error: not same data!")

    def test_update_particle_wrong_unknown_value(self):
        """Trying to update a Particle that is not in the container."""
        particle = pc.Particle()
        with self.assertRaises(KeyError):
            self.pc.update_particle(particle)

    def test_remove_particle_ok(self):
        """Removing an existing particle."""
        particle = self.p_list[0]
        self.pc.remove_particle(particle.id)
        self.assertFalse(self.pc.has_particle(particle.id))

    def test_remove_particle_wrong_unknown_value(self):
        """Removing a particle that is not in the container."""
        particle = pc.Particle()
        with self.assertRaises(KeyError):
            self.pc.remove_particle(particle.id)

    def test_iter_particles_ok_list(self):
        """Checking if the iteration of a set of particles is correct."""
        particle_ids = set([p.id for p in self.p_list[::2]])
        iterated_ids = set()
        for particle in self.pc.iter_particles(particle_ids):
            iterated_ids.add(particle.id)
        self.assertEqual(particle_ids, iterated_ids,
                         'Error: incorrect iteration! {0}---\n{1}'
                         .format(particle_ids, iterated_ids))

    def test_iter_particles_ok_all(self):
        """Checking if the iteration of all the particles is correct."""
        particle_ids = set([p.id for p in self.p_list[:]])
        iterated_ids = set()
        for particle in self.pc.iter_particles():
            iterated_ids.add(particle.id)
        self.assertEqual(particle_ids, iterated_ids,
                         'Error: incorrect iteration! {0}---\n{1}'
                         .format(particle_ids, iterated_ids))

    def test_iter_particles_wrong_list(self):
        """Checking if the iteration fails with wrong ids as parameters."""
        particle_ids = [i for i in xrange(10)]
        with self.assertRaises(KeyError):
            for particle in self.pc.iter_particles(particle_ids):
                continue


class ParticleContainerBondsTestCase1(unittest.TestCase):
    """Test case for addition of Bond to ParticleContainer."""
    def setUp(self):
        self.p_list = []
        self.b_list = []
        for i in xrange(10):
            self.p_list.append(pc.Particle([i, i*10, i*100]))
            self.b_list.append(pc.Bond([1, 2, 3]))
        self.pc = pc.ParticleContainer('Test_Pc')

    def test_has_bond_ok(self):
        """Checks that a bond already added is in the container."""
        self.pc.add_bond(self.b_list[0])
        self.assertTrue(self.pc.has_bond(self.b_list[0].id))

    def test_has_bond_wrong(self):
        """Checks that an unexisting bond is not in the container."""
        self.assertFalse(self.pc.has_bond(3765))

    def test_add_bond_ok(self):
        """Add bond to a ParticleContainer."""
        for bond in self.b_list:
            self.pc.add_bond(bond)
        for particle in self.p_list:
            self.assertTrue(self.pc.has_bond(bond.id),
                            "Error: bond not inside the container!")

    def test_add_bond_wrong_duplicated_value(self):
        """Add a bond that already exists in the container."""
        for bond in self.b_list:
            self.pc.add_bond(bond)
        with self.assertRaises(Exception):
            self.pc.add_bond(self.b_list[0])


class ParticleContainerBondsTestCase2(unittest.TestCase):
    """Test case for updating, removing and iteration of Bond inside
    the container."""
    def setUp(self):
        self.p_list = []
        self.b_list = []
        self.pc = pc.ParticleContainer('Test_Pc')
        for i in xrange(10):
            self.p_list.append(pc.Particle([i, i*10, i*100]))
            self.b_list.append(pc.Bond([1, 2, 3]))
            self.pc.add_bond(self.b_list[i])

    def test_n_bonds_ok(self):
        """Test that the particle container has correct number of bonds."""
        self.assertEqual(self.pc.get_n_bonds(), 10)

    def test_update_bond_ok(self):
        """Update an existing bond in a correct way."""
        bond = self.pc.get_bond(self.b_list[1].id)
        bond.particles.append(99)
        self.pc.update_bond(bond)
        new_bond = self.pc.get_bond(bond.id)
        self.assertTrue(new_bond is not bond)
        self.assertEqual(bond.id, new_bond.id,
                         "Error: not same id!")
        self.assertEqual(bond.particles, new_bond.particles,
                         "Error: not same particles!")
        self.assertEqual(bond.data, bond.data,
                         "Error: not same data!")

    def test_update_bond_wrong_unknown_value(self):
        """Trying to update a Bond that is not in the container."""
        bond = pc.Bond([1, 2])
        with self.assertRaises(KeyError):
            self.pc.update_bond(bond)

    def test_remove_bond_ok(self):
        """Removing an existing particle."""
        bond = self.b_list[0]
        self.pc.remove_bond(bond.id)
        self.assertFalse(self.pc.has_bond(bond.id))

    def test_remove_bond_wrong_unknown_value(self):
        """Removing a bond that is not in the container."""
        bond = pc.Bond([1, 2])
        with self.assertRaises(KeyError):
            self.pc.remove_bond(bond.id)

    def test_iter_bonds_ok_list(self):
        """Checking if the iteration of a set of bonds is correct."""
        bonds_ids = set([b.id for b in self.b_list[::2]])
        iterated_ids = set()
        for bond in self.pc.iter_bonds(bonds_ids):
            iterated_ids.add(bond.id)
        self.assertEqual(bonds_ids, iterated_ids,
                         'Error: incorrect iteration! {0}---\n{1}'
                         .format(bonds_ids, iterated_ids))

    def test_iter_bonds_ok_all(self):
        """Checking if the iteration of all the bonds is correct."""
        bonds_ids = set([b.id for b in self.b_list[:]])
        iterated_ids = set()
        for bond in self.pc.iter_bonds():
            iterated_ids.add(bond.id)
        self.assertEqual(bonds_ids, iterated_ids,
                         'Error: incorrect iteration! {0}---\n{1}'
                         .format(bonds_ids, iterated_ids))

    def test_iter_bonds_wrong_list(self):
        """Checking if the iteration fails with wrong ids as parameters."""
        bonds_ids = [i for i in xrange(10)]
        with self.assertRaises(KeyError):
            for bond in self.pc.iter_bonds(bonds_ids):
                continue


if __name__ == '__main__':
    unittest.main()
