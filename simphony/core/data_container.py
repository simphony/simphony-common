from collections import Mapping

from simphony.core.cuba import CUBA

_ERROR_MESSAGE = "Keys {!r} are not in the approved CUBA keywords"
_CUBA_KEYS = set(CUBA)


class DataContainer(dict):
    """ A DataContainer instance

    The DataContainer object is implemented as a python dictionary whose keys
    are restricted to be members of the CUBA enum class.

    """

    # Memory usage optimization.
    __slots__ = ()

    def __init__(self, *args, **kwards):
        """ Contructor.

        Initialization follows the behaviour of the python dict class.

        """
        self._check_arguments(args, kwards)
        if len(args) == 1 and not hasattr(args[0], 'keys'):
            super(DataContainer, self).__init__(**kwards)
            for key, value in args[0]:
                self.__setitem__(key, value)
            return
        super(DataContainer, self).__init__(*args, **kwards)

    def __setitem__(self, key, value):
        """ Set/Update the key value only when


        """
        if key in _CUBA_KEYS:
            super(DataContainer, self).__setitem__(key, value)
        else:
            message = "Key {!r} is not in the approved CUBA keywords"
            raise KeyError(message.format(key))

    def update(self, *args, **kwards):
        self._check_arguments(args, kwards)
        if len(args) == 1 and not hasattr(args[0], 'keys'):
            for key, value in argument:
                self.__setitem__(key, value)
            return
        super(DataContainer, self).update(*args, **kwards)

    def _check_arguments(self, args, kwards):
        """ Check for the right arguments

        """
        # See if there are any non CUBA keys in the mapping argument
        non_cuba_keys = kwards.viewkeys() - _CUBA_KEYS
        if len(non_cuba_keys) > 0:
            raise KeyError(_ERROR_MESSAGE.format(non_cuba_keys))
        if len(args) == 1:
            argument = args[0]
            if isinstance(argument, DataContainer):
                # This is already a DataContainer so we are sure that
                # it only contains CUBA keys.
                return
            if isinstance(argument, Mapping):
                # See if there any non CUBA keys in the mapping argument
                non_cuba_keys = set(argument.keys()) - _CUBA_KEYS
                if len(non_cuba_keys) > 0:
                    raise KeyError(_ERROR_MESSAGE.format(non_cuba_keys))
