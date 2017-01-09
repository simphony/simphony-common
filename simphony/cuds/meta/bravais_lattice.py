from . import validation
from simphony.core import Default
from .lattice import Lattice
from simphony.core.cuba import CUBA


class BravaisLattice(Lattice):
    """
    A Bravais lattice
    """
    cuba_key = CUBA.BRAVAIS_LATTICE

    def __init__(self,
                 primitive_cell,
                 origin,
                 lattice_parameter=Default,
                 size=Default,
                 *args,
                 **kwargs):
        super(BravaisLattice, self).__init__(*args, **kwargs)

        self._init_definition()
        self._init_lattice_parameter(lattice_parameter)
        self._init_primitive_cell(primitive_cell)
        self._init_size(size)
        self._init_origin(origin)

    def supported_parameters(self):
        try:
            base_params = super(BravaisLattice, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.LATTICE_PARAMETER,
            CUBA.PRIMITIVE_CELL,
            CUBA.SIZE,
            CUBA.ORIGIN, ) + base_params

    def _init_definition(self):
        self._definition = "A Bravais lattice"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_lattice_parameter(self, value):
        if value is Default:
            value = [1.0, 1.0, 1.0]

        self.lattice_parameter = value

    @property
    def lattice_parameter(self):
        return self.data[CUBA.LATTICE_PARAMETER]

    @lattice_parameter.setter
    def lattice_parameter(self, value):
        value = self._validate_lattice_parameter(value)
        self.data[CUBA.LATTICE_PARAMETER] = value

    def _validate_lattice_parameter(self, value):

        value = validation.cast_data_type(value, 'LATTICE_PARAMETER')
        validation.check_shape(value, [3])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'LATTICE_PARAMETER')

        return value

    def _init_primitive_cell(self, value):
        if value is Default:
            raise TypeError("Value for primitive_cell must be specified")

        self.primitive_cell = value

    @property
    def primitive_cell(self):
        return self.data[CUBA.PRIMITIVE_CELL]

    @primitive_cell.setter
    def primitive_cell(self, value):
        value = self._validate_primitive_cell(value)
        self.data[CUBA.PRIMITIVE_CELL] = value

    def _validate_primitive_cell(self, value):
        value = validation.cast_data_type(value, 'PRIMITIVE_CELL')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'PRIMITIVE_CELL')
        return value

    def _init_size(self, value):
        if value is Default:
            value = [1, 1, 1]

        self.size = value

    @property
    def size(self):
        return self.data[CUBA.SIZE]

    @size.setter
    def size(self, value):
        value = self._validate_size(value)
        self.data[CUBA.SIZE] = value

    def _validate_size(self, value):

        value = validation.cast_data_type(value, 'SIZE')
        validation.check_shape(value, [3])

        def flatten(container):
            for i in container:
                if isinstance(i, (list, tuple)):
                    for j in flatten(i):
                        yield j
                else:
                    yield i

        if has_attr(container, "flatten"):
            flat_array = container.flatten()
        else:
            flat_array = flatten(value)

        for entry in flat_array:
            validation.validate_cuba_keyword(entry, 'SIZE')

        return value

    def _init_origin(self, value):
        if value is Default:
            raise TypeError("Value for origin must be specified")

        self.origin = value

    @property
    def origin(self):
        return self.data[CUBA.ORIGIN]

    @origin.setter
    def origin(self, value):
        value = self._validate_origin(value)
        self.data[CUBA.ORIGIN] = value

    def _validate_origin(self, value):
        value = validation.cast_data_type(value, 'ORIGIN')
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'ORIGIN')
        return value
