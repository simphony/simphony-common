import uuid
from simphony.core.data_container import create_data_container
from simphony.core.cuba import CUBA
from .condition import Condition
from . import validation

_RestrictedDataContainer = create_data_container(
    (CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.UUID, CUBA.NAME),
    class_name="_RestrictedDataContainer")


class DirichletBoundaryCondition(Condition):
    '''Dirichlet boundary condition  # noqa
    '''

    cuba_key = CUBA.DIRICHLET_BOUNDARY_CONDITION

    def __init__(self, material, description=None, name=None, data=None):

        self.material = material
        self.description = description
        self.name = name
        if data:
            self.data = data
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Dirichlet boundary condition'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = None

    @property
    def material(self):
        return self.data[CUBA.MATERIAL]

    @material.setter
    def material(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'material')
            validation.check_shape(value, '(:)')
            for item in value:
                validation.validate_cuba_keyword(item, 'material')
        self.data[CUBA.MATERIAL] = value

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = _RestrictedDataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, _RestrictedDataContainer):
                raise TypeError("data is not a RestrictedDataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, _RestrictedDataContainer):
            self._data = new_data
        else:
            self._data = _RestrictedDataContainer(new_data)

    @property
    def models(self):
        return self._models

    @property
    def definition(self):
        return self._definition

    @property
    def variables(self):
        return self._variables

    @property
    def uid(self):
        if not hasattr(self, '_uid') or self._uid is None:
            self._uid = uuid.uuid4()
        return self._uid

    @classmethod
    def supported_parameters(cls):
        return (CUBA.DESCRIPTION, CUBA.MATERIAL, CUBA.UUID, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.CONDITION, CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
