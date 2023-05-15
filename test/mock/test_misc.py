import requests_mock
import unittest
from pysisnoapi import misc

class PySisnoApiTest(unittest.TestCase):

    def test_consulta_municipio(self):
        uf = "DF"

        with requests_mock.Mocker() as mocker:
            mocker.get(
                f'https://homolog.sisno.com.br/nfe-service/unidades-federativas/{uf}/municipios',
                json={'dados': [{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}]}
            )

            data = misc.get_municipios(uf=uf)
        
        assert data == [{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}]

if __name__ == "__main__":
    unittest.main()