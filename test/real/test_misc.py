import unittest
from pysisnoapi import misc
from test.misc_common import *

class MiscTest(unittest.TestCase):

    def test_consulta_municipio(self):
        uf = "DF"

        data = misc.get_municipios(uf=uf)
        
        check_municipios_do_DF(self, data)

if __name__ == "__main__":
    unittest.main()