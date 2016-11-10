"""
    Testing module for CUDS serialization functions.
"""
import unittest
import os
import shutil
from contextlib import closing
import tempfile

from simphony.cuds.meta.cuds_component import CUDSComponent
from simphony.cuds.meta.material import Material
from simphony.cuds.meta.material_relation import MaterialRelation
from simphony.cuds.model import CUDS
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

        for item in CC.iter(CUDSComponent):
            self.assertEqual(item, None)

    def test_save_CUDS_complicated_data(self):
        filename = os.path.join(self.temp_dir, 'test_full.yml')
        C = CUDS(name='full',
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
        C.add(M2)
        C.add(M3)
        C.add(MR1)
        C.add(MR2)

        with closing(open(filename, 'w')) as handle:
            save_CUDS(handle, C)

        with closing(open(filename, 'r')) as handle:
            CC = load_CUDS(handle)

        self.assertEqual(CC.name, C.name)
        self.assertEqual(CC.description, C.description)

        # Iterate over components in the original model and check
        # that they are present in the loaded model. Loaded model
        # has additionally material 'M1' included.
        for Citem in C.iter(CUDSComponent):
            # Check items that have name parameter defined
            if Citem.name is not None:
                CCitem = CC.get(Citem.name)
                for key in Citem.data.keys():
                    Ci = Citem.data[key]
                    CCi = CCitem.data[key]
                    _compare_components(Ci, CCi, testcase=self)


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
            self.assertEqual(value, comp2.data[key])
    else:
        self.assertEqual(comp1, comp2)
