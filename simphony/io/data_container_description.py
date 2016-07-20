import numpy
import tables
import warnings

from simphony.core.keywords import KEYWORDS
from simphony.core.cuba import CUBA


# This is a non-exhaustive mapping between
# data types and tables' column types
_TYPE_MAPPINGS = {
    numpy.str: tables.StringCol,
    str: tables.StringCol,
    numpy.float64: tables.Float64Col,
    numpy.int32: tables.Int32Col,
    numpy.bool: tables.BoolCol,
    bool: tables.BoolCol
}


def create_data_table(class_name, supported_cuba=CUBA):
    ''' Create tables.IsDescription class dynamically given
    a set of supported CUBA IntEnum

    Parameters
    ----------
    class_name : str
        Name of the created class

    supported_cuba : iterable
        Supported CUBA IntEnum

    Returns
    -------
    type : tables.IsDescription
    '''
    table_meta = {}

    ignored_keys = []
    for ikey, cuba_key in enumerate(supported_cuba):
        keyword = KEYWORDS[cuba_key.name]

        # We skip keywords that do not have a known type
        dtype = keyword.dtype
        if dtype not in _TYPE_MAPPINGS:
            ignored_keys.append(cuba_key.name)
            continue

        column_type = _TYPE_MAPPINGS[dtype]

        column_meta = {'pos': ikey}
        shape = keyword.shape
        if column_type is tables.StringCol:
            column_meta['itemsize'] = shape[0]
        else:
            column_meta['shape'] = tuple(shape)

        table_meta[cuba_key.name.lower()] = column_type(**column_meta)

    if ignored_keys:
        warnings.warn(
            'Some keywords are not supported for serialisation: {}'.format(
                ', '.join(ignored_keys)))

    return type(class_name,
                (tables.IsDescription,),
                table_meta)


Data = create_data_table('Data', CUBA)

# FIXME: Not all CUBA values are supported in serialisation
# Set of CUBA that are supported in serialisation
SUPPORTED_CUBA = frozenset(getattr(CUBA, name.upper())
                           for name in Data.columns)


class Record(tables.IsDescription):

    index = tables.StringCol(itemsize=32, pos=0)
    data = Data()
    mask = tables.BoolCol(pos=1, shape=(len(Data.columns),))


class NoUIDRecord(tables.IsDescription):

    data = Data()
    mask = tables.BoolCol(pos=1, shape=(len(Data.columns),))
