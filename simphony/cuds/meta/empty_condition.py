from simphony.core import Default  # noqa
from .condition import Condition
from simphony.core.cuba import CUBA


class EmptyCondition(Condition):
    """
    an entity to represent that no condition is applied on that
    domain or entitiy(ies)
    """
    cuba_key = CUBA.EMPTY_CONDITION

    def __init__(self, description=Default, name=Default):
        super(EmptyCondition, self).__init__(
            description=description, name=name)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(EmptyCondition, cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return tuple(set(() + base_params))

    def _default_definition(self):
        return "an entity to represent that no condition is applied on that domain or entitiy(ies)"  # noqa
