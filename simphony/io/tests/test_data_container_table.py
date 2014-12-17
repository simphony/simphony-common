import tempfile
import unittest
import shutil
import os


class TestDataContainerTable(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.filename = os.path.join(self.temp_dir, 'test_file.cuds')

    def tearDown(self):
        if os.path.exists(self.filename):
            self.file.close()
        shutil.rmtree(self.temp_dir)

    def test_creating_a_data_container_table(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
