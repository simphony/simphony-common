"""Engine extension tools and classes."""
import inspect
from abc import ABCMeta, abstractmethod
from enum import Enum


class EngineInterface(Enum):
    """Represents an available interface to an engine.

    An interface is either internal or fileio. Internal interfaces use
    a python package or a shared library to talk to the underlying engine.
    FileIO, on the other hand, uses input/output files to interact with
    an engine executable.
    """
    Internal = 'internal'
    FileIO = 'fileio'


class EngineManagerException(Exception):
    """Any excpetion related to engine manager."""
    pass


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
            raise EngineManagerException('Physics equation must have a value.')
        if not methods or len(methods) == 0:
            raise \
                EngineManagerException('At least one method must be provided.')
        self.physics_equation = physics_equation
        self.methods = methods


class EngineMetadata(object):
    """Data structure to represent engine metadata.

    This class represents one supported engine along with its features.

    Parameters
    ----------
    name: str
      fixed name of a support engine to be used in user's data, i.e. key.
    features: list
      features of this engine as a list of EngineFeatureMetadata objects
    interfaces: list
      supported engine interfaces as a list of EngineInterface enums

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
        engine_interface: EngineInterface
          the interface to interact with engine

        Returns
        -------
        ABCEngineExtension: A wrapper configured with cuds and ready to run
        """

    @staticmethod
    def create_engine_metadata(name, features, interfaces):
        """Factory method to create engine metadata.

        Parameters
        ----------
        name: str
          fixed name of a support engine to be used in user's data, i.e. key.
        features: list
          features of this engine as a list of EngineFeatureMetadata objects
        interfaces: list
          supported engine interfaces as a list of EngineInterface enums

        Returns
        -------
        EngineMetadata: a loaded engine metadata object
        """
        return EngineMetadata(name, features, interfaces)

    @staticmethod
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

    def load_metadata(self, plugin):
        """Load existing engine extensions into the manager.

        This method inspects the given module and looks for ABCEngineExtension
         subclasses. If provided, will instantiate and keep them for further
         interactions with corresponding engines.

        plugin: module
          A python module provided by an extension
        """
        if not inspect.ismodule(plugin):
            raise EngineManagerException(
                'The provided object is not a module: %s' % plugin)

        for name, value in inspect.getmembers(plugin, inspect.isclass):
            if not inspect.isabstract(value) and\
                    issubclass(value, ABCEngineExtension):
                # Load the corresponding engine extension
                extension = value()
                if not isinstance(extension, ABCEngineExtension):
                    raise ValueError('Expected ABCEngineExtension, got %s' %
                                     extension)
                self.add_extension(extension)

    def add_extension(self, extension):
        """Add an extension to the context.

        Parameters
        ----------
        extension: ABCEngineExtension
          an extension that has knowledge about its own engines.
        """
        for engine in extension.get_supported_engines():
            if engine.name in self._engine_extensions:
                raise Exception('There is already an extension registered'
                                ' for %s engine.' % engine.name)

            # This extension knows how to create wrappers for the given engine.
            # It is our interaction point with its engines.
            self._engine_extensions[engine.name] = extension

    def create_wrapper(self, cuds, engine_name, engine_interface=None):
        """Create a wrapper to the given engine.

        Parameters
        ----------
        cuds: CUDS
            A cuds object which contains model information.
        engine_name: str
            Name of the underlying engine to launch the simulation with.
        engine_interface: EngineInterface
            The interface to the engine, internal or fileio.
        """
        if engine_name in self._engine_extensions:
            extension = self._engine_extensions[engine_name]
            return extension.create_wrapper(cuds,
                                            engine_name,
                                            engine_interface)
        else:
            raise EngineManagerException(
                'Invalid engine name: %s. Available engines are %s'
                % (engine_name, self.get_supported_engine_names()))

    def get_supported_engines(self):
        """Get metadata about supported engines.

        Returns
        -------
        list: a list of EngineMetadata objects
        """
        return list(self._engine_extensions.values())

    def get_supported_engine_names(self):
        """Show a list of supported engines.

        Returns
        -------
        list: a list of engine names
        """
        return self._engine_extensions.keys()

