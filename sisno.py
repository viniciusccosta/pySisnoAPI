# ======================================================================================================================
import datetime
import json
import requests

# ======================================================================================================================
URL = "https://homolog.sisno.com.br/nfe-service/nfe/validacao-nota"     # TODO: "https://homolog.sisno.com.br/nfe-service/nfe"
HEADER_NFE = [
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

# ======================================================================================================================
class NotaFiscal:
    def __init__(self, **kwargs):
        self.serie                   = kwargs.get("serie", None)                # string
        self.operacao                = kwargs.get("operacao", None)             # string (0: Entrada, 1: Saída)
        self.natureza_operacao       = kwargs.get("natureza_operacao", None)    # string
        self.modelo                  = kwargs.get("modelo", None)               # string (55: NF-e, 65: NFC-e)
        self.finalidade              = kwargs.get("finalidade", None)           # string (1: Normal, 2: Complementar, 3: Ajuste, 4: Devolução ou Retorno)
        self.ambiente                = kwargs.get("ambiente", None)             # string (1: Produção, 2: Homologação)
        self.cliente                 = kwargs.get("cliente", None)              # Objeto CLIENTE
        self.produtos                = kwargs.get("produtos", None)             # list[PRODUTO]
        self.pedido                  = kwargs.get("pedido", None)               # Objeto PEDIDO
        self.data_entrada_saida      = kwargs.get("data_entrada_saida", None)   # string (dd/MM/yyyy HH:mm:ss)
        self.data_emissao            = kwargs.get("data_emissao", None)         # string (dd/MM/yyyy HH:mm:ss)

    def asdict(self):
        return {
            "serie"             : self.serie,
            "operacao"          : self.operacao,
            "natureza_operacao" : self.natureza_operacao,
            "modelo"            : self.modelo,
            "finalidade"        : self.finalidade,
            "ambiente"          : self.ambiente,
            "cliente"           : self.cliente.asdict(),
            "produtos"          : [p.asdict() for p in self.produtos],
            "pedido"            : self.pedido.asdict(),
            "data_entrada_saida": self.data_entrada_saida,
            "data_emissao"      : self.data_emissao,
        }

class Cliente:
    def __init__(self, **kwargs):
        # Deve ser informado apenas um dos campos [pessoa_fisica, pessoa_juridica]

        self.pessoa_fisica           = kwargs.get("pessoa_fisica", None)        # Objeto PESSOAFISICA
        self.pessoa_juridica         = kwargs.get("pessoa_juridica", None)      # Objeto PESSOAJURIDICA

        self.consumidor_final        = kwargs.get("consumidor_final", None)     # string (0: Não, 1: Sim)
        self.contribuinte            = kwargs.get("contribuinte", None)         # string (1: Contribuinte ICMS, 2: Contribuinte isento, 9: Não contribuinte)
        self.endereco                = kwargs.get("endereco", None)             # Objeto ENDERECO

    def asdict(self):
        # TODO: Deve ser informado apenas um dos campos [pessoa_fisica, pessoa_juridica]

        if self.pessoa_juridica:
            return {
                "pessoa_juridica"   : self.pessoa_juridica.asdict(),
                "consumidor_final"  : self.consumidor_final,
                "contribuinte"      : self.contribuinte,
                "endereco"          : self.endereco.asdict(),
            }
        else:
            return {
                "pessoa_fisica"     : self.pessoa_fisica.asdict(),
                "consumidor_final"  : self.consumidor_final,
                "contribuinte"      : self.contribuinte,
                "endereco"          : self.endereco.asdict(),
            }

class PessoaFisica:
    def __init__(self, **kwargs):
        # Deve ser informado apenas um dos campos [cpf, id_estrangeiro]

        self.cpf                     = kwargs.get("cpf", None)                  # string
        self.id_estrangeiro          = kwargs.get("id_estrangeiro", None)       # string
        self.nome_completo           = kwargs.get("nome_completo", None)        # string

    def asdict(self):
        # TODO: Deve ser informado apenas um dos campos [cpf, id_estrangeiro]

        if self.id_estrangeiro:
            return {
                "id_estrangeiro"    : self.id_estrangeiro,
                "nome_completo"     : self.nome_completo,
            }
        else:
            return {
                "cpf"               : self.cpf,
                "nome_completo"     : self.nome_completo,
            }

class PessoaJuridica:
    def __init__(self, **kwargs):
        self.cnpj                    = kwargs.get("cnpj", None)                 # string
        self.razao_social            = kwargs.get("razao_social", None)         # string

    def asdict(self):
        return self.__dict__

class Endereco:
    def __init__(self, **kwargs):
        self.codigo_pais             = kwargs.get("codigo_pais", None)          # string - Código IBGE
        self.descricao_pais          = kwargs.get("descricao_pais", None)       # string
        self.bairro                  = kwargs.get("bairro", None)               # string
        self.logradouro              = kwargs.get("logradouro", None)           # string
        self.numero                  = kwargs.get("numero", None)               # string

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

# ----------------------------------------------------------------
class Impostos:
    def __init__(self, tipo, **kwargs):
        # Quando produto, não informar o campo issqn. Quando serviço, não informar os campos icms e ipi.
        self.tipo                    = tipo

        self.icms                    = kwargs.get("icms", None)                 # Objeto ICMS
        self.ipi                     = kwargs.get("ipi", None)                  # Objeto IPI
        self.pis                     = kwargs.get("pis", None)                  # Objeto PIS
        self.cofins                  = kwargs.get("cofins", None)               # Objeto COFINS
        self.issqn                   = kwargs.get("issqn", None)                # Objeto ISSQN

    def asdict(self):
        # TODO: 0: Produto, 1: Serviço

        if self.tipo == "0":
            return {
                "icms"  : self.icms.asdict(),
                "ipi"   : self.ipi.asdict(),
                "pis"   : self.pis.asdict(),
                "cofins": self.cofins.asdict(),
            }
        elif self.tipo == "1":
            return {
                "pis"   : self.pis.asdict(),
                "cofins": self.cofins.asdict(),
                "issqn" : self.issqn.asdict(),
            }

class Icms:
    def __init__(self, **kwargs):
        self.situacao_tributaria     = kwargs.get("situacao_tributaria", None)  # string [ 00, 10, 20, 30, 40, 41, 50, 51, 60, 70, 90, 101, 102, 103, 201, 202, 203, 300, 400, 500, 900 ]

    def asdict(self):
        return self.__dict__

class Ipi:
    def __init__(self, **kwargs):
        self.situacao_tributaria     = kwargs.get("situacao_tributaria", None)  # string [ 00, 01, 02, 03, 04, 05, 49, 50, 51, 52, 53, 54, 55, 99 ]

    def asdict(self):
        return self.__dict__

class Pis:
    def __init__(self, **kwargs):
        self.situacao_tributaria     = kwargs.get("situacao_tributaria", None)  # string [ 01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 98, 99 ]

    def asdict(self):
        return self.__dict__

class Cofins:
    def __init__(self, **kwargs):
        self.situacao_tributaria     = kwargs.get("situacao_tributaria", None)  # string [ 01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 98, 99 ]

    def asdict(self):
        return self.__dict__

class Issqn:
    def __init__(self, **kwargs):
        """
            Indicador_exigibilidade_iss
                1: Exigível
                2: Não incidência
                3: Isenção
                4: Exportação
                5: Imunidade
                6: Exigibilidade suspensa por decisão judicial
                7: Exigibilidade suspensa por processo administrativo
        """

        self.indicador_exigibilidade_iss     = kwargs.get("indicador_exigibilidade_iss", None)   # string [ 1, 2, 3, 4, 5, 6, 7 ]
        self.indicador_incentivo_fiscal      = kwargs.get("indicador_incentivo_fiscal", None)    # string (1: Não, 2: Sim)
        self.item_lista_servicos             = kwargs.get("item_lista_servicos", None)           # string - Item da lista de serviços no Padrão ABRASF (Formato NN.NN)
        self.aliquota                        = kwargs.get("aliquota", None)                      # string ($0.0000)

    def asdict(self):
        return self.__dict__

# ----------------------------------------------------------------

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

class Observacao:
    def __init__(self, **kwargs):
        self.campo                   = kwargs.get("campo", None)                                # string
        self.texto                   = kwargs.get("texto", None)                                # string

    def asdict(self):
        return self.__dict__

# ======================================================================================================================
def print_curl(headers, nota_fiscal):
    print(f"curl -X 'POST' {URL}", end=" ")

    for k, v in headers.items():
        print(f"-H '{k}: {v}'", end=" ")

    data = str(nota_fiscal.asdict()).replace("\'", "\"")

    print(f"-d '{data}'")

def main():
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

    with open('api.keys', 'r', encoding="UTF8") as filekeys:
        headers                 = json.loads(filekeys.read())

        headers["tipo-emissao"] = "1"
        headers["accept"]       = "application/json"
        headers["Content-Type"] = "application/json"

        print_curl(headers, nota_fiscal)

        response = requests.post(URL, headers=headers, json=nota_fiscal.asdict())
        print("Status Code", response.status_code)
        print("JSON Response ", response.json())

# ======================================================================================================================
if __name__ == "__main__":
    main()

# ======================================================================================================================
