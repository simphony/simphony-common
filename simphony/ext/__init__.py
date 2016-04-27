"""Simphony extension module

This module contains types for loading extensions.
"""
from .extension import ABCEngineExtension
from .extension import EngineInterface
from .extension import EngineManager


__all__ = ['ABCEngineExtension', 'EngineInterface',
           'EngineManager']


# TODO: Use an application server and put this in app context.
# Wrapper manager class.
_ENGINE_MANAGER = EngineManager()


def get_engine_manager():
    """Get the engine manager instance."""
    return _ENGINE_MANAGER


def create_wrapper(cuds, engine_name, engine_interface=None):
    """Create a wrapper to the given engine.

    Parameters
    ----------
    cuds: CUDS
        a cuds object which contains model information
    engine_name: str
        name of the underlying engine to launch the simulation with
    engine_interface: engine.EngineInterface
        the interface to the engine, internal or fileio

    Returns
    -------
    wrapper: engine.ABCEngineExtension
        an engine wrapper instance
    """
    return _ENGINE_MANAGER.create_wrapper(cuds, engine_name, engine_interface)
