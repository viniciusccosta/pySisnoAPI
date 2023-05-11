# ======================================================================================================================
from . import *

import requests

# ======================================================================================================================
def get_municipios(uf: str, *args, **kwargs) -> list[dict]:
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

def get_cfops(*args, **kwargs) -> list[dict]:
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

def get_ibpts(cod_desc: str, uf: str, *args, **kwargs) -> list[dict]:
    # TODO: Retonar uma lista de objetos "Ibpt"s

    if len(cod_desc) < 4:
        raise ValueError("Código ou Descrição precisa ter no mínimo 4 caracteres")
    
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
