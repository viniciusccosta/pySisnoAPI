''' 
    Módulo específico para geração de Notas Fiscais de Produto.
    
    Para utilizar esse módulo basta importá-lo da seguinte forma:  
    `from pysisnoapi import nfe`
'''

# =====================================================================
from . import *

import httpx
import json
import jsonpickle

from datetime import datetime

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
@dataclass
class ObjetoEmissaoNFe(BaseClass):
    numero_nota_sequencial  : str
    serie                   : str
    operacao                : str
    natureza_operacao       : str
    modelo                  : str
    finalidade              : str
    ambiente                : str
    cliente                 : Cliente
    produtos                : List['Produto']
    pedido                  : 'Pedido'
    data_entrada_saida      : datetime
    data_emissao            : datetime
    
    numero_pedido           : Optional[str]                       = None
    transporte              : Optional['Transporte']              = None
    fatura                  : Optional['Fatura']                  = None
    parcelas                : Optional[List['Parcela']]           = None
    exportacao              : Optional['Exportacao']              = None
    nfe_referenciada        : Optional[List[str]]                 = None
    retirada                : Optional['Local']                   = None
    entrega                 : Optional['Local']                   = None
    compra                  : Optional['Compra']                  = None
    indicador_intermediador : Optional[str]                       = None
    informacao_intermediador: Optional['InformacaoIntermediador'] = None
    
    def __post_init__(self):
        self.validate_numero_nota_sequencial()
        self.validate_operacao()
        self.validate_modelo()
        self.validate_finalidade()
        self.validate_ambiente()
    
    def validate_numero_nota_sequencial(self):
        if not isinstance(self.numero_nota_sequencial, str):
            raise TypeError(f'numero_nota_sequencialdeve ser string.')
        if len(self.numero_nota_sequencial) < 1 or len(self.numero_nota_sequencial) > 9:
            raise ValueError(f'numero_nota_sequencial deve conter entre 1 e 9 caracteres.')
    
    def validate_operacao(self):
        if self.operacao not in OPERACOES:
            raise ValueError(f'Operação {self.operacao} inválida')
    
    def validate_modelo(self):
        if self.modelo not in MODELOS:
            raise ValueError(f'Modelo {self.modelo} inválido')
    
    def validate_finalidade(self):
        if self.finalidade not in FINALIDADES:
            raise ValueError(f'Finalidade {self.finalidade} inválida')
    
    def validate_ambiente(self):
        if self.ambiente not in AMBIENTES:
            raise ValueError(f'Ambiente {self.ambiente} inválido')

@dataclass
class Pagamento:
    formas_pagamento: List['FormaPagamento']

@dataclass
class FormaPagamento:
    forma_pagamento         : str
    meio_pagamento          : str
    valor_pagamento         : str
    
    cnpj_credenciadora      : Optional[str] = None
    bandeira                : Optional[str] = None
    autorizacao             : Optional[str] = None
    data_vencimento         : Optional[str] = None
    descricao_meio_pagamento: Optional[str] = None
    # tipo_integracao         : Optional[str] = None    # TODO: Não está na documentação mas é obrigatório caso meio de pagamento seja 'crédito' ou 'débito'. O valor deve ser '1' ou '2'.
    
    def __post_init__(self):
        self.validate_forma_pagamento()
        self.validate_meios_pagamento()
        self.validate_bandeira()
        self.validate_descricao_meio_pagamento()
    
    def validate_forma_pagamento(self, *args, **kwargs):
        if self.forma_pagamento not in FORMAS_PAGAMENTO:
            raise ValueError(f'Forma de pagamento {self.forma_pagamento} inválido')

    def validate_meios_pagamento(self, *args, **kwargs):
        if self.meio_pagamento not in MEIOS_PAGAMENTO:
            raise ValueError(f'Meio de pagamento {self.meio_pagamento} inválido')

    def validate_bandeira(self, *args, **kwargs):
        if self.bandeira:
            if self.bandeira not in BANDEIRAS:
                raise ValueError(f'Bandeira {self.bandeira} inválida.')

    def validate_descricao_meio_pagamento(self, *args, **kwargs):
        if self.meio_pagamento == '99':
            if self.descricao_meio_pagamento is None:
                raise ValueError(f'Necessário preencher "descricao_meio_pagamento" quando a forma de pagamento é "(99) Outros".')
            if len(self.descricao_meio_pagamento) < 2 or len(self.descricao_meio_pagamento) > 60:
                raise ValueError(f'O campo "descricao_meio_pagamento" deve conter entre 2 a 60 caracteres')

@dataclass
class Produto:
    '''Classe Produto

    Raises:
        ValueError: Caso o valor de algum atributo seja inválido.
        TypeError: Caso algum campo obrigatório não for informado.
    '''
    item                            : str   # Número incremental na lista de produtos
    
    cfop                            : str
    nome                            : str
    codigo                          : str
    ncm                             : str
    quantidade                      : str
    unidade                         : str
    subtotal                        : str
    total                           : str
    impostos                        : Impostos
    
    numero_pedido                   : Optional[str]                    = None
    excessao_ibpt                   : Optional[str]                    = None
    peso_liquido                    : Optional[str]                    = None
    peso_bruto                      : Optional[str]                    = None
    origem                          : Optional[str]                    = None
    veiculo_usado                   : Optional[str]                    = None
    ind_escala                      : Optional[str]                    = None
    cnpj_fabricante                 : Optional[str]                    = None
    beneficio_fiscal                : Optional[str]                    = None
    gtin                            : Optional[str]                    = None
    gtin_tributavel                 : Optional[str]                    = None
    cest                            : Optional[str]                    = None
    nve                             : Optional[str]                    = None
    informacoes_adicionais          : Optional[str]                    = None
    veiculo_novo                    : Optional['VeiculoNovo']          = None
    exportacao                      : Optional['ExportacaoIndividual'] = None
    importacao                      : Optional['ImportacaoIndividual'] = None
    rastro                          : Optional['Rastreamento']         = None
    ex_tipi                         : Optional[str]                    = None
    valor_frete                     : Optional[str]                    = None
    valor_seguro                    : Optional[str]                    = None
    valor_desconto                  : Optional[str]                    = None
    valor_outras_despesas_acessorias: Optional[str]                    = None
    
    def __post_init__(self, *args, **kwargs):
        self.validate_unidade()
        self.validate_impostos()
        self.validate_origem()
        self.validate_total()
        self.validate_ind_escala()
        
    def validate_unidade(self, *args, **kwargs):
        if self.unidade not in UNIDADES:
            raise ValueError(f'Unidade {self.unidade} inválida.')
        
    def validate_impostos(self, *args, **kwargs):
        if not isinstance(self.impostos, Impostos):
            raise TypeError(f'Campo "impostos" deve ser {repr(Impostos)} e não {type(self.impostos)}')

    def validate_origem(self, *args, **kwargs):
        if self.origem:
            if self.origem not in ORIGENS:
                raise ValueError(f'Origem {self.origem} inválida.')
        
    def validate_total(self, *args, **kwargs):
        quantidade = float(self.quantidade)
        subtotal   = float(self.subtotal)
        total      = float(self.total)
        
        if f'{total:.2f}' != f'{quantidade*subtotal:.2f}':
            raise ValueError(f'Total {total:.2f} é diferente de quantidade {quantidade:.2f} * subtotal {subtotal:.2f} = {quantidade*subtotal:.2f}')
        
    def validate_ind_escala(self, *args, **kwargs):
        if self.ind_escala:
            if self.ind_escala not in INDICATIVOS_ESCALA:
                raise ValueError(f'Indicativo de escala {self.ind_escala} inválido.')
    
@dataclass
class ImpostosProduto(Impostos):
    icms: 'Icms'
    ipi : 'Ipi'

@dataclass
class Pedido:
    presenca                  : str
    pagamento                 : 'Pagamento'
    
    modalidade_frete          : Optional[str] = None
    frete                     : Optional[str] = None
    desconto                  : Optional[str] = None
    total                     : Optional[str] = None
    despesas_acessorias       : Optional[str] = None
    despesas_aduaneiras       : Optional[str] = None
    informacoes_complementares: Optional[str] = None
    informacoes_fisco         : Optional[str] = None
    observacoes_fisco         : Optional[str] = None
    observacoes_contribuinte  : Optional[str] = None
    
    def __post_init__(self):
        self.validate_presenca()
        self.validate_modalidade_frete()
    
    def validate_presenca(self, *args, **kwargs):
        if self.presenca not in PRESENCAS:
            raise ValueError(f'Presença {self.presenca} inválida.')
        
    def validate_modalidade_frete(self, *args, **kwargs):
        if self.modalidade_frete:
            if self.modalidade_frete not in MODALIDADES_FRETE:
                raise ValueError(f'Modalidade de Frete {self.modalidade_frete} inválida.')

@dataclass
class VeiculoNovo:
    tipo_operacao   : str
    chassi          : str
    cor             : str
    cor_descricao   : str
    cilindrada      : str
    peso_liquido    : str
    peso_bruto      : str
    serie           : str
    tipo_combustivel: str
    numero_motor    : str
    dist            : str
    ano_modelo      : str
    ano_fabricacao  : str
    tipo_pintura    : str
    tipo_veiculo    : str
    especie_veiculo : str
    condicao_veiculo: str
    marca_modelo    : str
    cor_denatran    : str
    lotacao         : str
    restricao       : str

    capacidade_maxima_tracao: Optional[str] = None
    condicao_chassi         : Optional[str] = None
    potencia                : Optional[str] = None
   
    def __post_init__(self):
       self.validate_tipo_operacao()
       self.validate_cor()
       self.validate_tipo_combustivel()
       self.validate_tipo_veiculo()
       self.validate_especie_veiculo()
       self.validate_condicao_veiculo()
       self.validate_restricao()
       self.validate_condicao_chassi()
    
    def validate_tipo_operacao(self, *args, **kwargs):
        if self.tipo_operacao not in TIPOS_OPERACAO:
            raise ValueError(f'Tipo de operação {self.tipo_operacao} inválido.')
    
    def validate_cor(self, *args, **kwargs):
        if self.cor not in CORES:
            raise ValueError(f'Cor {self.cor} inválida.')
    
    def validate_tipo_combustivel(self, *args, **kwargs):
        if self.tipo_combustivel not in TIPOS_COMBUSTIVEL:
            raise ValueError(f'Tipo combustível {self.tipo_combustivel} inválido.')
    
    def validate_tipo_veiculo(self, *args, **kwargs):
        if self.tipo_veiculo not in TIPOS_VEICULO:
            raise ValueError(f'Tipo de Veículo {self.tipo_veiculo} inválido.')
    
    def validate_especie_veiculo(self, *args, **kwargs):
        if self.especie_veiculo not in ESPECIES_VEICULO:
            raise ValueError(f'Espécie de Veículo {self.especie_veiculo} inválida.')
    
    def validate_condicao_veiculo(self, *args, **kwargs):
        if self.condicao_veiculo not in CONDICOES_VEICULO:
            raise ValueError(f'Condição do véiculo {self.condicao_veiculo} inválida.')
    
    def validate_restricao(self, *args, **kwargs):
        if self.restricao not in RESTRICOES:
            raise ValueError(f'Restrição {self.restricao} inválida.')
    
    def validate_condicao_chassi(self, *args, **kwargs):
        if self.condicao_chassi:
            if self.condicao_chassi not in CONDICOES_CHASSI:
                raise ValueError(f'Condição do Chassi {self.condicao_chassi} inválida.')

@dataclass
class ExportacaoIndividual:
    drawback      : Optional[str] = None
    reg_exportacao: Optional[str] = None
    nfe_exportacao: Optional[str] = None
    qtd_exportacao: Optional[str] = None

@dataclass
class ImportacaoIndividual:
    numero_registro                   : Optional[str]                                = None
    data_registro                     : Optional[str]                                = None
    cod_exportador                    : Optional[str]                                = None
    cod_via_transporte_internacional  : Optional[str]                                = None
    valor_afrmm                       : Optional[str]                                = None
    cod_forma_importacao_intermediacao: Optional[str]                                = None
    uf_desembaraco                    : Optional[str]                                = None
    local_desembaraco                 : Optional[str]                                = None
    data_desembaraco                  : Optional[str]                                = None
    cnpj_terceiro                     : Optional[str]                                = None
    uf_terceiro                       : Optional[str]                                = None
    iof                               : Optional[str]                                = None
    valor_despesas_aduaneiras         : Optional[str]                                = None
    adicoes                           : Optional[List['DeclaracaoImportacaoAdicao']] = None

@dataclass
class Rastreamento:
    lote           : str
    quantidade     : str
    data_fabricacao: str
    data_validade  : str
    
    codigo_agregacao: Optional[str] = None

@dataclass
class Fatura:
    numero       : str
    valor        : str
    desconto     : str
    valor_liquido: str

@dataclass
class Parcela:
    vencimento: str
    valor     : str

@dataclass
class Exportacao:
    uf_embarque   : str
    local_embarque: str
    
    local_despacho: Optional[str] = None

@dataclass
class Local:
    uf                  : str
    codigo_municipio    : str
    descricao_municipio : str
    bairro              : str
    logradouro          : str
    numero              : str
    complemento         : str
    
    cpf : Optional[str] = None
    cnpj: Optional[str] = None

@dataclass
class Compra:
    contrato    : Optional[str] = None
    nota_empenho: Optional[str] = None
    pedido      : Optional[str] = None

@dataclass
class InformacaoIntermediador:
    cnpj                                : Optional[str] = None
    identificador_cadastro_intermediador: Optional[str] = None

@dataclass
class PaginaNotas:
    total           : Optional[str]                = None
    itens_por_pagina: Optional[str]                = None
    pagina_atual    : Optional[str]                = None
    itens           : Optional[List['NotaFiscal']] = None

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
    json_str = jsonpickle.encode(objetoNfe.as_filtered_dict(), unpicklable=False)
    
    url = f'{BASE_URL}/nfe'
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json.loads(json_str))
        
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
    json_str = jsonpickle.encode(objetoNfe.as_filtered_dict(), unpicklable=False)
    
    url = f'{BASE_URL}/nfe/validacao-nota'
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=json.loads(json_str))
    
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
            nfes = [NotaFiscal.from_json(**d) for d in json_data['itens']]
            return nfes
        case _:
            return response.text

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