from simphony.core.cuba import CUBA

_CUBA_MEMBERS = CUBA.__members__


class DataContainer(dict):
    """ A DataContainer instance

    The DataContainer object is implemented as a python dictionary whose keys
    are restricted to be members of the CUBA enum class.

    The data container can be initialized like a typical python dict
    using the mapping and iterables where the keys are CUBA enum members.

    For convenience keywords can be passed as capitalized CUBA enum members::

        >>> DataContainer(ACCELERATION=234)  # CUBA.ACCELERATION is 22
        {<CUBA.ACCELERATION: 22>: 234}

    """

    # Memory usage optimization.
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        """ Constructor.

        Initialization follows the behaviour of the python dict class.

        """
        self._check_arguments(args, kwargs)
        if len(args) == 1 and not hasattr(args[0], 'keys'):
            super(DataContainer, self).__init__()
            for key, value in args[0]:
                self.__setitem__(key, value)
        elif len(args) == 1:
            mapping = args[0]
            if not isinstance(mapping, DataContainer):
                if any(not isinstance(key, CUBA) for key in mapping):
                    non_cuba_keys = [
                        key for key in mapping if not isinstance(key, CUBA)]
                    message = \
                        "Key(s) {!r} are not in the approved CUBA keywords"
                    raise ValueError(message.format(non_cuba_keys))
            super(DataContainer, self).__init__(mapping)
        super(DataContainer, self).update(
            {CUBA[kwarg]: value for kwarg, value in kwargs.viewitems()})

    def __setitem__(self, key, value):
        """ Set/Update the key value only when the key is a CUBA key.

        """
        if isinstance(key, CUBA):
            super(DataContainer, self).__setitem__(key, value)
        else:
            message = "Key {!r} is not in the approved CUBA keywords"
            raise ValueError(message.format(key))

    def update(self, *args, **kwargs):
        self._check_arguments(args, kwargs)
        if len(args) == 1 and not hasattr(args[0], 'keys'):
            for key, value in args[0]:
                self.__setitem__(key, value)
        elif len(args) == 1:
            mapping = args[0]
            if not isinstance(mapping, DataContainer):
                if any(not isinstance(key, CUBA) for key in mapping):
                    non_cuba_keys = [
                        key for key in mapping if not isinstance(key, CUBA)]
                    message = \
                        "Key(s) {!r} are not in the approved CUBA keywords"
                    raise ValueError(message.format(non_cuba_keys))
            super(DataContainer, self).update(mapping)
        super(DataContainer, self).update(
            {CUBA[kwarg]: value for kwarg, value in kwargs.viewitems()})

    def _check_arguments(self, args, kwargs):
        """ Check for the right arguments.

        """
        # See if there are any non CUBA keys in the keyword arguments
        if any(key not in _CUBA_MEMBERS for key in kwargs):
            non_cuba_keys = kwargs.viewkeys() - _CUBA_MEMBERS.viewkeys()
            message = "Key(s) {!r} are not in the approved CUBA keywords"
            raise ValueError(message.format(non_cuba_keys))
        # Only one positional argument is allowed.
        if len(args) > 1:
            message = 'DataContainer expected at most 1 arguments, got {}'
            raise TypeError(message.format(len(args)))


def create_dummy_data(restrict=None):
    """ Create a dummy data container while respecting the expected data types.

    This is a utility function to be used for testing and prototyping.

    Parameters
    ----------
    restrict : list
        The list of CUBA keys to restrict the value population. Default is to
        use all CUBA keys.

    Returns
    -------
    data : DataContainer


    """

    if restrict is None:
        restrict = CUBA
    data = {cuba: dummy_cuba_value(cuba) for cuba in restrict}
    return DataContainer(data)


def dummy_cuba_value(cuba):
    """  Return a dummy value for the CUBA keyword.

    """
    # local imports to avoid circular import issues
    import numpy
    from simphony.io.data_container_description import Record

    Data = Record.columns['Data']
    column = CUBA(cuba).name.lower()
    # get the column type
    try:
        column_type = Data.columns[column]
    except AttributeError:
        column_type = Data._v_colobjects[column]

    if numpy.issubdtype(column_type, str):
        value = column.upper()
    elif numpy.issubdtype(column_type, numpy.float):
        value = float(cuba + 3)
    elif numpy.issubdtype(column_type, numpy.integer):
        value = int(cuba + 3)
    else:
        shape = column_type.shape
        if column_type.kind == 'float':
            value = numpy.ones(
                shape=shape, dtype=numpy.float64) * cuba + 3
        elif column_type.kind == 'int':
            value = numpy.ones(
                shape=shape, dtype=numpy.int32) * cuba + 3
        else:
            raise RuntimeError(
                'cannot create value for {}'.format(column_type))
    return value
