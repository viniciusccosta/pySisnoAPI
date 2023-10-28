'''
    Módulo específico para geração de Notas Fiscais de Serviço.

    Para utilizar esse módulo basta importá-lo da seguinte forma:
    `from pysisnoapi import nfse`
'''

# =====================================================================
import json
import httpx

from datetime          import datetime
from typing            import Optional
from typing_extensions import Annotated
from pydantic          import BaseModel, Field, validate_call
from typing            import List
from enum              import StrEnum

from . import (
    HEADERS,
    BASE_URL,
    
    AmbientesEnum,
    
    Cliente,
    Uf,
    Municipio,
    Empresa,
    Impostos,
    
    validate_tokens,
)

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

STATUS = {
    'aprovado'    : 'aprovado',
    'reprovado'   : 'reprovado',
    'contingencia': 'contingencia',
    'cancelado'   : 'cancelado',
    'digitação'   : 'Em digitação',
}

# =====================================================================
IndicadoresExigibilidadeIssEnum = StrEnum('Indicadores de Exigibilidade do ISS', list(INDICADORES_EXIGIBILIDADE_ISS.keys()), )
IndicadoresIncentivoFiscalEnum  = StrEnum('Indicadores de Incentivo Fiscal', list(INDICADORES_INCENTIVO_FISCAL.keys()), )
IndicadoresIssRetidoEnum        = StrEnum('Indicadores de ISS Retido', list(INDICADORES_ISS_RETIDO.keys()), )
ResponsaveisRetencaoIssEnum     = StrEnum('Responsável pela Retenção do ISS', list(RESPONSAVEIS_RETENCAO_ISS.keys()), )
StatusEnum                      = StrEnum('Status', STATUS)

# =====================================================================
class Servico(BaseModel):
    '''_summary_

    Returns:
        _type_: _description_
    '''
    valor_servicos            : str               = Field()
    discriminacao             : str               = Field()
    impostos                  : 'ImpostosServico' = Field()

    id                        : Optional[Annotated[int, Field()]]                         = None    # TODO: Obrigatório ?   # TODO: int ?
    iss_retido                : Optional[Annotated[IndicadoresIssRetidoEnum, Field()]]    = None    # TODO: int ?
    responsavel_retencao_iss  : Optional[Annotated[ResponsaveisRetencaoIssEnum, Field()]] = None    # 

    intermediario             : Optional[Annotated['Cliente', Field()]]   = None
    deducoes                  : Optional[Annotated[str, Field()]]         = None
    desconto_incondicionado   : Optional[Annotated[str, Field()]]         = None
    desconto_condicionado     : Optional[Annotated[str, Field()]]         = None
    outras_retencoes          : Optional[Annotated[str, Field()]]         = None
    informacoes_complementares: Optional[Annotated[str, Field()]]         = None
    data_competencia          : Optional[Annotated[str, Field()]]         = None
    uf_local_prestacao        : Optional[Annotated['Uf', Field()]]        = None
    municipio_local_prestacao : Optional[Annotated['Municipio', Field()]] = None

class ConstrucaoCivil(BaseModel):
    codigo_obra: Optional[Annotated[str, Field()]] = None
    art        : Optional[Annotated[str, Field()]] = None

class ObjetoEmissaoNFSe(BaseModel):
    cliente: 'Cliente' = Field()
    servico: 'Servico' = Field()

    construcao_civil: Optional[Annotated['ConstrucaoCivil', Field()]] = None

class NotaFiscalServico(BaseModel):
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios

    id                   : Optional[Annotated[int, Field()]]         = None
    empresa              : Optional[Annotated['Empresa', Field()]]   = None
    uuid                 : Optional[Annotated[str, Field()]]         = None
    modelo               : Optional[Annotated[str, Field()]]         = None
    status               : Optional[Annotated[str, Field()]]         = None
    motivo               : Optional[Annotated[str, Field()]]         = None
    numero_nota          : Optional[Annotated[str, Field()]]         = None
    codigo_verificacao   : Optional[Annotated[str, Field()]]         = None
    protocolo            : Optional[Annotated[str, Field()]]         = None
    nome_destinatario    : Optional[Annotated[str, Field()]]         = None
    uf_destinatario      : Optional[Annotated[str, Field()]]         = None
    cpf_cnpj_destinatario: Optional[Annotated[str, Field()]]         = None
    valor_total          : Optional[Annotated[str, Field()]]         = None
    data_emissao         : Optional[Annotated[str, Field()]]         = None
    data_competencia     : Optional[Annotated[str, Field()]]         = None
    uf_prestacao         : Optional[Annotated['Uf', Field()]]        = None
    municipio_prestacao  : Optional[Annotated['Municipio', Field()]] = None
    ambiente             : Optional[Annotated[str, Field()]]         = None
    json_objeto_nfse     : Optional[Annotated[str, Field()]]         = None  # TODO: Não consta na documentação da API
    xml                  : Optional[Annotated[str, Field()]]         = None  # TODO: Não consta na documentação da API
    numer_nota           : Optional[Annotated[str, Field()]]         = None  # TODO: EXCLUIR! É um typo de "numero_nota", adicionei hoje (03/07/2023) apenas para o package não parar de funcionar.

    def __str__(self):
        return f'NFSe {self.uuid}'

    def __repr__(self):
        return f'NFSe {self.uuid}'

class PaginaNotasServico(BaseModel):
    total           : Optional[Annotated[str, Field()]]                       = None
    itens_por_pagina: Optional[Annotated[str, Field()]]                       = None
    pagina_atual    : Optional[Annotated[str, Field()]]                       = None
    itens           : Optional[Annotated[List['NotaFiscalServico'], Field()]] = None

class ImpostosServico(Impostos):
    issqn: 'Issqn' = Field()

class Issqn(BaseModel):
    indicador_exigibilidade_iss: IndicadoresExigibilidadeIssEnum = Field()
    indicador_incentivo_fiscal : IndicadoresIncentivoFiscalEnum  = Field()
    item_lista_servicos        : str = Field()
    aliquota                   : str = Field()
    codigo_servico             : str = Field()
    codigo_nbs                 : str = Field()
    cnae                       : str = Field()  # TODO: Obrigatório ?
    codigo_tributacao_municipio: str = Field()  # TODO: Obrigatório ?
    natureza_operacao          : str = Field()  # TODO: Obrigatório ?

    numero_processo            : Optional[Annotated[str, Field()]] = None
    aliquota_retencao          : Optional[Annotated[str, Field()]] = None
    aliquota_irrf              : Optional[Annotated[str, Field()]] = None
    aliquota_csll              : Optional[Annotated[str, Field()]] = None
    aliquota_previdencia_social: Optional[Annotated[str, Field()]] = None

# =====================================================================
@validate_call
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
    validate_tokens(token_empresa, token_secret_empresa)
    
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor
    headers['token-empresa']        = token_empresa
    headers['token-secret-empresa'] = token_secret_empresa

    # -----------------------------------------
    obj_dict = objetoNfse.model_dump(exclude_none=True)

    url = f'{BASE_URL}/nfse'
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=obj_dict)

    # Resultado:
    # TODO: Retornar algo mais útil do que simplesmente o response...
    return response

@validate_call
async def buscar_notas(token_emissor: str,
                 token_secret_emissor: str,
                 cnpjEmpresa:list=None,
                 data_inicio:datetime=None,
                 data_fim:datetime=None,
                 ambiente:AmbientesEnum=None,
                 status:str=None,
                 texto:str=None,
                 pagina:int=None,
                 qtd_por_pagina:int=None,
                 ordencao:str=None,
                 tipo_ordenacao:str=None,
                 *args, **kwargs) -> (httpx.Response, List[NotaFiscalServico],):
    '''Recupera as notas fiscais de serviço.

    Args:
        cnpj (str): CNPJ Empresa (apenas números).

        data_inicio (datetime): Início intervalo de datas (dd/MM/yyyy HH:mm:ss).

        data_fim (datetime): Fim intervalo de datas (dd/MM/yyyy HH:mm:ss).

        ambiente (AmbientesEnum):
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
    # TODO: o endpoint ignora o parâmetro cnpjEmpresa em alguns casos, descobrir quais os casos.
    # TODO: textoBusca é case sensitive e leva em consideração acentos.
    # TODO: dataFim não precisa de dataInicio

    headers = HEADERS.copy()
    
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor

    params = {
        'cnpjEmpresa'  : cnpjEmpresa,
        'dataInicio'   : data_inicio.strftime('%d/%m/%Y %H:%M:%S') if data_inicio else None,
        'dataFim'      : data_fim.strftime('%d/%m/%Y %H:%M:%S') if data_fim else None,
        'ambiente'     : ambiente,
        'status'       : status,
        'textoBusca'   : texto,
        'pagina'       : pagina,
        'qtdPorPagina' : qtd_por_pagina,
        'ordenacao'    : ordencao,
        'tipoOrdenacao': tipo_ordenacao
    }
    params = {k: v for k,v in params.items() if v}

    url = f'{BASE_URL}/nfse'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    match (response.status_code):
        case 200:
            itens = response.json()['dados']['itens']
            nfses = [NotaFiscalServico(**d) for d in itens]
            return (response, nfses)

    return (response, None)

@validate_call
async def retransmitir(token_emissor: str,
                 token_secret_emissor: str,
                 token_empresa:str,
                 token_secret_empresa:str,
                 *args, **kwargs):
    raise NotImplementedError

@validate_call
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

    url = f'{BASE_URL}/nfse/{id_nfse}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    # TODO: Retornar algo mais útil como uma instância de NotaFiscal por exemplo ?!
    return response

@validate_call
async def cancelar(token_emissor: str,
             token_secret_emissor: str,
             token_empresa:str,
             token_secret_empresa:str,
             *args, **kwargs):
    raise NotImplementedError

# =====================================================================
