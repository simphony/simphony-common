from .physics_equation import PhysicsEquation
from .newtonian_fluid_model import NewtonianFluidModel
from .constant_electrostatic_field_model import ConstantElectrostaticFieldModel
from .isothermal_model import IsothermalModel
from simphony.core.cuba import CUBA
from . import validation
from simphony.core import Default
from .laminar_flow_model import LaminarFlowModel
from .single_phase_model import SinglePhaseModel
from .incompressible_fluid_model import IncompressibleFluidModel


class Cfd(PhysicsEquation):
    """
    Computational fluid dynamics general (set of ) equations for
    momentum, mass and energy
    """
    cuba_key = CUBA.CFD

    def __init__(self,
                 multiphase_model=Default,
                 rheology_model=Default,
                 turbulence_model=Default,
                 gravity_model=Default,
                 thermal_model=Default,
                 compressibility_model=Default,
                 electrostatic_model=Default,
                 *args,
                 **kwargs):
        super(Cfd, self).__init__(*args, **kwargs)

        self._init_multiphase_model(multiphase_model)
        self._init_definition()
        self._init_rheology_model(rheology_model)
        self._init_turbulence_model(turbulence_model)
        self._init_models()
        self._init_variables()
        self._init_gravity_model(gravity_model)
        self._init_thermal_model(thermal_model)
        self._init_compressibility_model(compressibility_model)
        self._init_electrostatic_model(electrostatic_model)

    def supported_parameters(self):
        try:
            base_params = super(Cfd, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return (
            CUBA.MULTIPHASE_MODEL,
            CUBA.RHEOLOGY_MODEL,
            CUBA.TURBULENCE_MODEL,
            CUBA.GRAVITY_MODEL,
            CUBA.THERMAL_MODEL,
            CUBA.COMPRESSIBILITY_MODEL,
            CUBA.ELECTROSTATIC_MODEL, ) + base_params

    def _init_multiphase_model(self, value):
        if value is Default:
            value = SinglePhaseModel()

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'MULTIPHASE_MODEL')
        return value

    def _init_definition(self):
        self._definition = "Computational fluid dynamics general (set of ) equations for momentum, mass and energy"  # noqa

    @property
    def definition(self):
        return self._definition

    def _init_rheology_model(self, value):
        if value is Default:
            value = NewtonianFluidModel()

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'RHEOLOGY_MODEL')
        return value

    def _init_turbulence_model(self, value):
        if value is Default:
            value = LaminarFlowModel()

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'TURBULENCE_MODEL')
        return value

    def _init_models(self):
        self._models = ['CUBA.CONTINUUM']  # noqa

    @property
    def models(self):
        return self._models

    def _init_variables(self):
        self._variables = [
            'CUBA.POSITION', 'CUBA.VELOCITY', 'CUBA.MOMENTUM', 'CUBA.DENSITY',
            'CUBA.VISCOSITY', 'CUBA.TIME', 'CUBA.STRESS_TENSOR',
            'CUBA.PRESSURE', 'CUBA.DYNAMIC_PRESSURE', 'CUBA.VOLUME_FRACTION'
        ]  # noqa

    @property
    def variables(self):
        return self._variables

    def _init_gravity_model(self, value):
        if value is Default:
            value = None

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'GRAVITY_MODEL')
        return value

    def _init_thermal_model(self, value):
        if value is Default:
            value = IsothermalModel()

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'THERMAL_MODEL')
        return value

    def _init_compressibility_model(self, value):
        if value is Default:
            value = IncompressibleFluidModel()

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'COMPRESSIBILITY_MODEL')
        return value

    def _init_electrostatic_model(self, value):
        if value is Default:
            value = ConstantElectrostaticFieldModel()

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
        validation.check_shape(value, [1])
        validation.validate_cuba_keyword(value, 'ELECTROSTATIC_MODEL')
        return value
