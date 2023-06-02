import unittest
from pysisnoapi import nfe
from test.nfe_common import *

class NfeTest(unittest.TestCase):
    def test_buscar_notas_pelo_menos_uma(self):
        # TODO: Alterar esse teste, pois ele não faz sentido em um contexto real, onde a API pode retornar uma lista vazia.
        nfes = nfe.listar()
        check_buscar_notas_pelo_menos_uma(self, nfes)

if __name__ == "__main__":
    unittest.main()