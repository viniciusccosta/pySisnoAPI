import unittest
import requests
from unittest.mock import MagicMock
from pysisnoapi import nfse

class TestNfse(unittest.TestCase):
    def test_buscar_notas(self):
        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        mock_response.json.return_value = {
            'status': 'Sucesso', 
            'descricao': 'Página de notas de serviço do emissor',
            "dados": {
                'total': 1, 
                'itens_por_pagina': 10, 
                'pagina_atual': 0, 
                'itens': [
                    {
                        "id": 5,
                        "empresa": {
                            "cnpj": "05397048000107",                               # https://www.4devs.com.br/gerador_de_cnpj
                            "nome_fantasia": "Empresa do Fulano",
                            "razao_social": "Fulanos Inc.",
                            "endereco": {
                                "id": 7,
                                "codigo_pais": "1058",
                                "descricao_pais": "BRASIL",
                                "uf": "DF",
                                "codigo_municipio": "5300108",
                                "descricao_municipio": "Brasilia",
                                "cep": "70343-520",                                 # https://www.4devs.com.br/gerador_de_cep
                                "bairro": "ASA SUL",
                                "logradouro": "ENDERECO DA EMPRESA",
                                "numero": "7",
                                "complemento": "COMPLEMENTO QUALQUER"
                            },
                            "telefone": "(11) 9999-9999",
                            "inscricao_estadual": "0123456789123",
                            "regime_tributario": "1",
                            "classificacao_nacional_atividades_economicas": "8512100",
                            "ambiente": "2",
                            "id_csc": "1",
                            "csc": "A55B0362-814F-4F93-B652-F3DAAF8697F1",
                            "codigo_regime_especial_tributacao": "6",
                            "site": "https://fulanos.da.silva.junior.inc",
                            "utiliza_tributos_aproximados": True,
                            "informacoes_complementares": "Informações Complementares",
                            "senha_portal_prefeitura": "542 caracteres"
                        },
                        "uuid": "57d502a5-4b55-4c67-9de4-f68735cc3fa3",
                        "modelo": "nfse",
                        "status": "reprovado",
                        "motivo": "L003 - O Código de tributação informado não pertence a este contribuinte.(Numero RPS: 37) | Consulte junto a prefeitura de seu município o código vigente.",
                        "nome_destinatario": "FULANO DA SILVA JUNIOR",
                        "uf_destinatario": "DF",
                        "cpf_cnpj_destinatario": "943.463.870-47",  # https://www.4devs.com.br/gerador_de_cpf
                        "valor_total": "1.0",
                        "data_emissao": "02/06/2023 00:45:01",
                        "ambiente": "2",
                        "json_objeto_nfse": "",
                    }
                ], 
                'informacoesAdicionais': {
                    'totalAutorizadas': 0.0, 
                    'totalCanceladas': 0.0
                },
            }
        }
        
        requests.get = MagicMock(return_value=mock_response)
        
        # Chamando a Função:
        nfses = nfse.buscar_notas()
        
        # Checando resultado:
        self.assertGreaterEqual(len(nfses), 1)

if __name__ == "__main__":
    unittest.main()