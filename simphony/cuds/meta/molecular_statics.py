from simphony.core import Default  # noqa
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation


class MolecularStatics(PhysicsEquation):
    """
    Classical atomistic static molecular model
    """
    cuba_key = CUBA.MOLECULAR_STATICS

    def __init__(self, description=Default, name=Default):
        super(MolecularStatics, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(MolecularStatics, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_models(self):
        return ['CUBA.ATOMISTIC']  # noqa

    def _default_definition(self):
        return "Classical atomistic static molecular model"  # noqa

    def _default_variables(self):
        return ['CUBA.POSITION', 'CUBA.FORCE']  # noqa
