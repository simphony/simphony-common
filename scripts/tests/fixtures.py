from simphony_metaparser.flags import NoDefault

from simphony_metaparser.nodes import (
    Ontology, CUBADataType, CUDSItem, FixedPropertyEntry,
    VariablePropertyEntry)


def trivial_ontology():
    ontology = Ontology()
    ontology.data_types.extend([
        CUBADataType(name="CUBA.CUBA_DATA_ONE",
                     type="string"),
        CUBADataType(name="CUBA.CUBA_DATA_TWO",
                     type="string")
    ])
    ontology.root_cuds_item = CUDSItem(name="CUBA.CUDS_ROOT")
    ontology.root_cuds_item.children.extend([
        CUDSItem(name="CUBA.CUDS_C1", parent=ontology.root_cuds_item),
        CUDSItem(name="CUBA.CUDS_C2", parent=ontology.root_cuds_item)]
    )

    return ontology


def complex_ontology():
    ontology = Ontology()
    cuds_item = CUDSItem(name="CUBA.CUDS_ITEM")
    cuds_item.property_entries["data"] = FixedPropertyEntry(
        name="data",
        scope="CUBA.SYSTEM",
        default=NoDefault
    )

    cuds_item.property_entries["CUBA.UID"] = VariablePropertyEntry(
        name="CUBA.UID",
        scope="CUBA.SYSTEM",
        shape=[1],
        default=NoDefault
    )

    cuds_component = CUDSItem(name="CUBA.CUDS_COMPONENT",
                              parent=cuds_item)
    cuds_item.children.append(cuds_component)
    cuds_component.property_entries["CUBA.NAME"] = VariablePropertyEntry(
        name="CUBA.NAME",
        scope="CUBA.USER",
        shape=[1],
        default=""
    )

    physics_equation = CUDSItem(name="CUBA.PHYSICS_EQUATION",
                                parent=cuds_component)
    cuds_component.children.append(physics_equation)

    gravity_model = CUDSItem(name="CUBA.GRAVITY_MODEL",
                             parent=physics_equation)
    physics_equation.children.append(gravity_model)
    gravity_model.property_entries["models"] = FixedPropertyEntry(
        name="models",
        scope="CUBA.USER",
        default=["CUBA.MESOSCOPIC", "CUBA.CONTINUUM"]
    )
    gravity_model.property_entries["CUBA.ACCELERATION"] = \
        VariablePropertyEntry(name="CUBA.ACCELERATION",
                              scope="CUBA.USER",
                              shape=[1],
                              default=[0, 0, 0])

    ontology.root_cuds_item = cuds_item

    return ontology

def complex_ontology_output_gravity_model():
    return '''from simphony.core import Default  # noqa
from . import validation
from simphony.core.cuba import CUBA
from .physics_equation import PhysicsEquation
class GravityModel(PhysicsEquation):
    """
    """
    cuba_key = CUBA.GRAVITY_MODEL
    def __init__(self, acceleration=Default, name=Default):
        super(GravityModel, self).__init__(name=name)
        self._init_models()
        self._init_acceleration(acceleration)

    @classmethod
    def supported_parameters(cls):
        try:
            base_params = super(
                GravityModel,
                cls).supported_parameters()
        except AttributeError:
            base_params = ()
        return (CUBA.ACCELERATION, ) + base_params

    def _init_models(self):
        self._models = self._default_models()  # noqa

    @property
    def models(self):
        return self._models

    def _default_models(self):
        return ['CUBA.MESOSCOPIC', 'CUBA.CONTINUUM']  # noqa

    def _init_acceleration(self, value):
        if value is Default:
            value = self._default_acceleration()

        self.acceleration = value

    @property
    def acceleration(self):
        return self.data[CUBA.ACCELERATION]

    @acceleration.setter
    def acceleration(self, value):
        value = self._validate_acceleration(value)
        self.data[CUBA.ACCELERATION] = value

    def _validate_acceleration(self, value):
        value = validation.cast_data_type(value, 'ACCELERATION')
        validation.check_valid_shape(value, [1], 'ACCELERATION')
        validation.validate_cuba_keyword(value, 'ACCELERATION')
        return value

    def _default_acceleration(self):
        return [0, 0, 0]
'''
