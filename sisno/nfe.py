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

class Pagamento:
    def __init__(self, *args):
        self.formas_pagamento        = [f for f in args]                                        # list[FORMAPAGAMENTO]

    def asdict(self):
        return {
            "formas_pagamento": [f.asdict() for f in self.formas_pagamento]
        }

class FormaPagamento:
    def __init__(self, **kwargs):
        self.forma_pagamento         = kwargs.get("forma_pagamento", None)                      # string (0: À Vista, 1: À Prazo)
        self.meio_pagamento          = kwargs.get("meio_pagamento", None)                       # string [01, 02, 03, 04, 05, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 90, 99 ]
        self.valor_pagamento         = kwargs.get("valor_pagamento", None)                      # string ($0.00)

    def asdict(self):
        return self.__dict__

class Produto:
    def __init__(self, tipo, **kwargs):
        self.tipo                   = tipo                                      # TODO: 0: Produto, 1: Serviço

        self.cfop                   = kwargs.get("cfop", None)                  # string
        self.item                   = kwargs.get("item", None)                  # string (Número incremental na lista de produtos)
        self.nome                   = kwargs.get("nome", None)                  # string
        self.ncm                    = kwargs.get("ncm", None)                   # string
        self.quantidade             = kwargs.get("quantidade", None)            # string
        self.unidade                = kwargs.get("unidade", None)               # string (AMPOLA, BALDE, BANDEJ, BARRA, BISNAG, BLOCO, BOBINA, BOMB, CAPS, CART, CENTO, CJ, CM, CM2, CX, CX2, CX3, CX5, CX10, CX15, CX20, CX25, CX50, CX100, DISP, DUZIA, EMBAL, FARDO, FOLHA, FRASCO, GALAO, JOGO, KG, KIT, LATA, LITRO, M, M2, M3, MILHEI, ML, MWH, PACOTE, PALETE, PARES, PC, POTE, K, RESMA, ROLO, SACO, SACOLA, TAMBOR, TANQUE, TON, TUBO, UNID, VASIL, VIDRO)
        self.subtotal               = kwargs.get("subtotal", None)              # string ($0.0000000000) - VALOR UNITÁRIO
        self.total                  = kwargs.get("total", None)                 # string ($0.00) (Quantidade * Valor Unitário)
        self.impostos               = kwargs.get("impostos", None)              # Objeto IMPOSTOS

    def asdict(self):
        return {
            "cfop"          : self.cfop,
            "item"          : self.item,
            "nome"          : self.nome,
            "ncm"           : self.ncm,
            "quantidade"    : self.quantidade,
            "unidade"       : self.unidade,
            "subtotal"      : self.subtotal,
            "total"         : self.total,
            "impostos"      : self.impostos.asdict(),
        }

class Pedido:
    def __init__(self, **kwargs):
        self.presenca                        = kwargs.get("presenca", None)                     # string [ 0, 1, 2, 3, 4, 5, 9 ]
        self.pagamento                       = kwargs.get("pagamento", None)                    # Objeto PAGAMENTO

        self.informacoes_complementares      = kwargs.get("informacoes_complementares", None)   # string
        self.informacoes_fisco               = kwargs.get("informacoes_fisco", None)            # string
        self.observacoes_fisco               = kwargs.get("observacoes_fisco", None)            # list[OBSERVACAO]
        self.observacoes_contribuinte        = kwargs.get("observacoes_contribuinte", None)     # list[OBSERVACAO]

    def asdict(self):
        # TODO: Adicionar o restante dos atributos ao dicionário

        return {
            "presenca"                      : self.presenca,
            "pagamento"                     : self.pagamento.asdict(),
        }

class VeiculoNovo:
    def __init__(self, **kwargs):
        raise NotImplementedError

class ExportacaoIndividual:
    def __init__(self, **kwargs):
        raise NotImplementedError

class ImportacaoInvididual:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Rastreamento:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Fatura:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Exportacao:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Local:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Compra:
    def __init__(self, **kwargs):
        raise NotImplementedError

class InformacaoIntermediador:
    def __init__(self, **kwargs):
        raise NotImplementedError

class PaginaNotas:
    def __init__(self, **kwargs):
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