"""Tests for Simulation classes."""
import unittest

from simphony import CUDS
from simphony import Simulation
from simphony.ext import EngineManager
from simphony.ext import set_engine_manager
from simphony.engine.tests.test_engine_metadata import \
    get_example_engine_extension


class SimulationTestCase(unittest.TestCase):
    """Simulation tests."""
    def setUp(self):
        self.manager = EngineManager()
        cls = get_example_engine_extension()
        self.manager.add_extension(cls())
        # Patch api for test
        set_engine_manager(self.manager)

    def test_empty_simulation(self):
        cuds = CUDS()
        engine_names = self.manager.get_supported_engine_names()
        # There should be at least one dummy extension there
        self.assertGreater(len(engine_names), 0)
        engine_a_name = engine_names[0]
        engine_a = None
        for engine_ext in self.manager.get_supported_engines():
            for engine in engine_ext.get_supported_engines():
                if engine.name == engine_a_name:
                    engine_a = engine

        self.assertIsNotNone(engine_a)
        self.assertGreater(len(engine_a.interfaces), 0)

        sim = Simulation(cuds,
                         engine_a_name,
                         engine_a.interfaces[0])

        self.assertIsNotNone(sim)

    def test_run(self):
        cuds = CUDS()
        engine_names = self.manager.get_supported_engine_names()
        print engine_names
        # There should be at least one dummy extension there
        self.assertGreater(len(engine_names), 0)
        engine_a_name = engine_names[0]
        engine_a = None
        for engine_ext in self.manager.get_supported_engines():
            for engine in engine_ext.get_supported_engines():
                if engine.name == engine_a_name:
                    engine_a = engine

        self.assertIsNotNone(engine_a)
        self.assertGreater(len(engine_a.interfaces), 0)

        sim = Simulation(cuds,
                         engine_a_name,
                         engine_a.interfaces[0])
        sim.run()
        self.assertEqual(sim.get_cuds(), cuds)
