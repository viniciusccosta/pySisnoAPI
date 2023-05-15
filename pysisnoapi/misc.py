""" 
    Módulo genérico para funções que não se encaixam em outros módulos, como por exemplo a função de realizar uma requisição para a API para consultar municípios.
    Esse módulo faz parte de um package e é totalmente dependente de outros módulos.

    Para utilizar esse módulo basta importá-lo da seguinte forma:
    "from pysisnoapi import misc"
"""

# ======================================================================================================================
from . import *

import requests

# ======================================================================================================================
@requires_keys    # TODO: Sendo sincero, até o dia 11/05/2023 não está sendo exigido as API keys para consumir esse endpoint
def get_municipios(uf: str, *args, **kwargs) -> list[dict]:
    """Envia uma requisição para a API para consultar os municípios de um determinado estado.

    Args:
        uf (str): UF do Estado.  
            SP para São Paulo  
            RJ para Rio de Janeiro  
            e etc.

    Returns:
        list[dict]: Lista de dicionários exatamente da forma que a API retornou.
    """
    # TODO: Retonar uma lista de objetos "Municipio"s

    headers  = HEADERS
    url      = f'{URL}/unidades-federativas/{uf}/municipios'
    response = requests.get(url, headers=headers)

    match (response.status_code):
        case 200:
            return response.json().get('dados')
        case 412:
            return []
        case _:
            return

@requires_keys    # TODO: Sendo sincero, até o dia 11/05/2023 não está sendo exigido as API keys para consumir esse endpoint
def get_cfops(*args, **kwargs) -> list[dict]:
    """Envia uma requisição para a API para listar todos os CFOPs.

    Returns:
        list[dict]: Lista de dicionários exatamente da forma que a API retornou.
    """
    # TODO: Retonar uma lista de objetos "Cfop"s

    headers  = HEADERS
    url      = f'{URL}/cfops'
    response = requests.get(url, headers=headers)

    match (response.status_code):
        case 200:
            return response.json().get('dados')
        case 412:
            return []
        case _:
            return

@requires_keys    # TODO: Sendo sincero, até o dia 11/05/2023 não está sendo exigido as API keys para consumir esse endpoint
def get_ibpts(cod_desc: str, uf: str, *args, **kwargs) -> list[dict]:
    """Envia uma requisição para a API para listar todos os IBPTs.

    Args:
        cod_desc (str): Breve descrição do item ou código.
            Mínimo de 4 caracteres.
        
        uf (str): UF do Estado

    Raises:
        Exception: cod_desc menor que 4 caracteres

    Returns:
        list[dict]: Lista de dicionários exatamente da forma que a API retornou.
    """
    # TODO: Retonar uma lista de objetos "Ibpt"s

    if len(cod_desc) < 4:
        raise Exception("Código ou Descrição precisa ter no mínimo 4 caracteres")
    
    headers  = HEADERS
    headers["codigo-ou-descricao"] = cod_desc
    headers["uf"] = uf

    url      = f'{URL}/ibpts'
    response = requests.get(url, headers=headers)

    match (response.status_code):
        case 200:
            return response.json().get('dados')
        case 412:
            return []
        case _:
            return

# ======================================================================================================================
if __name__ == "__main__":
    pass

    # municipios = get_municipios('df')
    # if municipios:
    #     for municipio in municipios:
    #         print(municipio)

    # cfops = get_cfops()
    # if cfops:
    #     for cfop in cfops:
    #         print(cfop)

    # ibpts = get_ibpts("01012100", 'DF')
    # if ibpts:
    #     for ibpt in ibpts:
    #         print(ibpt)

# ======================================================================================================================
