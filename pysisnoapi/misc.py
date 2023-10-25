''' 
    O módulo misc.py contém funções genéricas que não se enquadram em outros módulos.
    
    Um exemplo é a função para realizar uma requisição à API a fim de consultar informações sobre municípios. 
    Este módulo faz parte de um pacote e depende completamente de outros módulos.

    Para utilizar as funções deste módulo, basta importá-lo da seguinte forma:  
    `from pysisnoapi import misc`
'''

# ======================================================================================================================
from . import *

import httpx
from typing import List

# ======================================================================================================================
async def get_municipios(token_emissor: str, 
                   token_secret_emissor: str, 
                   uf: str, 
                   *args, **kwargs) -> List[Municipio]:
    '''Consulta os municípios de um determinado estado através de uma requisição à API.

    Essa função permite consultar os municípios de um estado específico através de uma requisição à API.
    Ela retorna uma lista de objetos Municipio contendo informações sobre cada município.

    Args:
        uf (str): UF do estado para o qual deseja-se consultar os municípios.

    Returns:
        List[Municipio]: Uma lista de objetos Municipio, representando os municípios do estado consultado.
    '''

    headers  = HEADERS.copy()
    
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor
    
    url      = f'{BASE_URL}/unidades-federativas/{uf}/municipios'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    match (response.status_code):
        case 200:
            json_data  = response.json().get('dados')
            municipios = [Municipio(**d) for d in json_data]
            return municipios
        case 412:
            return []
        case _:
            return

async def get_cfops(token_emissor: str, 
              token_secret_emissor: str, 
              *args, **kwargs) -> List[Cfop]:
    '''Obtém a lista de todos os CFOPs disponíveis através de uma requisição à API.

    Essa função permite obter a lista completa de CFOPs (Código Fiscal de Operações e Prestações) disponíveis através de uma requisição à API.

    Returns:
        List[Cfop]: Uma lista de objetos Cfop, representando os CFOPs disponíveis.
    '''

    headers  = HEADERS.copy()
    
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor
    
    url      = f'{BASE_URL}/cfops'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    match (response.status_code):
        case 200:
            json_data = response.json().get('dados')
            cfops     = [Cfop(**d) for d in json_data]
            return cfops
        case 412:
            return []
        case _:
            return

async def get_ibpts(token_emissor: str, 
              token_secret_emissor: str, 
              cod_desc: str, 
              uf: str, 
              *args, **kwargs) -> List[Ibpt]:
    '''
    Obtém os IBPTs através de uma requisição à API.

    Essa função permite obter os dados de IBPTs (Impostos sobre Produtos e Serviços) para um determinado item ou código, em uma determinada UF (Unidade Federativa)
    
    Args:
        cod_desc (str): Breve descrição do item ou código. Deve ter no mínimo 4 caracteres.
        uf (str): UF do estado para o qual deseja-se consultar os IBPTs.

    Raises:
        Exception: Caso o parâmetro cod_desc tenha menos de 4 caracteres.

    Returns:
        List[Ibpt]: Uma lista de objetos Ibpt representando os IBPTs.
    '''

    if len(cod_desc) < 4:
        raise Exception('Código ou Descrição precisa ter no mínimo 4 caracteres')
    
    headers  = HEADERS.copy()
    
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor
    
    headers['codigo-ou-descricao'] = cod_desc
    headers['uf'] = uf

    url      = f'{BASE_URL}/ibpts'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    match (response.status_code):
        case 200:
            json_data = response.json().get('dados')
            ibpts     = [Ibpt.from_json(**d) for d in json_data]
            return ibpts
        case 412:
            return []
        case _:
            return

# ======================================================================================================================
