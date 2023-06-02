import unittest
from pysisnoapi import nfse
from test.nfse_common import *

class NfseTest(unittest.TestCase):
    def test_buscar_notas_pelo_menos_uma(self):
        nfses = nfse.buscar_notas()
        check_buscar_notas_pelo_menos_uma(self, nfses)

if __name__ == "__main__":
    unittest.main()