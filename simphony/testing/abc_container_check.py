import abc
from functools import partial

from simphony.testing.utils import (
    create_data_container, compare_data_containers)
from simphony.core.data_container import DataContainer
from simphony.core.cuba import CUBA


class ContainerCheck(object):

    __metaclass__ = abc.ABCMeta

    def setUp(self):
        self.addTypeEqualityFunc(
            DataContainer, partial(compare_data_containers, testcase=self))
        self.container = self.container_factory(u'foo')
        self.data = create_data_container()
        self.container.data = DataContainer(self.data)

    @abc.abstractmethod
    def container_factory(self, name):
        """ Create and return the container object
        """

    def test_name(self):
        self.assertEqual(self.contaoner.name, u'foo')

    def test_rename(self):
        container = self.container
        container.name = u'bar'
        self.assertEqual(container.name, u'bar')

    def test_data(self):
        self.assertEqual(self.container.data, self.data)
        self.assertIsNot(self.container.data, self.data)

    def test_update_data(self):
        container = self.container
        data = container.data
        data[CUBA.TEMPERATURE] = 23.4
        self.assertNotEqual(container.data, data)
        self.assertEqual(container.data, self.data)
        container.data = data
        self.assertEqual(container.data, data)
        self.assertIsNot(container.data, data)
