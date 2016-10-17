"""
    Testing module for CUDS serialization functions.
"""
import unittest
import os
import shutil
from contextlib import closing
import tempfile
import numpy
import string
import random
from importlib import import_module

from simphony.cuds.meta.cuds_component import CUDSComponent
from simphony.cuds.model import CUDS
from simphony.core.keywords import KEYWORDS
from simphony.core.cuba import CUBA
from simphony.io.serialisation import save_CUDS, load_CUDS
from simphony.cuds.meta.validation import to_camel_case


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

    def test_save_CUDS_full(self):
        filename = os.path.join(self.temp_dir, 'test_full.yml')
        C = CUDS(name='full', description='fully randomized model')

        for key in KEYWORDS.keys():
            if key not in ['VERSION']:
                comp = self._create_random_comp(key)
                if comp:
                    C.add(comp)

        with closing(open(filename, 'w')) as handle:
            save_CUDS(handle, C)

        with closing(open(filename, 'r')) as handle:
            CC = load_CUDS(handle)

        self.assertEqual(CC.name, C.name)
        self.assertEqual(CC.description, C.description)

        # Iterate over components in the original model and check
        # that they are present in the loaded model
        for Citem in C.iter(CUDSComponent):
            # Check items that have name parameter defined
            if hasattr(CCitem, 'name'):
                Citem = C.get(CCitem.name)
                self.assertEqual(Citem.name, CCitem.name)
                for key in CCitem.data:
                    self.assertEqual(Citem.data[key], CCitem.data[key])

    def _ran(self, dtype, shape):
        if dtype == numpy.int32:
            if shape == []:
                shape = [1]
            return numpy.random.randint(-9999999, 9999999, size=shape)
        elif dtype == numpy.float64:
            if shape == [] or shape is None:
                return numpy.random.rand(3)
            elif len(shape) == 2:
                return numpy.random.rand(shape[0], shape[1])
            elif len(shape) == 1:
                if shape[0] == 1:
                    return numpy.random.rand(1)[0]
                else:
                    return numpy.random.rand(shape[0])
        elif dtype == str:
            randstr = ''.join(random.choice(string.ascii_uppercase)
                              for _ in range(shape[0]))
            return randstr
        elif dtype == bool:
            return random.choice([True, False])

    def _create_random_comp(self, key):
        api = import_module('simphony.cuds.meta.api')
        if to_camel_case(key) in dir(api):
            mod = import_module('simphony.cuds.meta.%s' % key.lower())
            comp_class = getattr(mod, to_camel_case(key))

            if issubclass(comp_class, CUDSComponent):
                comp_inst = comp_class(None, None)
                data_dict = {}
                for prm in comp_inst.supported_parameters():
                    if prm is not CUBA.UUID:
                        name = str(prm).replace('CUBA.', '')
                        if numpy.random.randint(2):
                            if to_camel_case(name) in dir(api):
                                # Create one or two subcomponents if supported
                                if numpy.random.randint(2):
                                    subcomp1 = self._create_random_comp(name)
                                    data_dict[prm] = subcomp1
                                else:
                                    subcomp1 = self._create_random_comp(name)
                                    subcomp2 = self._create_random_comp(name)
                                    data_dict[prm] = [subcomp1, subcomp2]
                            else:
                                dtype = KEYWORDS[name].dtype
                                shape = KEYWORDS[name].shape
                                val = self._ran(dtype, shape)
                                data_dict[prm] = val
                comp_inst.data = data_dict
                return comp_inst
        return None
