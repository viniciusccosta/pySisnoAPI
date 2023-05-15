import unittest
from pysisnoapi import misc
from test.misc_common import *

class MiscTest(unittest.TestCase):

    def test_consulta_municipio(self):
        uf = "DF"

        data = misc.get_municipios(uf=uf)
        
        check_municipios_do_DF(self, data)

    def test_consulta_cfops_length(self):
        data = misc.get_cfops()
        
        check_cfops_length(self, data)

    def test_consulta_cfops_atributos(self):
        data = misc.get_cfops()
        
        check_cfop_attributes(self, data)

if __name__ == "__main__":
    unittest.main()