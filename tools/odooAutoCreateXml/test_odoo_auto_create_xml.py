import unittest
import os

from odoo_auto_create_xml import AutoOdooXml

class OdooAutoCreateXmlTestCase(unittest.TestCase):
    def setUp(self):
        self.oacx = AutoOdooXml('/path/path/path')
        self.test_case_path = os.path.join(os.path.dirname(__file__), 'test_case_files')
    

    def test_parse_py_right(self):
        file_path = os.path.join(self.test_case_path, 'test_parse_py_right.py')
        result = self.oacx.parse_py(file_path)
        self.assertEqual(len(result), 2)
        self.assertTrue('base.production.line' in result)
        self.assertTrue('base.production.line2' in result)
        self.assertEqual(len(result['base.production.line']['attrs']), 6)
        self.assertEqual(result['base.production.line']['description'], '产线')
        self.assertEqual(len(result['base.production.line2']['attrs']), 4)
        self.assertEqual(result['base.production.line2']['description'], '产线2')

    def test_parse_py_no_name(self):
        file_path = os.path.join(self.test_case_path, 'test_parse_py_no_name.py')
        result = self.oacx.parse_py(file_path)

        self.assertEqual(len(result), 1)
        self.assertTrue('base.production.line' in result)
        self.assertEqual(len(result['base.production.line']['attrs']), 1)
        self.assertEqual(result['base.production.line']['description'], '产线')

    def test_parse_py_no_description(self):
        file_path = os.path.join(self.test_case_path, 'test_parse_py_no_description.py')
        result = self.oacx.parse_py(file_path)
        self.assertEqual(result['base.production.line']['description'], 'base_production_line')

    def test_parset_py_no_attrs(self):
        file_path = os.path.join(self.test_case_path, 'test_parse_py_no_attrs.py')
        result = self.oacx.parse_py(file_path)
        self.assertTrue(result == {})

if __name__ == "__main__":
    unittest.main()






