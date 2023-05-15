import requests_mock
import unittest
from test.nfse_common import *
from pysisnoapi import nfse
from datetime import datetime

class NfseTest(unittest.TestCase):
    def test_buscar_notas_length(self):
        with requests_mock.Mocker() as mocker:
            mocker.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                json={
                    'status': 'Sucesso', 
                    'descricao': 'Página de notas de serviço do emissor',
                    "dados": {
                        'total': 0, 
                        'itens_por_pagina': 10, 
                        'pagina_atual': 0, 
                        'itens': [], 
                        'informacoesAdicionais': {
                            'totalAutorizadas': 0.0, 
                            'totalCanceladas': 0.0
                        },
                    }
                }
            )

            # TODO: Usar um .env apenas desenvolvimento da qual conste CNPJs para teste ?
            data = nfse.buscar_notas("00000001000191", datetime(2022, 1, 1), datetime(2023,12,31), )  # TODO: Solicitar a equipe de desenvolvimento da SISNO um banco de dados de teste.
        check_buscar_notas_atributos(self, data)

if __name__ == "__main__":
    unittest.main()