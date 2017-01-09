from .physics_equation import PhysicsEquation
from simphony.core.cuba import CUBA


class MolecularStatics(PhysicsEquation):
    """
    Classical atomistic static molecular model
    """
    cuba_key = CUBA.MOLECULAR_STATICS

    def __init__(self, *args, **kwargs):

        super(MolecularStatics, self).__init__(*args, **kwargs)
        self._init_models()
        self._init_definition()
        self._init_variables()

    def supported_parameters(self):
        try:
            base_params = super(MolecularStatics, self).supported_parameters()
        except AttributeError:
            base_params = ()

        return () + base_params

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa

    def _default_definition(self):
        return "Classical atomistic static molecular model"  # noqa

    def _default_variables(self):
        return ['CUBA.POSITION', 'CUBA.FORCE']  # noqa
