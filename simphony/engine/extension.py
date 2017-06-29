"""Engine extension tools and classes."""
import warnings
from enum import Enum
from abc import ABCMeta, abstractmethod

from .exceptions import EngineManagerError

__all__ = ['EngineFeatureMetadata',
           'EngineMetadata',
           'EngineManager']


class EngineInterface(Enum):
    """Represents an available interface to an engine.

    An interface is either internal or fileio. Internal interfaces use
    a python package or a shared library to talk to the underlying engine.
    FileIO, on the other hand, uses input/output files to interact with
    an engine executable.
    """
    Internal = 'internal'
    FileIO = 'fileio'


class EngineFeatureMetadata(object):
    """Represents a set of engine features.

    A feature provides a set of methods to solve a physics equation.

    Parameters
    ----------
    physics_equation: PhysicsEquation
      represents a physics equation
    methods: list
      methods to solve the equation as a list of ComputationalMethod objects
    """
    def __init__(self, physics_equation, methods):
        if not physics_equation:
            raise EngineManagerError('Physics equation must have a value.')
        if not methods or len(methods) == 0:
            raise \
                EngineManagerError('At least one method must be provided.')
        self.physics_equation = physics_equation
        self.methods = methods


class EngineMetadata(object):
    """Data structure to represent engine metadata.

    This class represents one supported engine along with its features.

    Parameters
    ----------
    name: str
      fixed name of a support engine to be used in user's data, i.e. key
    features: list
      features of this engine as a list of EngineFeatureMetadata objects
    interfaces: list
      supported engine interfaces as a list of engine.EngineInterface enums

    """
    def __init__(self, name, features, interfaces):
        self.name = name
        self.features = features
        self.interfaces = interfaces


class ABCEngineExtension(object):
    """Base class for all engine extensions."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_supported_engines(self):
        """Get metadata about supported engines.

        Returns
        -------
        list: a list of EngineMetadata objects
        """

    @abstractmethod
    def create_wrapper(self, cuds, engine_name, engine_interface):
        """Creates a wrapper to the requested engine.

        Parameters
        ----------
        cuds: CUDS
          CUDS computational model data
        engine_name: str
          name of the engine, must be supported by this extension
        engine_interface: engine.EngineInterface
          the interface to interact with engine

        Returns
        -------
        ABCEngineExtension: A wrapper configured with cuds and ready to run
        """

    def create_engine_metadata(name, features, interfaces):
        """Factory method to create engine metadata.

        Parameters
        ----------
        name: str
          fixed name of a support engine to be used in user's data, i.e. key
        features: list
          features of this engine as a list of EngineFeatureMetadata objects
        interfaces: list
          supported engine interfaces as a list of engine.EngineInterface enums

        Returns
        -------
        EngineMetadata: a loaded engine metadata object
        """
        return EngineMetadata(name, features, interfaces)

    def create_engine_metadata_feature(physics_equation, methods):
        """Factory method to create engine metadata feature.

        Parameters
        ----------
        physics_equation: PhysicsEquation
          represents a physics equation
        methods: list
          ComputationalMethod objects to solve the equation

        Return
        ------
        EngineFeatureMetadata: a loaded engine metadata feature object
        """
        return EngineFeatureMetadata(physics_equation, methods)


class EngineManager(object):
    """Controller class to keep track of engine extensions."""

    def __init__(self):
        self._engine_extensions = {}

        # List of registered class ids
        self._registry = []

    def register_extension(self, cls):
        """Register an engine extension class.

        Parameters
        ----------
        cls: ABCEngineExtension
          a subclass of base extension metadata type
        """
        if cls.__name__ in self._registry:
            warnings.warn(
                'Ignoring already registered class %s' % cls.__name__)
            return

        if not issubclass(cls, ABCEngineExtension):
            raise \
                EngineManagerError("Not valid engine metadata class %s" % cls)

        # Instantiate the extension
        extension = cls()

        if not isinstance(extension, ABCEngineExtension):
            raise ValueError('Expected ABCEngineExtension, got %s' %
                             extension)

        for engine in extension.get_supported_engines():
            if engine.name in self._engine_extensions:
                raise EngineManagerError(
                    'There is already an extension registered '
                    'for %s engine.' % engine.name)

            # This extension knows how to create wrappers for the given engine.
            # It is our interaction point with its engines.
            self._engine_extensions[engine.name] = extension
            self._registry.append(cls.__name__)

    def create_wrapper(self, cuds, engine_name, engine_interface=None):
        """Create a wrapper to the given engine.

        Parameters
        ----------
        cuds: CUDS
            a cuds object which contains model information
        engine_name: str
            name of the underlying engine to launch the simulation with
        engine_interface: engine.EngineInterface
            the interface to the engine, internal or fileio
        """
        if engine_name in self._engine_extensions:
            extension = self._engine_extensions[engine_name]
            return extension.create_wrapper(cuds,
                                            engine_name,
                                            engine_interface)
        else:
            raise EngineManagerError(
                'Invalid engine name: %s. Available engines are %s'
                % (engine_name, self.get_supported_engine_names()))

    def get_supported_engines(self):
        """Get metadata about supported engines.

        Returns
        -------
        metadata: list
            a list of EngineMetadata objects
        """
        return list(self._engine_extensions.values())

    def get_supported_engine_names(self):
        """Show a list of supported engines.

        Returns
        -------
        names: list
            a list of engine names
        """
        return self._engine_extensions.keys()
