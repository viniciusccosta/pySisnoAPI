'''
    Package criado para integração com a API da plataforma SISNO.

    Para utilizar esse package basta importá-lo da seguinte forma:
    `import pysisnoapi`

    Ou também poderá importar apenas os módulos necessários, como por exemplo:
    `from pysisnoapi import nfe`
'''

# ======================================================================================================================
# Imports:
from typing            import Optional
from typing_extensions import Annotated
from datetime          import datetime
from dateutil          import parser
from pydantic          import BaseModel, Field, model_validator
from enum              import StrEnum

# ======================================================================================================================
# Globals:
BASE_URL = 'https://homolog.arkaonline.com.br/nfe-service'               # TODO: Provisório, em breve voltará para 'https://homolog.sisno.com.br/nfe-service/'
HEADERS  = {
    'accept'      : 'application/json',
    'Content-Type': 'application/json',
}

# -------------------------------------------
AMBIENTES = {
    '1': 'Produção',
    '2': 'Homologação',
}

FORMAS_PAGAMENTO = {
    '0': 'À Vista',
    '1': 'À Prazo',
}

MEIOS_PAGAMENTO = {
    '01': 'Dinheiro',
    '02': 'Cheque',
    '03': 'Cartão de crédito',
    '04': 'Cartão de débito',
    '05': 'Cartão da loja',
    '10': 'Vale alimentação',
    '11': 'Vale refeição',
    '12': 'Vale presente',
    '13': 'Vale combustível',
    '14': 'Duplicata mercantil',
    '15': 'Boleto bancário',
    '16': 'Depósito bancário',
    '17': 'Pagamento Instantaneo (PIX)',
    '18': 'Transferência bancária',
    '19': 'Programa de fidelidade (Cashback)',
    '90': 'Sem pagamento',
    '99': 'Outros',
}

MOTIVOS_DESONERACAO = {
    '1' : 'Táxi',
    '3' : 'Produtor Agropecuário',
    '4' : 'Frotista Locadora',
    '5' : 'Diplomático Consular',
    '6' : 'Utilitários Motocicletas Amazônia Ocidental Áreas Livre Comércio',
    '7' : 'Suframa',
    '8' : 'Venda Órgãos Públicos',
    '9' : 'Outros',
    '10': 'Deficiente Condutor',
    '11': 'Deficiente Não Condutor',
    '12': 'Órgão de Fomento Desenvolvimento Agropecuário',
    '90': 'Solicitado pelo Fisco',
}

SITUACOES_TRIBUTARIAS_ICMS = {
    '00' : 'Tributada integralmente',
    '10' : 'Tributada com cobrança de ICMS por ST',
    '20' : 'Com redução da base de cálculo',
    '30' : 'Isenta ou não tributada com cobrança de ICMS por ST',
    '40' : 'Isenta',
    '41' : 'Não tributada',
    '50' : 'Suspensão',
    '51' : 'Diferimento',
    '60' : 'ICMS cobrado anteriormente por ST',
    '70' : 'Com redução da base de cálculo/Cobrança ICMS por ST/ICMS ST',
    '90' : 'Outros',
    '101': 'Tributada pelo Simples Nacional com permissão de crédito',
    '102': 'Tributada pelo Simples Nacional sem permissão de crédito',
    '103': 'Isenção do ICMS no Simples Nacional para faixa de receita bruta',
    '201': 'Tributada pelo Simples Nacional com permissão de crédito e com cobrança do ICMS por substituição tributária',
    '202': 'Tributada pelo Simples Nacional sem permissão de crédito e com cobrança do ICMS por substituição tributária',
    '203': 'Isenção do ICMS no Simples Nacional para faixa de receita bruta e com cobrança do ICMS por substituição tributária',
    '300': 'Imune',
    '400': 'Não tributada pelo Simples Nacional',
    '500': 'ICMS cobrado anteriormente por substituição tributária (substituído) ou por antecipação',
    '900': 'Outros',
}

SITUACOES_TRIBUTARIAS_IPI = {
    '00': 'Entrada com Recuperação de Crédito',
    '01': 'Entrada Tributada com Alíquota Zero',
    '02': 'Entrada Isenta',
    '03': 'Entrada Não Tributada',
    '04': 'Entrada Imune',
    '05': 'Entrada com Suspensão',
    '49': 'Outras Entradas',
    '50': 'Saída Tributada',
    '51': 'Saída Tributável com Alíquota Zero',
    '52': 'Saída Isenta',
    '53': 'Saída Não Tributada',
    '54': 'Saída Imune',
    '55': 'Saída com Suspensão',
    '99': 'Outras Saídas',
}

SITUACOES_TRIBUTARIAS_PIS_COFINS = {
    '01': 'Operação Tributável com Alíquota Básica',
    '02': 'Operação Tributável com Alíquota por Unidade de Medida de Produto',
    '03': 'Operação Tributável com Alíquota por Unidade de Medida de Produto',
    '04': 'Operação Tributável Monofásica - Revenda a Alíquota Zero',
    '05': 'Operação Tributável por Substituição Tributária',
    '06': 'Operação Tributável a Alíquota Zero',
    '07': 'Operação Isenta da Contribuição',
    '08': 'Operação sem Incidência da Contribuição',
    '09': 'Operação com Suspensão da Contribuição',
    '49': 'Outras Operações de Saída',
    '50': 'Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno',
    '51': 'Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno',
    '52': 'Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação',
    '53': 'Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno',
    '54': 'Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação',
    '55': 'Operação com Direito a Crédito - Vinculada a Receitas Não Tributadas Mercado Interno e de Exportação',
    '56': 'Oper. c/ Direito a Créd. Vinculada a Rec. Tributadas e Não-Tributadas Mercado Interno e de Exportação',
    '60': 'Crédito Presumido - Oper. de Aquisição Vinculada Exclusivamente a Rec. Tributada no Mercado Interno',
    '61': 'Créd. Presumido - Oper. de Aquisição Vinculada Exclusivamente a Rec. Não-Tributada Mercado Interno',
    '62': 'Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação',
    '63': 'Créd. Presumido - Oper. de Aquisição Vinculada a Rec.Tributadas e Não-Tributadas no Mercado Interno',
    '64': 'Créd. Presumido - Oper. de Aquisição Vinculada a Rec. Tributadas no Mercado Interno e de Exportação',
    '65': 'Créd. Presumido - Oper. de Aquisição Vinculada a Rec. Não-Tributadas Mercado Interno e Exportação',
    '66': 'Créd. Presumido - Oper. de Aquisição Vinculada a Rec. Trib. e Não-Trib. Mercado Interno e Exportação',
    '67': 'Crédito Presumido - Outras Operações',
    '70': 'Operação de Aquisição sem Direito a Crédito',
    '71': 'Operação de Aquisição com Isenção',
    '72': 'Operação de Aquisição com Suspensão',
    '73': 'Operação de Aquisição a Alíquota Zero',
    '74': 'Operação de Aquisição sem Incidência da Contribuição',
    '75': 'Operação de Aquisição por Substituição Tributária',
    '98': 'Outras Operações de Entrada',
    '99': 'Outras Operações',
}

TIPOS_CONSUMIDOR_FINAL = {
    '0': 'Não',
    '1': 'Sim',
} # TODO: Sugerir utilização de Boolean

TIPOS_CONTRIBUINTES = {
    '1': 'Contribuinte ICMS',
    '2': 'Contribuinte isento',
    '9': 'Não contribuinte',
}

UNIDADES = {
    'ampola': 'AMPOLA',
    'balde' : 'BALDE',
    'bandej': 'BANDEJ',
    'barra' : 'BARRA',
    'bisnag': 'BISNAG',
    'bloco' : 'BLOCO',
    'bobina': 'BOBINA',
    'bomb'  : 'BOMB',
    'caps'  : 'CAPS',
    'cart'  : 'CART',
    'cento' : 'CENTO',
    'cj'    : 'CJ',
    'cm'    : 'CM',
    'cm2'   : 'CM2',
    'cx'    : 'CX',
    'cx2'   : 'CX2',
    'cx3'   : 'CX3',
    'cx5'   : 'CX5',
    'cx10'  : 'CX10',
    'cx15'  : 'CX15',
    'cx20'  : 'CX20',
    'cx25'  : 'CX25',
    'cx50'  : 'CX50',
    'cx100' : 'CX100',
    'disp'  : 'DISP',
    'duzia' : 'DUZIA',
    'embal' : 'EMBAL',
    'fardo' : 'FARDO',
    'folha' : 'FOLHA',
    'frasco': 'FRASCO',
    'galao' : 'GALAO',
    'jogo'  : 'JOGO',
    'kg'    : 'KG',
    'kit'   : 'KIT',
    'lata'  : 'LATA',
    'litro' : 'LITRO',
    'm'     : 'M',
    'm2'    : 'M2',
    'm3'    : 'M3',
    'milhei': 'MILHEI',
    'ml'    : 'ML',
    'mwh'   : 'MWH',
    'pacote': 'PACOTE',
    'palete': 'PALETE',
    'pares' : 'PARES',
    'pc'    : 'PC',
    'pote'  : 'POTE',
    'k'     : 'K',
    'resma' : 'RESMA',
    'rolo'  : 'ROLO',
    'saco'  : 'SACO',
    'sacola': 'SACOLA',
    'tambor': 'TAMBOR',
    'tanque': 'TANQUE',
    'ton'   : 'TON',
    'tubo'  : 'TUBO',
    'unid'  : 'UNID',
    'vasil' : 'VASIL',
    'vidro' : 'VIDRO'
}

# ======================================================================================================================
AmbientesEnum                       = StrEnum('Ambientes', list(AMBIENTES.keys()), )
FormasPagamentoEnum                 = StrEnum('Formas de Pagamento', list(FORMAS_PAGAMENTO.keys()), )
MeiosPagamentoEnum                  = StrEnum('Meios de Pagamento', list(MEIOS_PAGAMENTO.keys()), )
MotivoDesoneracaoEnum               = StrEnum('Motivos de Desoneração', list(MOTIVOS_DESONERACAO.keys()), )
SituacoesTributariasICMSEnum        = StrEnum('Situações Tributárias ICMS', list(SITUACOES_TRIBUTARIAS_ICMS.keys()), )
SituacoesTributariasIPIEnum         = StrEnum('Situações Tributárias IPI', list(SITUACOES_TRIBUTARIAS_IPI.keys()), )
SituacoesTributariasPISCONFINSEnum  = StrEnum('Situações Tributárias PIS CONFINS', list(SITUACOES_TRIBUTARIAS_PIS_COFINS.keys()), )
ConsumidorFinalEnum                 = StrEnum('Tipo de Consumidor Final', list(TIPOS_CONSUMIDOR_FINAL.keys()), )
ContribuintesEnum                   = StrEnum('Tipos de Contribuintes', list(TIPOS_CONTRIBUINTES.keys()), )
UnidadesEnum                        = StrEnum('Unidades', UNIDADES)

# ======================================================================================================================
# Classes:
class Cfop(BaseModel):
    '''Classe `CFOP` (Código Fiscal de Operações e Prestações)
    '''
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    codigo   : Optional[Annotated[str, Field()]] = None
    descricao: Optional[Annotated[str, Field()]] = None
    aplicacao: Optional[Annotated[str, Field()]] = None

class Cliente(BaseModel):
    '''Classe `Cliente`
    Geralmente é o destinatário da NFe.
    '''
    consumidor_final: ConsumidorFinalEnum = Field()
    contribuinte    : ContribuintesEnum   = Field()
    endereco        : 'Endereco'          = Field()

    pessoa_fisica   : Optional[Annotated['PessoaFisica'  , Field()]] = None
    pessoa_juridica : Optional[Annotated['PessoaJuridica', Field()]] = None

    id              : Optional[Annotated[int, Field()]]  = None
    ie              : Optional[Annotated[str, Field()]]  = None
    telefone        : Optional[Annotated[str, Field()]]  = None
    email           : Optional[Annotated[str, Field()]]  = None
    faz_retencao    : Optional[Annotated[bool, Field()]] = None  # TODO: bool ?

    @model_validator(mode='after')
    def check_tipo_pessoa(self):
        if (self.pessoa_fisica and self.pessoa_juridica):
            raise ValueError('Informe somente um dos campos pessoa_fisica ou pessoa_juridica')
        if not self.pessoa_fisica and not self.pessoa_juridica:
            raise ValueError('Informe um dos campos pessoa_fisica ou pessoa_juridica')
        return self

class Cofins(BaseModel):
    '''Contribuição para Financiamento da Seguridade Social.

    situacao_tributaria:
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

    aliquota (str): $0.0000
        Passar percentual quando tributado pela alíquota ou em reais quando tributado por quantidade

    aliquota_st	(str): $0.0000

    aliquota_retencao (str): $0.0000
    '''
    situacao_tributaria : SituacoesTributariasPISCONFINSEnum = Field()

    aliquota            : Optional[Annotated[str, Field()]] = None
    aliquota_st         : Optional[Annotated[str, Field()]] = None
    aliquota_retencao   : Optional[Annotated[str, Field()]] = None

class DeclaracaoImportacaoAdicao(BaseModel):
    numero_sequencial: Optional[Annotated[str, Field()]] = None
    numero           : Optional[Annotated[str, Field()]] = None
    cod_fabricante   : Optional[Annotated[str, Field()]] = None
    desconto         : Optional[Annotated[str, Field()]] = None
    drawback         : Optional[Annotated[str, Field()]] = None

class Empresa(BaseModel):
    '''
        Classe que irá representar todas as empresas cadastradas da plataforma SISNO.
        Pela documentação do dia 11/05/2023, essa classe basicamente só terá sua utilidade ao consultar notas.
        Em resumo: não há necessidade de se preocupar com os campos, caso não saiba algum deles, pois, eles serão preenchidos automaticamente com aquilo que vier do endpoint.
    '''
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    id                                          : Optional[Annotated[str, Field()]]         = None
    token                                       : Optional[Annotated[str, Field()]]         = None # Necessário para emitir, mas não para consultar
    token_secret                                : Optional[Annotated[str, Field()]]         = None # Necessário para emitir, mas não para consultar
    cnpj                                        : Optional[Annotated[str, Field()]]         = None
    nome_fantasia                               : Optional[Annotated[str, Field()]]         = None
    razao_social                                : Optional[Annotated[str, Field()]]         = None
    endereco                                    : Optional[Annotated['Endereco', Field()]]  = None
    telefone                                    : Optional[Annotated[str, Field()]]         = None
    inscricao_estadual                          : Optional[Annotated[str, Field()]]         = None
    inscricao_municipal                         : Optional[Annotated[str, Field()]]         = None
    inscricao_estadual_substituicao_tributaria  : Optional[Annotated[str, Field()]]         = None
    regime_tributario                           : Optional[Annotated[str, Field()]]         = None
    classificacao_nacional_atividades_economicas: Optional[Annotated[str, Field()]]         = None
    ambiente                                    : Optional[Annotated[str, Field()]]         = None
    id_csc                                      : Optional[Annotated[str, Field()]]         = None
    csc                                         : Optional[Annotated[str, Field()]]         = None
    codigo_regime_especial_tributacao           : Optional[Annotated[str, Field()]]         = None
    porcentagem_icms_aproveitado                : Optional[Annotated[str, Field()]]         = None
    site                                        : Optional[Annotated[str, Field()]]         = None
    email                                       : Optional[Annotated[str, Field()]]         = None
    utiliza_tributos_aproximados                : Optional[Annotated[bool, Field()]]        = None  # TODO: Não consta na documentação da API
    informacoes_complementares                  : Optional[Annotated[str, Field()]]         = None  # TODO: Não consta na documentação da API
    senha_portal_prefeitura                     : Optional[Annotated[str, Field()]]         = None  # TODO: Não consta na documentação da API
    serie_rps                                   : Optional[Annotated[str, Field()]]         = None  # TODO: Não consta na documentação da API
    proximo_numero_rps                          : Optional[Annotated[str, Field()]]         = None  # TODO: Não consta na documentação da API
    proximo_numero_rps_homologacao              : Optional[Annotated[str, Field()]]         = None  # TODO: Não consta na documentação da API
    numero_lote_rps                             : Optional[Annotated[str, Field()]]         = None  # TODO: Não consta na documentação da API

class Endereco(BaseModel):
    '''Classe `Endereço`
    '''

    codigo_pais        : str = Field()
    descricao_pais     : str = Field()
    bairro             : str = Field()
    logradouro         : str = Field()
    numero             : str = Field()

    id                 : Optional[Annotated[int, Field()]] = None   # TODO: Obrigatório ?
    uf                 : Optional[Annotated[str, Field()]] = None
    codigo_municipio   : Optional[Annotated[str, Field()]] = None
    descricao_municipio: Optional[Annotated[str, Field()]] = None
    cep                : Optional[Annotated[str, Field()]] = None
    complemento        : Optional[Annotated[str, Field()]] = None

class Ibpt(BaseModel):
    '''Classe `IBPT` (Impostos sobre Produtos e Serviços)
    '''
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    codigo            : Optional[Annotated[str, Field()]]  = None
    ex                : Optional[Annotated[str, Field()]]  = None
    tipo              : Optional[Annotated[str, Field()]]  = None
    descricao         : Optional[Annotated[str, Field()]]  = None
    nacional_federal  : Optional[Annotated[str, Field()]]  = None
    importados_federal: Optional[Annotated[str, Field()]]  = None
    estadual          : Optional[Annotated[str, Field()]]  = None
    municipal         : Optional[Annotated[str, Field()]]  = None
    vigencia_inicio   : Optional[Annotated[str, Field()]]  = None
    vigencia_fim      : Optional[Annotated[str, Field()]]  = None
    versao            : Optional[Annotated[str, Field()]]  = None
    fonte             : Optional[Annotated[str, Field()]]  = None
    unidade_federativa: Optional[Annotated['Uf', Field()]] = None
    ativo             : Optional[Annotated[str, Field()]]  = None     # TODO: Até o dia 01/06/2023, não consta na Documentação

    @classmethod
    def from_json(cls, **kwargs):
        uf_dict = kwargs.pop('unidade_federativa', {})
        uf = Uf.from_json(**uf_dict)
        return cls(unidade_federativa=uf, **kwargs)

class Icms(BaseModel):
    '''Classe `ICMS` (Imposto sobre Circulação de Mercadorias e Serviços)
    '''
    situacao_tributaria                       : SituacoesTributariasICMSEnum = Field()

    codigo_cfop                               : Optional[Annotated[str, Field()]]  = None
    aliquota_icms                             : Optional[Annotated[str, Field()]]  = None
    percentual_reducao_bc_icms                : Optional[Annotated[str, Field()]]  = None
    aliquota_fcp                              : Optional[Annotated[str, Field()]]  = None
    percentual_reducao_bc_icms_st             : Optional[Annotated[str, Field()]]  = None
    aliquota_aplicavel_calculo_credito        : Optional[Annotated[str, Field()]]  = None
    aliquota_icms_st                          : Optional[Annotated[str, Field()]]  = None
    aliquota_fcp_st                           : Optional[Annotated[str, Field()]]  = None
    percentual_margem_valor_agregado_icms_st  : Optional[Annotated[str, Field()]]  = None
    percentual_diferimento                    : Optional[Annotated[str, Field()]]  = None
    percentual_desonerado                     : Optional[Annotated[str, Field()]]  = None
    motivo_desoneracao                        : Optional[Annotated[MotivoDesoneracaoEnum, Field()]]  = None
    percentual_icms_st_retido                 : Optional[Annotated[str, Field()]]  = None
    utilizar_tabela_aliquotas_interestaduais  : Optional[Annotated[bool, Field()]] = None
    utilizar_aliquota_interestadual_importacao: Optional[Annotated[bool, Field()]] = None

class Impostos(BaseModel):
    '''Classe Base para as Classes de Impostos de Produtos e Serviços.
    '''
    pis                    : 'Pis'    = Field()
    cofins                 : 'Cofins' = Field()
    
    descricao_grupo_imposto: Optional[Annotated[str, Field()]] = None   # TODO: Obrigatório ?

class Ipi(BaseModel):
    '''Classe `IPI` (Imposto Sobre Produtos Industrializados)

    situacao_tributaria:
        00: Entrada com Recuperação de Crédito
        01: Entrada Tributada com Alíquota Zero
        02: Entrada Isenta
        03: Entrada Não Tributada
        04: Entrada Imune
        05: Entrada com Suspensão
        49: Outras Entradas
        50: Saída Tributada
        51: Saída Tributável com Alíquota Zero
        52: Saída Isenta
        53: Saída Não Tributada
        54: Saída Imune
        55: Saída com Suspensão
        99: Outras Saídas
    '''
    situacao_tributaria : SituacoesTributariasIPIEnum = Field()

    aliquota            : Optional[Annotated[str, Field()]] = None
    codigo_enquadramento: Optional[Annotated[str, Field()]] = None
    codigo_selo         : Optional[Annotated[str, Field()]] = None
    qtd_selo            : Optional[Annotated[str, Field()]] = None

class Municipio(BaseModel):
    '''Classe `Município`
    '''
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    codigo_ibge : Optional[Annotated[int, Field()]] = None
    descricao   : Optional[Annotated[str, Field()]] = None

    @classmethod
    def from_json(cls, **kwargs):
        return cls(**kwargs)

class NotaFiscal(BaseModel):
    '''Classe `Nota Fiscal`.

    Até 01/2023 essa classe também era usada para Notas Fiscais de Serviço (NFSe).
    '''
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    id                      : Optional[Annotated[int, Field()]]       = None
    empresa                 : Optional[Annotated['Empresa', Field()]] = None
    tipo                    : Optional[Annotated[str, Field()]]       = None
    serie                   : Optional[Annotated[str, Field()]]       = None
    numero_nota             : Optional[Annotated[str, Field()]]       = None
    chave_acesso            : Optional[Annotated[str, Field()]]       = None
    protocolo               : Optional[Annotated[str, Field()]]       = None
    nome_destinatario       : Optional[Annotated[str, Field()]]       = None
    uf_destinatario         : Optional[Annotated[str, Field()]]       = None
    cpf_cnpj_destinatario   : Optional[Annotated[str, Field()]]       = None
    valor_total             : Optional[Annotated[str, Field()]]       = None
    status                  : Optional[Annotated[str, Field()]]       = None
    motivo                  : Optional[Annotated[str, Field()]]       = None
    data_emissao            : Optional[Annotated[datetime, Field()]]  = None
    data_autorizacao        : Optional[Annotated[datetime, Field()]]  = None
    modelo                  : Optional[Annotated[str, Field()]]       = None
    ambiente                : Optional[Annotated[str, Field()]]       = None
    xml                     : Optional[Annotated[str, Field()]]       = None
    json_objeto_nfe         : Optional[Annotated[str, Field()]]       = None
    tipo_emissao            : Optional[Annotated[str, Field()]]       = None
    numero_lote             : Optional[Annotated[str, Field()]]       = None

    @classmethod
    def from_json(cls, **kwargs):
        empresa_dict = kwargs.pop('empresa', {})
        empresa = Empresa.from_json(**empresa_dict)

        if data_emissao := kwargs.pop('data_emissao', None):
            data_emissao = parser.parse(data_emissao, dayfirst=True)

        if data_autorizacao := kwargs.pop('data_autorizacao', None):
            data_autorizacao = parser.parse(data_autorizacao, dayfirst=True)

        return cls(
            empresa=empresa,
            data_emissao=data_emissao,
            data_autorizacao=data_autorizacao,
            **kwargs
        )

    def __str__(self):
        return f'NFe {self.id}'

    def __repr__(self):
        return f'NFe {self.id}'

class Observacao(BaseModel):
    campo: Optional[Annotated[str, Field()]] = None
    texto: Optional[Annotated[str, Field()]] = None

class PessoaFisica(BaseModel):
    '''Classe `Pessoa Física`

    Deve ser informado apenas um dos campos [cpf, id_estrangeiro]
    '''
    nome_completo: str = Field()

    cpf           : Optional[Annotated[str, Field()]] = None
    id_estrangeiro: Optional[Annotated[str, Field()]] = None

    @model_validator(mode='after')
    def check_documentos(self):
        if self.cpf and self.id_estrangeiro:
            raise ValueError('Informe somente um dos campos: cpf ou id_estrangeiro')
        if not self.cpf and not self.id_estrangeiro:
            raise ValueError('Informe um dos campos: cpf ou id_estrangeiro')
        return self

class PessoaJuridica(BaseModel):
    '''Classe `Pessoa Jurídica`
    '''
    cnpj        : str = Field()
    razao_social: str = Field()

    im          : Optional[Annotated[str, Field()]] = None
    suframa     : Optional[Annotated[str, Field()]] = None

class Pis(BaseModel):
    '''Classe `PIS` (Programas de Integração Social)

    situacao_tributaria (str): Situação Tributária
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

    aliquota (str): $0.0000
        Passar percentual quando tributado pela alíquota ou em reais quando tributado por quantidade

    aliquota_st	(str): $0.0000

    aliquota_retencao (str): $0.0000

    '''
    situacao_tributaria: SituacoesTributariasPISCONFINSEnum = Field()

    aliquota           : Optional[Annotated[str, Field()]] = None
    aliquota_st        : Optional[Annotated[str, Field()]] = None
    aliquota_retencao  : Optional[Annotated[str, Field()]] = None

class RetencaoIcmsTransporte(BaseModel):
    valor_servico                                           : Optional[Annotated[str, Field()]] = None
    valor_icms_retido                                       : Optional[Annotated[str, Field()]] = None
    cfop                                                    : Optional[Annotated[str, Field()]] = None
    codigo_municipio_ocorrencia_fato_gerador_icms_transporte: Optional[Annotated[str, Field()]] = None
    base_calculo_retencao_icms                              : Optional[Annotated[str, Field()]] = None
    aliquota_retencao                                       : Optional[Annotated[str, Field()]] = None

class Transporte(BaseModel):
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    ...

class Uf(BaseModel):
    '''Classe `UF`(Unidade Federativa)

    Returns:
        _type_: _description_
    '''
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    # TODO: Até o dia 01/06/2023 essa classe só está sendo usada em classes de NFSe, entretanto, já deixarei ela por aqui mesmo, acredito que em breve as classes de NFe também usarão
    codigo_ibge: Optional[Annotated[str, Field()]] = None
    sigla      : Optional[Annotated[str, Field()]] = None
    descricao  : Optional[Annotated[str, Field()]] = None

    @classmethod
    def from_json(cls, **kwargs):
        return cls(**kwargs)

# ======================================================================================================================
def validate_tokens(token:str, token_secret:str):
    '''Verifica se os tokens informados pelo usuário estão corretos e válidos.'''

    if not isinstance(token, str) or len(token) < 1:
        raise Exception('Token Empresa inválido')
    if not isinstance(token_secret, str) or len(token_secret) < 1:
        raise Exception('Token Secret Empresa inválido')

    return True

# ======================================================================================================================
