import unittest
from typing import List
from pysisnoapi.nfe import NotaFiscal

def check_buscar_notas_pelo_menos_uma(test_case: unittest.TestCase, data: List[NotaFiscal]):
    test_case.assertGreaterEqual(len(data), 1)