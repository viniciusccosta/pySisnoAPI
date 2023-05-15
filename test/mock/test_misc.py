import requests_mock
import unittest
from pysisnoapi import misc
from test.misc_common import *

class MiscTest(unittest.TestCase):

    def test_consulta_municipios_do_DF(self):
        uf = "DF"

        with requests_mock.Mocker() as mocker:
            mocker.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                json={'dados': [{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}]}
            )

            data = misc.get_municipios(uf=uf)
        
        check_municipios_do_DF(self, data)

    def test_consulta_cfops_length(self):
        with requests_mock.Mocker() as mocker:
            mocker.register_uri(
                requests_mock.ANY,
                requests_mock.ANY,
                json={'dados': [{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}]}
            )

            data = misc.get_cfops()
        
        check_cfops_length(self, data)

    def test_consulta_cfops_atributos(self):
        with requests_mock.Mocker() as mocker:
            mocker.register_uri(requests_mock.ANY, requests_mock.ANY,
                json={
                    'dados': [
                        {'codigo': '1000', 'descricao': 'ENTRADAS OU AQUISIÇÕES DE SERVIÇOS DO ESTADO', 'aplicacao': 'Classificam-se, neste grupo, as operações ou prestações em que o estabelecimento remetente esteja localizado na mesma unidade da Federação do destinatário'}, 
                        {'codigo': '1100', 'descricao': 'COMPRAS PARA INDUSTRIALIZAÇÃO, PRODUÇÃO RURAL, COMERCIALIZAÇÃO OU PRESTAÇÃO DE SERVIÇOS', 'aplicacao': '(NR Ajuste SINIEF 05/2005) (DECRETO Nº 28.868, DE 31/01/2006)(Dec. 28.868/2006 - Efeitos a partir de 01/01/2006, ficando facultada ao contribuinte a sua adoção para fatos geradores ocorridos no período de 01 de novembro a 31 de dezembro de 2005)'}, 
                        {'codigo': '1101', 'descricao': 'Compra para industrialização ou produção rural (NR Ajuste SINIEF 05/2005) (Decreto 28.868/2006)', 'aplicacao': 'Compra de mercadoria a ser utilizada em processo de industrialização ou produção rural, bem como a entrada de mercadoria em estabelecimento industrial ou produtor rural de cooperativa recebida de seus cooperados ou de estabelecimento de outra cooperativa.(DECRETO Nº 28.868, DE 31/01/2006-- Efeitos a partir de 01/01/2006, ficando facultada ao contribuinte a sua adoção para fatos geradores ocorridos no período de 01 de novembro a 31 de dezembro de 2005).'}, 
                        {'codigo': '1102', 'descricao': 'Compra para comercialização', 'aplicacao': 'Classificam-se neste código as compras de mercadorias a serem comercializadas. Também serão classificadas neste código as entradas de mercadorias em estabelecimento comercial de cooperativa recebidas de seus cooperados ou de estabelecimento de outra cooperativa.'}, 
                        {'codigo': '1111', 'descricao': 'Compra para industrialização de mercadoria recebida anteriormente em consignação industrial', 'aplicacao': 'Classificam-se neste código as compras efetivas de mercadorias a serem utilizadas em processo de industrialização, recebidas anteriormente a título de consignação industrial.'},
                    ]
                }
            )

            data = misc.get_cfops()
        
        check_cfop_attributes(self, data)

if __name__ == "__main__":
    unittest.main()