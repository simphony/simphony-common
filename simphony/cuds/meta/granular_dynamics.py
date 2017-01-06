from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class GranularDynamics(PhysicsEquation):
    """
    Granular dynamics of spherical particles using DEM
    """

    cuba_key = CUBA.GRANULAR_DYNAMICS

    def __init__(self, *args, **kwargs):
        super(GranularDynamics, self).__init__(*args, **kwargs)

        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(GranularDynamics, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _init_models(self):
        self._models = ['CUBA.MESOSCOPIC']

    @property
    def models(self):
        return self._models

    def _init_definition(self):
        self._definition = "Granular dynamics of spherical particles using DEM"

    @property
    def definition(self):
        return self._definition

    def _init_variables(self):
        self._variables = [
            'CUBA.POSITION', 'CUBA.VELOCITY', 'CUBA.MOMENTUM',
            'CUBA.ACCELERATION', 'CUBA.MOMENT_INERTIA', 'CUBA.TORQUE',
            'CUBA.ANGULAR_VELOCITY'
        ]

    @property
    def variables(self):
        return self._variables
