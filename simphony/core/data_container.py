from simphony.core.cuba import CUBA

_CUBA_MEMBERS = CUBA.__members__.viewkeys()


class DataContainer(dict):
    """ A DataContainer instance

    The DataContainer object is implemented as a python dictionary whose keys
    are restricted to be members of the CUBA enum class.

    The data container can be initialized like a typical python dict
    using the mapping and iterables where the keys are CUBA enum members.

    For convenience int keys are also accepted, as long as they correspond
    to a CUBA member::

        >>> DataContainer({19: 234})  # CUBA.ACCELERATION is 19
        {<CUBA.ACCELERATION: 19>: 234}

    Similarly, keywords can be passed as capitalized CUBA enum members::

        >>> DataContainer(ACCELERATION=234)  # CUBA.ACCELERATION is 19
        {<CUBA.ACCELERATION: 19>: 234}

    """

    # Memory usage optimization.
    __slots__ = ()

    def __init__(self, *args, **kwards):
        """ Constructor.

        Initialization follows the behaviour of the python dict class.

        """
        self._check_arguments(args, kwards)
        if len(args) == 1 and not hasattr(args[0], 'keys'):
            super(DataContainer, self).__init__()
            for key, value in args[0]:
                self.__setitem__(key, value)
        elif len(args) == 1:
            mapping = args[0]
            if not isinstance(mapping, DataContainer):
                mapping = {
                    CUBA(key): value for key, value in mapping.iteritems()}
            super(DataContainer, self).__init__(mapping)
        super(DataContainer, self).update(
            {CUBA[kward]: value for kward, value in kwards.iteritems()})

    def __setitem__(self, key, value):
        """ Set/Update the key value only when it can successfully be coerced

        """
        super(DataContainer, self).__setitem__(CUBA(key), value)

    def update(self, *args, **kwards):
        self._check_arguments(args, kwards)
        if len(args) == 1 and not hasattr(args[0], 'keys'):
            for key, value in args[0]:
                self.__setitem__(key, value)
        elif len(args) == 1:
            mapping = args[0]
            if not isinstance(mapping, DataContainer):
                mapping = {
                    CUBA(key): value for key, value in mapping.iteritems()}
            super(DataContainer, self).update(mapping)
        super(DataContainer, self).update(
            {CUBA[kward]: value for kward, value in kwards.iteritems()})

    def _check_arguments(self, args, kwards):
        """ Check for the right arguments.

        """
        # See if there are any non CUBA keys in the keyword arguments
        non_cuba_keys = kwards.viewkeys() - _CUBA_MEMBERS
        if len(non_cuba_keys) > 0:
            message = "Keys {!r} are not in the approved CUBA keywords"
            raise ValueError(message.format(non_cuba_keys))
        if len(args) > 1:
            message = 'DataContainer expected at most 1 arguments, got {}'
            raise TypeError(message.format(len(args)))
