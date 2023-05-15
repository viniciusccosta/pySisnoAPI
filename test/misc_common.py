def check_municipios_do_DF(test_case, data):
    test_case.assertListEqual(data, [{'codigo_ibge': 5300108, 'descricao': 'Brasilia'}] )

def check_cfops_length(test_case, data):
    test_case.assertGreater(len(data), 0)

def check_cfop_attributes(test_case, data):
    atributos = ["codigo", "descricao", "aplicacao"]
    cfop = data[0]              # TODO: O teste anterior garantiu que existe pelo menos 1 item
    for atributo in atributos:
        with test_case.subTest(key=atributo):
            test_case.assertIn(atributo, cfop)

# TODO: Check se informado um UF inválido na consulta de municípios