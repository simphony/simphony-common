import abc
import uuid


class CheckMaterialRelation(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self._kind = retrieve_kind()
        pass

    @abc.abstractmethod
    def retrieve_kind():
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

        assertEqual(relation.name, 'foo_relation')

    def test_material_relation_name_update(self):
        """ Test that name is updated correctly

        """

        relation = self.container_factory('foo_relation')
        relation.name = 'other_name'

        assertEqual(relation.name, 'other_name')

    def test_material_relation_invalid_name_update(self):
        """ Test that name is updated correctly

        """

        relation = self.container_factory('foo_relation')

        with self.assertRaises(TypeError):
            relation.name = 42

    def test_material_relation_parameters(self):
        """ Test that material relation parameteres are set correctly

        """
        pass

    def test_material_relation_parameters_update(self):
        """ Test that material relation parameteres are updated correctly

        """
        pass

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
        pass

    def test_material_relation_materials_update(self):
        """ Test that name is updated correctly

        """
        pass

    def test_material_relation_kind(self):
        """ Test that kind is set correctly

        """

        relation = self.container_factory('foo_relation')

        assertEqual(self.kind, self.retrieve_kind())

        pass

    def test_material_relation_kind_update(self):
        """ Test that kind can't be accessed

        """

        relation = self.container_factory('foo_relation')

        with self.assertRaises(AttributeError):
            relation.kind = "invalid attribute"
