import unittest
from pysisnoapi import misc

class PySisnoApiTest(unittest.TestCase):

    def test_consulta_municipio(self):
        uf = "DF"

        data = misc.get_municipios(uf=uf)
        
        assert data == [{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}]