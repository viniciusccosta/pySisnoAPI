""" 
    Módulo específico para geração de Notas Fiscais de Serviço através da API da plataforma SISNO.
    Esse módulo faz parte de um package e é totalmente dependente de outros módulos.

    Para utilizar esse módulo basta importá-lo da seguinte forma:
    "from pysisnoapi import nfse"
"""
# =====================================================================
from . import *

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

        Keyword Args:
            intermediario (Cliente): Intermediário do Serviço
                Default: None
            iss_retido (int): 1-Sim, 2-Não
                Default: 2
            responsavel_retencao_iss (int): 1-Tomador, 2-Intermediário
                Default: 1
            deducoes (str): Soma total das deduções/descontos gerais
                Default: ''
            desconto_incondicionado (str): Soma total dos descontos incondicionados
                Default: ''
            desconto_condicionado (str): Soma total dos descontos condicionados
                Default: ''
            outras_retencoes (str): Soma total de outras retenções
                Default: ''
            informacoes_complementares (str): Informações complementares
                Default: '' 
            data_competencia (str): Data da competência do serviço
                Default: datetime.now()
            uf_local_prestacao (Uf): UF do local da prestação do serviço
                Default: ''
            municipio_local_prestacao (Municipio): Município do local da prestação do serviço
                Default: ''
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

class NotaFiscalServico:
    def __init__(self, *args, **kwargs):
        # TODO: Até o dia 10/05/2023, não consta na Documentação quais são os campos obrigatórios
        self.id                     = kwargs.get("id", 0)
        self.empresa                = kwargs.get("empresa", None)
        self.uuid                   = kwargs.get("uuid", '')
        self.modelo                 = kwargs.get("modelo", '')
        self.status                 = kwargs.get("status", '')
        self.motivo                 = kwargs.get("motivo", '')
        self.numero_nota            = kwargs.get("numero_nota", '')
        self.codigo_verificacao     = kwargs.get("codigo_verificacao", '')
        self.protocolo              = kwargs.get("protocolo", '')
        self.nome_destinatario      = kwargs.get("nome_destinatario", '')
        self.uf_destinatario        = kwargs.get("uf_destinatario", '')
        self.cpf_cnpj_destinatario  = kwargs.get("cpf_cnpj_destinatario", '')
        self.valor_total            = kwargs.get("valor_total", '')
        self.data_emissao           = kwargs.get("data_emissao", '')
        self.data_competencia       = kwargs.get("data_competencia", '')
        self.uf_prestacao           = kwargs.get("uf_prestacao", None)
        self.municipio_prestacao    = kwargs.get("municipio_prestacao", None)
        self.ambiente               = kwargs.get("ambiente", '')
    
    def asdict(self,):
        return self.__dict__
    
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
@requires_keys
def emitir(obj_emissao_nfse: ObjetoEmissaoNFSe, *args, **kwargs):
    """Método responsável por enviar uma requisição para a plataforma SISNO solicitando a emissão de uma nova fiscal de SERVIÇO.

    Atenção:
        Esse método é diretamente vinculado as chaves de API.
        Isso quer dizer que é através das chaves que a plataforma da SISNO irá decidir quem será o emissor dessa nota.
        Para alterar o emissor, basta chamar a função "sisno.alterar_emissor()" e passar as novas chaves.

    Args:
        obj_emissao_nfse (ObjetoEmissaoNFSe): Objeto da classe "ObjetoEmissaoNFSe" que contém todos os dados necessários

    Returns:
        dict: Dicionário com os dados da requisição
        str: Com o response.text em caso de falha da requisição
    """

    json_obj = json.dumps(obj_emissao_nfse, default=lambda o: o.asdict())
    
    headers = HEADERS
    url     = f'{URL}/nfse'
    response = requests.post(url, data=json_obj, headers=headers)

    match (response.status_code):
        case 200:
            return response.json().get('dados')
        case _:
            return response.text

@requires_keys
def buscar_notas(*args, **kwargs):
    raise NotImplementedError

@requires_keys
def retransmitir(*args, **kwargs):
    raise NotImplementedError

@requires_keys
def recuperar_dados(id_nfse:int, *args, **kwargs):
    # TODO: Cada NFSe possui um ID mesmo que de empresas diferentes ?
    # TODO: Essa função deveria estar atrelada as chaves de API, uma vez que será através delas que emitiremos as notas por uma empresa ou por outra ?

    if not isinstance(id_nfse, int):
        raise ValueError("Necessário informar um ID de NFSe válido.")
    
    headers  = HEADERS
    url      = f'{URL}/nfse/{id_nfse}'
    response = requests.get(url, headers=headers)

    match (response.status_code):
        case 200:
            return response.json().get('dados')
        case 412:
            return []
        case _:
            return

@requires_keys
def cancelar(*args, **kwargs):
    raise NotImplementedError

# =====================================================================
def __emitir_nota_teste(*args, **kwargs):
    # TODO: Enviar para módulo de testes

    # TODO: Os impostos, os produtos (e até mesmo os clientes) já deverão estar cadastrados em algum banco de dados
    
    # --------------------------------------------
    # Cliente:
    endereco        = Endereco(codigo_pais='55', descricao_pais='Brasil', bairro='Brasilia', logradouro='Praça dos 3 poderes', numero='123', )
    pessoa_fisica   = PessoaFisica(cpf="00000000000", nome_completo="João da Silva Júnior")
    cliente         = Cliente(pessoa_fisica=pessoa_fisica, consumidor_final='0', contribuinte='9', endereco=endereco)

    # --------------------------------------------
    # Serviço:
    pis             = Pis(situacao_tributaria="99")                                                                                                                     #
    cofins          = Cofins(situacao_tributaria="99")                                                                                                                  #
    issqn           = Issqn(indicador_exigibilidade_iss="1", indicador_incentivo_fiscal="1", item_lista_servicos="08.01", aliquota="0.0000")                            # Exigível, Não, 08.01, 0.0000%
    impostos        = Impostos(tipo="1", pis=pis, cofins=cofins, issqn=issqn)                                                                                           # Serviço

    uf              = Uf(codigo_ibge=53, sigla='DF', descricao='Distrito Federal')
    municipio       = Municipio(codigo_ibge=5300108, descricao='Brasilia')

    servico         = Servico(valor_servicos="1.00", discriminacao="Teste", impostos=impostos, uf_local_prestacao=uf, municipio_local_prestacao=municipio)

    # --------------------------------------------
    # Construção Civil:

    # --------------------------------------------
    # Objeto Emissão NFSe:
    obj_emissao_nfse = ObjetoEmissaoNFSe(cliente=cliente, servico=servico)
    
    return emitir(obj_emissao_nfse=obj_emissao_nfse)

# =====================================================================
