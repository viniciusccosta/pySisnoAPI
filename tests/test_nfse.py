# =================================================================
import unittest
import requests

from unittest.mock import MagicMock
from pydantic import ValidationError

from pysisnoapi import (
    nfse,

    Cliente,
    Empresa,
    Endereco,
    PessoaFisica,
    Pis,
    Cofins,
    Municipio,
    Uf,
)

# =================================================================
class NfseTestCase(unittest.TestCase):
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

        impostos = nfse.ImpostosServico(
            pis = Pis(
                situacao_tributaria = '99',
                aliquota            = '3.5',
            ),
            cofins = Cofins(
                situacao_tributaria = '99',
                aliquota            = '3.5',
            ),
            issqn = nfse.Issqn(
                aliquota                    = "3.5",
                item_lista_servicos         = "08.01",
                indicador_incentivo_fiscal  = "1",
                indicador_exigibilidade_iss = "1",
                codigo_servico              = '08.01',
                codigo_nbs                  = '1.2606.00.00',
                cnae                        = '8512100',
                codigo_tributacao_municipio = '801',
                natureza_operacao           = '1.2606.00.00',
            ),
        )

        servico = nfse.Servico(
            valor_servicos  = '1.0',
            discriminacao   = 'TESTE',
            impostos        = impostos,
        )

        self.objeto = nfse.ObjetoEmissaoNFSe(
            cliente = cliente,
            servico = servico,
        )

    async def test_buscar_notas(self):
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
        response, nfses = await nfse.buscar_notas(token_emissor='token', token_secret_emissor='token-secret',)

        # Checando resultado:
        self.assertEquals(response.status_code, 200)
        self.assertGreaterEqual(len(nfses), 1)

    async def test_buscar_notas_servidor_fora_dor_ar(self):
        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code       = 502
        mock_response.headers           = {
            'Server'        : 'nginx/1.10.3 (Ubuntu)',
            'Date'          : 'Wed, 12 Jul 2023 15:04:23 GMT',
            'Content-Type'  : 'text/html',
            'Content-Length': '182',
            'Connection'    : 'keep-alive'
        }
        mock_response._content          = b'<html>\r\n<head><title>502 Bad Gateway</title></head>\r\n<body bgcolor="white">\r\n<center><h1>502 Bad Gateway</h1></center>\r\n<hr><center>nginx/1.10.3 (Ubuntu)</center>\r\n</body>\r\n</html>\r\n'
        mock_response._content_consumed = True
        mock_response._next             = None
        mock_response.encoding          = 'ISO-8859-1'
        mock_response.history           = []
        mock_response.reason            = 'Bad Gateway'

        requests.get = MagicMock(return_value=mock_response)

        # Chamando a Função:
        response, nfses = await nfse.buscar_notas(token_emissor='token', token_secret_emissor='token-secret',)

        # Checando resultado:
        self.assertEquals(response.status_code, 502)
        self.assertEquals(response._content, b'<html>\r\n<head><title>502 Bad Gateway</title></head>\r\n<body bgcolor="white">\r\n<center><h1>502 Bad Gateway</h1></center>\r\n<hr><center>nginx/1.10.3 (Ubuntu)</center>\r\n</body>\r\n</html>\r\n')
        self.assertEquals(response._content_consumed, True)
        self.assertEquals(response._next, None)
        self.assertEquals(response.encoding, 'ISO-8859-1')
        self.assertEquals(len(response.history), 0)
        self.assertEquals(response.reason, 'Bad Gateway')
        self.assertEquals(nfses, None)

    async def test_emitir_status_processando(self):
        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_response.json.return_value = {
            "id": 22,
            "empresa": {    # https://www.4devs.com.br/gerador_de_empresas
                "cnpj": "47520244000169",
                "nome_fantasia": "Amanda e Ricardo Ferragens ME",
                "razao_social": "Amanda e Ricardo Ferragens ME",
                "endereco": {
                    "id": 76,
                    "codigo_pais": "1058",
                    "descricao_pais": "BRASIL",
                    "uf": "DF",
                    "codigo_municipio": "5300108",
                    "descricao_municipio": "Brasilia",
                    "cep": "71070-037",
                    "bairro": "TAGUATINGA",
                    "logradouro": "Quadra QE 44 Conjunto C",
                    "numero": "503",
                    "complemento": "COMPLEMENTO"
                },
                "telefone": "(61) 2622-0226",
                "inscricao_estadual": "0727000600110",
                "regime_tributario": "1",
                "classificacao_nacional_atividades_economicas": "8512100",
                "ambiente": "2",
                "id_csc": "1",
                "csc": "A55B7362-874F-4F97-B752-F7DAAF8697F1",
                "codigo_regime_especial_tributacao": "6",
                "site": "almoxarifado@amandaericardoferragensme.com.br",
                "utiliza_tributos_aproximados": True,
                "informacoes_complementares": "Procon - 151 Endereço do Procon - Shopping Venâncio, Setor Comercial Sul Q. 6 - Brasilia, DF, CEP 70308-200",
                "senha_portal_prefeitura": "eyJlbmMiOiJBMTI7R7NNIiwiYWxnIjoiUlNBLU7BRVAtMjU7In0.CUFL72ld7_tcjqcE-djx0JTxWG7BnPhVkIF7LR7fLIzKyIJ0XreUq7mG_Ed9kR7AyorVbNMH6qaL7ACHELdcUhVoKsEQfCtQxM7kqhs6hXOm-ylmHr6I7pg1Z3SMNxTaQDzXzVUO3HiRRsu9JrlRyE6V9TcdX_U2ZnsAedIl86D3UkZF0In2-OKwyHHxW0Hi58ar0jzqRvN6he__kLhnA5Fxf-1k1qnlg5wq5Xrpdjz16JhVzjTTjDv8DvqCe27pxhbZ7HJHLkoySoYCHwFmq71N-tW2Sx7XOW8YecAEgc7q8nemWSkltjkK9N6GuCLX_zmA-7ISmPWx0hcBrCvZQg.mcbaIXUxn7uIqYgb.dSTq5dovLYxJ73MIzik7_OOuTpsZjXat7UjNvZSLyuqoKN-_wl69s5w0eRu4Y668HuF745wgJgTP6lPDhOUrYSCJdtWLMx-Gvudw5_l0a4o.Xohm6iR1rw1NHzGsAED9Jw"
            },
            "uuid": "57d502a5-8f28-4177-acfd-a8e04929b682",
            "modelo": "nfse",
            "status": "processando",
            "motivo": "Lote enviado para processamento",
            "nome_destinatario": "Tânia Aurora Mariah Moura", # https://www.4devs.com.br/gerador_de_pessoas
            "uf_destinatario": "DF",
            "cpf_cnpj_destinatario": "016.968.211-00",
            "valor_total": "5.00",
            "data_emissao": "Jun 21, 2023 6:08:18 PM",
            "ambiente": "2",
            "json_objeto_nfse": ""
        }

        requests.post = MagicMock(return_value=mock_response)

        # Chamando a Função:
        resultado = await nfse.emitir(token_emissor='token', token_secret_emissor='token-secret', objetoNfse=self.objeto, token_empresa="token_empresa", token_secret_empresa="token_secret_empresa")

        self.assertIn('id', resultado)
        self.assertIn('empresa', resultado)
        self.assertIn('uuid', resultado)
        self.assertIn('modelo', resultado)
        self.assertIn('status', resultado)
        self.assertIn('motivo', resultado)
        self.assertIn('nome_destinatario', resultado)
        self.assertIn('uf_destinatario', resultado)
        self.assertIn('cpf_cnpj_destinatario', resultado)
        self.assertIn('valor_total', resultado)
        self.assertIn('data_emissao', resultado)
        self.assertIn('ambiente', resultado)
        self.assertIn('json_objeto_nfse', resultado)

        self.assertEqual(resultado['status'], 'processando')

# =================================================================
class ConstrucaoCivilTestCase(unittest.TestCase):
    def test_valid_construcao_civil(self):
        # Test a valid instance of ConstrucaoCivil
        construcao_civil = nfse.ConstrucaoCivil(
            codigo_obra="12345",
            art="56789"
        )
        self.assertEqual(construcao_civil.codigo_obra, "12345")
        self.assertEqual(construcao_civil.art, "56789")

    def test_optional_fields(self):
        # Test when both fields are None (optional)
        construcao_civil = nfse.ConstrucaoCivil()
        self.assertIsNone(construcao_civil.codigo_obra)
        self.assertIsNone(construcao_civil.art)

    def test_invalid_field_type(self):
        # Test when a field has an invalid type (should raise a ValidationError)
        with self.assertRaises(ValidationError):
            nfse.ConstrucaoCivil(codigo_obra=12345, art="56789")

class ImpostosServicoTestCase(unittest.TestCase):
    def test_valid_impostos_servico(self):
        # Test a valid instance of ImpostosServico
        issqn = nfse.Issqn(
            indicador_exigibilidade_iss="1",
            indicador_incentivo_fiscal="1",
            item_lista_servicos="08.02",
            aliquota="3.5",
            codigo_servico="802",
            codigo_nbs="1.2606.00.00",
            cnae="8512100",
            codigo_tributacao_municipio="801",
            natureza_operacao="1.2606.00.00"
        )
        pis = Pis(
            situacao_tributaria = '99',             # 99 - Outras Operações
            aliquota            = '0.0000',
            aliquota_retencao   = '0.0000',
        )
        cofins = Cofins(
            situacao_tributaria = '99',             # 99 - Outras Operações
            aliquota            = '0.0000',
            aliquota_retencao   = '0.0000',
        )
        impostos_servico = nfse.ImpostosServico(pis=pis, cofins=cofins, issqn=issqn)
        self.assertEqual(impostos_servico.issqn, issqn)

    def test_missing_required_field(self):
        # Test when a required field is missing in Issqn (should raise a ValidationError)
        with self.assertRaises(ValidationError):
            nfse.Issqn(
                indicador_exigibilidade_iss="1",
                indicador_incentivo_fiscal="1",
                item_lista_servicos="08.02",
                aliquota="3.5",
                codigo_servico="802",
                # Missing required fields: codigo_nbs, cnae, codigo_tributacao_municipio, natureza_operacao
            )

class IssqnTestCase(unittest.TestCase):
    def test_valid_issqn(self):
        # Test a valid instance of Issqn
        issqn = nfse.Issqn(
            indicador_exigibilidade_iss="1",
            indicador_incentivo_fiscal="1",
            item_lista_servicos="08.02",
            aliquota="3.5",
            codigo_servico="802",
            codigo_nbs="1.2606.00.00",
            cnae="8512100",
            codigo_tributacao_municipio="801",
            natureza_operacao="1.2606.00.00"
        )
        self.assertEqual(issqn.indicador_exigibilidade_iss, "1")
        self.assertEqual(issqn.indicador_incentivo_fiscal, "1")
        self.assertEqual(issqn.item_lista_servicos, "08.02")
        self.assertEqual(issqn.aliquota, "3.5")
        self.assertEqual(issqn.codigo_servico, "802")
        self.assertEqual(issqn.codigo_nbs, "1.2606.00.00")
        self.assertEqual(issqn.cnae, "8512100")
        self.assertEqual(issqn.codigo_tributacao_municipio, "801")
        self.assertEqual(issqn.natureza_operacao, "1.2606.00.00")

    def test_optional_fields(self):
        # Test an instance with optional fields set to None
        issqn = nfse.Issqn(
            indicador_exigibilidade_iss="1",
            indicador_incentivo_fiscal="1",
            item_lista_servicos="08.02",
            aliquota="3.5",
            codigo_servico="802",
            codigo_nbs="1.2606.00.00",
            cnae="8512100",
            codigo_tributacao_municipio="801",
            natureza_operacao="1.2606.00.00",
            numero_processo=None,
            aliquota_retencao=None,
            aliquota_irrf=None,
            aliquota_csll=None,
            aliquota_previdencia_social=None
        )
        self.assertIsNone(issqn.numero_processo)
        self.assertIsNone(issqn.aliquota_retencao)
        self.assertIsNone(issqn.aliquota_irrf)
        self.assertIsNone(issqn.aliquota_csll)
        self.assertIsNone(issqn.aliquota_previdencia_social)

    def test_missing_required_field(self):
        # Test when a required field is missing (should raise a ValidationError)
        with self.assertRaises(ValidationError):
            nfse.Issqn(
                indicador_exigibilidade_iss="1",
                indicador_incentivo_fiscal="1",
                item_lista_servicos="08.02",
                aliquota="3.5",
                codigo_servico="802",
                codigo_nbs="1.2606.00.00",
                cnae="8512100",
                # Missing required field: codigo_tributacao_municipio
                natureza_operacao="1.2606.00.00"
            )

class NotaFiscalServicoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.empresa   = Empresa()      # TODO: Até 29/10/2023 todos os campos são opcionais...
        self.municipio = Municipio()    # TODO: Até 29/10/2023 todos os campos são opcionais...
        self.uf        = Uf()           # TODO: Até 29/10/2023 todos os campos são opcionais...

    def test_optional_fields(self):
        nota_fiscal = nfse.NotaFiscalServico(
            id                    = 1,
            empresa               = self.empresa,
            uuid                  = '123456',
            modelo                = 'Model A',
            status                = 'Approved',
            motivo                = 'No reason',
            numero_nota           = '12345',
            codigo_verificacao    = 'ABCDEF',
            protocolo             = 'Protocol 123',
            nome_destinatario     = 'John Doe',
            uf_destinatario       = 'TX',
            cpf_cnpj_destinatario = '1234567890',
            valor_total           = '100.00',
            data_emissao          = '2023-10-29',
            data_competencia      = '2023-10-30',
            uf_prestacao          = self.uf,
            municipio_prestacao   = self.municipio,
            ambiente              = 'Production',
            json_objeto_nfse      = '{"key": "value"}',
            xml                   = '<xml>...</xml>',
            numer_nota            = '54321'
        )

        self.assertEqual(nota_fiscal.id, 1)
        self.assertEqual(nota_fiscal.empresa, self.empresa)
        self.assertEqual(nota_fiscal.uuid, '123456')
        self.assertEqual(nota_fiscal.modelo, 'Model A')
        self.assertEqual(nota_fiscal.status, 'Approved')
        self.assertEqual(nota_fiscal.motivo, 'No reason')
        self.assertEqual(nota_fiscal.numero_nota, '12345')
        self.assertEqual(nota_fiscal.codigo_verificacao, 'ABCDEF')
        self.assertEqual(nota_fiscal.protocolo, 'Protocol 123')
        self.assertEqual(nota_fiscal.nome_destinatario, 'John Doe')
        self.assertEqual(nota_fiscal.uf_destinatario, 'TX')
        self.assertEqual(nota_fiscal.cpf_cnpj_destinatario, '1234567890')
        self.assertEqual(nota_fiscal.valor_total, '100.00')
        self.assertEqual(nota_fiscal.data_emissao, '2023-10-29')
        self.assertEqual(nota_fiscal.data_competencia, '2023-10-30')
        self.assertEqual(nota_fiscal.uf_prestacao, self.uf)
        self.assertEqual(nota_fiscal.municipio_prestacao, self.municipio)
        self.assertEqual(nota_fiscal.ambiente, 'Production')
        self.assertEqual(nota_fiscal.json_objeto_nfse, '{"key": "value"}')
        self.assertEqual(nota_fiscal.xml, '<xml>...</xml>')
        self.assertEqual(nota_fiscal.numer_nota, '54321')
    
class ObjetoEmissaoNFSeTestCase(unittest.TestCase):
    ...

class PaginaNotasServicoTestCase():
    ...

class ServicoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.impostos = nfse.ImpostosServico(
            pis    = Pis(
                situacao_tributaria = '99',
                aliquota            = '3.5',
            ),
            cofins = Cofins(
                situacao_tributaria = '99',
                aliquota            = '3.5',
            ),
            issqn  = nfse.Issqn(
                aliquota                    = "3.5",
                item_lista_servicos         = "08.02",
                indicador_incentivo_fiscal  = "1",
                indicador_exigibilidade_iss = "1",
                codigo_servico              = '802',
                codigo_nbs                  = '1.2606.00.00',
                cnae                        = '8512100',
                codigo_tributacao_municipio = '801',
                natureza_operacao           = '1.2606.00.00',
            ),
        )

    def test_todos_campos_obrigatorios(self):
        servico = nfse.Servico(
            valor_servicos = "1.00",
            discriminacao  = "TESTE",
            impostos       = self.impostos
        )

        self.assertEqual(servico.valor_servicos, "1.00")
        self.assertEqual(servico.discriminacao, "TESTE")
        self.assertEqual(servico.impostos, self.impostos)

    def test_campo_obrigatorio_valor_servicos(self):
        with self.assertRaises(ValidationError):
            nfse.Servico(
                discriminacao  = "TESTE",
                impostos       = self.impostos
            )

    def test_campo_obrigatorio_discriminacao(self):
        with self.assertRaises(ValidationError):
            nfse.Servico(
                valor_servicos = "1.00",

                impostos       = self.impostos
            )

    def test_campo_obrigatorio_impostos(self):
        with self.assertRaises(ValidationError):
            nfse.Servico(
                valor_servicos = "1.00",
                discriminacao  = "TESTE",

            )

# =================================================================
if __name__ == "__main__":
    unittest.main()

# =================================================================