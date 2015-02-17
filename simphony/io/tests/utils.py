import numpy

from simphony.io.data_container_description import Data
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA


def create_data_container(restrict=None):
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
        data = numpy.arange(numpy.prod(shape)) * cuba
        data = numpy.reshape(data, shape)
        if column_type.kind == 'float':
            value = numpy.ones(
                shape=shape, dtype=numpy.float64) * data
        elif column_type.kind == 'int':
            value = numpy.ones(
                shape=shape, dtype=numpy.int32) * data
        else:
            raise RuntimeError(
                'cannot create value for {}'.format(column_type))
    return value
