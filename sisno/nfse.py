# =====================================================================
from .sisno import *

# =====================================================================
HEADER_NFSE = [
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
class ObjetoEmissaoNFSe:
    def __init__(self, cliente, servico, construcao_civil, *args, **kwargs):
        self.cliente            = cliente
        self.servico            = servico
        self.construcao_civil   = construcao_civil
    
class Servico:
    def __init__(self, valor_servicos, discriminacao, impostos, *args, **kwargs):
        self.valor_servicos             = valor_servicos
        self.discriminacao              = discriminacao
        self.impostos                   = impostos
        self.intermediario              = kwargs.get("intermediario", '')
        self.iss_retido                 = kwargs.get("iss_retido", '')
        self.responsavel_retencao_iss   = kwargs.get("responsavel_retencao_iss", '')
        self.deducoes                   = kwargs.get("deducoes", '')
        self.desconto_incondicionado    = kwargs.get("desconto_incondicionado", '')
        self.desconto_condicionado      = kwargs.get("desconto_condicionado", '')
        self.outras_retencoes           = kwargs.get("outras_retencoes", '')
        self.informacoes_complementares = kwargs.get("informacoes_complementares", '')
        self.data_competencia           = kwargs.get("data_competencia", '')
        self.uf_local_prestacao         = kwargs.get("uf_local_prestacao", '')
        self.municipio_local_prestacao  = kwargs.get("municipio_local_prestacao", '')
    
class ConstrucaoCivil:
    def __init__(self, *args, **kwargs):
        # TODO: Até o dia 10/05/2023, não consta na Documentação quais são os campos obrigatórios
        self.codigo_obra = kwargs.get("codigo_obra", '')
        self.art         = kwargs.get("art", '')
    
class NotaFiscalServico:
    def __init__(self, *args, **kwargs):
        # TODO: Até o dia 10/05/2023, não consta na Documentação quais são os campos obrigatórios
        self.id                     = kwargs.get("id", 0)
        self.empresa                = kwargs.get("empresa", None)     #
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
    
class PaginaNotaServico:
    def __init__(self, *args, **kwargs):
        # TODO: Até o dia 10/05/2023, não consta na Documentação quais são os campos obrigatórios
        self.total              = kwargs.get("total", 0)
        self.itens_por_pagina   = kwargs.get("itens_por_pagina", 0)
        self.pagina_atual       = kwargs.get("pagina_atual", 0)
        self.itens              = kwargs.get("art", [])

# =====================================================================
def emitir(*args, **kwargs):
    raise NotImplementedError

def buscar_notas(*args, **kwargs):
    raise NotImplementedError

def retransmitir(*args, **kwargs):
    raise NotImplementedError

def recuperar_dados(*args, **kwargs):
    raise NotImplementedError

def cancelar(*args, **kwargs):
    raise NotImplementedError

# =====================================================================