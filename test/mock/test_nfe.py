import requests_mock
import unittest
from pysisnoapi import nfe
from test.nfe_common import *

class NfeTest(unittest.TestCase):
    def test_buscar_notas_pelo_menos_uma(self):
        with requests_mock.Mocker() as mocker:
            mocker.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                json={
                    'status': 'Sucesso', 
                    'descricao': 'Página de notas de serviço do emissor',
                    "dados": {
                        'total': 1, 
                        'itens_por_pagina': 10,
                        'pagina_atual': 0, 
                        'itens': [
                            {
                                "id": 31833,
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
                                "tipo": "NF-e",
                                "serie": "1",
                                "numero_nota": "50",
                                "chave_acesso": "53230500665143000112550010000000777777777777",
                                "protocolo": "353230007777777",
                                "nome_destinatario": "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL",
                                "uf_destinatario": "DF",
                                "cpf_cnpj_destinatario": "94346387047",  # https://www.4devs.com.br/gerador_de_cpf
                                "valor_total": "4.00",
                                "status": "Autorizada",
                                "motivo": "Autorizado o uso da NF-e",
                                "data_emissao": "02/06/2023 17:25:57",
                                "data_autorizacao": "02/06/2023 21:29:40",
                                "modelo": "55",
                                "ambiente": "2",
                                "xml": "XML",
                                "json_objeto_nfe": "OBJETO JSON",
                                "tipo_emissao": "1"
                            }
                        ], 
                        'informacoesAdicionais': {
                            'totalAutorizadas': 0.0, 
                            'totalCanceladas': 0.0
                        },
                    }
                }
            )

            nfes = nfe.listar()
        check_buscar_notas_pelo_menos_uma(self, nfes)
        
if __name__ == "__main__":
    unittest.main()