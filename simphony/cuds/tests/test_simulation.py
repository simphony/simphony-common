"""Tests for Simulation classes."""
import unittest
from mock import patch

from simphony.api import CUDS
from simphony.api import Simulation
from simphony.engine import get_engine_manager
from simphony.engine.tests.test_engine_metadata import \
    get_example_engine_extension
from simphony.engine.extension import EngineManager


@patch('simphony.engine._ENGINE_MANAGER', EngineManager())
class SimulationTestCase(unittest.TestCase):
    """Simulation tests."""
    def test_empty_simulation(self):
        get_engine_manager().register_extension(get_example_engine_extension())
        cuds = CUDS()
        engine_names = get_engine_manager().get_supported_engine_names()
        # There should be at least one dummy extension there
        self.assertGreater(len(engine_names), 0)
        engine_a_name = engine_names[0]
        engine_a = None
        for engine_ext in get_engine_manager().get_supported_engines():
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
        get_engine_manager().register_extension(get_example_engine_extension())
        cuds = CUDS()
        engine_names = get_engine_manager().get_supported_engine_names()
        # There should be at least one dummy extension there
        self.assertGreater(len(engine_names), 0)
        engine_a_name = engine_names[0]
        engine_a = None
        for engine_ext in get_engine_manager().get_supported_engines():
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
