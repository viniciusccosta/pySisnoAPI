from pysisnoapi import Municipio

def check_municipios_do_DF(test_case, data):
    test_case.assertEqual(data, [Municipio(codigo_ibge=5300108, descricao = 'Brasilia')] )

# TODO: Check se informado um UF inválido na consulta de municípios