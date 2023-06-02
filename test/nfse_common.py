import unittest
from pysisnoapi.nfse import *

def check_buscar_notas_pelo_menos_uma(test_case: unittest.TestCase, data: List[NotaFiscalServico]):
    test_case.assertGreaterEqual(len(data), 1)