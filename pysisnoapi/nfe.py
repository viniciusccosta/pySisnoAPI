""" 
    Módulo específico para geração de Notas Fiscais de Produto.
    
    Para utilizar esse módulo basta importá-lo da seguinte forma:  
    `from pysisnoapi import nfe`
"""

# =====================================================================
from . import *

from datetime import datetime
# from pydantic import BaseModel, validator
import requests
import json
import jsonpickle

# =====================================================================
CSV_HEADERS = [
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
@dataclass
class ObjetoEmissaoNFe(BaseClass):
    numero_nota_sequencial  : str
    serie                   : str
    operacao                : str
    natureza_operacao       : str
    modelo                  : str
    finalidade              : str
    ambiente                : str
    cliente                 : Cliente
    produtos                : List["Produto"]
    pedido                  : "Pedido"
    data_entrada_saida      : datetime
    data_emissao            : datetime
    
    numero_pedido           : Optional[str]                       = None
    transporte              : Optional["Transporte"]              = None
    fatura                  : Optional["Fatura"]                  = None
    parcelas                : Optional[List["Parcela"]]           = None
    exportacao              : Optional["Exportacao"]              = None
    nfe_referenciada        : Optional[List[str]]                 = None
    retirada                : Optional["Local"]                   = None
    entrega                 : Optional["Local"]                   = None
    compra                  : Optional["Compra"]                  = None
    indicador_intermediador : Optional[str]                       = None
    informacao_intermediador: Optional["InformacaoIntermediador"] = None
    
    # @validator('operacao')
    # def validate_operacao(cls, operacao):
    #     if not isinstance(operacao, str):
    #         raise TypeError("Operação tem que ser uma string")
    #     if operacao not in ['0', '1']:
    #         raise ValueError(f"Operação {operacao} inválida")
    #     return operacao
    
    # @validator('modelo')
    # def validate_modelo(cls, modelo):
    #     if not isinstance(modelo, str):
    #         raise TypeError("Modelo tem que ser uma string")
    #     if modelo not in ['55', '65']:
    #         raise ValueError(f"Modelo {modelo} inválido")
    #     return modelo
    
    # @validator('finalidade')
    # def validate_finalidade(cls, finalidade):
    #     if not isinstance(finalidade, str):
    #         raise TypeError("Finalidade tem que ser uma string")
    #     if finalidade not in ['1', '2', '3', '4']:
    #         raise ValueError(f"Finalidade {finalidade} inválida")
    #     return finalidade
    
    # @validator('ambiente')
    # def validate_ambiente(cls, ambiente):
    #     if not isinstance(ambiente, str):
    #         raise TypeError("Ambiente tem que ser uma string")
    #     if ambiente not in ['1', '2',]:
    #         raise ValueError(f"Ambiente {ambiente} inválido")
    #     return ambiente

@dataclass
class Pagamento:
    formas_pagamento: List["FormaPagamento"]

@dataclass
class FormaPagamento:
    forma_pagamento         : str
    meio_pagamento          : str
    valor_pagamento         : str
    
    cnpj_credenciadora      : Optional[str] = None
    bandeira                : Optional[str] = None
    autorizacao             : Optional[str] = None
    data_vencimento         : Optional[str] = None
    descricao_meio_pagamento: Optional[str] = None

@dataclass
class Produto:
    cfop                            : str
    item                            : str
    nome                            : str
    codigo                          : str
    ncm                             : str
    quantidade                      : str
    unidade                         : str
    subtotal                        : str
    total                           : str
    impostos                        : str
    
    numero_pedido                   : Optional[str]                    = None
    excessao_ibpt                   : Optional[str]                    = None
    peso_liquido                    : Optional[str]                    = None
    peso_bruto                      : Optional[str]                    = None
    origem                          : Optional[str]                    = None
    veiculo_usado                   : Optional[str]                    = None
    ind_escala                      : Optional[str]                    = None
    cnpj_fabricante                 : Optional[str]                    = None
    beneficio_fiscal                : Optional[str]                    = None
    gtin                            : Optional[str]                    = None
    gtin_tributavel                 : Optional[str]                    = None
    cest                            : Optional[str]                    = None
    nve                             : Optional[str]                    = None
    informacoes_adicionais          : Optional[str]                    = None
    veiculo_novo                    : Optional['VeiculoNovo']          = None
    exportacao                      : Optional['ExportacaoIndividual'] = None
    importacao                      : Optional['ImportacaoIndividual'] = None
    rastro                          : Optional['Rastreamento']         = None
    ex_tipi                         : Optional[str]                    = None
    valor_frete                     : Optional[str]                    = None
    valor_seguro                    : Optional[str]                    = None
    valor_desconto                  : Optional[str]                    = None
    valor_outras_despesas_acessorias: Optional[str]                    = None
    
    # @validator('unidade')
    # def validate_unidade(cls, unidade):
    #     if not isinstance(str, unidade):
    #         return TypeError("Unidade precisa ser uma string")
    #     if unidade not in ['AMPOLA', 'BALDE', 'BANDEJ', 'BARRA', 'BISNAG', 'BLOCO', 'BOBINA', 'BOMB', 'CAPS', 'CART', 'CENTO', 'CJ', 'CM', 'CM2', 'CX', 'CX2', 'CX3', 'CX5', 'CX10', 'CX15', 'CX20', 'CX25', 'CX50', 'CX100', 'DISP', 'DUZIA', 'EMBAL', 'FARDO', 'FOLHA', 'FRASCO', 'GALAO', 'JOGO', 'KG', 'KIT', 'LATA', 'LITRO', 'M', 'M2', 'M3', 'MILHEI', 'ML', 'MWH', 'PACOTE', 'PALETE', 'PARES', 'PC', 'POTE', 'K', 'RESMA', 'ROLO', 'SACO', 'SACOLA', 'TAMBOR', 'TANQUE', 'TON', 'TUBO', 'UNID', 'VASIL', 'VIDRO',]:
    #         return ValueError(f"Unidade {unidade} inválida")
    #     return unidade

@dataclass
class ImpostosProduto(Impostos):
    icms: "Icms"
    ipi : "Ipi"

@dataclass
class Pedido:
    presenca                  : str
    pagamento                 : "Pagamento"
    
    modalidade_frete          : Optional[str] = None
    frete                     : Optional[str] = None
    desconto                  : Optional[str] = None
    total                     : Optional[str] = None
    despesas_acessorias       : Optional[str] = None
    despesas_aduaneiras       : Optional[str] = None
    informacoes_complementares: Optional[str] = None
    informacoes_fisco         : Optional[str] = None
    observacoes_fisco         : Optional[str] = None
    observacoes_contribuinte  : Optional[str] = None
    
class VeiculoNovo:
    def __init__(self, **kwargs):
        raise NotImplementedError

class ExportacaoIndividual:
    def __init__(self, **kwargs):
        raise NotImplementedError

class ImportacaoIndividual:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Rastreamento:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Fatura:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Parcela:
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
@requires_emissor
@requires_empresa
def emitir(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def corrigir(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def cancelar(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def validar(objetoNfe:ObjetoEmissaoNFe, tipo_emissao:str, *args, **kwargs) -> None:
    """Endpoint utilizado para validar a nota fiscal eletrônica antes de emitir.

    Args:
        nfe (ObjetoEmissaoNFe): Nota Fiscal a ser validada.
        
        tipo_emissao (str): Tipo de Emissão  
            1: Normal  
            6: Contigência SNC-AN  
            7: Contigência SVC-RS  
    """
    headers = HEADERS.copy()
    headers['tipo-emissao'] = tipo_emissao    # TODO: Validar antes
    json_str = jsonpickle.encode(objetoNfe.as_filtered_dict(), unpicklable=False)
    
    url = f'{URL}/nfe/validacao-nota'
    response = requests.post(url, headers=headers, json=json.loads(json_str))
    
    match response.status_code:
        case 200:
            return response.json()
        case _:
            return response.text

@requires_emissor
def listar(qtd:str = None, pagina:str = None, *args, **kwargs) -> List[NotaFiscal]:
    """Recupera as notas fiscais.
    
    No Distrito Federal (DF), antes de 01/2023, as notas fiscais de serviço eram emitidas como NFe.

    Args:
        qtd (str, optional): Quantidade de notas por página.
        pagina (str, optional): Página a ser retornada.

    Returns:
        List[NotaFiscal]: Lista contendo as notas fiscais.
    """
    headers = HEADERS.copy()
    params   = {}
    
    if qtd:
        params["qtd"] = qtd
    if pagina:
        params["pagina"] = pagina
    
    url = f'{URL}/nfe/lista-notas'
    response = requests.get(url, params, headers=headers)
    
    match (response.status_code):
        case 200:
            json_data = response.json().get('dados')
            nfes = [NotaFiscal.from_json(**d) for d in json_data['itens']]
            return nfes
        case _:
            return response.text

@requires_emissor
def buscar(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
def get_nota(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def inutilizar_numeracao(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def get_pre_visualizacao(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def get_danfe(*args, **kwargs):
    raise NotImplementedError

# =====================================================================