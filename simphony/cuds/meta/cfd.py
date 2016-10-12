import uuid
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA
from .single_phase_model import SinglePhaseModel
from .physics_equation import PhysicsEquation
from .newtonian_fluid_model import NewtonianFluidModel
from .laminar_flow_model import LaminarFlowModel
from .isothermal_model import IsothermalModel
from .incompressible_fluid_model import IncompressibleFluidModel
from .constant_electrostatic_field_model import ConstantElectrostaticFieldModel
from . import validation


class Cfd(PhysicsEquation):
    '''Computational fluid dynamics general (set of ) equations for momentum, mass and energy  # noqa
    '''

    cuba_key = CUBA.CFD

    def __init__(self,
                 description=None,
                 name=None,
                 data=None,
                 multiphase_model=None,
                 rheology_model=None,
                 turbulence_model=None,
                 gravity_model=None,
                 thermal_model=None,
                 compressibility_model=None,
                 electrostatic_model=None):

        self.description = description
        self.name = name
        if data:
            self.data = data

        if multiphase_model:
            self.multiphase_model = multiphase_model
        else:
            self.multiphase_model = SinglePhaseModel()

        if rheology_model:
            self.rheology_model = rheology_model
        else:
            self.rheology_model = NewtonianFluidModel()

        if turbulence_model:
            self.turbulence_model = turbulence_model
        else:
            self.turbulence_model = LaminarFlowModel()
        self.gravity_model = gravity_model

        if thermal_model:
            self.thermal_model = thermal_model
        else:
            self.thermal_model = IsothermalModel()

        if compressibility_model:
            self.compressibility_model = compressibility_model
        else:
            self.compressibility_model = IncompressibleFluidModel()

        if electrostatic_model:
            self.electrostatic_model = electrostatic_model
        else:
            self.electrostatic_model = ConstantElectrostaticFieldModel()
        # This is a system-managed, read-only attribute
        self._models = [CUBA.CONTINUUM]
        # This is a system-managed, read-only attribute
        self._definition = 'Computational fluid dynamics general (set of ) equations for momentum, mass and energy'  # noqa
        # This is a system-managed, read-only attribute
        self._variables = [
            CUBA.POSITION, CUBA.VELOCITY, CUBA.MOMENTUM, CUBA.DENSITY,
            CUBA.VISCOSITY, CUBA.TIME, CUBA.STRESS_TENSOR, CUBA.PRESSURE,
            CUBA.DYNAMIC_PRESSURE, CUBA.VOLUME_FRACTION
        ]

    @property
    def data(self):
        try:
            data_container = self._data
        except AttributeError:
            self._data = DataContainer()
            return self._data
        else:
            # One more check in case the
            # property setter is by-passed
            if not isinstance(data_container, DataContainer):
                raise TypeError("data is not a DataContainer. "
                                "data.setter is by-passed.")
            return data_container

    @data.setter
    def data(self, new_data):
        if isinstance(new_data, DataContainer):
            self._data = new_data
        else:
            self._data = DataContainer(new_data)

    @property
    def multiphase_model(self):
        return self.data[CUBA.MULTIPHASE_MODEL]

    @multiphase_model.setter
    def multiphase_model(self, value):
        value = validation.cast_data_type(value, 'multiphase_model')
        validation.validate_cuba_keyword(value, 'multiphase_model')
        self.data[CUBA.MULTIPHASE_MODEL] = value

    @property
    def rheology_model(self):
        return self.data[CUBA.RHEOLOGY_MODEL]

    @rheology_model.setter
    def rheology_model(self, value):
        value = validation.cast_data_type(value, 'rheology_model')
        validation.validate_cuba_keyword(value, 'rheology_model')
        self.data[CUBA.RHEOLOGY_MODEL] = value

    @property
    def turbulence_model(self):
        return self.data[CUBA.TURBULENCE_MODEL]

    @turbulence_model.setter
    def turbulence_model(self, value):
        value = validation.cast_data_type(value, 'turbulence_model')
        validation.validate_cuba_keyword(value, 'turbulence_model')
        self.data[CUBA.TURBULENCE_MODEL] = value

    @property
    def gravity_model(self):
        return self.data[CUBA.GRAVITY_MODEL]

    @gravity_model.setter
    def gravity_model(self, value):
        if value is not None:
            value = validation.cast_data_type(value, 'gravity_model')
            validation.validate_cuba_keyword(value, 'gravity_model')
        self.data[CUBA.GRAVITY_MODEL] = value

    @property
    def thermal_model(self):
        return self.data[CUBA.THERMAL_MODEL]

    @thermal_model.setter
    def thermal_model(self, value):
        value = validation.cast_data_type(value, 'thermal_model')
        validation.validate_cuba_keyword(value, 'thermal_model')
        self.data[CUBA.THERMAL_MODEL] = value

    @property
    def compressibility_model(self):
        return self.data[CUBA.COMPRESSIBILITY_MODEL]

    @compressibility_model.setter
    def compressibility_model(self, value):
        value = validation.cast_data_type(value, 'compressibility_model')
        validation.validate_cuba_keyword(value, 'compressibility_model')
        self.data[CUBA.COMPRESSIBILITY_MODEL] = value

    @property
    def electrostatic_model(self):
        return self.data[CUBA.ELECTROSTATIC_MODEL]

    @electrostatic_model.setter
    def electrostatic_model(self, value):
        value = validation.cast_data_type(value, 'electrostatic_model')
        validation.validate_cuba_keyword(value, 'electrostatic_model')
        self.data[CUBA.ELECTROSTATIC_MODEL] = value

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
        return (CUBA.UUID, CUBA.TURBULENCE_MODEL, CUBA.COMPRESSIBILITY_MODEL,
                CUBA.DESCRIPTION, CUBA.GRAVITY_MODEL, CUBA.RHEOLOGY_MODEL,
                CUBA.THERMAL_MODEL, CUBA.ELECTROSTATIC_MODEL,
                CUBA.MULTIPHASE_MODEL, CUBA.NAME)

    @classmethod
    def parents(cls):
        return (CUBA.PHYSICS_EQUATION, CUBA.MODEL_EQUATION,
                CUBA.CUDS_COMPONENT, CUBA.CUDS_ITEM)
