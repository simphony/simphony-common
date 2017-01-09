from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class MolecularDynamics(PhysicsEquation):
    """
    Classical atomistic molecular dynamics using Newtons
    equations of motion
    """
    cuba_key = CUBA.MOLECULAR_DYNAMICS

    def __init__(self, *args, **kwargs):

        super(MolecularDynamics, self).__init__(*args, **kwargs)
        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(MolecularDynamics, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa    

    def _default_definition(self):
        return "Classical atomistic molecular dynamics using Newtons equations of motion"  # noqa    

    def _default_variables(self):
        return [
            'CUBA.POSITION', 'CUBA.VELOCITY', 'CUBA.MOMENTUM',
            'CUBA.ACCELERATION', 'CUBA.FORCE'
        ]  # noqa
