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
class Servico:
    def __init__(self, valor_servicos, discriminacao, impostos, *args, **kwargs):
        """
        Construtor da classe Serviço.

        Args:
            valor_servicos (str): Valor do Serviço no formato $0.00
            
            discriminacao (str): Descrição do Serviço
            
            impostos (Imposto): Instância da classe "Imposto"
            
            **intermediario (Cliente): Intermediário do Serviço
            
            **iss_retido (int):  
                1. Sim  
                2. Não
                
            **responsavel_retencao_iss (int):  
                1. Tomador  
                2. Intermediário
                
            **deducoes (str): Soma total das deduções/descontos gerais
            
            **desconto_incondicionado (str): Soma total dos descontos incondicionados
            
            **desconto_condicionado (str): Soma total dos descontos condicionados
            
            **outras_retencoes (str): Soma total de outras retenções
            
            **informacoes_complementares (str): Informações complementares
            
            **data_competencia (str): Data da competência do serviço
            
            **uf_local_prestacao (Uf): UF do local da prestação do serviço
            
            **municipio_local_prestacao (Municipio): Município do local da prestação do serviço
        """
        self.valor_servicos             = valor_servicos
        self.discriminacao              = discriminacao
        self.impostos                   = impostos                                      # Objeto "Imposto"
        self.intermediario              = kwargs.get("intermediario", None)             # Objeto "Cliente"
        self.iss_retido                 = kwargs.get("iss_retido", 2)                   # 1: Sim, 2: Não                # TODO: Campo obrigatório ?
        self.responsavel_retencao_iss   = kwargs.get("responsavel_retencao_iss", 1)     # 1: Tomador, 2: Intermediário  # TODO: Campo obrigatório ?
        self.deducoes                   = kwargs.get("deducoes", '')                    # TODO: $0.00
        self.desconto_incondicionado    = kwargs.get("desconto_incondicionado", '')     # TODO: $0.00
        self.desconto_condicionado      = kwargs.get("desconto_condicionado", '')       # TODO: $0.00
        self.outras_retencoes           = kwargs.get("outras_retencoes", '')            # TODO: $0.00
        self.informacoes_complementares = kwargs.get("informacoes_complementares", '')  # 
        self.data_competencia           = kwargs.get("data_competencia", '')            # TODO: $dd/MM/yyyy HH:mm:ss.SSS = datetime.now().strftime("%d/%m/%Y %H:%m:%s.%f") ? # TODO: Campo obrigatório ?
        self.uf_local_prestacao         = kwargs.get("uf_local_prestacao", '')          # Objeto "Uf"
        self.municipio_local_prestacao  = kwargs.get("municipio_local_prestacao", '')   # Objeto "Municipio"
    
    def asdict(self,):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None
    
class ConstrucaoCivil:
    def __init__(self, *args, **kwargs):
        # TODO: Até o dia 10/05/2023, não consta na Documentação quais são os campos obrigatórios
        self.codigo_obra = kwargs.get("codigo_obra", '')
        self.art         = kwargs.get("art", '')

    def asdict(self,):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class ObjetoEmissaoNFSe:
    def __init__(self, cliente:Cliente, servico:Servico, *args, **kwargs):
        self.cliente            = cliente
        self.servico            = servico
        self.construcao_civil   = kwargs.get("construcao_civil", None)                  # Objeto "ConstrucaoCivil"

    def asdict(self,):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

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
    
    @classmethod
    def from_json(cls, **kwargs):
        empresa_dict = kwargs.pop('empresa', {})
        empresa = Empresa.from_json(**empresa_dict)
        
        uf_dict = kwargs.pop('uf_prestacao', {})
        uf      = Uf.from_json(**uf_dict)
        
        municipio_dict = kwargs.pop('municipio_prestacao', {})
        municipio = Municipio.from_json(**municipio_dict)
        
        return cls(empresa=empresa, uf_prestacao=uf, municipio_prestacao=municipio, **kwargs)
        
class PaginaNotaServico:
    def __init__(self, *args, **kwargs):
        # TODO: Até o dia 10/05/2023, não consta na Documentação quais são os campos obrigatórios
        self.total              = kwargs.get("total", 0)
        self.itens_por_pagina   = kwargs.get("itens_por_pagina", 0)
        self.pagina_atual       = kwargs.get("pagina_atual", 0)
        self.itens              = kwargs.get("art", [])
    
    def asdict(self,):
        return self.__dict__

# =====================================================================
@requires_emissor
@requires_empresa
def emitir(obj_emissao_nfse: ObjetoEmissaoNFSe, *args, **kwargs):
    """Método responsável por enviar uma requisição para a plataforma SISNO solicitando a emissão de uma nova fiscal de SERVIÇO.
    
    Args:
        obj_emissao_nfse (ObjetoEmissaoNFSe): Objeto da classe "ObjetoEmissaoNFSe" que contém todos os dados necessários

    Returns:
        dict: Dicionário com os dados da requisição
        str: Com o response.text em caso de falha da requisição
    """

    json_obj = json.dumps(obj_emissao_nfse, default=lambda o: o.asdict())
    
    headers = HEADERS.copy()
    url     = f'{URL}/nfse'
    response = requests.post(url, data=json_obj, headers=headers)

    match (response.status_code):
        case 200:
            return response.json().get('dados')
        case _:
            return response.text

@requires_emissor
def buscar_notas(cnpj:str=None, data_inicio:datetime=None, data_fim:datetime=None, ambiente:str=None, status:str=None, texto:str=None, pagina:str=None, qtd_por_pagina:str=None, ordencao:str=None, tipo_ordenacao:str=None, *args, **kwargs) -> List[NotaFiscalServico]:
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

    url = f'{URL}/nfse'
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
    url      = f'{URL}/nfse/{id_nfse}'
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
