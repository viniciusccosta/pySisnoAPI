''' 
    Módulo específico para geração de Notas Fiscais de Serviço.
    
    Para utilizar esse módulo basta importá-lo da seguinte forma:  
    `from pysisnoapi import nfse`
'''

# =====================================================================
from . import *

import json
import httpx
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

INDICADORES_EXIGIBILIDADE_ISS = {
    '1': 'Exigível',
    '2': 'Não incidência',
    '3': 'Isenção',
    '4': 'Exportação',
    '5': 'Imunidade',
    '6': 'Exigibilidade suspensa por decisão judicial',
    '7': 'Exigibilidade suspensa por processo administrativo',
}

INDICADORES_INCENTIVO_FISCAL = {
    '1': 'Não',
    '2': 'Sim',
}

INDICADORES_ISS_RETIDO = {
    '1': 'Sim',
    '2': 'Não',
} # TODO: Sugerir a utilização de Boolean.

RESPONSAVEIS_RETENCAO_ISS = {
    '1': 'Tomador',
    '2': 'Intermediário',
}

STATUS = [
    'aprovado',
    'reprovado',
    'contingencia',
    'cancelado',
    'Em digitação',
]

# =====================================================================
@dataclass
class Servico:
    '''_summary_

    Returns:
        _type_: _description_
    '''
    valor_servicos            : str
    discriminacao             : str
    impostos                  : 'ImpostosServico'
    
    iss_retido                : Optional[str]         = None
    responsavel_retencao_iss  : Optional[str]         = None
    
    intermediario             : Optional['Cliente']   = None
    deducoes                  : Optional[str]         = None
    desconto_incondicionado   : Optional[str]         = None
    desconto_condicionado     : Optional[str]         = None
    outras_retencoes          : Optional[str]         = None
    informacoes_complementares: Optional[str]         = None
    data_competencia          : Optional[str]         = None
    uf_local_prestacao        : Optional['Uf']        = None
    municipio_local_prestacao : Optional['Municipio'] = None
    
    def __post_init__(self, *args, **kwargs):
        self.validate_iss_retido()
        self.validate_responsavel_retencao_iss()
    
    def validate_iss_retido(self, *args, **kwargs):
        if self.iss_retido and self.iss_retido not in INDICADORES_ISS_RETIDO:
            raise ValueError(f'Indicador de ISS retido {self.iss_retido} inválido.')
    
    def validate_responsavel_retencao_iss(self, *args, **kwargs):
        if self.responsavel_retencao_iss and self.responsavel_retencao_iss not in RESPONSAVEIS_RETENCAO_ISS:
            raise ValueError(f'Responsável pela retenção do ISS {self.responsavel_retencao_iss} inválido.')

@dataclass
class ConstrucaoCivil:
    codigo_obra: Optional[str] = None
    art        : Optional[str] = None
    
@dataclass
class ObjetoEmissaoNFSe(BaseClass):
    cliente: 'Cliente'
    servico: 'Servico'
    
    construcao_civil: Optional['ConstrucaoCivil'] = None

@dataclass
class NotaFiscalServico(BaseClass):
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
    xml                  : Optional[str]        = None  # TODO: Não consta na documentação da API
    
    numer_nota           : Optional[str]        = None  # TODO: EXCLUIR! É um typo de "numero_nota", adicionei hoje (03/07/2023) apenas para o package não parar de funcionar.
    
    @classmethod
    def from_json(cls, **kwargs):
        empresa_dict = kwargs.pop('empresa', {})
        empresa = Empresa.from_json(**empresa_dict)
        
        uf_dict = kwargs.pop('uf_prestacao', {})
        uf      = Uf.from_json(**uf_dict)
        
        municipio_dict = kwargs.pop('municipio_prestacao', {})
        municipio = Municipio.from_json(**municipio_dict)
        
        return cls(empresa=empresa, uf_prestacao=uf, municipio_prestacao=municipio, **kwargs)

    def to_json(self, *args, **kwargs):
        json_str = jsonpickle.encode(self.as_filtered_dict(), unpicklable=False)
        return json_str
    
    def __str__(self):
        return f'NFSe {self.uuid}'
    
    def __repr__(self):
        return f'NFSe {self.uuid}'

@dataclass
class PaginaNotasServico:
    total           : Optional[str]                       = None
    itens_por_pagina: Optional[str]                       = None
    pagina_atual    : Optional[str]                       = None
    itens           : Optional[List['NotaFiscalServico']] = None
    
@dataclass
class ImpostosServico(Impostos):
    issqn: 'Issqn'

@dataclass
class Issqn:
    indicador_exigibilidade_iss: str
    indicador_incentivo_fiscal : str
    item_lista_servicos        : str
    aliquota                   : str
    
    numero_processo            : Optional[str] = None
    codigo_servico             : Optional[str] = None
    aliquota_retencao          : Optional[str] = None
    aliquota_irrf              : Optional[str] = None
    aliquota_csll              : Optional[str] = None
    aliquota_previdencia_social: Optional[str] = None
    
    def __post_init__(self, *args, **kwargs):
        self.validate_indicador_exigibilidade_iss()
        self.validate_indicador_incentivo_fiscal()
    
    def validate_indicador_exigibilidade_iss(self, *args, **kwargs):
        if self.indicador_exigibilidade_iss not in INDICADORES_EXIGIBILIDADE_ISS:
            raise ValueError(f'Indicador de Exigibilidade Fiscal {self.indicador_exigibilidade_iss} inválido.')
    
    def validate_indicador_incentivo_fiscal(self, *args, **kwargs):
        if self.indicador_incentivo_fiscal not in INDICADORES_INCENTIVO_FISCAL:
            raise ValueError(f'Indicador de Incentivo Fiscal {self.indicador_incentivo_fiscal} inválido.')
    
# =====================================================================
async def emitir(token_emissor: str, 
           token_secret_emissor: str,
           token_empresa: str, 
           token_secret_empresa: str, 
           objetoNfse: ObjetoEmissaoNFSe, 
           *args, **kwargs) -> httpx.Response:
    '''Método responsável por enviar uma requisição para a plataforma SISNO solicitando a emissão de uma nova fiscal de SERVIÇO.
    
    Args:
        obj_emissao_nfse (ObjetoEmissaoNFSe): Objeto da classe "ObjetoEmissaoNFSe" que contém todos os dados necessários

    Returns:
        httpx.Response: Resposta do servidor
    '''

    headers = HEADERS.copy()
    
    # -----------------------------------------
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor
    
    validate_tokens(token_empresa, token_secret_empresa)
    headers['token-empresa']        = token_empresa
    headers['token-secret-empresa'] = token_secret_empresa
    
    # -----------------------------------------
    json_str = jsonpickle.encode(objetoNfse.as_filtered_dict(), unpicklable=False)
    
    url     = f'{BASE_URL}/nfse'
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json.loads(json_str))
    
    # Resultado:
    # TODO: Retornar algo mais útil do que simplesmente o response...
    return response

async def buscar_notas(token_emissor: str, 
                 token_secret_emissor: str,
                 cnpjEmpresa:list=None, 
                 data_inicio:datetime=None, 
                 data_fim:datetime=None, 
                 ambiente:str=None, 
                 status:str=None, 
                 texto:str=None, 
                 pagina:int=None, 
                 qtd_por_pagina:int=None, 
                 ordencao:str=None, 
                 tipo_ordenacao:str=None,
                 *args, **kwargs) -> (httpx.Response, List[NotaFiscalServico]):
    '''Recupera as notas fiscais de serviço.

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
        httpx.Reponse: Resposta do servidor
        List[NotaFiscalServico]: Lista com todas as NFSe
    '''
    
    # TODO: o parâmetro cnpjEmpresa está errado na documentação ('CNPJ Empresa')
    # TODO: o endpoint ignora o parâmetro cnpjEmpresa em alguns casos, descrir quais os casos.
    # TODO: textoBusca é case sensitive e leva em consideração acentos.
    # TODO: dataFim não precisa de dataInicio
    
    headers = HEADERS.copy()
    
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor
    
    params = {}
    if cnpjEmpresa:
        params['cnpjEmpresa'] = cnpjEmpresa
    if data_inicio:
        params['dataInicio'] = data_inicio.strftime('%d/%m/%Y %H:%M:%S')
    if data_fim:
        params['dataFim'] = data_fim.strftime('%d/%m/%Y %H:%M:%S')
    if ambiente:
        if ambiente not in AMBIENTES:
            raise ValueError(f'Ambiente {ambiente} inválido.')
        params['ambiente'] = ambiente      
    if status:
        if status not in STATUS:
            raise ValueError(f'Status {status} inválido.')
        params['status'] = status
    if texto:
        params['textoBusca'] = texto
    if pagina:
        params['pagina'] = str(pagina)
    if qtd_por_pagina:
        params['qtdPorPagina'] = str(qtd_por_pagina)
    if ordencao:
        params['ordenacao'] = ordencao
    if tipo_ordenacao:
        params['tipoOrdenacao'] = tipo_ordenacao

    url = f'{BASE_URL}/nfse'
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    match (response.status_code):
        case 200:
            json_dados = response.json().get('dados')
            nfses      = [NotaFiscalServico.from_json(**d) for d in json_dados['itens']]
            return (response, nfses)
    
    return (response, None)

async def retransmitir(token_emissor: str, 
                 token_secret_emissor: str,
                 token_empresa:str, 
                 token_secret_empresa:str, 
                 *args, **kwargs):
    raise NotImplementedError

async def recuperar_dados(token_emissor: str, 
                    token_secret_emissor: str,
                    token_empresa:str, 
                    token_secret_empresa:str, 
                    id_nfse:int,
                    *args, **kwargs) -> httpx.Response:
    # TODO: Cada NFSe possui um ID mesmo que de empresas diferentes ?
    # TODO: Essa função deveria estar atrelada as chaves de API, uma vez que será através delas que emitiremos as notas por uma empresa ou por outra ?

    if not isinstance(id_nfse, int):
        raise ValueError('Necessário informar um ID de NFSe válido.')
    
    headers  = HEADERS.copy()
    
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor
    
    validate_tokens(token_empresa, token_secret_empresa)
    headers['token-empresa']        = token_empresa
    headers['token-secret-empresa'] = token_secret_empresa
    
    url      = f'{BASE_URL}/nfse/{id_nfse}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
    
    # TODO: Retornar algo mais útil como uma instância de NotaFiscal por exemplo ?!
    return response

async def cancelar(token_emissor: str, 
             token_secret_emissor: str, 
             token_empresa:str,
             token_secret_empresa:str, 
             *args, **kwargs):
    raise NotImplementedError

# =====================================================================
