from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class GranularDynamics(PhysicsEquation):
    """
    Granular dynamics of spherical particles using DEM
    """
    cuba_key = CUBA.GRANULAR_DYNAMICS

    def __init__(self, description=Default, name=Default):

        super(GranularDynamics, self).__init__(
            description=description, name=name)

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
