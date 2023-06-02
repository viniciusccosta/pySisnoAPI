""" 
    Módulo específico para geração de Notas Fiscais de Produto.
    
    Para utilizar esse módulo basta importá-lo da seguinte forma:  
    `from pysisnoapi import nfe`
"""

# =====================================================================
from . import *

from datetime import datetime
import requests

# =====================================================================
CSV_HEADERS = [
    'CNPJ EMITENTE',
    'MODELO',
    'CPF/CNPJ DESTINATÁRIO',
    'NOME/RAZAO SOCIAL DESTINATÁRIO',
    'INDICADOR IE',
    'CONSUMIDOR FINAL',
    'FAZ RETENÇÃO DE IMPOSTOS',
    'CEP',
    'BAIRRO',
    'LOGRADOURO',
    'NUMERO',
    'EMAIL DESTINATÁRIO',
    'OPERAÇÃO',
    'FINALIDADE',
    'PRODUTOS',
    'MEIO PAGAMENTO',
    'INFORMAÇÕES COMPLEMENTARES',
    'SIGLA UF',
    'IBGE MUNICÍPIO',
    'COMPLEMENTO ENDEREÇO'
]

# =====================================================================
class ObjetoEmissaoNFe:
    def __init__(self, *args, **kwargs):
        raise NotImplementedError

class Pagamento:
    def __init__(self, *args):
        self.formas_pagamento        = [f for f in args]                                        # list[FORMAPAGAMENTO]

    def asdict(self):
        return {
            "formas_pagamento": [f.asdict() for f in self.formas_pagamento]
        }

class FormaPagamento:
    def __init__(self, **kwargs):
        self.forma_pagamento         = kwargs.get("forma_pagamento", None)                      # string (0: À Vista, 1: À Prazo)
        self.meio_pagamento          = kwargs.get("meio_pagamento", None)                       # string [01, 02, 03, 04, 05, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 90, 99 ]
        self.valor_pagamento         = kwargs.get("valor_pagamento", None)                      # string ($0.00)

    def asdict(self):
        return self.__dict__

class Produto:
    def __init__(self, tipo, **kwargs):
        self.tipo                   = tipo                                      # TODO: 0: Produto, 1: Serviço

        self.cfop                   = kwargs.get("cfop", None)                  # string
        self.item                   = kwargs.get("item", None)                  # string (Número incremental na lista de produtos)
        self.nome                   = kwargs.get("nome", None)                  # string
        self.ncm                    = kwargs.get("ncm", None)                   # string
        self.quantidade             = kwargs.get("quantidade", None)            # string
        self.unidade                = kwargs.get("unidade", None)               # string (AMPOLA, BALDE, BANDEJ, BARRA, BISNAG, BLOCO, BOBINA, BOMB, CAPS, CART, CENTO, CJ, CM, CM2, CX, CX2, CX3, CX5, CX10, CX15, CX20, CX25, CX50, CX100, DISP, DUZIA, EMBAL, FARDO, FOLHA, FRASCO, GALAO, JOGO, KG, KIT, LATA, LITRO, M, M2, M3, MILHEI, ML, MWH, PACOTE, PALETE, PARES, PC, POTE, K, RESMA, ROLO, SACO, SACOLA, TAMBOR, TANQUE, TON, TUBO, UNID, VASIL, VIDRO)
        self.subtotal               = kwargs.get("subtotal", None)              # string ($0.0000000000) - VALOR UNITÁRIO
        self.total                  = kwargs.get("total", None)                 # string ($0.00) (Quantidade * Valor Unitário)
        self.impostos               = kwargs.get("impostos", None)              # Objeto IMPOSTOS

    def asdict(self):
        return {
            "cfop"          : self.cfop,
            "item"          : self.item,
            "nome"          : self.nome,
            "ncm"           : self.ncm,
            "quantidade"    : self.quantidade,
            "unidade"       : self.unidade,
            "subtotal"      : self.subtotal,
            "total"         : self.total,
            "impostos"      : self.impostos.asdict(),
        }

class Pedido:
    def __init__(self, **kwargs):
        self.presenca                        = kwargs.get("presenca", None)                     # string [ 0, 1, 2, 3, 4, 5, 9 ]
        self.pagamento                       = kwargs.get("pagamento", None)                    # Objeto PAGAMENTO

        self.informacoes_complementares      = kwargs.get("informacoes_complementares", None)   # string
        self.informacoes_fisco               = kwargs.get("informacoes_fisco", None)            # string
        self.observacoes_fisco               = kwargs.get("observacoes_fisco", None)            # list[OBSERVACAO]
        self.observacoes_contribuinte        = kwargs.get("observacoes_contribuinte", None)     # list[OBSERVACAO]

    def asdict(self):
        # TODO: Adicionar o restante dos atributos ao dicionário

        return {
            "presenca"                      : self.presenca,
            "pagamento"                     : self.pagamento.asdict(),
        }

class VeiculoNovo:
    def __init__(self, **kwargs):
        raise NotImplementedError

class ExportacaoIndividual:
    def __init__(self, **kwargs):
        raise NotImplementedError

class ImportacaoInvididual:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Rastreamento:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Fatura:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Exportacao:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Local:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Compra:
    def __init__(self, **kwargs):
        raise NotImplementedError

class InformacaoIntermediador:
    def __init__(self, **kwargs):
        raise NotImplementedError

class PaginaNotas:
    def __init__(self, **kwargs):
        raise NotImplementedError

# =====================================================================
@requires_emissor
@requires_empresa
def emitir(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def corrigir(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def cancelar(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def validar(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
def listar(qtd:str = None, pagina:str = None, *args, **kwargs) -> List[NotaFiscal]:
    """Recupera as notas fiscais.
    
    No Distrito Federal (DF), antes de 01/2023, as notas fiscais de serviço eram emitidas como NFe.

    Args:
        qtd (str, optional): Quantidade de notas por página.
        pagina (str, optional): Página a ser retornada.

    Returns:
        List[NotaFiscal]: Lista contendo as notas fiscais.
    """
    headers = HEADERS.copy()
    params   = {}
    
    if qtd:
        params["qtd"] = qtd
    if pagina:
        params["pagina"] = pagina
    
    url = f'{URL}/nfe/lista-notas'
    response = requests.get(url, params, headers=headers)
    
    match (response.status_code):
        case 200:
            json_data = response.json().get('dados')
            nfes = [NotaFiscal.from_json(**d) for d in json_data['itens']]
            return nfes
        case _:
            return response.text

@requires_emissor
def buscar_notas(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
def get_nota(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def inutilizar_numeracao(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def get_pre_visualizacao(*args, **kwargs):
    raise NotImplementedError

@requires_emissor
@requires_empresa
def get_danfe(*args, **kwargs):
    raise NotImplementedError

# =====================================================================
@requires_emissor
def __emitir_nota_teste(*args, **kwargs):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # TODO: Os impostos, os produtos (e até mesmo os clientes) já deverão estar cadastrados em algum banco de dados

    # Grupos de Impostos:
    pis             = Pis(situacao_tributaria="99")                                                                                                                     #
    cofins          = Cofins(situacao_tributaria="99")                                                                                                                  #
    issqn           = Issqn(indicador_exigibilidade_iss="1", indicador_incentivo_fiscal="1", item_lista_servicos="08.01", aliquota="0.0000")                            # Exigível, Não, 08.01, 0.0000%
    impostos        = Impostos(tipo="1", pis=pis, cofins=cofins, issqn=issqn)                                                                                           # Serviço

    # Produtos e Serviços:
    produto         = Produto(tipo="1", cfop="5933", item="2", nome="MENSALIDADE DE ENSINO REGULAR, PRÉ-ESCOLAR, E FUNDAMENTAL", ncm="00000000", quantidade="1.0000", unidade="UNID", subtotal="1.0000000000", total="1.00", impostos=impostos)  # TODO: O total deveria ser calculado e não informado

    # Destinatários:
    endereco        = Endereco(codigo_pais="55", descricao_pais="Brasil", bairro="Nome do Bairro", logradouro="Rua Ciclano da Silva Júnior", numero="0")                #
    pessoa_fisica   = PessoaFisica(cpf="65386056808", nome_completo="Nome do Cliente")                                                                                  # CPF gerado randomicamente pelo site https://www.geradordecpf.org/
    cliente         = Cliente(pessoa_fisica=pessoa_fisica, consumidor_final="1", contribuinte="9", endereco=endereco)                                                   # Consumidor Final e Não Contribuinte

    # Pedido:
    forma_pagamento = FormaPagamento(forma_pagamento="0", meio_pagamento="01", valor_pagamento="1.00")                                                                  # À vista, dinheiro, R$ 1,00
    pagamento       = Pagamento(forma_pagamento)                                                                                                                        # TODO: Supostamente podemos passar mais de uma forma de pagamento, mas será que ele irá validar o "valor_pagamento" com o total dos produtos/serviços ?
    pedido          = Pedido(presenca="0", pagamento=pagamento)                                                                                                         # Não se aplica

    # Nota Fiscal:
    nota_fiscal     = NotaFiscal(serie="1", operacao="1", natureza_operacao="Prestação de Serviço", modelo="55", finalidade="1", ambiente="2", cliente=cliente, produtos=[produto], pedido=pedido, data_entrada_saida=agora, data_emissao=agora)  # TODO: Como saber qual a série?

# =====================================================================
if __name__ == "__main__":
    __emitir_nota_teste()

# =====================================================================