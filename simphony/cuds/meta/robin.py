from simphony.core import Default  # noqa
from .mixed_condition import MixedCondition
from simphony.core.cuba import CUBA
from simphony.cuds import meta_validation


class Robin(MixedCondition):
    """
    A mixed boundary condition $\alpha \Phi (x) + \beta (x)
    \partial {\Phi} / \partial {\bf{n}} (x) = h(x)$, with $h$ is
    the value.
    """
    cuba_key = CUBA.ROBIN

    def __init__(self,
                 dirichlet,
                 neumann,
                 material,
                 description=Default,
                 name=Default):
        super(Robin, self).__init__(
            material=material, description=description, name=name)
        self._init_dirichlet(dirichlet)
        self._init_neumann(neumann)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(Robin, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set((
            CUBA.DIRICHLET,
            CUBA.NEUMANN, ) + base_params))

    def _default_definition(self):
        return "A mixed boundary condition $\alpha \Phi (x) + \beta (x) \partial {\Phi} / \partial {\bf{n}} (x) = h(x)$, with $h$ is the value."  # noqa

    def _init_dirichlet(self, value):
        if value is Default:
            value = self._default_dirichlet()

        self.dirichlet = value

    @property
    def dirichlet(self):
        return self.data[CUBA.DIRICHLET]

    @dirichlet.setter
    def dirichlet(self, value):
        value = self._validate_dirichlet(value)
        self.data[CUBA.DIRICHLET] = value

    def _validate_dirichlet(self, value):
        value = meta_validation.cast_data_type(value, 'DIRICHLET')
        meta_validation.check_valid_shape(value, [1], 'DIRICHLET')
        meta_validation.validate_cuba_keyword(value, 'DIRICHLET')
        return value

    def _default_dirichlet(self):
        raise TypeError("No default for dirichlet")

    def _init_neumann(self, value):
        if value is Default:
            value = self._default_neumann()

        self.neumann = value

    @property
    def neumann(self):
        return self.data[CUBA.NEUMANN]

    @neumann.setter
    def neumann(self, value):
        value = self._validate_neumann(value)
        self.data[CUBA.NEUMANN] = value

    def _validate_neumann(self, value):
        value = meta_validation.cast_data_type(value, 'NEUMANN')
        meta_validation.check_valid_shape(value, [1], 'NEUMANN')
        meta_validation.validate_cuba_keyword(value, 'NEUMANN')
        return value

    def _default_neumann(self):
        raise TypeError("No default for neumann")
