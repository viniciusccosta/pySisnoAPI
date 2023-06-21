# =================================================================
import requests
import unittest

from unittest.mock import MagicMock

from pysisnoapi import nfe
from pysisnoapi import *
from datetime import datetime

# =================================================================
class NfeTestCase(unittest.TestCase):
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
    
    def test_listar(self):
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
        
    def test_validar(self):
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

# =================================================================
# Models:
class ObjetoEmissaoNFeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.endereco = Endereco (
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
        
        self.cliente  = Cliente(
            consumidor_final = '1',
            contribuinte     = '9',
            pessoa_fisica    = PessoaFisica(nome_completo="Vicente Marcos Samuel Nunes", cpf='44301337199'),
            endereco         = self.endereco,
        )
        
        self.impostos = nfe.ImpostosProduto(
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
        
        self.produtos = [
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
                impostos               = self.impostos,
                informacoes_adicionais = "Emitido pelo pySisnoAPI",
            ),
        ]
        
        self.pagamento = nfe.Pagamento(
            formas_pagamento = [
                nfe.FormaPagamento(
                    forma_pagamento='0',
                    meio_pagamento='01',
                    valor_pagamento='1.0'
                )
            ]
        )
        
        self.pedido   = nfe.Pedido(
            presenca='0',
            pagamento=self.pagamento,
            informacoes_complementares='Procon - 151 Endereço do Procon - Shopping Venâncio, Setor Comercial Sul Q. 6 - Brasilia, DF, CEP 70308-200nEMPRESA ENQUADRADA NO SIMPLES NACIONAL LC 123/2006n',
        )
        
        self.data = datetime(2023, 5, 19, 17, 25, 57)
    
    def test_todos_campos_obrigatorios(self):
        objeto = nfe.ObjetoEmissaoNFe (
            numero_nota_sequencial = '123456',
            serie                  = '1',
            operacao               = '1',
            natureza_operacao      = 'NATUREZA',
            modelo                 = '55',
            finalidade             = '1',
            ambiente               = '2',
            cliente                = self.cliente,
            produtos               = self.produtos,
            pedido                 = self.pedido,
            data_entrada_saida     = self.data,
            data_emissao           = self.data,
        )
        
        assert objeto.numero_nota_sequencial == "123456"
        assert objeto.serie                  == "1"
        assert objeto.operacao               == "1"
        assert objeto.natureza_operacao      == "NATUREZA"
        assert objeto.modelo                 == "55"
        assert objeto.finalidade             == "1"
        assert objeto.ambiente               == "2"
        assert objeto.cliente                == self.cliente
        assert objeto.produtos               == self.produtos
        assert objeto.pedido                 == self.pedido
        assert objeto.data_entrada_saida     == self.data
        assert objeto.data_emissao           == self.data
        
        assert objeto.numero_pedido            is None
        assert objeto.transporte               is None
        assert objeto.fatura                   is None
        assert objeto.parcelas                 is None
        assert objeto.exportacao               is None
        assert objeto.nfe_referenciada         is None
        assert objeto.retirada                 is None
        assert objeto.entrega                  is None
        assert objeto.compra                   is None
        assert objeto.indicador_intermediador  is None
        assert objeto.informacao_intermediador is None

    def test_campo_obrigatorio_numero_sequencial(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
    
    def test_campo_obrigatorio_serie(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
    
    def test_campo_obrigatorio_operacao(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_natureza_operacao(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_modelo(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_finalidade(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_ambiente(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_cliente(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_produtos(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_pedido(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_data_entrada_saida(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_emissao           = self.data,
            )
        
    def test_campo_obrigatorio_emissao(self):
        with self.assertRaises(TypeError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
            )

    def test_operacao_invalida(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '123456',
                serie                 = '1',
                operacao              = '',
                natureza_operacao     = 'NATUREZA',
                modelo                = '55',
                finalidade            = '1',
                ambiente              = '2',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )
    
    def test_modelo_invalido(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '123456',
                serie                 = '1',
                operacao              = '1',
                natureza_operacao     = 'NATUREZA',
                modelo                = '',
                finalidade            = '1',
                ambiente              = '2',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )
    
    def test_finalidade_invalida(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '123456',
                serie                 = '1',
                operacao              = '1',
                natureza_operacao     = 'NATUREZA',
                modelo                = '55',
                finalidade            = '',
                ambiente              = '2',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )
    
    def test_ambiente_invalido(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '123456',
                serie                 = '1',
                operacao              = '1',
                natureza_operacao     = 'NATUREZA',
                modelo                = '55',
                finalidade            = '1',
                ambiente              = '',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )

class PagamentoUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.forma_pgto = nfe.FormaPagamento (
            forma_pagamento = '0',
            meio_pagamento  = '01',
            valor_pagamento = '1.00',
        )
        
    def test_todos_campos_obrigatorios(self):
        pagamento = nfe.Pagamento (
            formas_pagamento = [
                self.forma_pgto,
                self.forma_pgto,
            ]
        )
        
        self.assertEqual(len(pagamento.formas_pagamento), 2)

class FormaPagamentoUnitTest(unittest.TestCase):
    def test_todos_campos_obrigatorios(self):
        forma_pgto = nfe.FormaPagamento (
            forma_pagamento = '0',
            meio_pagamento  = '01',
            valor_pagamento = '1.00',
        )
        
        self.assertEqual(forma_pgto.forma_pagamento, '0')
        self.assertEqual(forma_pgto.meio_pagamento , '01')
        self.assertEqual(forma_pgto.valor_pagamento, '1.00')
    
    def test_campo_obrigatorio_forma_pagamento(self):
        with self.assertRaises(TypeError):
            nfe.FormaPagamento(
                meio_pagamento  = '01',
                valor_pagamento = '1.00',
            )
        
    def test_campo_obrigatorio_meio_pagamento(self):
        with self.assertRaises(TypeError):
            nfe.FormaPagamento(
                forma_pagamento = '0',
                valor_pagamento = '1.00',
            )
    
    def test_campo_obrigatorio_valor_pagamento(self):
        with self.assertRaises(TypeError):
            nfe.FormaPagamento(
                forma_pagamento = '0',
                meio_pagamento  = '01',
            )
    
    def test_forma_pagamento_invalido(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento = '',
                meio_pagamento  = '01',
                valor_pagamento = '1.00',
            )
            
    def test_meio_pagamento_invalido(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento = '0',
                meio_pagamento  = '',
                valor_pagamento = '1.00',
            )
            
    def test_descricao_obrigatorio(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento = '0',
                meio_pagamento  = '99',
                valor_pagamento = '1.00'
            )
            
    def test_tamanho_descricao_menor_que_dois(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento          = '0',
                meio_pagamento           = '99',
                valor_pagamento          = '1.00',
                descricao_meio_pagamento = 'a',
            )
    
    def test_tamanho_descricao_maior_que_sessenta(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento          = '0',
                meio_pagamento           = '99',
                valor_pagamento          = '1.00',
                descricao_meio_pagamento = 'x'*70,
            )

class ProdutoUnitTest(unittest.TestCase):
    """Testes da classe produtos"""
    
    def setUp(self) -> None:
        self.impostos = nfe.ImpostosProduto(
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
    
    def test_todos_campos_obrigatorios(self):
        produto = nfe.Produto(
            item       = "1",
            cfop       = '5102',
            nome       = "UNIFORMES",
            codigo     = "123456",
            ncm        = "62069000",
            quantidade = "2.0",
            unidade    = "UNID",
            subtotal   = "2.0",
            total      = "2.0",
            impostos   = self.impostos,
        )
    
        self.assertEqual(produto.cfop      , '5102')
        self.assertEqual(produto.item      , '1')
        self.assertEqual(produto.nome      , 'UNIFORMES')
        self.assertEqual(produto.codigo    , '123456')
        self.assertEqual(produto.ncm       , '62069000')
        self.assertEqual(produto.quantidade, '2.0')
        self.assertEqual(produto.unidade   , 'UNID')
        self.assertEqual(produto.subtotal  , '2.0')
        self.assertEqual(produto.total     , '2.0')
        self.assertEqual(produto.impostos  , self.impostos)
        
    def test_campo_obrigatorio_item(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "2.0",
                total      = "2.0",
                impostos   = self.impostos,
            )
        
    def test_campo_obrigatorio_cfop(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "2.0",
                total      = "2.0",
                impostos   = self.impostos,
            )
            
    def test_campo_obrigatorio_nome(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "2.0",
                total      = "2.0",
                impostos   = self.impostos,
            )
            
    def test_campo_obrigatorio_codigo(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "2.0",
                total      = "2.0",
                impostos   = self.impostos,
            )
            
    def test_campo_obrigatorio_ncm(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "2.0",
                total      = "2.0",
                impostos   = self.impostos,
            )
            
    def test_campo_obrigatorio_quantidade(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                
                unidade    = "UNID",
                subtotal   = "2.0",
                total      = "2.0",
                impostos   = self.impostos,
            )
            
    def test_campo_obrigatorio_unidade(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                
                subtotal   = "2.0",
                total      = "2.0",
                impostos   = self.impostos,
            )
            
    def test_campo_obrigatorio_subtotal(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                
                total      = "2.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_total(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "2.0",
                
                impostos   = self.impostos,
            )
    
    def test_campo_obrigatorio_impostos(self):
        with self.assertRaises(TypeError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "2.0",
                total      = "2.0",
                
            )

# =================================================================
if __name__ == "__main__":
    unittest.main()

# =================================================================
