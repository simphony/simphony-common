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

    def _default_models(self):
        return ['CUBA.MESOSCOPIC']  # noqa

    def _default_definition(self):
        return "Granular dynamics of spherical particles using DEM"  # noqa

    def _default_variables(self):
        return [
            'CUBA.POSITION', 'CUBA.VELOCITY', 'CUBA.MOMENTUM',
            'CUBA.ACCELERATION', 'CUBA.MOMENT_INERTIA', 'CUBA.TORQUE',
            'CUBA.ANGULAR_VELOCITY'
        ]  # noqa
