""" 
    Módulo específico para geração de Notas Fiscais de Produto.
    
    Para utilizar esse módulo basta importá-lo da seguinte forma:  
    `from pysisnoapi import nfe`
"""

# =====================================================================
from . import *

import requests
import json
import jsonpickle

from datetime import datetime

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
    
    def __post_init__(self):
        self.validate_operacao()
        self.validate_modelo()
        self.validate_finalidade()
        self.validate_ambiente()
    
    def validate_operacao(self):
        if self.operacao not in ['0', '1']:
            raise ValueError(f"Operação {self.operacao} inválida")
    
    def validate_modelo(self):
        if self.modelo not in ['55', '65']:
            raise ValueError(f"Modelo {self.modelo} inválido")
    
    def validate_finalidade(self):
        if self.finalidade not in ['1', '2', '3', '4']:
            raise ValueError(f"Finalidade {self.finalidade} inválida")
    
    def validate_ambiente(self):
        if self.ambiente not in ['1', '2',]:
            raise ValueError(f"Ambiente {self.ambiente} inválido")

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
    # tipo_integracao         : Optional[str] = None    # TODO: Não está na documentação mas é obrigatório caso meio de pagamento seja 'crédito' ou 'débito'. O valor deve ser '1' ou '2'.
    
    def __post_init__(self):
        self.validate_forma_pagamento()
        self.validate_meios_pagamento()
        self.validate_descricao()
    
    def validate_forma_pagamento(self):
        if self.forma_pagamento not in FORMAS_PAGAMENTO:
            raise ValueError(f'Forma de pagamento {self.forma_pagamento} inválido')
        
    def validate_meios_pagamento(self):
        if self.meio_pagamento not in MEIOS_PAGAMENTO:
            raise ValueError(f'Meio de pagamento {self.meio_pagamento} inválido')
        
    def validate_descricao(self):
        if self.meio_pagamento == '99':
            if self.descricao_meio_pagamento is None:
                raise ValueError(f'Necessário preencher "descricao_meio_pagamento" quando a forma de pagamento é "(99) Outros".')
            if len(self.descricao_meio_pagamento) < 2 or len(self.descricao_meio_pagamento) > 60:
                raise ValueError(f'O campo "descricao_meio_pagamento" deve conter entre 2 a 60 caracteres')

@dataclass
class Produto:
    """Classe Produto

    Raises:
        ValueError: Caso o valor de algum atributo seja inválido.
        TypeError: Caso algum campo obrigatório não for informado.
    """
    item                            : str   # Número incremental na lista de produtos
    
    cfop                            : str
    nome                            : str
    codigo                          : str
    ncm                             : str
    quantidade                      : str
    unidade                         : str
    subtotal                        : str
    total                           : str
    impostos                        : Impostos
    
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
    
    def __post_init__(self):
        self.validate_unidade()
        self.validate_impostos()
        
    def validate_unidade(self):
        if self.unidade not in UNIDADES:
            raise ValueError(f"Unidade {self.unidade} inválida.")
        
    def validate_impostos(self):
        if not isinstance(self.impostos, Impostos):
            raise TypeError(f'Campo "impostos" deve ser {repr(Impostos)} e não {type(self.impostos)}')

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
def emitir(objetoNfe:ObjetoEmissaoNFe, 
    tipo_emissao:str, *args, **kwargs) -> str:
    """Endpoint utilizado para efetivamente emitir uma nota fiscal eletrônica.

    Args:
        nfe (ObjetoEmissaoNFe): Nota Fiscal a ser emitida.
        
        tipo_emissao (str): Tipo de Emissão  
            1: Normal  
            6: Contigência SNC-AN  
            7: Contigência SVC-RS  
    """

    headers = HEADERS.copy()
    headers['tipo-emissao'] = tipo_emissao    # TODO: Validar antes
    json_str = jsonpickle.encode(objetoNfe.as_filtered_dict(), unpicklable=False)
    
    url = f'{BASE_URL}/nfe'
    response = requests.post(url, headers=headers, json=json.loads(json_str))
        
    match response.status_code:
        case 200:
            return response.json()
        case 412:
            return response.json()
        case _:
            return response.text
    
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
def validar(objetoNfe:ObjetoEmissaoNFe, 
    tipo_emissao:str, *args, **kwargs) -> str:
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
    
    url = f'{BASE_URL}/nfe/validacao-nota'
    response = requests.post(url, headers=headers, json=json.loads(json_str))
    
    match response.status_code:
        case 200:
            return response.json()
        case _:
            return response.text

@requires_emissor
def listar(qtd:str = None, 
    pagina:str = None, *args, **kwargs) -> List[NotaFiscal]:
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
    
    url = f'{BASE_URL}/nfe/lista-notas'
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