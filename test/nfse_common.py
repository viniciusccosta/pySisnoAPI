def check_buscar_notas_atributos(test_case, data):
    atributos = ["informacoesAdicionais", "itens", "itens_por_pagina", "pagina_atual", "total"]
    for atributo in atributos:
        with test_case.subTest(key=atributo):
            test_case.assertIn(atributo, data)