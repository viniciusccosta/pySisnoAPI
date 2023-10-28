import unittest
from pysisnoapi import *

class CfopTestCase(unittest.TestCase):
    def test_criar_cfop_com_dados_obrigatorios(self):
        cfop = Cfop(codigo='5102', descricao='Venda de produção do estabelecimento para entrega futura')
        self.assertEqual(cfop.codigo, '5102')
        self.assertEqual(cfop.descricao, 'Venda de produção do estabelecimento para entrega futura')
        self.assertIsNone(cfop.aplicacao)

    def test_criar_cfop_sem_descricao(self):
        cfop = Cfop(codigo='5102')
        self.assertEqual(cfop.codigo, '5102')
        self.assertIsNone(cfop.descricao)
        self.assertIsNone(cfop.aplicacao)

    def test_criar_cfop_com_codigo_descricao_e_aplicacao(self):
        cfop = Cfop(codigo='5102', descricao='Venda de produção do estabelecimento para entrega futura', aplicacao='Teste')
        self.assertEqual(cfop.codigo, '5102')
        self.assertEqual(cfop.descricao, 'Venda de produção do estabelecimento para entrega futura')
        self.assertEqual(cfop.aplicacao, 'Teste')

class ClientTestCase(unittest.TestCase):
    def test_novo_cliente_somente_dados_obrigatorios_pessoa_fisica(self):
        # https://www.4devs.com.br/gerador_de_pessoas

        # Mocking:
        pessoa_fisica = PessoaFisica(
            nome_completo   = "Vanessa Sophia Ayla Moura",
            cpf             = "557.986.321-72",
        )

        endereco = Endereco (
            codigo_pais         = "1058",
            descricao_pais      = "BRASIL",
            uf                  = "DF",
            codigo_municipio    = "5300108",
            descricao_municipio = "Brasilia",
            cep                 = "70343-520",
            bairro              = "ASA SUL",
            logradouro          = "ENDERECO DA EMPRESA",
            numero              = "7",
            complemento         = "COMPLEMENTO QUALQUER",
        )

        cliente = Cliente(
            consumidor_final = '1',
            contribuinte     = '9',
            pessoa_fisica    = pessoa_fisica,
            endereco         = endereco,
        )

        # Assert:
        self.assertEqual(cliente.pessoa_fisica, pessoa_fisica)
        self.assertEqual(cliente.consumidor_final, '1')
        self.assertEqual(cliente.contribuinte, '9')
        self.assertEqual(cliente.endereco, endereco)

        self.assertIsNone(cliente.pessoa_juridica)
        self.assertIsNone(cliente.ie)
        self.assertIsNone(cliente.telefone)
        self.assertIsNone(cliente.email)
        self.assertIsNone(cliente.faz_retencao)

    def test_novo_cliente_somente_dados_obrigatorios_pessoa_juridica(self):
        # https://www.4devs.com.br/gerador_de_pessoas
        # https://www.4devs.com.br/gerador_de_empresas

        # Mocking:
        pessoa_juridica = PessoaJuridica (
            razao_social = "Francisca e Giovanni Comercio de Bebidas ME",
            cnpj         = "85.241.341/0001-01",
        )

        endereco = Endereco (
            codigo_pais         = "1058",
            descricao_pais      = "BRASIL",
            uf                  = "DF",
            codigo_municipio    = "5300108",
            descricao_municipio = "Brasilia",
            cep                 = "70343-520",
            bairro              = "ASA SUL",
            logradouro          = "ENDERECO DA EMPRESA",
            numero              = "7",
            complemento         = "COMPLEMENTO QUALQUER",
        )

        cliente = Cliente(
            consumidor_final = '1',
            contribuinte     = '9',
            pessoa_juridica  = pessoa_juridica,
            endereco         = endereco,
        )

        # Assert:
        self.assertEqual(cliente.pessoa_juridica, pessoa_juridica)
        self.assertEqual(cliente.consumidor_final, '1')
        self.assertEqual(cliente.contribuinte, '9')
        self.assertEqual(cliente.endereco, endereco)
        self.assertIsNone(cliente.pessoa_fisica)
        self.assertIsNone(cliente.ie)
        self.assertIsNone(cliente.telefone)
        self.assertIsNone(cliente.email)
        self.assertIsNone(cliente.faz_retencao)

    def test_novo_cliente_somente_dados_obrigatorios_pessoa_fisica_e_pessoa_juridica(self):
        # https://www.4devs.com.br/gerador_de_pessoas
        # https://www.4devs.com.br/gerador_de_empresas

        # Mocking:
        pessoa_fisica = PessoaFisica (
            nome_completo   = "Vanessa Sophia Ayla Moura",
            cpf             = "557.986.321-72",
        )

        pessoa_juridica = PessoaJuridica (
            razao_social = "Francisca e Giovanni Comercio de Bebidas ME",
            cnpj         = "85.241.341/0001-01",
        )

        endereco = Endereco (
            codigo_pais         = "1058",
            descricao_pais      = "BRASIL",
            uf                  = "DF",
            codigo_municipio    = "5300108",
            descricao_municipio = "Brasilia",
            cep                 = "70343-520",
            bairro              = "ASA SUL",
            logradouro          = "ENDERECO DA EMPRESA",
            numero              = "7",
            complemento         = "COMPLEMENTO QUALQUER",
        )

        with self.assertRaises(ValueError):
            Cliente (
                consumidor_final = '1',
                contribuinte     = '9',
                pessoa_fisica    = pessoa_fisica,
                pessoa_juridica  = pessoa_juridica,
                endereco         = endereco,
            )

    def test_novo_cliente_consumidor_final_invalido(self):
        # https://www.4devs.com.br/gerador_de_pessoas

        # Mocking:
        pessoa_fisica = PessoaFisica(
            nome_completo   = "Vanessa Sophia Ayla Moura",
            cpf             = "557.986.321-72",
        )

        endereco = Endereco (
            codigo_pais         = "1058",
            descricao_pais      = "BRASIL",
            uf                  = "DF",
            codigo_municipio    = "5300108",
            descricao_municipio = "Brasilia",
            cep                 = "70343-520",
            bairro              = "ASA SUL",
            logradouro          = "ENDERECO DA EMPRESA",
            numero              = "7",
            complemento         = "COMPLEMENTO QUALQUER",
        )

        # Assert:
        with self.assertRaises(ValueError):
            Cliente (
                consumidor_final = '',
                contribuinte     = '9',
                pessoa_fisica    = pessoa_fisica,
                endereco         = endereco,
            )

    def test_novo_cliente_contribuinte_invalido(self):
        # https://www.4devs.com.br/gerador_de_pessoas

        # Mocking:
        pessoa_fisica = PessoaFisica(
            nome_completo   = "Vanessa Sophia Ayla Moura",
            cpf             = "557.986.321-72",
        )

        endereco = Endereco (
            codigo_pais         = "1058",
            descricao_pais      = "BRASIL",
            uf                  = "DF",
            codigo_municipio    = "5300108",
            descricao_municipio = "Brasilia",
            cep                 = "70343-520",
            bairro              = "ASA SUL",
            logradouro          = "ENDERECO DA EMPRESA",
            numero              = "7",
            complemento         = "COMPLEMENTO QUALQUER",
        )

        # Assert:
        with self.assertRaises(ValueError):
            Cliente (
                consumidor_final = '1',
                contribuinte     = '',
                pessoa_fisica    = pessoa_fisica,
                endereco         = endereco,
            )

class CofinsTestCase(unittest.TestCase):
    def test_criar_cofins_com_dados_obrigatorios(self):
        cofins = Cofins(situacao_tributaria='01')
        self.assertEqual(cofins.situacao_tributaria, '01')
        self.assertIsNone(cofins.aliquota)
        self.assertIsNone(cofins.aliquota_st)
        self.assertIsNone(cofins.aliquota_retencao)

    def test_criar_cofins_com_aliquota(self):
        cofins = Cofins(situacao_tributaria='01', aliquota='0.65')
        self.assertEqual(cofins.situacao_tributaria, '01')
        self.assertEqual(cofins.aliquota, '0.65')
        self.assertIsNone(cofins.aliquota_st)
        self.assertIsNone(cofins.aliquota_retencao)

    def test_criar_cofins_com_aliquota_st(self):
        cofins = Cofins(situacao_tributaria='05', aliquota_st='0.75')
        self.assertEqual(cofins.situacao_tributaria, '05')
        self.assertIsNone(cofins.aliquota)
        self.assertEqual(cofins.aliquota_st, '0.75')
        self.assertIsNone(cofins.aliquota_retencao)

    def test_criar_cofins_com_aliquota_retencao(self):
        cofins = Cofins(situacao_tributaria='09', aliquota_retencao='0.50')
        self.assertEqual(cofins.situacao_tributaria, '09')
        self.assertIsNone(cofins.aliquota)
        self.assertIsNone(cofins.aliquota_st)
        self.assertEqual(cofins.aliquota_retencao, '0.50')

    def test_criar_cofins_com_situacao_tributaria_invalida(self):
        with self.assertRaises(ValueError):
            Cofins(situacao_tributaria='123')

class DeclaracaoImportacaoAdicaoTestCase(unittest.TestCase):
    def test_criar_adicao_com_dados_obrigatorios(self):
        adicao = DeclaracaoImportacaoAdicao()
        self.assertIsNone(adicao.numero_sequencial)
        self.assertIsNone(adicao.numero)
        self.assertIsNone(adicao.cod_fabricante)
        self.assertIsNone(adicao.desconto)
        self.assertIsNone(adicao.drawback)

    def test_criar_adicao_com_numero_sequencial(self):
        adicao = DeclaracaoImportacaoAdicao(numero_sequencial='1')
        self.assertEqual(adicao.numero_sequencial, '1')
        self.assertIsNone(adicao.numero)
        self.assertIsNone(adicao.cod_fabricante)
        self.assertIsNone(adicao.desconto)
        self.assertIsNone(adicao.drawback)

    def test_criar_adicao_com_numero_e_cod_fabricante(self):
        adicao = DeclaracaoImportacaoAdicao(numero='A123', cod_fabricante='F456')
        self.assertIsNone(adicao.numero_sequencial)
        self.assertEqual(adicao.numero, 'A123')
        self.assertEqual(adicao.cod_fabricante, 'F456')
        self.assertIsNone(adicao.desconto)
        self.assertIsNone(adicao.drawback)

    def test_criar_adicao_com_desconto_e_drawback(self):
        adicao = DeclaracaoImportacaoAdicao(desconto='0.05', drawback='Sim')
        self.assertIsNone(adicao.numero_sequencial)
        self.assertIsNone(adicao.numero)
        self.assertIsNone(adicao.cod_fabricante)
        self.assertEqual(adicao.desconto, '0.05')
        self.assertEqual(adicao.drawback, 'Sim')

class EmpresaTestCase(unittest.TestCase):
    def test_criar_empresa_com_dados_obrigatorios(self):
        empresa = Empresa()

        self.assertIsNone(empresa.id)
        self.assertIsNone(empresa.token)
        self.assertIsNone(empresa.token_secret)
        self.assertIsNone(empresa.cnpj)
        self.assertIsNone(empresa.nome_fantasia)
        self.assertIsNone(empresa.razao_social)
        self.assertIsNone(empresa.endereco)
        self.assertIsNone(empresa.telefone)
        self.assertIsNone(empresa.inscricao_estadual)
        self.assertIsNone(empresa.inscricao_municipal)
        self.assertIsNone(empresa.inscricao_estadual_substituicao_tributaria)
        self.assertIsNone(empresa.regime_tributario)
        self.assertIsNone(empresa.classificacao_nacional_atividades_economicas)
        self.assertIsNone(empresa.ambiente)
        self.assertIsNone(empresa.id_csc)
        self.assertIsNone(empresa.csc)
        self.assertIsNone(empresa.codigo_regime_especial_tributacao)
        self.assertIsNone(empresa.porcentagem_icms_aproveitado)
        self.assertIsNone(empresa.site)
        self.assertIsNone(empresa.email)
        self.assertIsNone(empresa.utiliza_tributos_aproximados)
        self.assertIsNone(empresa.informacoes_complementares)
        self.assertIsNone(empresa.senha_portal_prefeitura)
        self.assertIsNone(empresa.serie_rps)
        self.assertIsNone(empresa.proximo_numero_rps)
        self.assertIsNone(empresa.proximo_numero_rps_homologacao)
        self.assertIsNone(empresa.numero_lote_rps)

    def test_criar_empresa_com_cnpj(self):
        empresa = Empresa(cnpj='12345678901234')
        self.assertEqual(empresa.cnpj, '12345678901234')

    def test_criar_empresa_com_nome_fantasia(self):
        empresa = Empresa(nome_fantasia='Minha Empresa')
        self.assertEqual(empresa.nome_fantasia, 'Minha Empresa')

    def test_criar_empresa_com_razao_social(self):
        empresa = Empresa(razao_social='Razão Social Ltda.')
        self.assertEqual(empresa.razao_social, 'Razão Social Ltda.')

    def test_criar_empresa_com_endereco(self):
        endereco = Endereco(codigo_pais='1058', descricao_pais='Brasil', bairro='Bairro', logradouro='Logradouro', numero='N')
        empresa = Empresa(endereco=endereco)
        self.assertEqual(empresa.endereco, endereco)

    def test_criar_empresa_com_telefone(self):
        empresa = Empresa(telefone='(11) 1234-5678')
        self.assertEqual(empresa.telefone, '(11) 1234-5678')

    def test_criar_empresa_com_email(self):
        empresa = Empresa(email='contato@empresa.com')
        self.assertEqual(empresa.email, 'contato@empresa.com')

class EnderecoTestCase(unittest.TestCase):
    def test_criar_endereco_com_dados_obrigatorios(self):
        endereco = Endereco(
            codigo_pais='1058',
            descricao_pais='BRASIL',
            bairro='Centro',
            logradouro='Rua Principal',
            numero='123'
        )

        self.assertEqual(endereco.codigo_pais, '1058')
        self.assertEqual(endereco.descricao_pais, 'BRASIL')
        self.assertEqual(endereco.bairro, 'Centro')
        self.assertEqual(endereco.logradouro, 'Rua Principal')
        self.assertEqual(endereco.numero, '123')
        self.assertIsNone(endereco.id)
        self.assertIsNone(endereco.uf)
        self.assertIsNone(endereco.codigo_municipio)
        self.assertIsNone(endereco.descricao_municipio)
        self.assertIsNone(endereco.cep)
        self.assertIsNone(endereco.complemento)

    def test_criar_endereco_com_uf(self):
        endereco = Endereco(
            codigo_pais='1058',
            descricao_pais='BRASIL',
            bairro='Centro',
            logradouro='Rua Principal',
            numero='123',
            uf='SP'
        )

        self.assertEqual(endereco.uf, 'SP')

    def test_criar_endereco_com_codigo_municipio(self):
        endereco = Endereco(
            codigo_pais='1058',
            descricao_pais='BRASIL',
            bairro='Centro',
            logradouro='Rua Principal',
            numero='123',
            codigo_municipio='5300108'
        )

        self.assertEqual(endereco.codigo_municipio, '5300108')

    def test_criar_endereco_com_descricao_municipio(self):
        endereco = Endereco(
            codigo_pais='1058',
            descricao_pais='BRASIL',
            bairro='Centro',
            logradouro='Rua Principal',
            numero='123',
            descricao_municipio='Brasília'
        )

        self.assertEqual(endereco.descricao_municipio, 'Brasília')

    def test_criar_endereco_com_cep(self):
        endereco = Endereco(
            codigo_pais='1058',
            descricao_pais='BRASIL',
            bairro='Centro',
            logradouro='Rua Principal',
            numero='123',
            cep='70000-000'
        )

        self.assertEqual(endereco.cep, '70000-000')

    def test_criar_endereco_com_complemento(self):
        endereco = Endereco(
            codigo_pais='1058',
            descricao_pais='BRASIL',
            bairro='Centro',
            logradouro='Rua Principal',
            numero='123',
            complemento='Apto 101'
        )

        self.assertEqual(endereco.complemento, 'Apto 101')

class PessoaFisicaTestCase(unittest.TestCase):
    def test_nova_pessoa_fisica_campos_obrigatorios_cpf(self):
        pessoa_fisica = PessoaFisica(
            nome_completo   = "Vanessa Sophia Ayla Moura",
            cpf             = "557.986.321-72",
        )

        self.assertEqual(pessoa_fisica.nome_completo, "Vanessa Sophia Ayla Moura")
        self.assertEqual(pessoa_fisica.cpf, "557.986.321-72")
        self.assertIsNone(pessoa_fisica.id_estrangeiro)

    def test_nova_pessoa_fisica_campos_obrigatorios_id_estrangeiro(self):
        pessoa_fisica = PessoaFisica(
            nome_completo   = "Vanessa Sophia Ayla Moura",
            id_estrangeiro  = "07534038001-40",
        )

        self.assertEquals(pessoa_fisica.nome_completo, "Vanessa Sophia Ayla Moura")
        self.assertEquals(pessoa_fisica.id_estrangeiro, "07534038001-40")
        self.assertIsNone(pessoa_fisica.cpf)

    def test_nova_pessoa_fisica_todos_campos(self):
        with self.assertRaises(ValueError):
            PessoaFisica (
                nome_completo   = "Vanessa Sophia Ayla Moura",
                cpf             = "557.986.321-72",
                id_estrangeiro  = "07534038001-40",
            )

class TestMunicipio(unittest.TestCase):
    def test_default_values(self):
        m = Municipio()
        self.assertIsNone(m.codigo_ibge)
        self.assertIsNone(m.descricao)

    def test_custom_values(self):
        m = Municipio(codigo_ibge=123, descricao='foo')
        self.assertEqual(m.codigo_ibge, 123)
        self.assertEqual(m.descricao, 'foo')

if __name__ == "__main__":
    unittest.main()
