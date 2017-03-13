from simphony.core import Default  # noqa
from .constant_electrostatic_field_model import ConstantElectrostaticFieldModel
from .single_phase_model import SinglePhaseModel
from .newtonian_fluid_model import NewtonianFluidModel
from .isothermal_model import IsothermalModel
from simphony.core.cuba import CUBA
from . import validation
from .gravity_model import GravityModel
from .laminar_flow_model import LaminarFlowModel
from .physics_equation import PhysicsEquation
from .incompressible_fluid_model import IncompressibleFluidModel


class Cfd(PhysicsEquation):
    """
    Computational fluid dynamics general (set of ) equations for
    momentum, mass and energy
    """
    cuba_key = CUBA.CFD

    def __init__(self,
                 compressibility_model=Default,
                 electrostatic_model=Default,
                 gravity_model=Default,
                 multiphase_model=Default,
                 rheology_model=Default,
                 thermal_model=Default,
                 turbulence_model=Default,
                 description=Default,
                 name=Default):
        super(Cfd, self).__init__(description=description, name=name)
        self._init_multiphase_model(multiphase_model)
        self._init_gravity_model(gravity_model)
        self._init_turbulence_model(turbulence_model)
        self._init_rheology_model(rheology_model)
        self._init_thermal_model(thermal_model)
        self._init_compressibility_model(compressibility_model)
        self._init_electrostatic_model(electrostatic_model)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Cfd, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(
            set((CUBA.MULTIPHASE_MODEL, CUBA.GRAVITY_MODEL,
                 CUBA.TURBULENCE_MODEL, CUBA.RHEOLOGY_MODEL,
                 CUBA.THERMAL_MODEL, CUBA.COMPRESSIBILITY_MODEL,
                 CUBA.ELECTROSTATIC_MODEL, ) + base_params))

    def _init_multiphase_model(self, value):
        if value is Default:
            value = self._default_multiphase_model()

        self.multiphase_model = value

    @property
    def multiphase_model(self):
        return self.data[CUBA.MULTIPHASE_MODEL]

    @multiphase_model.setter
    def multiphase_model(self, value):
        value = self._validate_multiphase_model(value)
        self.data[CUBA.MULTIPHASE_MODEL] = value

    def _validate_multiphase_model(self, value):
        value = validation.cast_data_type(value, 'MULTIPHASE_MODEL')
        validation.check_valid_shape(value, [1], 'MULTIPHASE_MODEL')
        validation.validate_cuba_keyword(value, 'MULTIPHASE_MODEL')
        return value

    def _default_multiphase_model(self):
        return SinglePhaseModel()

    def _default_definition(self):
        return "Computational fluid dynamics general (set of ) equations for momentum, mass and energy"  # noqa

    def _init_gravity_model(self, value):
        if value is Default:
            value = self._default_gravity_model()

        self.gravity_model = value

    @property
    def gravity_model(self):
        return self.data[CUBA.GRAVITY_MODEL]

    @gravity_model.setter
    def gravity_model(self, value):
        value = self._validate_gravity_model(value)
        self.data[CUBA.GRAVITY_MODEL] = value

    def _validate_gravity_model(self, value):
        value = validation.cast_data_type(value, 'GRAVITY_MODEL')
        validation.check_valid_shape(value, [1], 'GRAVITY_MODEL')
        validation.validate_cuba_keyword(value, 'GRAVITY_MODEL')
        return value

    def _default_gravity_model(self):
        return GravityModel()

    def _init_turbulence_model(self, value):
        if value is Default:
            value = self._default_turbulence_model()

        self.turbulence_model = value

    @property
    def turbulence_model(self):
        return self.data[CUBA.TURBULENCE_MODEL]

    @turbulence_model.setter
    def turbulence_model(self, value):
        value = self._validate_turbulence_model(value)
        self.data[CUBA.TURBULENCE_MODEL] = value

    def _validate_turbulence_model(self, value):
        value = validation.cast_data_type(value, 'TURBULENCE_MODEL')
        validation.check_valid_shape(value, [1], 'TURBULENCE_MODEL')
        validation.validate_cuba_keyword(value, 'TURBULENCE_MODEL')
        return value

    def _default_turbulence_model(self):
        return LaminarFlowModel()

    def _default_models(self):
        return ['CUBA.CONTINUUM']  # noqa

    def _default_variables(self):
        return [
            'CUBA.POSITION', 'CUBA.VELOCITY', 'CUBA.MOMENTUM', 'CUBA.DENSITY',
            'CUBA.VISCOSITY', 'CUBA.TIME', 'CUBA.STRESS_TENSOR',
            'CUBA.PRESSURE', 'CUBA.DYNAMIC_PRESSURE', 'CUBA.VOLUME_FRACTION'
        ]  # noqa

    def _init_rheology_model(self, value):
        if value is Default:
            value = self._default_rheology_model()

        self.rheology_model = value

    @property
    def rheology_model(self):
        return self.data[CUBA.RHEOLOGY_MODEL]

    @rheology_model.setter
    def rheology_model(self, value):
        value = self._validate_rheology_model(value)
        self.data[CUBA.RHEOLOGY_MODEL] = value

    def _validate_rheology_model(self, value):
        value = validation.cast_data_type(value, 'RHEOLOGY_MODEL')
        validation.check_valid_shape(value, [1], 'RHEOLOGY_MODEL')
        validation.validate_cuba_keyword(value, 'RHEOLOGY_MODEL')
        return value

    def _default_rheology_model(self):
        return NewtonianFluidModel()

    def _init_thermal_model(self, value):
        if value is Default:
            value = self._default_thermal_model()

        self.thermal_model = value

    @property
    def thermal_model(self):
        return self.data[CUBA.THERMAL_MODEL]

    @thermal_model.setter
    def thermal_model(self, value):
        value = self._validate_thermal_model(value)
        self.data[CUBA.THERMAL_MODEL] = value

    def _validate_thermal_model(self, value):
        value = validation.cast_data_type(value, 'THERMAL_MODEL')
        validation.check_valid_shape(value, [1], 'THERMAL_MODEL')
        validation.validate_cuba_keyword(value, 'THERMAL_MODEL')
        return value

    def _default_thermal_model(self):
        return IsothermalModel()

    def _init_compressibility_model(self, value):
        if value is Default:
            value = self._default_compressibility_model()

        self.compressibility_model = value

    @property
    def compressibility_model(self):
        return self.data[CUBA.COMPRESSIBILITY_MODEL]

    @compressibility_model.setter
    def compressibility_model(self, value):
        value = self._validate_compressibility_model(value)
        self.data[CUBA.COMPRESSIBILITY_MODEL] = value

    def _validate_compressibility_model(self, value):
        value = validation.cast_data_type(value, 'COMPRESSIBILITY_MODEL')
        validation.check_valid_shape(value, [1], 'COMPRESSIBILITY_MODEL')
        validation.validate_cuba_keyword(value, 'COMPRESSIBILITY_MODEL')
        return value

    def _default_compressibility_model(self):
        return IncompressibleFluidModel()

    def _init_electrostatic_model(self, value):
        if value is Default:
            value = self._default_electrostatic_model()

        self.electrostatic_model = value

    @property
    def electrostatic_model(self):
        return self.data[CUBA.ELECTROSTATIC_MODEL]

    @electrostatic_model.setter
    def electrostatic_model(self, value):
        value = self._validate_electrostatic_model(value)
        self.data[CUBA.ELECTROSTATIC_MODEL] = value

    def _validate_electrostatic_model(self, value):
        value = validation.cast_data_type(value, 'ELECTROSTATIC_MODEL')
        validation.check_valid_shape(value, [1], 'ELECTROSTATIC_MODEL')
        validation.validate_cuba_keyword(value, 'ELECTROSTATIC_MODEL')
        return value

    def _default_electrostatic_model(self):
        return ConstantElectrostaticFieldModel()
