import abc
import uuid


class CheckMaterialRelation(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        pass

    @abc.abstractmethod
    def get_kind():
        """ Returns the kinf of the tested relation

        """
        pass

    @abc.abstractmethod
    def container_factory(self, number):
        """ Create and return a given number of material relations.

        """
        pass

    def test_material_relation_name(self):
        """ Test that name is set correctly

        """

        relation = self.container_factory('foo_relation')
        original_name = relation.name
        original_name = 'foo_relation_2'

        assertEqual(relation.name, 'foo_relation')

    def test_material_relation_name_update(self):
        """ Test that name is updated correctly

        """

        relation = self.container_factory('foo_relation')
        relation.name = 'foo_relation_2'

        assertEqual(relation.name, 'foo_relation_2')

    def test_material_relation_invalid_name_update(self):
        """ Test that name is updated correctly

        """

        relation = self.container_factory('foo_relation')

        with self.assertRaises(TypeError):
            relation.name = 42

    def test_material_relation_parameters(self):
        """ Test that material relation parameteres are set correctly

        """

        # when
        relation = self.container_factory('foo_relation')

        # then
        self.assertEqual(relation._parameters, DataContainer())

    def test_material_relation_parameters_update(self):
        """ Test that material relation parameteres are updated correctly

        """

        # given
        relation = self.container_factory('foo_relation')
        data = create_data_container()
        expected_data = create_data_container(
            restrict=self.supported_parameters
        )

        # when
        relation.data = data

        # then
        self.assertEqual(relation.data, expected_data)
        self.assertIsNot(relation.data, expected_data)

    def test_material_relation_supported_parameters(self):
        """ Test that name is set correctly

        """
        pass

    def test_material_relation_supported_parameters_update(self):
        """ Test that name is updated correctly

        """

        relation = self.container_factory('foo_relation')

        with self.assertRaises(AttributeError):
            relation.kind = "invalid attribute"

    def test_material_relation_materials(self):
        """ Test that name is set correctly

        """

        relation = self.container_factory('foo_relation')
        relation.name = 'foo_relation_2'

        assertEqual(relation.name, 'foo_relation_2')

        pass

    def test_material_relation_materials_update(self):
        """ Test that name is updated correctly

        """
        pass

    def test_material_relation_kind(self):
        """ Test that kind is set correctly

        """

        relation = self.container_factory('foo_relation')

        assertEqual(self.kind, self.get_kind())

        pass

    def test_material_relation_kind_update(self):
        """ Test that kind can't be accessed

        """

        relation = self.container_factory('foo_relation')

        with self.assertRaises(AttributeError):
            relation.kind = "invalid attribute"
