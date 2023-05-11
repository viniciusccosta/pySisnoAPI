# ======================================================================================================================
import datetime
import json
import requests

# ======================================================================================================================
URL     = "https://homolog.sisno.com.br/nfe-service"                    # TODO: "https://homolog.sisno.com.br/nfe-service/nfe"
HEADERS = {"accept": "application/json",}

# TODO: Não to curtindo isso está aqui solto...
with open('api.keys', 'r', encoding="UTF8") as filekeys:                # TODO: System variables
    api_headers = json.loads(filekeys.read())

HEADERS |= api_headers

# ======================================================================================================================
class Empresa:
    def __init__(self, **kwargs):
        # TODO: Até o dia 10/05/2023, não consta na Documentação quais são os campos obrigatórios

        self.id                                             = kwargs.get("id", 0)
        self.token                                          = kwargs.get("token", '')
        self.token_secret                                   = kwargs.get("token_secret", '')
        self.cnpj                                           = kwargs.get("cnpj", '')
        self.nome_fantasia                                  = kwargs.get("nome_fantasia", '')
        self.razao_social                                   = kwargs.get("razao_social", '')
        self.endereco                                       = kwargs.get("endereco	", None)
        self.telefone                                       = kwargs.get("telefone", '')
        self.inscricao_estadual                             = kwargs.get("inscricao_estadual", '')
        self.inscricao_municipal                            = kwargs.get("inscricao_municipal", '')
        self.inscricao_estadual_substituicao_tributaria     = kwargs.get("inscricao_estadual_substituicao_tributaria", '')
        self.regime_tributario                              = kwargs.get("regime_tributario", '')
        self.classificacao_nacional_atividades_economicas   = kwargs.get("classificacao_nacional_atividades_economicas", '')
        self.ambiente                                       = kwargs.get("ambiente", '')
        self.id_csc                                         = kwargs.get("id_csc", '')
        self.csc                                            = kwargs.get("csc", '')
        self.codigo_regime_especial_tributacao              = kwargs.get("codigo_regime_especial_tributacao", '')
        self.porcentagem_icms_aproveitado                   = kwargs.get("porcentagem_icms_aproveitado", 0)
        self.site                                           = kwargs.get("site", '')
        self.email                                          = kwargs.get("email", '')
    
    def asdict(self):
        return self.__dict__

class Endereco:
    def __init__(self, codigo_pais, descricao_pais, bairro, logradouro, numero, **kwargs):
        self.codigo_pais            = codigo_pais
        self.descricao_pais         = descricao_pais
        self.uf                     = kwargs.get("uf", '')
        self.codigo_municipio       = kwargs.get("codigo_municipio", '')
        self.descricao_municipio    = kwargs.get("descricao_municipio", '')
        self.cep                    = kwargs.get("descricao_municipio", '')
        self.bairro                 = bairro
        self.logradouro             = logradouro
        self.numero                 = numero
        self.complemento            = kwargs.get("numero", '')

    def asdict(self):
        return self.__dict__

class NotaFiscal:
    def __init__(self, **kwargs):
        self.empresa                 = kwargs.get("empresa", None)              # string
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
    def __init__(self, situacao_tributaria, **kwargs):
        """
        :param situacao_tributaria: string [ 00, 01, 02, 03, 04, 05, 49, 50, 51, 52, 53, 54, 55, 99 ]
            01: Operação Tributável com Alíquota Básica
            02: Operação Tributável com Alíquota por Unidade de Medida de Produto
            03: Operação Tributável com Alíquota por Unidade de Medida de Produto
            04: Operação Tributável Monofásica - Revenda a Alíquota Zero
            05: Operação Tributável por Substituição Tributária
            06: Operação Tributável a Alíquota Zero
            07: Operação Isenta da Contribuição
            08: Operação sem Incidência da Contribuição
            09: Operação com Suspensão da Contribuição
            49: Outras Operações de Saída
            50: Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno
            51: Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno
            52: Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação
            53: Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno
            54: Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação
            55: Operação com Direito a Crédito - Vinculada a Receitas Não Tributadas Mercado Interno e de Exportação
            56: Oper. c/ Direito a Créd. Vinculada a Rec. Tributadas e Não-Tributadas Mercado Interno e de Exportação
            60: Crédito Presumido - Oper. de Aquisição Vinculada Exclusivamente a Rec. Tributada no Mercado Interno
            61: Créd. Presumido - Oper. de Aquisição Vinculada Exclusivamente a Rec. Não-Tributada Mercado Interno
            62: Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação
            63: Créd. Presumido - Oper. de Aquisição Vinculada a Rec.Tributadas e Não-Tributadas no Mercado Interno
            64: Créd. Presumido - Oper. de Aquisição Vinculada a Rec. Tributadas no Mercado Interno e de Exportação
            65: Créd. Presumido - Oper. de Aquisição Vinculada a Rec. Não-Tributadas Mercado Interno e Exportação
            66: Créd. Presumido - Oper. de Aquisição Vinculada a Rec. Trib. e Não-Trib. Mercado Interno e Exportação
            67: Crédito Presumido - Outras Operações
            70: Operação de Aquisição sem Direito a Crédito
            71: Operação de Aquisição com Isenção
            72: Operação de Aquisição com Suspensão
            73: Operação de Aquisição a Alíquota Zero
            74: Operação de Aquisição sem Incidência da Contribuição
            75: Operação de Aquisição por Substituição Tributária
            98: Outras Operações de Entrada
            99: Outras Operações
        :param aliquota: string($0.0000)
            Passar percentual quando tributado pela alíquota ou em reais quando tributado por quantidade
        :param aliquota_st	string($0.0000)
        :aliquota_retencao	string($0.0000)
        """
        
        self.situacao_tributaria = situacao_tributaria
        self.aliquota            = kwargs.get("aliquota", None)
        self.aliquota_st         = kwargs.get("aliquota_st", None)
        self.aliquota_retencao   = kwargs.get("aliquota_retencao", None)

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
class Uf:
    # TODO: Até o dia 10/05/2023 essa classe só está sendo usada em classes de NFSe, entretanto, já deixarei ela por aqui mesmo, acredito que em breve as classes de NFe também usarão
    def __init__(self, **kwargs):
        raise NotImplementedError

class Municipio:
    def __init__(self, **kwargs):
        raise NotImplementedError

class Cfop:
    def __init__(self, **kwargs):
        raise NotImplementedError
    
class Ibpt:
    def __init__(self, **kwargs):
        raise NotImplementedError
    
# ----------------------------------------------------------------
class Observacao:
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    
    def __init__(self, **kwargs):
        self.campo                   = kwargs.get("campo", None)                                # string
        self.texto                   = kwargs.get("texto", None)                                # string

    def asdict(self):
        return self.__dict__

class DeclaracaoImportacaoAdicao:
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    def __init__(self, **kwargs):
        raise NotImplementedError

class Transporte:
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    def __init__(self, **kwargs):
        raise NotImplementedError

class RetencaoIcmsTransporte:
    # TODO: Até o dia 10/05/2023 essa classe só está sendo usada na classe "Transporte", que não está sendo usada
    def __init__(self, **kwargs):
        raise NotImplementedError

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
def print_curl(headers, nota_fiscal, *args, **kwargs):
    print(f"curl -X 'POST' {URL}", end=" ")

    for k, v in headers.items():
        print(f"-H '{k}: {v}'", end=" ")

    data = str(nota_fiscal.asdict()).replace("\'", "\"")

    print(f"-d '{data}'")

def main(*args, **kwargs):
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

    with open('api.keys', 'r', encoding="UTF8") as filekeys:        # TODO: System variables
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
