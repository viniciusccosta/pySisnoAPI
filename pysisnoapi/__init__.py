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

# ======================================================================================================================
# Globals:
load_dotenv()

URL     = "https://homolog.arkaonline.com.br/nfe-service"
HEADERS = {
    "token-emissor"         : os.getenv("token-emissor", ""),
    "token-secret-emissor"  : os.getenv("token-secret-emissor", ""),
    "token-empresa"         : os.getenv("token-empresa", ""),
    "token-secret-empresa"  : os.getenv("token-secret-empresa", ""),
    "accept"                : "application/json",
    "Content-Type"          : "application/json",
}
REQUIRED_KEYS = [ "token-emissor", "token-secret-emissor", "token-empresa", "token-secret-empresa", ]

# ======================================================================================================================
# Decorators:
def requires_keys(func):
    """Esse decorador é utilizado para garantir que as chaves de API estão presentes no HEADERS antes da função ser executada."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for key in REQUIRED_KEYS:
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
        return asdict(self, dict_factory=dict_factory)
    
@dataclass
class Cfop(BaseClass):
    """CFOP (Código Fiscal de Operações e Prestações)
    """
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    codigo: Optional[str] = None
    descricao: Optional[str] = None
    aplicacao: Optional[str] = None

class Cliente:
    def __init__(self, consumidor_final, contribuinte, endereco, **kwargs):
        # Deve ser informado apenas um dos campos [pessoa_fisica, pessoa_juridica]
        if "pessoa_fisica" not in kwargs and "pessoa_juridica" not in kwargs:
            raise Exception("Necessário conter pelo menos um dos campos 'pessoa_fisica' ou 'pessoa_jurica'")
        elif "pessoa_fisica" in kwargs and "pessoa_juridica" in kwargs:
            raise Exception("Informar apenas um dos campos 'pessoa_fisica' ou 'pessoa_jurica'")

        self.pessoa_fisica      = kwargs.get("pessoa_fisica", None)         # Objeto PessoaFisica
        self.pessoa_juridica    = kwargs.get("pessoa_juridica", None)       # Objeto PessoaJuridica

        self.ie                 = kwargs.get("ie", '')
        self.consumidor_final   = consumidor_final                          # string (0: Não, 1: Sim)
        self.contribuinte       = contribuinte                              # string (1: Contribuinte ICMS, 2: Contribuinte isento, 9: Não contribuinte)
        self.endereco           = endereco                                  # Objeto Endereco
        self.telefone           = kwargs.get("telefone", '')
        self.email              = kwargs.get("email", '')
        self.faz_retencao       = kwargs.get("faz_retencao", None)          # boolean

    def asdict(self):
        # Deve ser informado apenas um dos campos [pessoa_fisica, pessoa_juridica]

        if self.pessoa_juridica:
            dados = {
                "ie"                : self.ie,
                "pessoa_juridica"   : self.pessoa_juridica,
                "consumidor_final"  : self.consumidor_final,
                "contribuinte"      : self.contribuinte,
                "endereco"          : self.endereco,
                "telefone"          : self.telefone,
                "email"             : self.email,
                "faz_retencao"      : self.faz_retencao,
            }
        else:
            dados = {
                "ie"                : self.ie,
                "pessoa_fisica"     : self.pessoa_fisica,
                "consumidor_final"  : self.consumidor_final,
                "contribuinte"      : self.contribuinte,
                "endereco"          : self.endereco,
                "telefone"          : self.telefone,
                "email"             : self.email,
                "faz_retencao"      : self.faz_retencao,
            }
        
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class Cofins:
    def __init__(self, **kwargs):
        self.situacao_tributaria     = kwargs.get("situacao_tributaria", None)  # string [ 01, 02, 03, 04, 05, 06, 07, 08, 09, 49, 50, 51, 52, 53, 54, 55, 56, 60, 61, 62, 63, 64, 65, 66, 67, 70, 71, 72, 73, 74, 75, 98, 99 ]

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class DeclaracaoImportacaoAdicao:
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    def __init__(self, **kwargs):
        raise NotImplementedError

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class Empresa:
    """
        Classe que irá representar todas as empresas cadastradas da plataforma SISNO.
        Pela documentação do dia 11/05/2023, essa classe basicamente só terá sua utilidade ao consultar notas.
        Em resumo: não há necessidade de se preocupar com os campos, caso não saiba algum deles, pois, eles serão preenchidos automaticamente com aquilo que vier do endpoint.
    """
    
    def __init__(self, id, **kwargs):
        """
        Construtor da Classe.

        Args:
            id (int): ID da empresa registrada na plataforma SISNO.  
                Default is 0
            token (str): String de 775 caracters fornecido pela plataforma SISNO para utilização da API.  
                Default is ''  
            token_secret (str): String de 166 caracters fornecido pela plataforma SISNO para utilização da API. Geralmente começa com "1000:".
                Default is ''
            cnpj (str): CNPJ da Empresa.
                Default is ''
            nome_fantasia (str): Nome Fantasia da Empresa.
                Default is ''
            razao_social (str): Razão Social da Empresa.
                Default is ''
            endereco (str): Endereço da Empresa.
                Default is, None
            telefone (str): Telefone da Empresa.
                Default is ''
            inscricao_estadual (str): Inscrição Estadual da Empresa.
                Default is ''
            inscricao_municipal (str): Inscrição Municipal da Empresa.
                Default is ''
            inscricao_estadual_substituicao_tributaria (str): .
                Default is ''
            regime_tributario (str): Regime Tributário da Empresa (Lucro Real, Lucro Presumido, Simples Nacional, ...).
                Default is ''
            classificacao_nacional_atividades_economicas (str): CNAE.
                Default is ''
            ambiente (str): Produção ou Homologação.
                Default is ''
            id_csc (str): ID do Código de Segurança do Contribuinte.
                Default is ''
            csc (str): Código de Segurança do Contribuinte.
                Default is ''
            codigo_regime_especial_tributacao (str): Código do Regime Especial de Tributação (Microempresa municipal, Estimativa, Sociedade Profissional, Cooperativa, Microempresario individual MEI, Microempresário e empresa de pequeno porte).
                Default is ''
            porcentagem_icms_aproveitado (float): % ICMS Aproveitado.
                Default is 0.00
            site (str): Site da Empresa.
                Default is ''
            email (str): E-mail da Empresa.
                Default is ''
        """

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
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class Endereco:
    def __init__(self, codigo_pais, descricao_pais, bairro, logradouro, numero, **kwargs):
        """
        Construtor da Classe.

        Args:
            codigo_pais (str): Código do Pais (55 para Brasil).
            
            descricao_pais (str): Nome do País.

            bairro (str): Bairro do Endereço.
            
            logradouro (str): Endereço em si (sugestão: utilize exatamente aquilo que informado ao consultar o CEP nos correios).
            
            numero (str): Número do Endereço (apenas números).

            uf (str): Default is ''
            
            codigo_municipio (str): Default is ''
            
            descricao_municipio (str): Default is ''
            
            cep (str): Default is ''
            
            complemento (str): Default is ''
        """

        self.codigo_pais            = codigo_pais
        self.descricao_pais         = descricao_pais
        self.uf                     = kwargs.get("uf", '')
        self.codigo_municipio       = kwargs.get("codigo_municipio", '')
        self.descricao_municipio    = kwargs.get("descricao_municipio", '')
        self.cep                    = kwargs.get("cep", '')                     # TODO: Apenas números
        self.bairro                 = bairro
        self.logradouro             = logradouro
        self.numero                 = numero                                    # TODO: Apenas números
        self.complemento            = kwargs.get("complemento", '')

    def asdict(self):
        # Quando o país não for Brasil, ignorar os campos [uf, codigo_municipio, descricao_municipio, cep]

        if self.codigo_pais == "55":
            dados = {
                "codigo_pais"        : self.codigo_pais,
                "descricao_pais"     : self.descricao_pais,
                "uf"                 : self.uf,
                "codigo_municipio"   : self.codigo_municipio,
                "descricao_municipio": self.descricao_municipio,
                "cep"                : self.cep,
                "bairro"             : self.bairro,
                "logradouro"         : self.logradouro,
                "numero"             : self.numero,
                "complemento"        : self.complemento
            }
        else:
            dados = {
                "codigo_pais"        : self.codigo_pais,
                "descricao_pais"     : self.descricao_pais,
                "bairro"             : self.bairro,
                "logradouro"         : self.logradouro,
                "numero"             : self.numero,
                "complemento"        : self.complemento
            }
        
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

@dataclass
class Ibpt(BaseClass):
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
        uf_dict = kwargs.pop('unidade_federativa', None)
        uf = Uf.from_json(**uf_dict)
        return cls(unidade_federativa=uf, **kwargs)

class Icms:
    def __init__(self, **kwargs):
        self.situacao_tributaria     = kwargs.get("situacao_tributaria", None)  # string [ 00, 10, 20, 30, 40, 41, 50, 51, 60, 70, 90, 101, 102, 103, 201, 202, 203, 300, 400, 500, 900 ]

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class Impostos:
    def __init__(self, tipo, pis, cofins, **kwargs):
        # Quando produto, não informar o campo issqn. Quando serviço, não informar os campos icms e ipi.
        self.tipo                    = tipo                         # 0: Produto, 1: Serviço

        self.icms                    = kwargs.get("icms", None)     # Objeto ICMS
        self.ipi                     = kwargs.get("ipi", None)      # Objeto IPI
        self.pis                     = pis
        self.cofins                  = cofins
        self.issqn                   = kwargs.get("issqn", None)    # Objeto ISSQN

    def asdict(self):
        # 0: Produto, 1: Serviço

        if self.tipo == "0":
            dados = {
                "icms"  : self.icms,
                "ipi"   : self.ipi,
                "pis"   : self.pis,
                "cofins": self.cofins,
            }
        elif self.tipo == "1":
            dados = {
                "pis"   : self.pis,
                "cofins": self.cofins,
                "issqn" : self.issqn,
            }
        
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class Ipi:
    def __init__(self, **kwargs):
        self.situacao_tributaria     = kwargs.get("situacao_tributaria", None)  # string [ 00, 01, 02, 03, 04, 05, 49, 50, 51, 52, 53, 54, 55, 99 ]

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

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
class Municipio(BaseClass):
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    codigo_ibge : Optional[str] = None
    descricao   : Optional[str] = None

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

class Observacao:
    # TODO: Até o dia 10/05/2023 essa classe não está sendo usada
    
    def __init__(self, **kwargs):
        self.campo                   = kwargs.get("campo", None)                                # string
        self.texto                   = kwargs.get("texto", None)                                # string

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class PessoaFisica:
    def __init__(self, nome_completo, **kwargs):
        # Deve ser informado apenas um dos campos [cpf, id_estrangeiro]
        if "cpf" not in kwargs and "id_estrangeiro" not in kwargs:
            raise Exception("Necessário conter pelo menos um dos campos 'cpf' ou 'id_estrangeiro'")
        elif "cpf" in kwargs and "id_estrangeiro" in kwargs:
            raise Exception("Informar apenas um dos campos 'cpf' ou 'id_estrangeiro'")

        self.cpf            = kwargs.get("cpf", '')                 # string
        self.id_estrangeiro = kwargs.get("id_estrangeiro", '')      # string
        self.nome_completo  = nome_completo                         # string

    def asdict(self):
        # TODO: Deve ser informado apenas um dos campos [cpf, id_estrangeiro]

        if self.id_estrangeiro:
            dados = {
                "id_estrangeiro"    : self.id_estrangeiro,
                "nome_completo"     : self.nome_completo,
            }
        else:
            dados = {
                "cpf"               : self.cpf,
                "nome_completo"     : self.nome_completo,
            }
        
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class PessoaJuridica:
    def __init__(self, **kwargs):
        self.cnpj                    = kwargs.get("cnpj", None)                 # string
        self.razao_social            = kwargs.get("razao_social", None)         # string

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

class Pis:
    def __init__(self, situacao_tributaria, **kwargs):
        """
        Args:
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

        self.situacao_tributaria = situacao_tributaria
        self.aliquota            = kwargs.get("aliquota", None)
        self.aliquota_st         = kwargs.get("aliquota_st", None)
        self.aliquota_retencao   = kwargs.get("aliquota_retencao", None)

    def asdict(self):
        dados = self.__dict__
        dados = {k: v for k,v in dados.items() if (v is not None) and (not isinstance(v, str) or v != '')}    # Removendo os dados que possuem valores vazios (None ou '')
        return dados if len(dados) > 0 else None

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
class Uf(BaseClass):
    # TODO: Até o dia 01/06/2023, não consta na Documentação quais são os campos obrigatórios
    # TODO: Até o dia 01/06/2023 essa classe só está sendo usada em classes de NFSe, entretanto, já deixarei ela por aqui mesmo, acredito que em breve as classes de NFe também usarão
    codigo_ibge: Optional[str]  = None
    sigla      : Optional[str]  = None
    descricao  : Optional[str]  = None

    @classmethod
    def from_json(cls, **kwargs):
        return cls(**kwargs)

# ======================================================================================================================
def alterar_emissor(token_emissor:str, token_secret_emissor:str, token_empresa:str, token_secret_empresa:str):
    """
    Método responsável por alterar as chaves de API.
    A alteração das chaves de API é necessária para consultar/emitir notas fiscais de diferente empresas.
    É através das chaves que a plataforma de SISNO irá identificar quem é o emissor e irá listar (ou emitir) as notas para essa empresa em específico.

    Args:
        token_emissor (str): String de 775 caracters fornecido pela plataforma SISNO para utilização da API
        token_secret_emissor (str): String de 166 caracters fornecido pela plataforma SISNO para utilização da API. Geralmente começa com "1000:".
        token_empresa (str): String de 775 caracters fornecido pela plataforma SISNO para utilização da API
        token_secret_empresa (str): String de 166 caracters fornecido pela plataforma SISNO para utilização da API. Geralmente começa com "1000:".

    Raises:
        Exception: Caso alguma das chaves seja inválida
    """
    global HEADERS

    # TODO: Validar outros parâmetros, como tipos de caracters e etc.

    if not isinstance(token_emissor, str) or len(token_emissor) != 775:
        raise Exception('Token Emissor inválido')
    if not isinstance(token_secret_emissor, str) or len(token_secret_emissor) != 166:
        raise Exception('Token Secret Emissor inválido')
    if not isinstance(token_empresa, str) or len(token_empresa) != 775:
        raise Exception('Token Empresa inválido')
    if not isinstance(token_secret_empresa, str) or len(token_secret_empresa) != 166:
        raise Exception('Token Secret Empresa inválido')
    
    HEADERS["token-emissor"]        = token_emissor
    HEADERS["token-secret-emissor"] = token_secret_emissor
    HEADERS["token-empresa"]        = token_empresa
    HEADERS["token-secret-empresa"] = token_secret_empresa

def dict_factory(x: List[Tuple]) -> Optional[Dict]:
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
