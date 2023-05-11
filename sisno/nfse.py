# =====================================================================
from sisno import *

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
class Servico:
    def __init__(self, valor_servicos, discriminacao, impostos, *args, **kwargs):
        self.valor_servicos             = valor_servicos
        self.discriminacao              = discriminacao
        self.impostos                   = impostos                                      # Objeto "Imposto"
        self.intermediario              = kwargs.get("intermediario", None)             # Objeto "Cliente"
        self.iss_retido                 = kwargs.get("iss_retido", '')
        self.responsavel_retencao_iss   = kwargs.get("responsavel_retencao_iss", '')
        self.deducoes                   = kwargs.get("deducoes", '')
        self.desconto_incondicionado    = kwargs.get("desconto_incondicionado", '')
        self.desconto_condicionado      = kwargs.get("desconto_condicionado", '')
        self.outras_retencoes           = kwargs.get("outras_retencoes", '')
        self.informacoes_complementares = kwargs.get("informacoes_complementares", '')
        self.data_competencia           = kwargs.get("data_competencia", '')
        self.uf_local_prestacao         = kwargs.get("uf_local_prestacao", '')          # Objeto "Uf"
        self.municipio_local_prestacao  = kwargs.get("municipio_local_prestacao", '')   # Objeto "Municipio"
    
class ConstrucaoCivil:
    def __init__(self, *args, **kwargs):
        # TODO: Até o dia 10/05/2023, não consta na Documentação quais são os campos obrigatórios
        self.codigo_obra = kwargs.get("codigo_obra", '')
        self.art         = kwargs.get("art", '')

class ObjetoEmissaoNFSe:
    def __init__(self, cliente:Cliente, servico:Servico, *args, **kwargs):
        self.cliente            = cliente
        self.servico            = servico
        self.construcao_civil   = kwargs.get("construcao_civil", None)                  # Objeto "ConstrucaoCivil"

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
def __emitir_nota_teste(*args, **kwargs):
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
    objeto_emissao = ObjetoEmissaoNFSe(cliente=cliente, servico=servico)
    print(objeto_emissao)

    # --------------------------------------------


# =====================================================================
if __name__ == "__main__":
    __emitir_nota_teste()

# =====================================================================