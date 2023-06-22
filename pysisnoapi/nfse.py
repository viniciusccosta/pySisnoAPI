""" 
    Módulo específico para geração de Notas Fiscais de Serviço.
    
    Para utilizar esse módulo basta importá-lo da seguinte forma:  
    `from pysisnoapi import nfse`
"""

# =====================================================================
from . import *

import json
import requests
from datetime import datetime
import jsonpickle

# =====================================================================
CSV_HEADERS = [
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
@dataclass
class Servico:
    """_summary_

    Returns:
        _type_: _description_
    """
    valor_servicos            : str
    discriminacao             : str
    impostos                  : "ImpostosServico"
    
    iss_retido                : Optional[str]         = 2 # 1: Sim, 2: Não
    responsavel_retencao_iss  : Optional[str]         = 1 # 1: Tomador, 2: Intermediário
    
    intermediario             : Optional["Cliente"]   = None
    deducoes                  : Optional[str]         = None
    desconto_incondicionado   : Optional[str]         = None
    desconto_condicionado     : Optional[str]         = None
    outras_retencoes          : Optional[str]         = None
    informacoes_complementares: Optional[str]         = None
    data_competencia          : Optional[str]         = None
    uf_local_prestacao        : Optional["Uf"]        = None
    municipio_local_prestacao : Optional["Municipio"] = None

@dataclass
class ConstrucaoCivil:
    codigo_obra: Optional[str] = None
    art        : Optional[str] = None
    
@dataclass
class ObjetoEmissaoNFSe(BaseClass):
    cliente: "Cliente"
    servico: "Servico"
    
    construcao_civil: Optional["ConstrucaoCivil"] = None

@dataclass
class NotaFiscalServico:
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    
    id                   : Optional[int]        = None
    empresa              : Optional[Empresa]    = None
    uuid                 : Optional[str]        = None
    modelo               : Optional[str]        = None
    status               : Optional[str]        = None
    motivo               : Optional[str]        = None
    numero_nota          : Optional[str]        = None
    codigo_verificacao   : Optional[str]        = None
    protocolo            : Optional[str]        = None
    nome_destinatario    : Optional[str]        = None
    uf_destinatario      : Optional[str]        = None
    cpf_cnpj_destinatario: Optional[str]        = None
    valor_total          : Optional[str]        = None
    data_emissao         : Optional[str]        = None
    data_competencia     : Optional[str]        = None
    uf_prestacao         : Optional[Uf]         = None
    municipio_prestacao  : Optional[Municipio]  = None
    ambiente             : Optional[str]        = None
    json_objeto_nfse     : Optional[str]        = None  # TODO: Não consta na documentação da API
    
    @classmethod
    def from_json(cls, **kwargs):
        empresa_dict = kwargs.pop('empresa', {})
        empresa = Empresa.from_json(**empresa_dict)
        
        uf_dict = kwargs.pop('uf_prestacao', {})
        uf      = Uf.from_json(**uf_dict)
        
        municipio_dict = kwargs.pop('municipio_prestacao', {})
        municipio = Municipio.from_json(**municipio_dict)
        
        return cls(empresa=empresa, uf_prestacao=uf, municipio_prestacao=municipio, **kwargs)

@dataclass
class PaginaNotasServico:
    total           : Optional[str]                       = None
    itens_por_pagina: Optional[str]                       = None
    pagina_atual    : Optional[str]                       = None
    itens           : Optional[List["NotaFiscalServico"]] = None
    
@dataclass
class ImpostosServico(Impostos):
    issqn: "Issqn"

# =====================================================================
@requires_emissor
@requires_empresa
def emitir(objetoNfse: ObjetoEmissaoNFSe, *args, **kwargs):
    """Método responsável por enviar uma requisição para a plataforma SISNO solicitando a emissão de uma nova fiscal de SERVIÇO.
    
    Args:
        obj_emissao_nfse (ObjetoEmissaoNFSe): Objeto da classe "ObjetoEmissaoNFSe" que contém todos os dados necessários

    Returns:
        dict: Dicionário com os dados da requisição
        str: Com o response.text em caso de falha da requisição
    """

    json_str = jsonpickle.encode(objetoNfse.as_filtered_dict(), unpicklable=False)
    
    headers = HEADERS.copy()
    url     = f'{BASE_URL}/nfse'
    response = requests.post(url, headers=headers, json=json.loads(json_str))

    match (response.status_code):
        case 200:
            return response.json()
        case _:
            return response.text

@requires_emissor
def buscar_notas(cnpj:str=None, 
    data_inicio:datetime=None, 
    data_fim:datetime=None, 
    ambiente:str=None, 
    status:str=None, 
    texto:str=None, 
    pagina:str=None, 
    qtd_por_pagina:str=None, 
    ordencao:str=None, 
    tipo_ordenacao:str=None, *args, **kwargs) -> List[NotaFiscalServico]:
    """Recupera as notas fiscais de serviço.

    Args:
        cnpj (str): CNPJ Empresa (apenas números).
        
        data_inicio (datetime): Início intervalo de datas (dd/MM/yyyy HH:mm:ss).
        
        data_fim (datetime): Fim intervalo de datas (dd/MM/yyyy HH:mm:ss).
        
        ambiente (str):  
            1: Produção  
            2: Homologação
            
        status (str): Status da NFSe.
            - aprovado  
            - reprovado  
            - contingencia    
            - cancelado  
            - Em digitação
            
        texto (str): Texto de busca livre.
        
        pagina (int): Número da página.
        
        qtd_por_pagina (int): Quantidade de notas por página.
        
        ordencao (str): Campo para ordenação das notas.  
            - empresa  
            - ambiente  
            - numero_nota  
            - status  
            - data_emissao  
            - nome_destinatario  
            - uf_destinatario  
            - valor_total
            
        tipo_ordenacao (str): Tipo de Ordenação.
            - desc  
            - asc  
    
    Returns:
        List[NotaFiscalServico]: Lista com todas as NFSe
    """
    
    headers = HEADERS.copy()
    
    if cnpj:
        headers['CNPJ Empresa'] = cnpj
    if data_inicio:
        headers['dataInicio'] = data_inicio.strftime("%d/%m/%Y %H:%M:%S")
    if data_fim:
        headers['dataFim'] = data_fim.strftime("%d/%m/%Y %H:%M:%S")
    if ambiente:
        headers['ambiente'] = ambiente
    if status:
        headers['status'] = status
    if texto:
        headers['textoBusca'] = texto
    if pagina:
        headers['pagina'] = pagina                  # TODO: Na documentação diz que deve ser inteiro, mas "Header part (1) from ('pagina', 1) must be of type str or bytes, not <class 'int'>"
    if qtd_por_pagina:
        headers['qtdPorPagina'] = qtd_por_pagina    # TODO: Na documentação diz que deve ser inteiro, mas "Header part (10) from ('qtdPorPagina', 10) must be of type str or bytes, not <class 'int'>"
    if ordencao:
        headers['ordenacao'] = ordencao
    if tipo_ordenacao:
        headers['tipoOrdenacao'] = tipo_ordenacao

    url = f'{BASE_URL}/nfse'
    response = requests.get(url, headers=headers)

    match (response.status_code):
        case 200:
            json_data = response.json().get('dados')
            nfses = [NotaFiscalServico.from_json(**d) for d in json_data['itens']]
            return nfses
        case _:
            return response.text

@requires_emissor
@requires_empresa
def retransmitir(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def recuperar_dados(id_nfse:int, *args, **kwargs):
    # TODO: Cada NFSe possui um ID mesmo que de empresas diferentes ?
    # TODO: Essa função deveria estar atrelada as chaves de API, uma vez que será através delas que emitiremos as notas por uma empresa ou por outra ?

    if not isinstance(id_nfse, int):
        raise ValueError("Necessário informar um ID de NFSe válido.")
    
    headers  = HEADERS.copy()
    url      = f'{BASE_URL}/nfse/{id_nfse}'
    response = requests.get(url, headers=headers)

    match (response.status_code):
        case 200:
            return response.json().get('dados')
        case 412:
            return []
        case _:
            return

@requires_emissor
@requires_empresa
def cancelar(*args, **kwargs):
    raise NotImplementedError

# =====================================================================
