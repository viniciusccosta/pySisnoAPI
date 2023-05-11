# =====================================================================
from .sisno import *

# =====================================================================
HEADER_NFSE = [
    'CNPJ',
    'CPF',
    'Nome',
    'Indicador IE',
    'Consumidor Final',
    'Faz Retenção',
    'CEP',
    'UF',
    'IBGE',
    'Bairro',
    'Endereço',
    'Número',
    'Complemento',
    'E-mail',
    'Serviço',
    'Informações Complementares',
]

# =====================================================================
class ObjetoEmissaoNFSe:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
class Servico:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
class ConstrucaoCivil:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
class NotaFiscalServico:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError
    
class PaginaNotaServico:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

# =====================================================================
def emitir(*args, **kwargs):
    raise NotImplementedError

def buscar_notas(*args, **kwargs):
    raise NotImplementedError

def retransmitir(*args, **kwargs):
    raise NotImplementedError

def recuperar_dados(*args, **kwargs):
    raise NotImplementedError

def cancelar(*args, **kwargs):
    raise NotImplementedError

# =====================================================================