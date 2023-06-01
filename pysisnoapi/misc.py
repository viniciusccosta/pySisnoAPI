""" 
    O módulo misc.py contém funções genéricas que não se enquadram em outros módulos específicos. 
    Um exemplo é a função para realizar uma requisição à API a fim de consultar informações sobre municípios. 
    Este módulo faz parte de um pacote e depende completamente de outros módulos.

    Para utilizar as funções deste módulo, basta importá-lo da seguinte forma:
    "from pysisnoapi import misc"
"""

# ======================================================================================================================
from . import *

import requests
from typing import List

# ======================================================================================================================
@requires_keys
def get_municipios(uf: str, *args, **kwargs) -> List[Municipio]:
    """Envia uma requisição para a API para consultar os municípios de um determinado estado.

    Args:
        uf (str): Sigla do estado.  
            Exemplo: "SP" para São Paulo, "RJ" para Rio de Janeiro, etc.

    Returns:
        List[Municipio]: Lista de objetos Municipio representando os municípios.
    """

    headers  = HEADERS
    url      = f'{URL}/unidades-federativas/{uf}/municipios'
    response = requests.get(url, headers=headers)

    match (response.status_code):
        case 200:
            json_data  = response.json().get('dados')
            municipios = [Municipio(**d) for d in json_data]
            return municipios
        case 412:
            return []
        case _:
            return

@requires_keys
def get_cfops(*args, **kwargs) -> List[Cfop]:
    """Envia uma requisição para a API a fim de obter a lista de todos os CFOPs disponíveis.

    Returns:
        List[Cfop]: Uma lista de objetos Cfop representando os CFOPs.
    """

    headers  = HEADERS
    url      = f'{URL}/cfops'
    response = requests.get(url, headers=headers)

    match (response.status_code):
        case 200:
            json_data = response.json().get('dados')
            cfops     = [Cfop(**d) for d in json_data]
            return cfops
        case 412:
            return []
        case _:
            return

@requires_keys
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

# ======================================================================================================================
