# =====================================================================
from .sisno import *

# =====================================================================
HEADER_NFE = [
    'CNPJ EMITENTE',
    'MODELO',
    'CPF/CNPJ DESTINATÁRIO',
    'NOME/RAZAO SOCIAL DESTINATÁRIO',
    'INDICADOR IE',
    'CONSUMIDOR FINAL',
    'FAZ RETENÇÃO DE IMPOSTOS',
    'CEP',
    'BAIRRO',
    'LOGRADOURO',
    'NUMERO',
    'EMAIL DESTINATÁRIO',
    'OPERAÇÃO',
    'FINALIDADE',
    'PRODUTOS',
    'MEIO PAGAMENTO',
    'INFORMAÇÕES COMPLEMENTARES',
    'SIGLA UF',
    'IBGE MUNICÍPIO',
    'COMPLEMENTO ENDEREÇO'
]

# =====================================================================
class ObjetoEmissaoNFe:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

# =====================================================================
def emitir(*args, **kwargs):
    raise NotImplementedError

def corrigir(*args, **kwargs):
    raise NotImplementedError

def cancelar(*args, **kwargs):
    raise NotImplementedError

def validar(*args, **kwargs):
    raise NotImplementedError

def listar(*args, **kwargs):
    raise NotImplementedError

def buscar_notas(*args, **kwargs):
    raise NotImplementedError

def get_nota(*args, **kwargs):
    raise NotImplementedError

def inutilizar_numeracao(*args, **kwargs):
    raise NotImplementedError

def get_pre_visualizacao(*args, **kwargs):
    raise NotImplementedError

def get_danfe(*args, **kwargs):
    raise NotImplementedError

# =====================================================================