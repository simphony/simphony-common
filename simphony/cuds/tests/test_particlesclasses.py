"""
    Testing for particlesclasses module.
"""

import unittest

import particlesclasses as pc
import pcexceptions as pce


class ParticleTestCase(unittest.TestCase):
    """Test case for Particle class."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_particle_default(self):
        """Creation of the particle."""
        particle = pc.Particle()
        self.assertIsInstance(particle, pc.Particle, "Error: not a Particle!")
        self.assertEqual(particle.coordinates, [0, 0, 0])

    def test_simple_particle_custom(self):
        """Creation of the particle."""
        particle = pc.Particle([20.5, 30.5, 40.5])
        self.assertIsInstance(particle, pc.Particle, "Error: not a Particle!")
        self.assertEqual(particle.coordinates, [20.5, 30.5, 40.5])

    def test_simple_particle_print(self):
        """Conversion to str - this could change as the str method in the
        class could change also due to specifications -."""
        particle = pc.Particle()
        self.assertNotEqual(str(particle), '', "Error: empty string!")
        total_str = str(particle.get_id()) + '_' + str(particle.coordinates)
        # print total_str
        self.assertEqual(str(particle), total_str,
                         "Error: wrong str conversion!")


class BondTestCase(unittest.TestCase):
    """Test case for Bond class."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_simple_bond(self):
        """Creation of the bond."""
        bond = pc.Bond((1, 2, 3))
        self.assertIsInstance(bond, pc.Bond, "Error: not a Bond!")
        self.assertNotEqual(bond.particles, (), "Error: empty particles!")
        self.assertEqual(bond.particles, (1, 2, 3), "Error: wrong particles!")

    def test_wrong_tuple(self):
        """Expected a exception when the constructor recives an empty tuple."""
        with self.assertRaises(pce.B_IncorrectTupleError) as cm:
            bond = pc.Bond(())
        exc = cm.exception
        self.assertIsInstance(exc, pce.B_IncorrectTupleError)

    def test_simple_bond_print(self):
        """Conversion to str - this could change as the str method in the
        class could change also due to specifications -."""
        bond = pc.Bond([1, 2, 3])
        self.assertNotEqual(str(bond), '', "Error: empty string!")
        total_str = str(bond.get_id()) + '_[1, 2, 3]'
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
        self.pc = pc.ParticleContainer()

    def tearDown(self):
        pass

    def test_add_particle_ok(self):
        """Add particles to a ParticleContainer."""
        for particle in self.p_list:
            self.pc.add_particle(particle)
        for particle in self.p_list:
            self.assertIn(particle, self.pc,
                          "Error: particle not inside the container!")

    def test_add_particle_wrong_type_error(self):
        """Add something that is not a particle to the container."""
        with self.assertRaises(TypeError) as cm:
            self.pc.add_particle(self.b_list[0])

        exc = cm.exception
        self.assertIsInstance(exc, TypeError)

    def test_add_particle_wrong_duplicated_value(self):
        """Add a particle that already exists in the container."""
        for particle in self.p_list:
            self.pc.add_particle(particle)
        with self.assertRaises(pce.PC_DuplicatedValueError) as cm:
            self.pc.add_particle(self.p_list[0])

        exc = cm.exception
        self.assertIsInstance(exc, pce.PC_DuplicatedValueError)


class ParticleContainerParticlesTestCase2(unittest.TestCase):
    """Test case for updating, removing and iteration of Particle inside
    the container."""
    def setUp(self):
        self.p_list = []
        self.b_list = []
        self.pc = pc.ParticleContainer()
        for i in xrange(10):
            self.p_list.append(pc.Particle([i, i*10, i*100]))
            self.b_list.append(pc.Bond([1, 2, 3]))
            self.pc.add_particle(self.p_list[i])

    def tearDown(self):
        pass

    def test_update_particle_ok(self):
        """Update an existing particle in a correct way."""
        particle = self.pc.get_particle(self.p_list[1].get_id())
        particle.coordinates = [123, 456, 789]
        part_coords = particle.coordinates
        self.pc.update_particle(particle)
        new_particle = self.pc.get_particle(particle.get_id())
        self.assertTrue(new_particle is not particle)
        new_part_coords = new_particle.coordinates

        self.assertEqual(part_coords, new_part_coords,
                         "Error: not same coords!")

    def test_update_particle_wrong_type_error(self):
        """Trying to pass a non-Particle item."""
        with self.assertRaises(TypeError) as cm:
            self.pc.update_particle(self.b_list[0])

        exc = cm.exception
        self.assertIsInstance(exc, TypeError)

    def test_update_particle_wrong_unknown_value(self):
        """Trying to update a Particle that is not in the container."""
        particle = pc.Particle()
        with self.assertRaises(pce.PC_UnknownValueError) as cm:
            self.pc.update_particle(particle)

        exc = cm.exception
        self.assertIsInstance(exc, pce.PC_UnknownValueError)

    def test_remove_particle_ok(self):
        """Removing an existing particle."""
        particle = self.p_list[0]
        self.pc.remove_particle(particle)
        self.assertNotIn(particle, self.pc)

    def test_remove_particle_wrong_type_error(self):
        """Removing a non-Particle item."""
        with self.assertRaises(TypeError) as cm:
            self.pc.remove_particle(self.b_list[0])

        exc = cm.exception
        self.assertIsInstance(exc, TypeError)

    def test_remove_particle_wrong_unknown_value(self):
        """Removing a particle that is not in the container."""
        particle = pc.Particle()
        with self.assertRaises(pce.PC_UnknownValueError) as cm:
            self.pc.remove_particle(particle)

        exc = cm.exception
        self.assertIsInstance(exc, pce.PC_UnknownValueError)

    def test_iter_particles_ok_list(self):
        particle_ids = [p.get_id() for p in self.p_list[::2]]
        iterated_ids = []
        for particle in self.pc.iter_particles(particle_ids):
            iterated_ids.append(particle.get_id())
        self.assertEqual(particle_ids.sort(), iterated_ids.sort(),
                         "Error: incorrect iteration!")

    def test_iter_particles_ok_all(self):
        particle_ids = [p.get_id() for p in self.p_list[:]]
        iterated_ids = []
        for particle in self.pc.iter_particles():
            iterated_ids.append(particle.get_id())
        self.assertEqual(particle_ids.sort(), iterated_ids.sort(),
                         "Error: incorrect iteration!")

    def test_iter_particles_wrong_list(self):
        particle_ids = [i for i in xrange(10)]
        for particle in self.pc.iter_particles(particle_ids):
            self.assertEqual(particle, None, "Error: incorrect iteration!")

    def test_iter_particles_ok_mixed_list(self):
        correct_ids = [p.get_id() for p in self.p_list[:]]
        particle_ids = []
        for i in xrange(10):
            particle_ids.append(self.p_list[i])
            particle_ids.append(i)

        iterated_ids = []
        for particle in self.pc.iter_particles(particle_ids):
            if particle:
                iterated_ids.append(particle.get_id())
        self.assertEqual(correct_ids.sort(), iterated_ids.sort(),
                         "Error: incorrect iteration!")


class ParticleContainerBondsTestCase1(unittest.TestCase):
    """Test case for addition of Bond to ParticleContainer."""
    def setUp(self):
        self.p_list = []
        self.b_list = []
        for i in xrange(10):
            self.p_list.append(pc.Particle([i, i*10, i*100]))
            self.b_list.append(pc.Bond([1, 2, 3]))
        self.pc = pc.ParticleContainer()

    def tearDown(self):
        pass

    def test_add_bond_ok(self):
        """Add bond to a ParticleContainer."""
        for bond in self.b_list:
            self.pc.add_bond(bond)
        for particle in self.p_list:
            self.assertIn(bond, self.pc,
                          "Error: particle not inside the container!")

    def test_add_bond_wrong_type_error(self):
        """Add something that is not a bond to the container."""
        with self.assertRaises(TypeError) as cm:
            self.pc.add_bond(self.p_list[0])

        exc = cm.exception
        self.assertIsInstance(exc, TypeError)

    def test_add_bond_wrong_duplicated_value(self):
        """Add a bond that already exists in the container."""
        for bond in self.b_list:
            self.pc.add_bond(bond)
        with self.assertRaises(pce.PC_DuplicatedValueError) as cm:
            self.pc.add_bond(self.b_list[0])

        exc = cm.exception
        self.assertIsInstance(exc, pce.PC_DuplicatedValueError)


class ParticleContainerBondsTestCase2(unittest.TestCase):
    """Test case for updating, removing and iteration of Bond inside
    the container."""
    def setUp(self):
        self.p_list = []
        self.b_list = []
        self.pc = pc.ParticleContainer()
        for i in xrange(10):
            self.p_list.append(pc.Particle([i, i*10, i*100]))
            self.b_list.append(pc.Bond([1, 2, 3]))
            self.pc.add_bond(self.b_list[i])

    def tearDown(self):
        pass

    def test_update_bond_ok(self):
        """Update an existing bond in a correct way."""
        bond = self.pc.get_bond(self.b_list[1].get_id())
        bond.particles.append(99)
        bond_particles = bond.particles
        self.pc.update_bond(bond)
        new_bond = self.pc.get_bond(bond.get_id())
        self.assertTrue(new_bond is not bond)
        bond_new_particles = new_bond.particles

        self.assertEqual(bond_particles, bond_new_particles,
                         "Error: not same coords!")

    def test_update_bond_wrong_type_error(self):
        """Trying to pass a non-Bond item."""
        with self.assertRaises(TypeError) as cm:
            self.pc.update_bond(self.p_list[0])

        exc = cm.exception
        self.assertIsInstance(exc, TypeError)

    def test_update_bond_wrong_unknown_value(self):
        """Trying to update a Bond that is not in the container."""
        bond = pc.Bond([1, 2])
        with self.assertRaises(pce.PC_UnknownValueError) as cm:
            self.pc.update_bond(bond)

        exc = cm.exception
        self.assertIsInstance(exc, pce.PC_UnknownValueError)

    def test_remove_bond_ok(self):
        """Removing an existing particle."""
        bond = self.b_list[0]
        self.pc.remove_bond(bond)
        self.assertNotIn(bond, self.pc)

    def test_remove_bond_wrong_type_error(self):
        """Removing a non-Bond item."""
        with self.assertRaises(TypeError) as cm:
            self.pc.remove_bond(self.p_list[0])

        exc = cm.exception
        self.assertIsInstance(exc, TypeError)

    def test_remove_bond_wrong_unknown_value(self):
        """Removing a bond that is not in the container."""
        bond = pc.Bond([1, 2])
        with self.assertRaises(pce.PC_UnknownValueError) as cm:
            self.pc.remove_bond(bond)

        exc = cm.exception
        self.assertIsInstance(exc, pce.PC_UnknownValueError)

    def test_iter_bonds_ok_list(self):
        bonds_ids = [b.get_id() for b in self.b_list[::2]]
        iterated_ids = []
        for bond in self.pc.iter_bonds(bonds_ids):
            iterated_ids.append(bond.get_id())
        self.assertEqual(bonds_ids.sort(), iterated_ids.sort(),
                         "Error: incorrect iteration!")

    def test_iter_bonds_ok_all(self):
        particle_ids = [p.get_id() for p in self.p_list[:]]
        iterated_ids = []
        for particle in self.pc.iter_particles():
            iterated_ids.append(particle.get_id())
        self.assertEqual(particle_ids.sort(), iterated_ids.sort(),
                         "Error: incorrect iteration!")

    def test_iter_bonds_wrong_list(self):
        bonds_ids = [i for i in xrange(10)]
        for bond in self.pc.iter_bonds(bonds_ids):
            self.assertEqual(bond, None, "Error: incorrect iteration!")

    def test_iter_bonds_ok_mixed_list(self):
        correct_ids = [b.get_id() for b in self.b_list[:]]
        bonds_ids = []
        for i in xrange(10):
            bonds_ids.append(self.b_list[i])
            bonds_ids.append(i)

        iterated_ids = []
        for bond in self.pc.iter_bonds(bonds_ids):
            if bond:
                iterated_ids.append(bond.get_id())
        self.assertEqual(correct_ids.sort(), iterated_ids.sort(),
                         "Error: incorrect iteration!")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ParticleTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(BondTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(
        ParticleContainerParticlesTestCase1)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(
        ParticleContainerParticlesTestCase2)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(
        ParticleContainerBondsTestCase1)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(
        ParticleContainerBondsTestCase2)
    unittest.TextTestRunner(verbosity=2).run(suite)
