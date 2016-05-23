import sys as _sys

from simphony.core.cuba import CUBA


class DataContainer(dict):
    """ A DataContainer instance

    The DataContainer object is implemented as a python dictionary whose keys
    are restricted to the instance's `restricted_keys`, default to the CUBA
    enum members.

    The data container can be initialized like a typical python dict
    using the mapping and iterables where the keys are CUBA enum members.

    For convenience keywords can be passed as capitalized CUBA enum members::

        >>> DataContainer(ACCELERATION=234)  # CUBA.ACCELERATION is 22
        {<CUBA.ACCELERATION: 22>: 234}

    """

    # Memory usage optimization.
    __slots__ = ()

    # These are the allowed CUBA keys (faster to convert to set for lookup)
    restricted_keys = frozenset(CUBA)

    # Map CUBA enum name to CUBA enum
    # Used by assigning key using keyword name
    _restricted_mapping = CUBA.__members__

    def __init__(self, *args, **kwargs):
        """ Constructor.
        Initialization follows the behaviour of the python dict class.
        """

        super(DataContainer, self).__init__()
        self.update(*args, **kwargs)

    def __setitem__(self, key, value):
        """ Set/Update the key value only when the key is a CUBA key.

        """
        if isinstance(key, CUBA) and key in self.restricted_keys:
            super(DataContainer, self).__setitem__(key, value)
        else:
            message = "Key {!r} is not in the supported CUBA keywords"
            raise ValueError(message.format(key))

    def update(self, *args, **kwargs):
        self._check_arguments(args, kwargs)

        if args and not hasattr(args[0], 'keys'):
            # args is an iterator
            for key, value in args[0]:
                self[key] = value
        elif args:
            mapping = args[0]
            if (isinstance(mapping, DataContainer) and
                    mapping.restricted_keys == self.restricted_keys):
                super(DataContainer, self).update(mapping)
            else:
                self._check_mapping(mapping)
                super(DataContainer, self).update(mapping)

        super(DataContainer, self).update(
            {self._restricted_mapping[kwarg]: value
             for kwarg, value in kwargs.viewitems()})

    def _check_arguments(self, args, kwargs):
        """ Check for the right arguments.

        """
        # See if there are any non CUBA keys in the keyword arguments
        invalid_keys = [key for key in kwargs
                        if key not in self._restricted_mapping]
        if invalid_keys:
            message = "Key(s) {!r} are not in the supported CUBA keywords"
            raise ValueError(message.format(invalid_keys))
        # Only one positional argument is allowed.
        if len(args) > 1:
            message = 'DataContainer expected at most 1 arguments, got {}'
            raise TypeError(message.format(len(args)))

    def _check_mapping(self, mapping):
        ''' Check if the keys in the mappings are all supported CUBA keys

        Parameters
        ----------
        mapping : Mapping

        Raises
        ------
        ValueError
            if any of the keys in the mappings is not supported
        '''
        invalid_keys = [key for key in mapping
                        if (not isinstance(key, CUBA) or
                            key not in self.restricted_keys)]
        if invalid_keys:
            message = 'Key(s) {!r} are not in the supported CUBA keywords'
            raise ValueError(message.format(invalid_keys))


def create_data_container(restricted_keys,
                          class_name='RestrictedDataContainer'):
    ''' Create a DataContainer subclass with the given
    restricted keys

    Note
    ----
    For pickling to work, the created class needs to be assigned
    a name `RestrictedDataContainer` in the module where it is
    created

    Parameters
    ----------
    restricted_keys : sequence
        CUBA IntEnum

    class_name : str
        Name of the returned class

    Returns
    -------
    RestrictedDataContainer : DataContainer
        subclass of DataContainer with the given `restricted_keys`

    Examples
    --------
    >>> RestrictedDataContainer = create_data_container((CUBA.NAME,
                                                         CUBA.VELOCITY))
    >>> container = RestrictedDataContainer()
    >>> container.restricted_keys
    frozenset({<CUBA.VELOCITY: 55>, <CUBA.NAME: 61>})
    >>> container[CUBA.NAME] = 'name'
    >>> container[CUBA.POSITION] = (1.0, 1.0, 1.0)
    ...
    ValueError: Key <CUBA.POSITION: 119> is not in the supported CUBA keywords
    '''
    # Make sure all restricted keys are CUBA keys
    if any(not isinstance(key, CUBA) for key in restricted_keys):
        raise ValueError('All restricted keys should be CUBA IntEnum')

    mapping = {key.name: key for key in restricted_keys}

    new_class = type(class_name, (DataContainer,),
                     {'__doc__': DataContainer.__doc__,
                      '__slots__': (),
                      'restricted_keys': frozenset(restricted_keys),
                      '_restricted_mapping': mapping})

    # For the dynamically generated class to have a chance to be
    # pickleable.  Bypass this step for some Python implementations
    try:
        new_class.__module__ = _sys._getframe(1).f_globals.get(
            '__name__', '__main__')
    except AttributeError:
        pass

    return new_class
