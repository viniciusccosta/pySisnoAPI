import unittest
from pysisnoapi import *

# TODO: Teste para verificar se as chaves da API estão configuradas
# TODO: Teste para verificar se as chaves são válidas
# TODO: Teste para verificar se a plataforma reconhece as chaves
# TODO: Teste para verificar se existe .env
# TODO: Teste para verificar se a função de alterar as chaves da API está funcionando

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
        self.assertEquals(cliente.pessoa_fisica, pessoa_fisica)
        self.assertEquals(cliente.consumidor_final, '1')
        self.assertEquals(cliente.contribuinte, '9')
        self.assertEquals(cliente.endereco, endereco)
        
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
        self.assertEquals(cliente.pessoa_juridica, pessoa_juridica)
        self.assertEquals(cliente.consumidor_final, '1')
        self.assertEquals(cliente.contribuinte, '9')
        self.assertEquals(cliente.endereco, endereco)
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
    
class PessoaFisicaTestCase(unittest.TestCase):
    def test_nova_pessoa_fisica_campos_obrigatorios_cpf(self):
        pessoa_fisica = PessoaFisica(
            nome_completo   = "Vanessa Sophia Ayla Moura",
            cpf             = "557.986.321-72",
        )
        
        self.assertEquals(pessoa_fisica.nome_completo, "Vanessa Sophia Ayla Moura")
        self.assertEquals(pessoa_fisica.cpf, "557.986.321-72")
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
        
    def test_from_json(self):
        json_dict = {'codigo_ibge': 456, 'descricao': 'bar'}
        m = Municipio.from_json(**json_dict)
        self.assertEqual(m.codigo_ibge, 456)
        self.assertEqual(m.descricao, 'bar')

if __name__ == "__main__":
    unittest.main()