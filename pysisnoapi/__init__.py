"""
    Package criado para integração com a API da plataforma SISNO.

    Para utilizar esse package basta importá-lo da seguinte forma:  
    `import pysisnoapi`  
    
    Ou também poderá importar apenas os módulos necessários, como por exemplo:  
    `from pysisnoapi import nfe` 
"""

# ======================================================================================================================
# Imports:
import os
import functools
from dotenv import load_dotenv
from dataclasses import dataclass, asdict
from typing import Optional, List, Tuple, Dict
from datetime import datetime
from dateutil import parser
# from pydantic import BaseModel, validator

# ======================================================================================================================
# Globals:
load_dotenv()

URL     = "https://homolog.arkaonline.com.br/nfe-service"               # TODO: Provisório, em breve voltará para 'https://homolog.sisno.com.br/nfe-service/'
HEADERS = {
    "token-emissor"         : os.getenv("token-emissor", ""),
    "token-secret-emissor"  : os.getenv("token-secret-emissor", ""),
    "token-empresa"         : os.getenv("token-empresa", ""),
    "token-secret-empresa"  : os.getenv("token-secret-empresa", ""),
    "accept"                : "application/json",
    "Content-Type"          : "application/json",
}

# ======================================================================================================================
# Decorators:
def requires_emissor(func):
    """Esse decorador é utilizado para garantir que as chaves de API do emissor estão presentes no HEADERS antes da função ser executada."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for key in ["token-emissor", "token-secret-emissor"]:
            if key in HEADERS and HEADERS[key] is not None and len(HEADERS[key]) in (116, 775):
                return func(*args, **kwargs)
            else:
                raise ValueError(f"Chave '{key}' não configurada.")
    return wrapper

def requires_empresa(func):
    """Esse decorador é utilizado para garantir que as chaves de API da empresa estão presentes no HEADERS antes da função ser executada."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for key in ["token-empresa", "token-secret-empresa"]:
            if key in HEADERS and HEADERS[key] is not None and len(HEADERS[key]) in (116, 775):
                return func(*args, **kwargs)
            else:
                raise ValueError(f"Chave '{key}' não configurada.")
    return wrapper

# ======================================================================================================================
# Classes:
@dataclass
class BaseClass:
    """Classe genérica utilizada como base para as demais classes neste package.
    
    A principal finalidade desta classe é fornecer o método `as_filtered_dict` para filtrar e retornar um dicionário com os atributos relevantes da instância.
    Para maiores informações consulte a documentação do método [aqui](#pysisnoapi.BaseClass.as_filtered_dict).
    """
    
    def as_filtered_dict(self)-> dict[str:str]:
        """
        Retorna um dicionário contendo os campos/atributos da classe com valores não nulos.

        O dicionário resultante possui chaves (str) correspondentes aos nomes dos campos
        da classe e valores (str) representando os respectivos valores desses campos,
        desde que esses valores não sejam nulos (None).
        
        Returns:
            dict: Um dicionário que mapeia os campos não nulos da classe em pares chave-valor.
        """
        return asdict(self, dict_factory=_dict_factory)

@dataclass
class Cfop:
    """Classe `CFOP` (Código Fiscal de Operações e Prestações)
    """
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    aplicacao: Optional[str] = None

@dataclass
class Cliente:
    """Classe `Cliente`
    Geralmente é o destinatário da NFe.
    """
    consumidor_final: str
    contribuinte    : str
    endereco        : "Endereco"
    
    pessoa_fisica   : Optional["PessoaFisica"] = None
    pessoa_juridica : Optional["PessoaJuridica"] = None
    
    id              : Optional[int] = None
    ie              : Optional[str] = None
    telefone        : Optional[str] = None
    email           : Optional[str] = None
    faz_retencao    : Optional[str] = None
    
    # @validator('pessoa_juridica')
    # def validate_pessoa_juridica(cls, value, values):
    #     if not isinstance(value, PessoaJuridica):
    #         raise TypeError("Pessoa Juridica deve ser um objeto da classe PessoaJuridica")
    #     if value and values.get('pessoa_fisica'):
    #         raise ValueError("Informe apenas um dos campos PessoaFisica ou PessoaJuridica")
    #     if not value and not values.get('pessoa_fisica'):
    #         raise ValueError("Informe pelo menos um dos campos PessoaFisica ou PessoaJuridica")
    #     return value
    
    # @validator('consumidor_final')
    # def validate_consumidor_final(cls, consumidor_final):
    #     if not isinstance(consumidor_final, str):
    #         raise TypeError("Consumidor Final tem que ser uma string")
    #     if consumidor_final not in ['1', '2',]:
    #         raise ValueError(f"Consumidor Final {consumidor_final} inválido")
    #     return consumidor_final
    
    # @validator('contribuinte')
    # def validate_contribuinte(cls, contribuinte):
    #     if not isinstance(contribuinte, str):
    #         raise TypeError("Contribuinte tem que ser uma string")
    #     if contribuinte not in ['1', '2', '9']:
    #         raise ValueError(f"Contribuinte {contribuinte} inválido")
    #     return contribuinte

@dataclass
class Cofins:
    """Contribuição para Financiamento da Seguridade Social.

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
    """
    situacao_tributaria : str
    
    aliquota            : Optional[str] = None
    aliquota_st         : Optional[str] = None
    aliquota_retencao   : Optional[str] = None

class DeclaracaoImportacaoAdicao:
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    def __init__(self, **kwargs):
        raise NotImplementedError

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

@dataclass
class Empresa:
    """
        Classe que irá representar todas as empresas cadastradas da plataforma SISNO.
        Pela documentação do dia 11/05/2023, essa classe basicamente só terá sua utilidade ao consultar notas.
        Em resumo: não há necessidade de se preocupar com os campos, caso não saiba algum deles, pois, eles serão preenchidos automaticamente com aquilo que vier do endpoint.
    """
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    id                                          : Optional[str]         = None
    token                                       : Optional[str]         = None
    token_secret                                : Optional[str]         = None
    cnpj                                        : Optional[str]         = None
    nome_fantasia                               : Optional[str]         = None
    razao_social                                : Optional[str]         = None
    endereco                                    : Optional['Endereco']  = None
    telefone                                    : Optional[str]         = None
    inscricao_estadual                          : Optional[str]         = None
    inscricao_municipal                         : Optional[str]         = None
    inscricao_estadual_substituicao_tributaria  : Optional[str]         = None
    regime_tributario                           : Optional[str]         = None
    classificacao_nacional_atividades_economicas: Optional[str]         = None
    ambiente                                    : Optional[str]         = None
    id_csc                                      : Optional[str]         = None
    csc                                         : Optional[str]         = None
    codigo_regime_especial_tributacao           : Optional[str]         = None
    porcentagem_icms_aproveitado                : Optional[str]         = None
    site                                        : Optional[str]         = None
    email                                       : Optional[str]         = None
    utiliza_tributos_aproximados                : Optional[bool]        = None  # TODO: Não consta na documentação da API
    informacoes_complementares                  : Optional[str]         = None  # TODO: Não consta na documentação da API
    senha_portal_prefeitura                     : Optional[str]         = None  # TODO: Não consta na documentação da API
    
    @classmethod
    def from_json(cls, **kwargs):
        endereco_dict = kwargs.pop('endereco', {})
        endereco = Endereco.from_json(**endereco_dict)
        
        return cls(endereco=endereco, **kwargs)

@dataclass
class Endereco:
    """Classe `Endereço`
    """
    
    codigo_pais        : str
    descricao_pais     : str
    bairro             : str
    logradouro         : str
    numero             : str
    
    id                 : Optional[int] = None
    uf                 : Optional[str] = None
    codigo_municipio   : Optional[str] = None
    descricao_municipio: Optional[str] = None
    cep                : Optional[str] = None
    complemento        : Optional[str] = None
    
    @classmethod
    def from_json(cls, **kwargs):
        return cls(**kwargs)
    
@dataclass
class Ibpt:
    """Classe `IBPT` (Impostos sobre Produtos e Serviços)
    """
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    codigo            : Optional[str]  = None
    ex                : Optional[str]  = None
    tipo              : Optional[str]  = None
    descricao         : Optional[str]  = None
    nacional_federal  : Optional[str]  = None
    importados_federal: Optional[str]  = None
    estadual          : Optional[str]  = None
    municipal         : Optional[str]  = None
    vigencia_inicio   : Optional[str]  = None
    vigencia_fim      : Optional[str]  = None
    versao            : Optional[str]  = None
    fonte             : Optional[str]  = None
    unidade_federativa: Optional['Uf'] = None
    ativo             : Optional[str]  = None     # TODO: Até o dia 01/06/2023, não consta na Documentação
    
    @classmethod
    def from_json(cls, **kwargs):
        uf_dict = kwargs.pop('unidade_federativa', {})
        uf = Uf.from_json(**uf_dict)
        return cls(unidade_federativa=uf, **kwargs)

@dataclass
class Icms:
    """Classe `ICMS` (Imposto sobre Circulação de Mercadorias e Serviços)
    """
    situacao_tributaria                       : str
    
    codigo_cfop                               : Optional[str] = None
    aliquota_icms                             : Optional[str] = None
    percentual_reducao_bc_icms                : Optional[str] = None
    aliquota_fcp                              : Optional[str] = None
    percentual_reducao_bc_icms_st             : Optional[str] = None
    aliquota_aplicavel_calculo_credito        : Optional[str] = None
    aliquota_icms_st                          : Optional[str] = None
    aliquota_fcp_st                           : Optional[str] = None
    percentual_margem_valor_agregado_icms_st  : Optional[str] = None
    percentual_diferimento                    : Optional[str] = None
    percentual_desonerado                     : Optional[str] = None
    motivo_desoneracao                        : Optional[str] = None
    percentual_icms_st_retido                 : Optional[str] = None
    utilizar_tabela_aliquotas_interestaduais  : Optional[str] = None
    utilizar_aliquota_interestadual_importacao: Optional[str] = None

@dataclass
class Impostos:
    """Classe Base para as Classes de Impostos de Produtos e Serviços.
    """
    pis   : "Pis"
    cofins: "Cofins"

@dataclass
class Ipi:
    """Classe `IPI` (Imposto Sobre Produtos Industrializados)

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
    """
    situacao_tributaria : str
    
    aliquota            : Optional[str] = None
    codigo_enquadramento: Optional[str] = None
    codigo_selo         : Optional[str] = None
    qtd_selo            : Optional[str] = None

class Issqn:
    def __init__(self, **kwargs):
        """
            Indicador_exigibilidade_iss  
                1. Exigível  
                2. Não incidência  
                3. Isenção  
                4. Exportação  
                5. Imunidade  
                6. Exigibilidade suspensa por decisão judicial  
                7. Exigibilidade suspensa por processo administrativo  
        """
        
        self.indicador_exigibilidade_iss     = kwargs.get("indicador_exigibilidade_iss", None)   # string [ 1, 2, 3, 4, 5, 6, 7 ]
        self.indicador_incentivo_fiscal      = kwargs.get("indicador_incentivo_fiscal", None)    # string (1: Não, 2: Sim)
        self.item_lista_servicos             = kwargs.get("item_lista_servicos", None)           # string - Item da lista de serviços no Padrão ABRASF (Formato NN.NN)
        self.aliquota                        = kwargs.get("aliquota", None)                      # string ($0.0000)

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

@dataclass
class Municipio:
    """Classe `Município`
    """
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    codigo_ibge : Optional[int] = None
    descricao   : Optional[str] = None
    
    @classmethod
    def from_json(cls, **kwargs):
        return cls(**kwargs)

@dataclass
class NotaFiscal:
    """Classe `Nota Fiscal`.
    
    Até 01/2023 essa classe também era usada para Notas Fiscais de Serviço (NFSe).
    """
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    id                      : Optional[int]         = None
    empresa                 : Optional['Empresa']   = None
    tipo                    : Optional[str]         = None
    serie                   : Optional[str]         = None
    numero_nota             : Optional[str]         = None
    chave_acesso            : Optional[str]         = None
    protocolo               : Optional[str]         = None
    nome_destinatario       : Optional[str]         = None
    uf_destinatario         : Optional[str]         = None
    cpf_cnpj_destinatario   : Optional[str]         = None
    valor_total             : Optional[str]         = None
    status                  : Optional[str]         = None
    motivo                  : Optional[str]         = None
    data_emissao            : Optional[datetime]    = None
    data_autorizacao        : Optional[datetime]    = None
    modelo                  : Optional[str]         = None
    ambiente                : Optional[str]         = None
    xml                     : Optional[str]         = None
    json_objeto_nfe         : Optional[str]         = None
    tipo_emissao            : Optional[str]         = None
    numero_lote             : Optional[str]         = None
    
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

class Observacao:
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    
    def __init__(self, **kwargs):
        self.campo                   = kwargs.get("campo", None)                                # string
        self.texto                   = kwargs.get("texto", None)                                # string

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

@dataclass
class PessoaFisica:
    """Classe `Pessoa Física`
    
    Deve ser informado apenas um dos campos [cpf, id_estrangeiro]
    """
    nome_completo: str
    
    cpf           : Optional[str] = None
    id_estrangeiro: Optional[str] = None
    
    # TODO: Só pode passar um dos dois: "cpf" ou "id_estrangeiro"

@dataclass
class PessoaJuridica:
    """Classe `Pessoa Jurídica`
    """
    cnpj        : str
    razao_social: str
    
    im          : Optional[str]
    suframa     : Optional[str]

@dataclass
class Pis:
    """Classe `PIS` (Programas de Integração Social)

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
    
    """
    situacao_tributaria: str
    
    aliquota           : Optional[str] = None
    aliquota_st        : Optional[str] = None
    aliquota_retencao  : Optional[str] = None
    
class RetencaoIcmsTransporte:
    # TODO: Até o dia 10/05/2023 essa classe só está sendo usada na classe "Transporte", que não está sendo usada
    def __init__(self, **kwargs):
        raise NotImplementedError

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class Transporte:
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    def __init__(self, **kwargs):
        raise NotImplementedError

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

@dataclass
class Uf:
    """Classe `UF`(Unidade Federativa)

    Returns:
        _type_: _description_
    """
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    # TODO: Até o dia 01/06/2023 essa classe só está sendo usada em classes de NFSe, entretanto, já deixarei ela por aqui mesmo, acredito que em breve as classes de NFe também usarão
    codigo_ibge: Optional[str]  = None
    sigla      : Optional[str]  = None
    descricao  : Optional[str]  = None

    @classmethod
    def from_json(cls, **kwargs):
        return cls(**kwargs)

# ======================================================================================================================
def alterar_empresa(token_empresa:str, token_secret_empresa:str):
    """
    Altera as chaves de API utilizadas para a emissão de notas fiscais na plataforma SISNO.

    Esse método é responsável por modificar as chaves de API, necessárias para a emissão de notas fiscais em empresas distintas.
    As chaves de API são utilizadas pela plataforma SISNO para identificar a empresa na qual a nota fiscal será emitida.

    Args:
        token_empresa (str): String de 775 caracters fornecido pela plataforma SISNO para utilização da API.
        token_secret_empresa (str): String de 166 caracters fornecido pela plataforma SISNO para utilização da API. Geralmente começa com "1000:".

    Raises:
        Exception: Lançada caso alguma das chaves seja inválida.
    """
    
    # TODO: Realizar melhores validações
    
    if not isinstance(token_empresa, str) or len(token_empresa) != 775:
        raise Exception('Token Empresa inválido')
    if not isinstance(token_secret_empresa, str) or len(token_secret_empresa) != 166:
        raise Exception('Token Secret Empresa inválido')
    
    HEADERS["token-empresa"]        = token_empresa
    HEADERS["token-secret-empresa"] = token_secret_empresa

def _dict_factory(x: List[Tuple]) -> Optional[Dict]:
    """Cria um dicionário filtrado contendo apenas as chaves cujos valores são diferentes de None.

    Essa função é chamada automaticamente durante a conversão de uma classe para um dicionário usando `dataclasses.asdict`, 
    quando é atribuída a opção `dict_factory` como seu valor. 
    
    No caso, estamos usando essa função no método `as_filtered_dict` da classe `BaseClass`.
    
    A função recebe uma lista de tuplas contendo pares chave-valor e retorna um dicionário contendo apenas as chaves cujos valores são diferentes de None.

    Args:
        x (List[Tuple]): Uma lista de tuplas contendo pares chave-valor.

    Returns:
        dict ou None: Um dicionário filtrado com as chaves cujos valores são diferentes de None ou retorna None se o dicionário resultante estiver vazio.
    """
    dic = {k: v for (k, v) in x if v is not None}
    return dic if len(dic) > 0 else None

# ======================================================================================================================
