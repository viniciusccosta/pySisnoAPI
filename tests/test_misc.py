# ==========================================================================
import unittest
import requests

from pysisnoapi import misc, Municipio, Cfop
from unittest.mock import MagicMock
from typing import List

# ==========================================================================
UF = 'MG'

# ==========================================================================
class TestGetMunicipios(unittest.TestCase):
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

class TestGetCfops(unittest.TestCase):
    def test_get_cfops_success(self):
        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "Sucesso",
            "descricao": "Lista de municípios",
            'dados': [
                {
                    'codigo': '5102', 
                    'descricao': 'Venda de mercadoria adquirida ou recebida de terceiros', 
                    'aplicacao': ''
                },
                {
                    'codigo': '5929', 
                    'descricao': 'Outra saída de mercadoria ou prestação de serviço não especificado', 
                    'aplicacao': ''
                },
            ]
        }
        requests.get = MagicMock(return_value=mock_response)
        
        # Chamando função:
        cfops = misc.get_cfops()
        
        # Checando resultados:
        self.assertEqual(len(cfops), 2)
        for cfop in cfops:
            self.assertIsInstance(cfop, Cfop)
        self.assertEqual(cfops[0].codigo, '5102')
        self.assertEqual(cfops[0].descricao, 'Venda de mercadoria adquirida ou recebida de terceiros')
        self.assertEqual(cfops[1].codigo, '5929')
        self.assertEqual(cfops[1].descricao, 'Outra saída de mercadoria ou prestação de serviço não especificado')

    def test_get_cfops_falha_412(self):
        # Mocking
        mock_response = MagicMock()
        mock_response.status_code = 412
        requests.get = MagicMock(return_value=mock_response)
        
        # Chamando Função:
        cfops = misc.get_cfops()
        
        # Checando resultados:
        self.assertEqual(len(cfops), 0)
        
    def test_get_cfops_falha_outros(self):
        # Nocking:
        mock_response = MagicMock()
        mock_response.status_code = 500
        requests.get = MagicMock(return_value=mock_response)

        # Chama a função:
        municipios = misc.get_cfops()

        # Checando resultado:
        assert municipios is None

# ==========================================================================
if __name__ == "__main__":
    unittest.main()
    
# ==========================================================================