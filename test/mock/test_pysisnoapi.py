import unittest
from pysisnoapi import Municipio

class TestMunicipio(unittest.TestCase):       
    def test_default_values(self):
        m = Municipio()
        self.assertIsNone(m.codigo_ibge)
        self.assertIsNone(m.descricao)
        
    def test_custom_values(self):
        m = Municipio(codigo_ibge=123, descricao='foo')
        self.assertEqual(m.codigo_ibge, 123)
        self.assertEqual(m.descricao, 'foo')
        
    def test_from_json(self):
        json_dict = {'codigo_ibge': 456, 'descricao': 'bar'}
        m = Municipio.from_json(**json_dict)
        self.assertEqual(m.codigo_ibge, 456)
        self.assertEqual(m.descricao, 'bar')

if __name__ == "__main__":
    unittest.main()