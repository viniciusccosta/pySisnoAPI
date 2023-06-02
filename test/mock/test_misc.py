import requests_mock
import unittest
from pysisnoapi import misc
from test.misc_common import *

class MiscTest(unittest.TestCase):

    def test_consulta_municipios_do_DF(self):
        uf = "DF"

        with requests_mock.Mocker() as mocker:
            mocker.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                json={'dados': [{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}]}
            )

            data = misc.get_municipios(uf=uf)
        
        check_municipios_do_DF(self, data)

if __name__ == "__main__":
    unittest.main()