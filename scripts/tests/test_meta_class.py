import inspect
import unittest
import warnings
from collections import Sequence

import numpy
import uuid

from simphony.api import CUBA
from simphony.core import DataContainer
from simphony.cuds.meta import api as meta_class


class TestMetaClass(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ''' Collect classes that can be instantiated without arguments
        '''
        cls.no_required_args_classes = []

        for name, klass in inspect.getmembers(meta_class, inspect.isclass):
            # Inspect the __init__ signature
            init_spec = inspect.getargspec(klass.__init__)

            # Number of required arguments
            num_required = len(init_spec.args) - len(init_spec.defaults) - 1

            if num_required > 0:
                if not hasattr(cls, 'test_'+name):
                    message = ('Instantiation of `{0}` required {1} arguments '
                               'and is not tested in batch. A test case '
                               '`test_{0}` is not found either. '
                               'Please add a test case.')
                    warnings.warn(message.format(name, num_required))
                continue

            cls.no_required_args_classes.append((name, klass))

    def check_cuds_item(self, instance):
        ''' Check properties of a CUDSItem '''
        self.assertIsInstance(instance.uid, uuid.UUID)
        self.assertIsNotNone(instance.data)

        # uuid is read-only
        with self.assertRaises(AttributeError):
            instance.uid = uuid.uuid4()

    def check_cuds_component(self, instance):
        ''' Check properties of a CUDS Component '''
        self.assertTrue(hasattr(instance, 'description'),
                        'Should have an attribute called `description`')
        self.assertTrue(hasattr(instance, 'name'),
                        'Should have an attribute called `name`')

        # definition is read-only
        with self.assertRaises(AttributeError):
            instance.definition = 'blah'

        # name should be a string, but it would be casted as such
        instance.name = 1
        self.assertIsInstance(instance.name, str)

        # description should be a string and it would be casted as such
        instance.description = 1
        self.assertIsInstance(instance.description, str)

        # Since NAME and DESCRIPTION are CUBA keys
        # Make sure that their values are stored in
        # the DataContainer as well
        instance.name = 'dummy name'
        self.assertEqual(instance.data[CUBA.NAME], 'dummy name')

        instance.description = 'dummy description'
        self.assertEqual(instance.data[CUBA.DESCRIPTION], 'dummy description')

    def check_model_equation(self, instance):
        ''' Check properties of a ModelEquation '''
        self.assertTrue(hasattr(instance, 'models'),
                        'Should have an attribute called `models`')
        self.assertIsNotNone(instance.models)
        self.assertTrue(hasattr(instance, 'variables'),
                        'Should have an attribute called `variables`')
        self.assertIsNotNone(instance.variables)

        # variables is read-only
        with self.assertRaises(AttributeError):
            instance.variables = ('1', '2')

        # models is read-only
        with self.assertRaises(AttributeError):
            instance.models = []

    def test_all_instantiate(self):
        ''' Test if classes that do not required arguments in init can be instantiated '''  # noqa
        errors = []

        message = ('Error when instantiating {klass} with {error_type}:'
                   '{error_message}')
        # Test instantiation
        for name, klass in self.no_required_args_classes:
            try:
                klass()
            except Exception as exception:
                errors.append(
                    message.format(klass=name,
                                   error_type=type(exception).__name__,
                                   error_message=str(exception)))
        if errors:
            self.fail('\n'.join(errors))

    def test_all_inherit_cuds_item(self):
        ''' Test if all classes that can be instantiated inherit from CUDSItem '''  # noqa
        errors = []

        message = '{klass} does not inherit from CUDSItem'

        # Test subclass
        for name, klass in self.no_required_args_classes:
            if not issubclass(klass, meta_class.CUDSItem):
                errors.append(message.format(klass=name))

            # Test properties for CUDSItem
            meta_obj = klass()
            self.check_cuds_item(meta_obj)

        if errors:
            self.fail('\n'.join(errors))

    def test_initialization_with_data(self):
        errors = []

        for name, klass in self.no_required_args_classes:
            if CUBA.NAME not in klass.supported_parameters():
                continue

            meta_obj = klass(data=DataContainer(NAME="foobar"))
            self.check_cuds_item(meta_obj)
            self.assertEqual(meta_obj.name, "foobar")

        if errors:
            self.fail('\n'.join(errors))

    def test_cuds_components_properties(self):
        ''' Test the properties of CUDSComponent '''
        for name, klass in self.no_required_args_classes:
            if issubclass(klass, meta_class.CUDSComponent):
                meta_obj = klass()
                self.check_cuds_component(meta_obj)

    def test_cuba_key(self):
        ''' Test API for cuba key '''
        for name, klass in self.no_required_args_classes:
            meta_obj = klass()
            self.assertIsInstance(meta_obj.cuba_key, CUBA)

    def test_parents(self):
        ''' Test API for parents '''
        for name, klass in self.no_required_args_classes:
            meta_obj = klass()
            self.assertIsInstance(meta_obj.parents(), Sequence)

    def test_supported_parameters(self):
        ''' Test API for supported_parameters '''
        for name, klass in self.no_required_args_classes:
            meta_obj = klass()
            self.assertIsInstance(meta_obj.supported_parameters(), Sequence)

    def test_Cfd(self):
        ''' Test for Cfd '''
        gravity_model = meta_class.GravityModel()

        meta_obj = meta_class.Cfd(gravity_model=gravity_model)

        # Test setting the attribute on init
        self.assertEqual(meta_obj.gravity_model, gravity_model)

        self.assertEqual(meta_obj.definition,
                         'Computational fluid dynamics general (set of ) equations for momentum, mass and energy')  # noqa

        # Test the default values
        self.assertIsInstance(meta_obj.compressibility_model,
                              meta_class.IncompressibleFluidModel)
        self.assertIsInstance(meta_obj.thermal_model,
                              meta_class.IsothermalModel)
        self.assertIsInstance(meta_obj.turbulence_model,
                              meta_class.LaminarFlowModel)
        self.assertIsInstance(meta_obj.multiphase_model,
                              meta_class.SinglePhaseModel)
        self.assertIsInstance(meta_obj.rheology_model,
                              meta_class.NewtonianFluidModel)
        self.assertIsInstance(meta_obj.electrostatic_model,
                              meta_class.ConstantElectrostaticFieldModel)

        self.check_cuds_item(meta_obj)
        self.check_cuds_component(meta_obj)
        self.check_model_equation(meta_obj)

    def test_ComputationalMethod(self):
        ''' Test for ComputationalMethod '''
        meta_obj = meta_class.ComputationalMethod()
        self.assertEqual(meta_obj.definition,
                         'A computational method according to the RoMM')  # noqa

        self.check_cuds_item(meta_obj)
        self.check_cuds_component(meta_obj)

    def test_LennardJones_6_12(self):
        ''' Test validation code using LennardJones_6_12 '''
        # Material needs to be of shape of 2, both instance of Material
        materials = (meta_class.Material(), meta_class.Material())
        meta_obj = meta_class.LennardJones_6_12(material=materials)

        # van_der_waals has to be a float
        with self.assertRaises(TypeError):
            # Casting None to float would raise an Error
            meta_obj.van_der_waals_radius = None

        # But this is fine
        meta_obj.van_der_waals_radius = 1.0

        # This is fine too, integer is upcasted to float
        meta_obj.van_der_waals_radius = 1
        self.assertIsInstance(meta_obj.van_der_waals_radius, float)

        with self.assertRaises(ValueError):
            # Has to be between two materials
            meta_obj.material = [1, 3, 5]

        with self.assertRaises(TypeError):
            # The items of the sequence are not instance of Material
            meta_obj.material = [1, 2]

    def test_Empty(self):
        ''' Test for EmptyBoundaryCondition '''
        # It can accept any number of materials
        for num_materials in range(5):
            materials = tuple(meta_class.Material()
                              for _ in range(num_materials))
            meta_obj = meta_class.Empty(material=materials)

        self.check_cuds_item(meta_obj)
        self.check_cuds_component(meta_obj)

    def test_Version(self):
        ''' Test for Version '''
        # This is fine
        meta_obj = meta_class.Version('1', '2', '3', '4')

        # minor/patch/... should be str, these can be casted
        meta_obj = meta_class.Version(1, '2', '3', '4')
        self.assertIsInstance(meta_obj.minor, str)
        self.assertIsInstance(meta_obj.patch, str)
        self.assertIsInstance(meta_obj.major, str)
        self.assertIsInstance(meta_obj.full, str)

        # But these can't be casted, raise an Error
        with self.assertRaises(TypeError):
            meta_obj = meta_class.Version(str, str, str, str)

        self.check_cuds_item(meta_obj)

    def test_physics_equation_are_model_equation(self):
        ''' Test all physics equations are model equations '''
        for name, klass in self.no_required_args_classes:
            if issubclass(klass, meta_class.PhysicsEquation):
                self.check_model_equation(klass())

    def test_Coulomb(self):
        meta_class.Coulomb(
            material=(meta_class.Material(), meta_class.Material()))

    def test_CoulombFrictionForce(self):
        # CoulombFrictionForce is a material relation
        # material should be a sequence of Material (any number)
        meta_class.CoulombFrictionForce(
            material=(meta_class.Material(), meta_class.Material()))

    def test_Dirichlet(self):
        meta_class.Dirichlet(
            material=(meta_class.Material(), meta_class.Material()))

    def test_DissipationForce(self):
        meta_class.DissipationForce(
            material=(meta_class.Material(), meta_class.Material()))

    def test_InteratomicPotential(self):
        meta_class.InteratomicPotential(
            material=(meta_class.Material(), meta_class.Material()))

    def test_MaterialRelation(self):
        meta_class.MaterialRelation(
            material=(meta_class.Material(), meta_class.Material()))

    def test_Neumann(self):
        meta_class.Neumann(
            material=(meta_class.Material(), meta_class.Material(),
                      meta_class.Material()))

    def test_PairPotential(self):
        meta_class.PairPotential(
            material=(meta_class.Material(), meta_class.Material()))

    def test_SjkrCohesionForce(self):
        meta_class.SjkrCohesionForce(
            material=(meta_class.Material(), meta_class.Material()))

    def test_SurfaceTensionRelation(self):
        meta_class.SurfaceTensionRelation(
            material=(meta_class.Material(), meta_class.Material()))

    def test_assign_vector(self):
        '''Test for assigning value to a CUBA with vector+float type'''
        # GravityModel.acceleration is a vector of float
        gravity_model = meta_class.GravityModel()

        with self.assertRaises(ValueError):
            # shape should be (3)
            gravity_model.acceleration = (1.0, 2.0)

        # Make sure values assigned can be obtained within
        # numerical precision
        expected = (1.e-10, 1.e-10, 1.e-10)
        gravity_model.acceleration = expected
        actual = gravity_model.acceleration
        numpy.testing.assert_allclose(actual, expected)

    def test_Basis(self):
        basis = meta_class.Basis()
        arr = basis.vector == numpy.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        self.assertTrue(arr.all())

    def test_Origin(self):
        origin = meta_class.Origin()
        arr = origin.position == numpy.array([0, 0, 0])
        self.assertTrue(arr.all())

    def test_Box(self):
        box = meta_class.Box()
        arr = box.vector == numpy.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.assertTrue(arr.all())

    def test_Berendsen(self):
        material = meta_class.Material()
        berendsen = meta_class.Berendsen(material=[material])

        self.assertIsNotNone(berendsen.material)

    def test_IntegrationStep(self):
        integration_step = meta_class.IntegrationStep(10, 10)
        self.assertIsNotNone(integration_step.data)

    def test_TemperatureRescaling(self):
        material = meta_class.Material()
        temp_rescaling = meta_class.TemperatureRescaling([material])
        self.assertIsNotNone(temp_rescaling.data)

    def test_Thermostat(self):
        material = meta_class.Material()
        thermostat = meta_class.Thermostat([material])
        self.assertIsNotNone(thermostat.data)

    def test_NoseHooverBoundary(self):
        material = meta_class.Material()
        nose_hoover = meta_class.NoseHoover([material])
        self.assertIsNotNone(nose_hoover.data)

    def test_not_sharing_mutable(self):
        box1 = meta_class.Box()
        box2 = meta_class.Box()
        box1.vector[0][0] = 1.
        self.assertNotEqual(box1.vector[0][0], box2.vector[0][0])
