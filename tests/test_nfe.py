from unittest.mock import MagicMock
import requests
import unittest
from pysisnoapi import nfe
from pysisnoapi import *
from datetime import datetime

class TestNfe(unittest.TestCase):
    def setUp(self) -> None:
        endereco = Endereco (
            codigo_pais         = '1058',
            descricao_pais      = 'Brasil',
            uf                  = 'DF',
            codigo_municipio    = '5300108',
            descricao_municipio = 'Brasilia',
            cep                 = '70634300',
            bairro              = 'Zona Industrial',
            logradouro          = 'Quadra SOFN Quadra 3',
            numero              = '484',
            complemento         = 'Gerado por 4devs',
        )
        
        cliente  = Cliente(
            consumidor_final = '1',
            contribuinte     = '9',
            pessoa_fisica    = PessoaFisica(nome_completo="Vicente Marcos Samuel Nunes", cpf='44301337199'),
            endereco         = endereco,
        )
        
        impostos = nfe.ImpostosProduto(
            Pis (
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            Cofins(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            Icms (
                situacao_tributaria='102',
                aliquota_icms='0.0000',
                aliquota_icms_st='0.0000',
            ),
            Ipi(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
        )
        
        produtos = [
            nfe.Produto(
                cfop                   = '5102',
                item                   = "1",
                nome                   = "UNIFORMES",
                codigo                 = "123456",
                ncm                    = "62069000",
                quantidade             = "2.0",
                unidade                = "UNID",
                subtotal               = "2.0",
                total                  = "2.0",
                impostos               = impostos,
                informacoes_adicionais = "Emitido pelo pySisnoAPI",
            ),
        ]
        
        pagamento = nfe.Pagamento(
            formas_pagamento = [
                nfe.FormaPagamento(
                    forma_pagamento='0',
                    meio_pagamento='01',
                    valor_pagamento='1.0'
                )
            ]
        )
        
        pedido   = nfe.Pedido(
            presenca='0',
            pagamento=pagamento,
            # informacoes_complementares='Procon - 151 Endereço do Procon - Shopping Venâncio, Setor Comercial Sul Q. 6 - Brasilia, DF, CEP 70308-200nEMPRESA ENQUADRADA NO SIMPLES NACIONAL LC 123/2006n',
        )
        
        data = datetime(2023, 5, 19, 17, 25, 57).strftime("%d/%m/%Y %H:%M:%S")
        
        self.objeto = nfe.ObjetoEmissaoNFe(
            numero_nota_sequencial= '123456',
            serie                 = '1',
            operacao              = '1',
            natureza_operacao     = 'NATUREZA',
            modelo                = '55',
            finalidade            = '1',
            ambiente              = '2',
            cliente               = cliente,
            produtos              = produtos,
            pedido                = pedido,
            data_entrada_saida    = data,
            data_emissao          = data,
        )
    
    def test_listar_pelo_menos_uma_nfe(self):
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

        requests.get = MagicMock(return_value=mock_response)
        
        # Chamando a Função:
        nfes = nfe.listar()
        
        # Checando resultado:
        self.assertGreaterEqual(len(nfes), 1)
        
    def test_validar_nfe_normal(self):
        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'Sucesso', 
            'message': 'Nota validada pela API',
        }
        
        requests.get = MagicMock(return_value=mock_response)
        
        # Chamando a Função:
        result = nfe.validar(self.objeto, tipo_emissao='1')
        
        # Checando resultado:
        self.assertEqual('Sucesso', result['status'])
        self.assertEqual('Nota validada pela API', result['message'])
        
class ObjetoEmissaoNFeTestCase(unittest.TestCase):
    def test_novo_objeto_apenas_campos_obrigatorios(self):
        endereco = Endereco (
            codigo_pais         = '1058',
            descricao_pais      = 'Brasil',
            uf                  = 'DF',
            codigo_municipio    = '5300108',
            descricao_municipio = 'Brasilia',
            cep                 = '70634300',
            bairro              = 'Zona Industrial',
            logradouro          = 'Quadra SOFN Quadra 3',
            numero              = '484',
            complemento         = 'Gerado por 4devs',
        )
        
        cliente  = Cliente(
            consumidor_final = '1',
            contribuinte     = '9',
            pessoa_fisica    = PessoaFisica(nome_completo="Vicente Marcos Samuel Nunes", cpf='44301337199'),
            endereco         = endereco,
        )
        
        impostos = nfe.ImpostosProduto(
            Pis (
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            Cofins(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            Icms (
                situacao_tributaria='102',
                aliquota_icms='0.0000',
                aliquota_icms_st='0.0000',
            ),
            Ipi(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
        )
        
        produtos = [
            nfe.Produto(
                cfop                   = '5102',
                item                   = "1",
                nome                   = "UNIFORMES",
                codigo                 = "123456",
                ncm                    = "62069000",
                quantidade             = "2.0",
                unidade                = "UNID",
                subtotal               = "2.0",
                total                  = "2.0",
                impostos               = impostos,
                informacoes_adicionais = "Emitido pelo pySisnoAPI",
            ),
        ]
        
        pagamento = nfe.Pagamento(
            formas_pagamento = [
                nfe.FormaPagamento(
                    forma_pagamento='0',
                    meio_pagamento='01',
                    valor_pagamento='1.0'
                )
            ]
        )
        
        pedido   = nfe.Pedido(
            presenca='0',
            pagamento=pagamento,
            informacoes_complementares='Procon - 151 Endereço do Procon - Shopping Venâncio, Setor Comercial Sul Q. 6 - Brasilia, DF, CEP 70308-200nEMPRESA ENQUADRADA NO SIMPLES NACIONAL LC 123/2006n',
        )
        
        data = datetime(2023, 5, 19, 17, 25, 57)
        
        objeto = nfe.ObjetoEmissaoNFe(
            numero_nota_sequencial= '123456',
            serie                 = '1',
            operacao              = '1',
            natureza_operacao     = 'NATUREZA',
            modelo                = '55',
            finalidade            = '1',
            ambiente              = '2',
            cliente               = cliente,
            produtos              = produtos,
            pedido                = pedido,
            data_entrada_saida    = data,
            data_emissao          = data,
        )
        
        assert objeto.numero_nota_sequencial == "123456"
        assert objeto.serie == "1"
        assert objeto.operacao == "1"
        assert objeto.natureza_operacao == "NATUREZA"
        assert objeto.modelo == "55"
        assert objeto.finalidade == "1"
        assert objeto.ambiente == "2"
        assert objeto.cliente == cliente
        assert objeto.produtos == produtos
        assert objeto.pedido == pedido
        assert objeto.data_entrada_saida == data
        assert objeto.data_emissao == data
        assert objeto.numero_pedido is None
        assert objeto.transporte is None
        assert objeto.fatura is None
        assert objeto.parcelas is None
        assert objeto.exportacao is None
        assert objeto.nfe_referenciada is None
        assert objeto.retirada is None
        assert objeto.entrega is None
        assert objeto.compra is None
        assert objeto.indicador_intermediador is None
        assert objeto.informacao_intermediador is None
        
if __name__ == "__main__":
    unittest.main()