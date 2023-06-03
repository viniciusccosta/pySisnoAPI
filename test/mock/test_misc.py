# ==========================================================================
import unittest
import requests

from pysisnoapi import misc
from test.misc_common import *
from unittest.mock import MagicMock
from typing import List

# ==========================================================================
UF = 'MG'

# ==========================================================================
class MiscTest(unittest.TestCase):
    def test_get_municipios_success(self):
        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "Sucesso",
            "descricao": "Lista de municípios",
            'dados': [
                {
                    'codigo_ibge': 3106200,
                    'descricao': 'Belo Horizonte',
                },
                {
                    'codigo_ibge': 3118601,
                    'descricao': 'Contagem',
                },
            ]
        }
        requests.get = MagicMock(return_value=mock_response)

        # Chama a função:
        municipios = misc.get_municipios(UF)

        # Checando resultado:
        self.assertIsInstance(municipios, List)
        self.assertEqual(len(municipios), 2)
        self.assertIsInstance(municipios[0], Municipio)
        self.assertEqual(municipios[0].descricao, 'Belo Horizonte')
        self.assertEqual(municipios[1].codigo_ibge, 3118601)
        
    def test_get_municipios_falha_412(self):
        # Nocking:
        mock_response = MagicMock()
        mock_response.status_code = 412
        requests.get = MagicMock(return_value=mock_response)

        # Chama a função:
        municipios = misc.get_municipios(UF)

        # Checando resultado:
        self.assertIsInstance(municipios, List)
        self.assertEqual(len(municipios), 0)

    def test_get_municipios_falha_outros(self):
        # Nocking:
        mock_response = MagicMock()
        mock_response.status_code = 500
        requests.get = MagicMock(return_value=mock_response)

        # Chama a função:
        municipios = misc.get_municipios(UF)

        # Checando resultado:
        assert municipios is None

# ==========================================================================
if __name__ == "__main__":
    unittest.main()
    
# ==========================================================================