'''
    Módulo específico para geração de Notas Fiscais de Produto.

    Para utilizar esse módulo basta importá-lo da seguinte forma:
    `from pysisnoapi import nfe`
'''

# =====================================================================
import httpx
import json

from pydantic import BaseModel
from typing   import List
from datetime import datetime

from . import *
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

BANDEIRAS = {
    '01': 'Visa / Visa Electron',
    '02': 'Mastercard / Maestro',
    '03': 'American Express',
    '04': 'Sorocred',
    '05': 'Diners Club',
    '06': 'Elo',
    '07': 'Hipercard',
    '08': 'Aura',
    '09': 'Cabal',
    '99': 'Outros',
}

CONDICOES_CHASSI = {
    'N': 'Normal',
    'R': 'Remarcado',
}

CONDICOES_VEICULO = {
    '1': 'Acabado',
    '2': 'Inacabado',
    '3': 'Semi-acabado',
}

CORES = {
    '01': 'Amarela',
    '02': 'Azul',
    '03': 'Bege',
    '04': 'Branca',
    '05': 'Cinza',
    '06': 'Dourada',
    '07': 'Grená',
    '08': 'Laranja',
    '09': 'Marrom',
    '10': 'Prata',
    '11': 'Preta',
    '12': 'Rosa',
    '13': 'Roxa',
    '14': 'Verde',
    '15': 'Vermelha',
    '16': 'Fantasia',
}

ESPECIES_VEICULO = {
    '1': 'Passageiro',
    '2': 'Carga',
    '3': 'Misto',
    '4': 'Corrida',
    '5': 'Tração',
    '6': 'Especial',
    '7': 'Coleção',
}

FINALIDADES = {
    '1': 'Normal',
    '2': 'Complementar',
    '3': 'Ajuste',
    '4': 'Devolução ou Retorno',
}

INDICATIVOS_ESCALA = {
    'S': 'Produzido em escala relevante',
    'N': 'Produzido em escala não relevante',
} # TODO: Sugerir utilização de Boolean.

MODALIDADES_FRETE = {
    '9': 'Sem ocorrência de transporte',
    '0': 'Contratação do frete por conta do remetente (CIF)',
    '1': 'Contratação do frete por conta do destinatário (FOB)',
    '2': 'Contratação do frete por conta de terceiros',
    '3': 'Transporte próprio por conta do remetente',
    '4': 'Transporte próprio por conta do destinatário',
}

MODELOS = {
    '55': 'NF-e',
    '65': 'NFC-e',
}

OPERACOES = {
    '0': 'Entrada',
    '1': 'Saída',
}

ORIGENS = {
    '0': 'Nacional',
    '1': 'Estrangeira importação direta',
    '2': 'Estrangeira adquirida mercado interno',
    '3': 'Nacional mercadoria ou bem conteúdo importação superior 40 P',
    '4': 'Nacional produção em conformidade com processos produtivos básicos',
    '5': 'Nacional mercadoria ou bem conteúdo importação inferior 40 P',
    '6': 'Estrangeira importação direta sem similar nacional constante em lista Camex',
    '7': 'Estrangeira adquirida mercado interno sem similar nacional constante em lista Camex',
    '8': 'Nacional mercadoria ou bem conteúdo importação superior 70 P',
}

PRESENCAS = {
    '0': 'Não se aplica',
    '1': 'Operação presencial',
    '2': 'Operação não presencial - Internet',
    '3': 'Operação não presencial - Teleatendimento',
    '4': 'NFC-e em operação com entrega a domicílio',
    '5': 'Operação presencial fora do estabelecimento',
    '9': 'Operação não presencial - Outros',
}

RESTRICOES = {
    '0': 'Não Há',
    '1': 'Alienação Fiduciária',
    '2': 'Arrendamento Mercantil',
    '3': 'Reserva Domínio',
    '4': 'Penhor',
    '9': 'Outras',
}

TIPOS_COMBUSTIVEL = {
    '01': 'Álcool',
    '02': 'Gasolina',
    '03': 'Diesel',
    '04': 'Gasogênio',
    '05': 'Gás Metano',
    '06': 'Elétrico (Fonte Interna)',
    '07': 'Elétrico (Fonte Externa)',
    '08': 'Gasol./Gás Natural/Combustível',
    '09': 'Álcool/Gás Natural',
    '10': 'Diesel/Gás Natural',
    '11': 'Vide Campo Observação',
    '12': 'Álcool/Gás Natural Veicular',
    '13': 'Gasolina/Gás Natural Veicular',
    '14': 'Diesel/Gás Natural Veicular',
    '15': 'Gás Natural Veicular',
    '16': 'Álcool/Gasolina',
    '17': 'Gasolina/Álcool/Gás natural',
    '18': 'Gasolina/Elétrico',
}

TIPOS_EMISSAO = {
    '1': 'Normal',
    '6': 'Contigência SNC-AN',
    '7': 'Contigência SVC-R',
}

TIPOS_OPERACAO = {
    '0': 'Outros',
    '1': 'Venda concessionária',
    '2': 'Faturamento direto consumidor final',
    '3': 'Venda direta grandes consumidores',
}

TIPOS_VEICULO = {
    '06': 'Automóvel',
    '14': 'Caminhão',
    '13': 'Caminhoneta',
    '24': 'Carga',
    '02': 'Ciclomotor',
    '22': 'Especial Ônibus',
    '07': 'Microônibus',
    '23': 'Misto',
    '04': 'Motociclo',
    '03': 'Motoneta',
    '08': 'Ônibus',
    '10': 'Reboque',
    '05': 'Triciclo',
    '17': 'Trator',
}

# =====================================================================
class ObjetoEmissaoNFe(BaseModel):
    numero_nota_sequencial  : str             = Field()
    serie                   : str             = Field()
    operacao                : str             = Field()
    natureza_operacao       : str             = Field()
    modelo                  : str             = Field()
    finalidade              : str             = Field()
    ambiente                : str             = Field()
    cliente                 : Cliente         = Field()
    produtos                : List['Produto'] = Field()
    pedido                  : 'Pedido'        = Field()
    data_entrada_saida      : datetime        = Field()
    data_emissao            : datetime        = Field()

    numero_pedido           : Optional[Annotated[str                      , Field()]] = None
    transporte              : Optional[Annotated['Transporte'             , Field()]] = None
    fatura                  : Optional[Annotated['Fatura'                 , Field()]] = None
    parcelas                : Optional[Annotated[List['Parcela']          , Field()]] = None
    exportacao              : Optional[Annotated['Exportacao'             , Field()]] = None
    nfe_referenciada        : Optional[Annotated[List[str]                , Field()]] = None
    retirada                : Optional[Annotated['Local'                  , Field()]] = None
    entrega                 : Optional[Annotated['Local'                  , Field()]] = None
    compra                  : Optional[Annotated['Compra'                 , Field()]] = None
    indicador_intermediador : Optional[Annotated[str                      , Field()]] = None
    informacao_intermediador: Optional[Annotated['InformacaoIntermediador', Field()]] = None

    @model_validator(mode='after')
    def validate_numero_nota_sequencial(self):
        if not isinstance(self.numero_nota_sequencial, str):
            raise TypeError(f'numero_nota_sequencialdeve ser string.')
        if len(self.numero_nota_sequencial) < 1 or len(self.numero_nota_sequencial) > 9:
            raise ValueError(f'numero_nota_sequencial deve conter entre 1 e 9 caracteres.')
        return self

    @model_validator(mode='after')
    def validate_operacao(self):
        if self.operacao not in OPERACOES:
            raise ValueError(f'Operação {self.operacao} inválida')
        return self

    @model_validator(mode='after')
    def validate_modelo(self):
        if self.modelo not in MODELOS:
            raise ValueError(f'Modelo {self.modelo} inválido')
        return self

    @model_validator(mode='after')
    def validate_finalidade(self):
        if self.finalidade not in FINALIDADES:
            raise ValueError(f'Finalidade {self.finalidade} inválida')
        return self

    @model_validator(mode='after')
    def validate_ambiente(self):
        if self.ambiente not in AMBIENTES:
            raise ValueError(f'Ambiente {self.ambiente} inválido')
        return self

class Pagamento(BaseModel):
    formas_pagamento: List['FormaPagamento'] = Field()

class FormaPagamento(BaseModel):
    forma_pagamento         : str = Field()
    meio_pagamento          : str = Field()
    valor_pagamento         : str = Field()

    cnpj_credenciadora      : Optional[Annotated[str, Field()]] = None
    bandeira                : Optional[Annotated[str, Field()]] = None
    autorizacao             : Optional[Annotated[str, Field()]] = None
    data_vencimento         : Optional[Annotated[str, Field()]] = None
    descricao_meio_pagamento: Optional[Annotated[str, Field()]] = None
    # tipo_integracao       : Optional[Annotated[str, Field()]] = None    # TODO: Não está na documentação mas é obrigatório caso meio de pagamento seja 'crédito' ou 'débito'. O valor deve ser '1' ou '2'.

    @model_validator(mode='after')
    def validate_forma_pagamento(self, *args, **kwargs):
        if self.forma_pagamento not in FORMAS_PAGAMENTO:
            raise ValueError(f'Forma de pagamento {self.forma_pagamento} inválido')
        return self

    @model_validator(mode='after')
    def validate_meios_pagamento(self, *args, **kwargs):
        if self.meio_pagamento not in MEIOS_PAGAMENTO:
            raise ValueError(f'Meio de pagamento {self.meio_pagamento} inválido')
        return self

    @model_validator(mode='after')
    def validate_bandeira(self, *args, **kwargs):
        if self.bandeira:
            if self.bandeira not in BANDEIRAS:
                raise ValueError(f'Bandeira {self.bandeira} inválida.')
        return self

    @model_validator(mode='after')
    def validate_descricao_meio_pagamento(self, *args, **kwargs):
        if self.meio_pagamento == '99':
            if self.descricao_meio_pagamento is None:
                raise ValueError(f'Necessário preencher "descricao_meio_pagamento" quando a forma de pagamento é "(99) Outros".')
            if len(self.descricao_meio_pagamento) < 2 or len(self.descricao_meio_pagamento) > 60:
                raise ValueError(f'O campo "descricao_meio_pagamento" deve conter entre 2 a 60 caracteres')
        return self

class Produto(BaseModel):
    '''Classe Produto

    Raises:
        ValueError: Caso o valor de algum atributo seja inválido.
        TypeError: Caso algum campo obrigatório não for informado.
    '''
    item                            : str      = Field()   # Número incremental na lista de produtos
    cfop                            : str      = Field()
    nome                            : str      = Field()
    codigo                          : str      = Field()
    ncm                             : str      = Field()
    quantidade                      : str      = Field()
    unidade                         : str      = Field()
    subtotal                        : str      = Field()
    total                           : str      = Field()
    impostos                        : Impostos = Field()

    numero_pedido                   : Optional[Annotated[str, Field()]]                    = None
    excessao_ibpt                   : Optional[Annotated[str, Field()]]                    = None
    peso_liquido                    : Optional[Annotated[str, Field()]]                    = None
    peso_bruto                      : Optional[Annotated[str, Field()]]                    = None
    origem                          : Optional[Annotated[str, Field()]]                    = None
    veiculo_usado                   : Optional[Annotated[str, Field()]]                    = None
    ind_escala                      : Optional[Annotated[str, Field()]]                    = None
    cnpj_fabricante                 : Optional[Annotated[str, Field()]]                    = None
    beneficio_fiscal                : Optional[Annotated[str, Field()]]                    = None
    gtin                            : Optional[Annotated[str, Field()]]                    = None
    gtin_tributavel                 : Optional[Annotated[str, Field()]]                    = None
    cest                            : Optional[Annotated[str, Field()]]                    = None
    nve                             : Optional[Annotated[str, Field()]]                    = None
    informacoes_adicionais          : Optional[Annotated[str, Field()]]                    = None
    veiculo_novo                    : Optional[Annotated['VeiculoNovo', Field()]]          = None
    exportacao                      : Optional[Annotated['ExportacaoIndividual', Field()]] = None
    importacao                      : Optional[Annotated['ImportacaoIndividual', Field()]] = None
    rastro                          : Optional[Annotated['Rastreamento', Field()]]         = None
    ex_tipi                         : Optional[Annotated[str, Field()]]                    = None
    valor_frete                     : Optional[Annotated[str, Field()]]                    = None
    valor_seguro                    : Optional[Annotated[str, Field()]]                    = None
    valor_desconto                  : Optional[Annotated[str, Field()]]                    = None
    valor_outras_despesas_acessorias: Optional[Annotated[str, Field()]]                    = None

    @model_validator(mode='after')
    def validate_unidade(self, *args, **kwargs):
        if self.unidade not in UNIDADES:
            raise ValueError(f'Unidade {self.unidade} inválida.')
        return self

    @model_validator(mode='after')
    def validate_impostos(self, *args, **kwargs):
        if not isinstance(self.impostos, Impostos):
            raise TypeError(f'Campo "impostos" deve ser {repr(Impostos)} e não {type(self.impostos)}')
        return self

    @model_validator(mode='after')
    def validate_origem(self, *args, **kwargs):
        if self.origem:
            if self.origem not in ORIGENS:
                raise ValueError(f'Origem {self.origem} inválida.')
        return self

    @model_validator(mode='after')
    def validate_total(self, *args, **kwargs):
        quantidade = float(self.quantidade)
        subtotal   = float(self.subtotal)
        total      = float(self.total)

        if f'{total:.2f}' != f'{quantidade*subtotal:.2f}':
            raise ValueError(f'Total {total:.2f} é diferente de quantidade {quantidade:.2f} * subtotal {subtotal:.2f} = {quantidade*subtotal:.2f}')
        return self

    @model_validator(mode='after')
    def validate_ind_escala(self, *args, **kwargs):
        if self.ind_escala:
            if self.ind_escala not in INDICATIVOS_ESCALA:
                raise ValueError(f'Indicativo de escala {self.ind_escala} inválido.')
        return self

class ImpostosProduto(Impostos):
    icms: 'Icms'= Field()
    ipi : 'Ipi' = Field()

class Pedido(BaseModel):
    presenca                  : str         = Field()
    pagamento                 : 'Pagamento' = Field()

    modalidade_frete          : Optional[Annotated[str, Field()]] = None
    frete                     : Optional[Annotated[str, Field()]] = None
    desconto                  : Optional[Annotated[str, Field()]] = None
    total                     : Optional[Annotated[str, Field()]] = None
    despesas_acessorias       : Optional[Annotated[str, Field()]] = None
    despesas_aduaneiras       : Optional[Annotated[str, Field()]] = None
    informacoes_complementares: Optional[Annotated[str, Field()]] = None
    informacoes_fisco         : Optional[Annotated[str, Field()]] = None
    observacoes_fisco         : Optional[Annotated[str, Field()]] = None
    observacoes_contribuinte  : Optional[Annotated[str, Field()]] = None

    @model_validator(mode='after')
    def validate_presenca(self, *args, **kwargs):
        if self.presenca not in PRESENCAS:
            raise ValueError(f'Presença {self.presenca} inválida.')
        return self

    @model_validator(mode='after')
    def validate_modalidade_frete(self, *args, **kwargs):
        if self.modalidade_frete:
            if self.modalidade_frete not in MODALIDADES_FRETE:
                raise ValueError(f'Modalidade de Frete {self.modalidade_frete} inválida.')
        return self

class VeiculoNovo(BaseModel):
    tipo_operacao   : str = Field()
    chassi          : str = Field()
    cor             : str = Field()
    cor_descricao   : str = Field()
    cilindrada      : str = Field()
    peso_liquido    : str = Field()
    peso_bruto      : str = Field()
    serie           : str = Field()
    tipo_combustivel: str = Field()
    numero_motor    : str = Field()
    dist            : str = Field()
    ano_modelo      : str = Field()
    ano_fabricacao  : str = Field()
    tipo_pintura    : str = Field()
    tipo_veiculo    : str = Field()
    especie_veiculo : str = Field()
    condicao_veiculo: str = Field()
    marca_modelo    : str = Field()
    cor_denatran    : str = Field()
    lotacao         : str = Field()
    restricao       : str = Field()

    capacidade_maxima_tracao: Optional[Annotated[str, Field()]] = None
    condicao_chassi         : Optional[Annotated[str, Field()]] = None
    potencia                : Optional[Annotated[str, Field()]] = None


    @model_validator(mode='after')
    def validate_tipo_operacao(self, *args, **kwargs):
        if self.tipo_operacao not in TIPOS_OPERACAO:
            raise ValueError(f'Tipo de operação {self.tipo_operacao} inválido.')
        return self

    @model_validator(mode='after')
    def validate_cor(self, *args, **kwargs):
        if self.cor not in CORES:
            raise ValueError(f'Cor {self.cor} inválida.')
        return self

    @model_validator(mode='after')
    def validate_tipo_combustivel(self, *args, **kwargs):
        if self.tipo_combustivel not in TIPOS_COMBUSTIVEL:
            raise ValueError(f'Tipo combustível {self.tipo_combustivel} inválido.')
        return self

    @model_validator(mode='after')
    def validate_tipo_veiculo(self, *args, **kwargs):
        if self.tipo_veiculo not in TIPOS_VEICULO:
            raise ValueError(f'Tipo de Veículo {self.tipo_veiculo} inválido.')
        return self

    @model_validator(mode='after')
    def validate_especie_veiculo(self, *args, **kwargs):
        if self.especie_veiculo not in ESPECIES_VEICULO:
            raise ValueError(f'Espécie de Veículo {self.especie_veiculo} inválida.')
        return self

    @model_validator(mode='after')
    def validate_condicao_veiculo(self, *args, **kwargs):
        if self.condicao_veiculo not in CONDICOES_VEICULO:
            raise ValueError(f'Condição do véiculo {self.condicao_veiculo} inválida.')
        return self

    @model_validator(mode='after')
    def validate_restricao(self, *args, **kwargs):
        if self.restricao not in RESTRICOES:
            raise ValueError(f'Restrição {self.restricao} inválida.')
        return self

    @model_validator(mode='after')
    def validate_condicao_chassi(self, *args, **kwargs):
        if self.condicao_chassi:
            if self.condicao_chassi not in CONDICOES_CHASSI:
                raise ValueError(f'Condição do Chassi {self.condicao_chassi} inválida.')
        return self

class ExportacaoIndividual(BaseModel):
    drawback      : Optional[Annotated[str, Field()]] = None
    reg_exportacao: Optional[Annotated[str, Field()]] = None
    nfe_exportacao: Optional[Annotated[str, Field()]] = None
    qtd_exportacao: Optional[Annotated[str, Field()]] = None

class ImportacaoIndividual(BaseModel):
    numero_registro                   : Optional[Annotated[str, Field()]]            = None
    data_registro                     : Optional[Annotated[str, Field()]]            = None
    cod_exportador                    : Optional[Annotated[str, Field()]]            = None
    cod_via_transporte_internacional  : Optional[Annotated[str, Field()]]            = None
    valor_afrmm                       : Optional[Annotated[str, Field()]]            = None
    cod_forma_importacao_intermediacao: Optional[Annotated[str, Field()]]            = None
    uf_desembaraco                    : Optional[Annotated[str, Field()]]            = None
    local_desembaraco                 : Optional[Annotated[str, Field()]]            = None
    data_desembaraco                  : Optional[Annotated[str, Field()]]            = None
    cnpj_terceiro                     : Optional[Annotated[str, Field()]]            = None
    uf_terceiro                       : Optional[Annotated[str, Field()]]            = None
    iof                               : Optional[Annotated[str, Field()]]            = None
    valor_despesas_aduaneiras         : Optional[Annotated[str, Field()]]            = None
    adicoes                           : Optional[List['DeclaracaoImportacaoAdicao']] = None

class Rastreamento(BaseModel):
    lote           : str = Field()
    quantidade     : str = Field()
    data_fabricacao: str = Field()
    data_validade  : str = Field()

    codigo_agregacao: Optional[Annotated[str, Field()]] = None

class Fatura(BaseModel):
    numero       : str = Field()
    valor        : str = Field()
    desconto     : str = Field()
    valor_liquido: str = Field()

class Parcela(BaseModel):
    vencimento: str = Field()
    valor     : str = Field()

class Exportacao(BaseModel):
    uf_embarque   : str = Field()
    local_embarque: str = Field()

    local_despacho: Optional[Annotated[str, Field()]] = None

class Local(BaseModel):
    uf                  : str = Field()
    codigo_municipio    : str = Field()
    descricao_municipio : str = Field()
    bairro              : str = Field()
    logradouro          : str = Field()
    numero              : str = Field()
    complemento         : str = Field()

    cpf : Optional[Annotated[str, Field()]] = None
    cnpj: Optional[Annotated[str, Field()]] = None

class Compra(BaseModel):
    contrato    : Optional[Annotated[str, Field()]] = None
    nota_empenho: Optional[Annotated[str, Field()]] = None
    pedido      : Optional[Annotated[str, Field()]] = None

class InformacaoIntermediador(BaseModel):
    cnpj                                : Optional[Annotated[str, Field()]] = None
    identificador_cadastro_intermediador: Optional[Annotated[str, Field()]] = None

class PaginaNotas(BaseModel):
    total           : Optional[Annotated[str, Field()]] = None
    itens_por_pagina: Optional[Annotated[str, Field()]] = None
    pagina_atual    : Optional[Annotated[str, Field()]] = None
    itens           : Optional[List['NotaFiscal']]      = None

# =====================================================================
async def emitir(token_emissor: str,
           token_secret_emissor: str,
           token_empresa: str,
           token_secret_empresa: str,
           objetoNfe: ObjetoEmissaoNFe,
           tipo_emissao: str,
           *args, **kwargs):
    '''Endpoint utilizado para efetivamente emitir uma nota fiscal eletrônica.

    Args:
        nfe (ObjetoEmissaoNFe): Nota Fiscal a ser emitida.

        tipo_emissao (str): Tipo de Emissão
            1: Normal
            6: Contigência SNC-AN
            7: Contigência SVC-RS
    '''

    headers = HEADERS.copy()

    # -----------------------------------------
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor

    validate_tokens(token_empresa, token_secret_empresa)
    headers['token-empresa']        = token_empresa
    headers['token-secret-empresa'] = token_secret_empresa

    # -----------------------------------------
    if not tipo_emissao or tipo_emissao not in TIPOS_EMISSAO:
        raise ValueError(f'Tipo de Emissão {tipo_emissao} inválido')

    headers['tipo-emissao'] = tipo_emissao

    # -----------------------------------------
    obj_dict = objetoNfe.model_dump(exclude_none=True)  # TODO: mode: 'json'

    url = f'{BASE_URL}/nfe'
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json.dumps(obj_dict))

    match response.status_code:
        case 200:
            return response.json()
        case 412:
            return response.json()
        case _:
            return response.text

async def corrigir(token_emissor: str,
             token_secret_emissor: str,
             token_empresa:str,
             token_secret_empresa:str,
             *args, **kwargs):
    raise NotImplementedError

async def cancelar(token_emissor: str,
             token_secret_emissor: str,
             token_empresa:str,
             token_secret_empresa:str,
             *args, **kwargs):
    raise NotImplementedError

async def validar(token_emissor: str,
            token_secret_emissor: str,
            token_empresa:str,
            token_secret_empresa:str,
            objetoNfe:ObjetoEmissaoNFe,
            tipo_emissao:str,
            *args, **kwargs) -> str:
    '''Endpoint utilizado para validar a nota fiscal eletrônica antes de emitir.

    Args:
        nfe (ObjetoEmissaoNFe): Nota Fiscal a ser validada.

        tipo_emissao (str): Tipo de Emissão
            1: Normal
            6: Contigência SNC-AN
            7: Contigência SVC-RS
    '''

    headers = HEADERS.copy()

    # -----------------------------------------
    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor

    validate_tokens(token_empresa, token_secret_empresa)
    headers['token-empresa']        = token_empresa
    headers['token-secret-empresa'] = token_secret_empresa

    # -----------------------------------------
    if not tipo_emissao or tipo_emissao not in TIPOS_EMISSAO:
        raise ValueError(f'Tipo de Emissão {tipo_emissao} inválido')

    headers['tipo-emissao'] = tipo_emissao
    obj_dict = objetoNfe.model_dump(exclude_none=True)  # TODO: mode: 'json'

    url = f'{BASE_URL}/nfe/validacao-nota'
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json.dumps(obj_dict))

    match response.status_code:
        case 200:
            return response.json()
        case _:
            return response.text

async def listar(token_emissor: str,
           token_secret_emissor: str,
           qtd:str = None,
           pagina:str = None,
           *args, **kwargs) -> List[NotaFiscal]:
    '''Recupera as notas fiscais.

    No Distrito Federal (DF), antes de 01/2023, as notas fiscais de serviço eram emitidas como NFe.

    Args:
        qtd (str, optional): Quantidade de notas por página.
        pagina (str, optional): Página a ser retornada.

    Returns:
        List[NotaFiscal]: Lista contendo as notas fiscais.
    '''
    headers = HEADERS.copy()

    validate_tokens(token_emissor, token_secret_emissor)
    headers['token-emissor']        = token_emissor
    headers['token-secret-emissor'] = token_secret_emissor

    params   = {}

    if qtd:
        params['qtd'] = qtd
    if pagina:
        params['pagina'] = pagina

    url = f'{BASE_URL}/nfe/lista-notas'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)

    match (response.status_code):
        case 200:
            json_data = response.json().get('dados')
            nfes = [NotaFiscal(d) for d in json_data['itens']]
            return response, nfes

    return response, None

async def buscar(token_emissor: str,
           token_secret_emissor: str,
           *args, **kwargs):
    raise NotImplementedError

async def get_nota(token_emissor: str,
             token_secret_emissor: str,
             *args, **kwargs):
    raise NotImplementedError

async def inutilizar_numeracao(token_emissor: str,
                         token_secret_emissor: str,
                         token_empresa:str,
                         token_secret_empresa:str,
                         *args, **kwargs):
    raise NotImplementedError

async def get_pre_visualizacao(token_emissor: str,
                         token_secret_emissor: str,
                         token_empresa:str,
                         token_secret_empresa:str,
                         *args, **kwargs):
    raise NotImplementedError

async def get_danfe(token_emissor: str,
              token_secret_emissor: str,
              token_empresa:str,
              token_secret_empresa:str,
              *args, **kwargs):
    raise NotImplementedError

# =====================================================================