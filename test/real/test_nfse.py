import unittest
from pysisnoapi import nfse
from test.nfse_common import *
from datetime import datetime

class NfseTest(unittest.TestCase):
    def test_buscar_notas_length(self):
        # TODO: Usar um .env apenas desenvolvimento da qual conste CNPJs para teste ?
        data = nfse.buscar_notas("00000001000191", datetime(2022, 1, 1), datetime(2023,12,31), )  # TODO: Solicitar a equipe de desenvolvimento da SISNO um banco de dados de teste.
        check_buscar_notas_atributos(self, data)

if __name__ == "__main__":
    unittest.main()