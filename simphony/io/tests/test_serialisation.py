"""
    Testing module for CUDS serialization functions.
"""
import unittest
import os
import shutil
from contextlib import closing
import tempfile
import uuid

from simphony.core import CUBA
from simphony.cuds.meta.api import CUDSComponent
from simphony.cuds.meta.api import Material
from simphony.cuds.meta.api import MaterialRelation
from simphony.cuds import CUDS
from simphony.io.serialisation import save_CUDS, load_CUDS


class TestSerialisation(unittest.TestCase):
    """Tests for CUDS Yaml serialisation functions."""
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_save_CUDS_name(self):
        name = 'somename'
        filename = os.path.join(self.temp_dir, 'test_named.yml')
        C = CUDS(name=name)
        with closing(open(filename, 'w')) as handle:
            save_CUDS(handle, C)

        with closing(open(filename, 'r')) as handle:
            CC = load_CUDS(handle)
        self.assertEqual(CC.name, name)

    def test_save_CUDS_description(self):
        description = 'some very long description'
        filename = os.path.join(self.temp_dir, 'test_description.yml')
        C = CUDS(description=description)
        with closing(open(filename, 'w')) as handle:
            save_CUDS(handle, C)

        with closing(open(filename, 'r')) as handle:
            CC = load_CUDS(handle)
        self.assertEqual(CC.description, description)

    def test_save_CUDS_empty(self):
        filename = os.path.join(self.temp_dir, 'test_empty.yml')
        C = CUDS(name='empty', description='just an empty model')
        with closing(open(filename, 'w')) as handle:
            save_CUDS(handle, C)

        with closing(open(filename, 'r')) as handle:
            CC = load_CUDS(handle)

        self.assertEqual(CC.name, C.name)
        self.assertEqual(CC.description, C.description)

        for item in CC.iter(item_type=CUBA.CUDS_COMPONENT):
            self.assertEqual(item, None)

    def test_save_CUDS_complicated_data(self):
        filename = os.path.join(self.temp_dir, 'test_full.yml')
        cuds = CUDS(name='full',
                    description='model with crossreferenced components')

        M1 = Material(name='steel',
                      description='FCC steel sphere structure')
        M2 = Material(name='epoxy', description='')
        M3 = Material(name='iron', description='sheet metal container')
        MR1 = MaterialRelation(name='steel spheres in epoxy',
                               material=[M1, M2])
        MR2 = MaterialRelation(name='epoxy in sheet metal container',
                               material=[M2, M3])
        # M1 is not added
        cuds.add([M2])
        cuds.add([M3])
        cuds.add([MR1])
        cuds.add([MR2])

        with closing(open(filename, 'w')) as handle:
            save_CUDS(handle, cuds)
            print("cuds data", cuds.data)

        with closing(open(filename, 'r')) as handle:
            loaded_cuds = load_CUDS(handle)
            print("loaded_cuds data", loaded_cuds.data)

        self.assertEqual(loaded_cuds.name, cuds.name)
        self.assertEqual(loaded_cuds.description, cuds.description)

        for cuds_item in cuds.iter(item_type=CUBA.CUDS_COMPONENT):
            print('item original', cuds_item)

        for cuds_item in loaded_cuds.iter(item_type=CUBA.CUDS_COMPONENT):
            print('item loaded', cuds_item)

        # Iterate over components in the original model and check
        # that they are present in the loaded model. Loaded model
        # has additionally material 'M1' included.
        for cuds_item in cuds.iter(item_type=CUBA.CUDS_COMPONENT):
            # Check items that have name parameter defined
            print("cuds_item", cuds_item)
            if cuds_item.name is not None:
                loaded_item = loaded_cuds.get(cuds_item.uid)
                print("loaded_item", loaded_item)
                for key in cuds_item.data.keys():
                    ci = cuds_item.data[key]
                    li = loaded_item.data[key]
                    _compare_components(ci, li, testcase=self)


def _compare_components(comp1, comp2, testcase):
    self = testcase
    if type(comp1) == list:
        for i in xrange(len(comp1)):
            if isinstance(comp1[i], CUDSComponent):
                _compare_components(comp1[i], comp2[i], self)
            else:
                self.assertEqual(comp1[i], comp2[i])
    elif isinstance(comp1, CUDSComponent):
        for key, value in comp1.data.iteritems():
            if type(value) == list:
                for i in xrange(len(value)):
                    if isinstance(value[i], CUDSComponent):
                        _compare_components(value[i], comp2.data[key][i],
                                            self)
                    else:
                        self.assertEqual(value[i], comp2.data[key][i])
            elif type(value) == uuid.UUID:
                # Skip the uuid
                continue
            self.assertEqual(value, comp2.data[key])
    elif isinstance(comp1, uuid.UUID):
        # Skip the uuid
        pass
    else:
        self.assertEqual(comp1, comp2)
