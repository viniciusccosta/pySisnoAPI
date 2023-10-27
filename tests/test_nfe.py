# =================================================================
import requests
import unittest

from unittest.mock  import MagicMock
from datetime       import datetime
from pydantic       import ValidationError

from pysisnoapi import *
from pysisnoapi import nfe

# =================================================================
class NfeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        endereco = Endereco (
            codigo_pais         = '1058',
            descricao_pais      = 'Brasil',
            uf                  = 'DF',
            codigo_municipio    = '5300108',
            descricao_municipio = 'Brasilia',
            cep                 = '70634300',
            bairro              = 'Zona Industrial',
            logradouro          = 'Quadra SOFN Quadra 3',
            numero              = '484',
            complemento         = 'Gerado por 4devs',
        )

        cliente  = Cliente(
            consumidor_final = '1',
            contribuinte     = '9',
            pessoa_fisica    = PessoaFisica(nome_completo="Vicente Marcos Samuel Nunes", cpf='44301337199'),
            endereco         = endereco,
        )

        impostos = nfe.ImpostosProduto(
            pis = Pis (
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            cofins = Cofins(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            icms = Icms (
                situacao_tributaria='102',
                aliquota_icms='0.0000',
                aliquota_icms_st='0.0000',
            ),
            ipi = Ipi(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
        )

        produtos = [
            nfe.Produto(
                cfop                   = '5102',
                item                   = "1",
                nome                   = "UNIFORMES",
                codigo                 = "123456",
                ncm                    = "62069000",
                quantidade             = "2.0",
                unidade                = "UNID",
                subtotal               = "5.0",
                total                  = "10.0",
                impostos               = impostos,
                informacoes_adicionais = "Emitido pelo pySisnoAPI",
            ),
        ]

        pagamento = nfe.Pagamento(
            formas_pagamento = [
                nfe.FormaPagamento(
                    forma_pagamento='0',
                    meio_pagamento='01',
                    valor_pagamento='1.0'
                )
            ]
        )

        pedido   = nfe.Pedido(
            presenca='0',
            pagamento=pagamento,
            # informacoes_complementares='Procon - 151 Endereço do Procon - Shopping Venâncio, Setor Comercial Sul Q. 6 - Brasilia, DF, CEP 70308-200nEMPRESA ENQUADRADA NO SIMPLES NACIONAL LC 123/2006n',
        )

        data = datetime.now()

        self.objeto = nfe.ObjetoEmissaoNFe(
            numero_nota_sequencial= '123456',
            serie                 = '1',
            operacao              = '1',
            natureza_operacao     = 'NATUREZA',
            modelo                = '55',
            finalidade            = '1',
            ambiente              = '2',
            cliente               = cliente,
            produtos              = produtos,
            pedido                = pedido,
            data_entrada_saida    = data,
            data_emissao          = data,
        )

    async def test_listar(self):
        """Função responsável por testar a função nfe.listar() utilizando dados falsos.
        Essa função realiza uma solicitação ao endpoint correspondente e retorna uma lista de objetos NotaFiscal.
        """

        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_response.json.return_value = {
            'status': 'Sucesso',
            'descricao': 'Página de notas de serviço do emissor',
            "dados": {
                'total': 1,
                'itens_por_pagina': 10,
                'pagina_atual': 0,
                'itens': [
                    {
                        "id": 31833,
                        "empresa": {
                            "cnpj": "05397048000107",                               # https://www.4devs.com.br/gerador_de_cnpj
                            "nome_fantasia": "Empresa do Fulano",
                            "razao_social": "Fulanos Inc.",
                            "endereco": {
                                "id": 7,
                                "codigo_pais": "1058",
                                "descricao_pais": "BRASIL",
                                "uf": "DF",
                                "codigo_municipio": "5300108",
                                "descricao_municipio": "Brasilia",
                                "cep": "70343-520",                                 # https://www.4devs.com.br/gerador_de_cep
                                "bairro": "ASA SUL",
                                "logradouro": "ENDERECO DA EMPRESA",
                                "numero": "7",
                                "complemento": "COMPLEMENTO QUALQUER"
                            },
                            "telefone": "(11) 9999-9999",
                            "inscricao_estadual": "0123456789123",
                            "regime_tributario": "1",
                            "classificacao_nacional_atividades_economicas": "8512100",
                            "ambiente": "2",
                            "id_csc": "1",
                            "csc": "A55B0362-814F-4F93-B652-F3DAAF8697F1",
                            "codigo_regime_especial_tributacao": "6",
                            "site": "https://fulanos.da.silva.junior.inc",
                            "utiliza_tributos_aproximados": True,
                            "informacoes_complementares": "Informações Complementares",
                            "senha_portal_prefeitura": "542 caracteres"
                        },
                        "tipo": "NF-e",
                        "serie": "1",
                        "numero_nota": "50",
                        "chave_acesso": "53230500665143000112550010000000777777777777",
                        "protocolo": "353230007777777",
                        # "nome_destinatario": "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL",
                        # "uf_destinatario": "DF",
                        # "cpf_cnpj_destinatario": "94346387047",  # https://www.4devs.com.br/gerador_de_cpf
                        "valor_total": "4.00",
                        "status": "Autorizada",
                        "motivo": "Autorizado o uso da NF-e",
                        "data_emissao": "02/06/2023 17:25:57",
                        "data_autorizacao": "02/06/2023 21:29:40",
                        "modelo": "55",
                        "ambiente": "2",
                        "xml": "XML",
                        "json_objeto_nfe": "OBJETO JSON",
                        "tipo_emissao": "1"
                    }
                ],
                # 'informacoesAdicionais': {
                #     'totalAutorizadas': 0.0,
                #     'totalCanceladas': 0.0
                # },
            }
        }

        requests.get = MagicMock(return_value=mock_response)

        # Chamando a Função:
        nfes = await nfe.listar(token_emissor='token', token_secret_emissor='token-secret',)

        # Checando resultado:
        self.assertGreaterEqual(len(nfes), 1)

    async def test_validar(self):
        """Função responsável por testar a função nfe.validar() utilizando dados falsos.
        Essa função realiza uma solicitação ao endpoint correspondente para validar uma nota fiscal antes de emiti-la.
        """

        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'status': 'Sucesso',
            'message': 'Nota validada pela API',
        }

        requests.post = MagicMock(return_value=mock_response)

        # Chamando a Função:
        result = await nfe.validar(token_emissor='token', token_secret_emissor='token-secret', objetoNfe=self.objeto, tipo_emissao='1', token_empresa="token_empresa", token_secret_empresa="token_secret_empresa")

        # Checando resultado:
        self.assertEqual('Sucesso', result['status'])
        self.assertEqual('Nota validada pela API', result['message'])

    async def test_emitir(self):
        """Função responsável por testar a função nfe.emitir() utilizando dados falsos.
        Essa função realiza uma solicitação ao endpoint correspondente para emitir uma nota fiscal.
        """

        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "Sucesso",
            "descricao": "Lote enviado com sucesso.",
            "retorno_sefaz": {
                "retorno": {
                    "versao": "4.00",
                    "ambiente": "HOMOLOGACAO",
                    "versaoAplicacao": "SVRS202305251555",
                    "status": "103",
                    "motivo": "Lote recebido com sucesso",
                    "uf": "DF",
                    "dataRecebimento": {
                        "dateTime": {
                            "date": {
                                "year": 2023,
                                "month": 6,
                                "day": 21
                            },
                            "time": {
                                "hour": 17,
                                "minute": 0,
                                "second": 12,
                                "nano": 0
                            }
                        },
                        "offset": {
                            "totalSeconds": -10800
                        },
                        "zone": {
                            "totalSeconds": -10800
                        }
                    },
                    "infoRecebimento": {
                        "recibo": "533002202262170",
                        "tempoMedio": "1"
                    }
                },
                "loteAssinado": {
                    "versao": "4.00",
                    "idLote": "24781",
                    "indicadorProcessamento": "PROCESSAMENTO_ASSINCRONO",
                    "notas": [
                        {
                            "identificadorLocal": 0,
                            "info": {
                                "identificador": "NFe53230500665143000112550017777740441235246385",     # Alterado manualmente
                                "versao": "4.00",
                                "identificacao": {
                                    "uf": "DF",
                                    "codigoRandomico": "23524638",
                                    "naturezaOperacao": "PRESTAÇÃO DE SERVIÇO",
                                    "modelo": "NFE",
                                    "serie": "1",
                                    "numeroNota": "4044",
                                    "dataHoraEmissao": {
                                        "dateTime": {
                                            "date": {
                                                "year": 2023,
                                                "month": 5,
                                                "day": 19
                                            },
                                            "time": {
                                                "hour": 17,
                                                "minute": 25,
                                                "second": 57,
                                                "nano": 0
                                            }
                                        },
                                        "offset": {
                                            "totalSeconds": -10800
                                        },
                                        "zone": {
                                            "totalSeconds": -10800
                                        }
                                    },
                                    "dataHoraSaidaOuEntrada": {
                                        "dateTime": {
                                            "date": {
                                                "year": 2023,
                                                "month": 5,
                                                "day": 19
                                            },
                                            "time": {
                                                "hour": 17,
                                                "minute": 25,
                                                "second": 57,
                                                "nano": 0
                                            }
                                        },
                                        "offset": {
                                            "totalSeconds": -10800
                                        },
                                        "zone": {
                                            "totalSeconds": -10800
                                        }
                                    },
                                    "tipo": "SAIDA",
                                    "identificadorLocalDestinoOperacao": "OPERACAO_INTERNA",
                                    "codigoMunicipio": "5300108",
                                    "tipoImpressao": "DANFE_NORMAL_RETRATO",
                                    "tipoEmissao": "EMISSAO_NORMAL",
                                    "digitoVerificador": 5,
                                    "ambiente": "HOMOLOGACAO",
                                    "finalidade": "NORMAL",
                                    "operacaoConsumidorFinal": "SIM",
                                    "indicadorPresencaComprador": "NAO_APLICA",
                                    "programaEmissor": "CONTRIBUINTE",
                                    "versaoEmissor": "1.0"
                                },
                                "emitente": {                   # Alterado manualmente
                                    "cnpj": "27578708000180",   # https://www.4devs.com.br/gerador_de_empresas
                                    "razaoSocial": "Oliver e Ana Pizzaria ME",
                                    "nomeFantasia": "Oliver e Ana Pizzaria ME",
                                    "endereco": {
                                        "logradouro": "Núcleo Rural Vargem Bonita Rua 3 Chácara 45",
                                        "numero": "447",
                                        "complemento": "SEM COMPLEMENTO",
                                        "bairro": "Núcleo Rural Vargem Bonita (Núcleo Bandeirante)",
                                        "codigoMunicipio": "5300108",
                                        "descricaoMunicipio": "Brasilia",
                                        "uf": "DF",
                                        "cep": "71751490",
                                        "codigoPais": "BRASIL",
                                        "descricaoPais": "BRASIL",
                                        "telefone": "6126807196"
                                    },
                                    "inscricaoEstadual": "0715935300115",
                                    "inscricaoMunicipal": "0715935300115",
                                    "classificacaoNacionalAtividadesEconomicas": "8512100",
                                    "regimeTributario": "SIMPLES_NACIONAL"
                                },
                                "destinatario": {               # Alterado manualmente
                                    "cpf": "01330291158",       # https://www.4devs.com.br/gerador_de_pessoas
                                    "razaoSocial": "NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL",
                                    "endereco": {
                                        "logradouro": "Quadra EQNO 4/6 Bloco A",
                                        "numero": "879",
                                        "bairro": "Ceilândia Norte (Ceilândia)",
                                        "codigoMunicipio": "5300108",
                                        "descricaoMunicipio": "Brasilia",
                                        "uf": "DF",
                                        "cep": "72250541",
                                        "codigoPais": "BRASIL",
                                        "descricaoPais": "BRASIL"
                                    },
                                    "indicadorIEDestinatario": "NAO_CONTRIBUINTE"
                                },
                                "itens": [
                                    {
                                        "numeroItem": 1,
                                        "produto": {
                                            "codigo": "123456",
                                            "codigoDeBarrasGtin": "SEM GTIN",
                                            "descricao": "UNIFORMES",
                                            "ncm": "62069000",
                                            "cfop": "5102",
                                            "unidadeComercial": "UNID",
                                            "quantidadeComercial": "2",
                                            "valorUnitario": "2",
                                            "valorTotalBruto": "2.00",
                                            "codigoDeBarrasGtinTributavel": "SEM GTIN",
                                            "unidadeTributavel": "UNID",
                                            "quantidadeTributavel": "2",
                                            "valorUnitarioTributavel": "2",
                                            "compoeValorNota": "SIM",
                                            "numeroPedidoItemCliente": 1
                                        },
                                        "imposto": {
                                            "valorTotalTributos": "0.51",
                                            "icms": {
                                                "isSelecionado": False,
                                                "icmssn102": {
                                                    "origem": "NACIONAL",
                                                    "situacaoOperacaoSN": "TRIBUTADA_SEM_PERMISSAO_CREDITO"
                                                }
                                            },
                                            "ipi": {
                                                "quantidadeSelo": 0,
                                                "codigoEnquadramento": "999",
                                                "tributado": {
                                                    "situacaoTributaria": "OUTRAS_SAIDAS",
                                                    "valorBaseCalculo": "0.00",
                                                    "percentualAliquota": "0.00",
                                                    "valorTributo": "0.00"
                                                }
                                            },
                                            "pis": {
                                                "outrasOperacoes": {
                                                    "situacaoTributaria": "OUTRAS_OPERACOES",
                                                    "valorBaseCalculo": "0.00",
                                                    "percentualAliquota": "0.00",
                                                    "valorTributo": "0.00"
                                                }
                                            },
                                            "cofins": {
                                                "outrasOperacoes": {
                                                    "situacaoTributaria": "OUTRAS_OPERACOES",
                                                    "valorBaseCalculo": "0.00",
                                                    "percentualCOFINS": "0.00",
                                                    "valorCOFINS": "0.00"
                                                }
                                            }
                                        },
                                        "informacoesAdicionais": "EMITIDO MANUALMENTE NO HOMOLOG ARKA"
                                    }
                                ],
                                "total": {
                                    "icmsTotal": {
                                        "baseCalculoICMS": "0.00",
                                        "valorTotalICMS": "0.00",
                                        "valorICMSDesonerado": "0.00",
                                        "valorICMSFundoCombatePobreza": "0.00",
                                        "valorICMSPartilhaDestinatario": "0.00",
                                        "valorICMSPartilhaRementente": "0.00",
                                        "valorTotalFundoCombatePobreza": "0.00",
                                        "baseCalculoICMSST": "0.00",
                                        "valorTotalICMSST": "0.00",
                                        "valorTotalFundoCombatePobrezaST": "0.00",
                                        "valorTotalFundoCombatePobrezaSTRetido": "0.00",
                                        "valorTotalDosProdutosServicos": "2.00",
                                        "valorTotalFrete": "0.00",
                                        "valorTotalSeguro": "0.00",
                                        "valorTotalDesconto": "0.00",
                                        "valorTotalII": "0.00",
                                        "valorTotalIPI": "0.00",
                                        "valorTotalIPIDevolvido": "0.00",
                                        "valorPIS": "0.00",
                                        "valorCOFINS": "0.00",
                                        "outrasDespesasAcessorias": "0.00",
                                        "valorTotalNFe": "2.00",
                                        "valorTotalTributos": "0.51"
                                    }
                                },
                                "transporte": {
                                    "modalidadeFrete": "SEM_OCORRENCIA_TRANSPORTE"
                                },
                                "pagamento": {
                                    "detalhamentoFormasPagamento": [
                                        {
                                            "indicadorFormaPagamento": "A_VISTA",
                                            "meioPagamento": "DINHEIRO",
                                            "valorPagamento": "1.00"
                                        }
                                    ]
                                },
                                "informacoesAdicionais": {
                                    "informacoesComplementaresInteresseContribuinte": "Procon - 151 Endereço do Procon - Shopping Venâncio, Setor Comercial Sul Q. 6 - Brasilia, DF, CEP 70308-200nEMPRESA ENQUADRADA NO SIMPLES NACIONAL LC 123/2006nEssa NF foi emitida de forma manual no homolog.arkaonline para teste da API"
                                },
                                "informacaoResposavelTecnico": {    # https://www.4devs.com.br/gerador_de_pessoas
                                    "cnpj": "89281646000106",
                                    "contatoNome": "Márcio Martin Alexandre Almeida",
                                    "email": "marciomartinalmeida@viacorte.com.br",
                                    "telefone": "61986997818"
                                }
                            },
                            "assinatura": {
                                "signedInfo": {
                                    "canonicalizationMethod": {
                                        "algorithm": "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
                                    },
                                    "signatureMethod": {
                                        "algorithm": "http://www.w3.org/2000/09/xmldsig#rsa-sha1"
                                    },
                                    "reference": {
                                        "uri": "#NFe53230500665143000112550010000040441235246385",
                                        "transform": [
                                            {
                                                "algorithm": "http://www.w3.org/2000/09/xmldsig#enveloped-signature"
                                            },
                                            {
                                                "algorithm": "http://www.w3.org/TR/2001/REC-xml-c14n-20010315"
                                            }
                                        ],
                                        "digestMethod": {
                                            "algorithm": "http://www.w3.org/2000/09/xmldsig#sha1"
                                        },
                                        "digestValue": "JvO8YEHQBA+s4sRr3Dih50k+ZQs="
                                    }
                                },
                                "signatureValue": "ftzKexUZpVnWsrsxVXVpYdQwzdXWKTDCcuwPfCwX7ERhLYQglSm/HmoT7JmfYNrmdLV7cpqGclOF\r\n7i7ksF7Tz/7rhgHwvBk7e7LKQHYq90vLJcdYIXOxCVzBVL02MZijHGAu39/1QqTeSf28zIWXmQTQ\r\nwF51ROJM9a8RUieXUTIuaerkOnn4+WsiSlH5OHEfwN0nEtyI4Vkf/yHyrlyoiMxS6fADmdARQec3\r\n9pGv4XAHzc/jA6r3ltwtDGFj6okIiuUcIPjv4Nyjt7RB2u70394+ICaZ3ljzZ2NsyZDFtdvCUlJw\r\nuUtA32r/59FLOGkLg+3Bt+UpINrtOCdU5XV89w==", # Alterado manualmente
                                "keyInfo": {
                                    "data": {
                                        "x509certificate": "MIIHjTCCBXWgAwIBAgIIS+ibNksbp/kwDQYJKoZIhvcNAQELBQAwczELMAkGA1UEBhMCQlIxEzAR\r\nBgNVBAoTCklDUC1CcmFzaWwxNjA7BgNVBAsTLVNlY3JldGFyaWEgZGEgUmVjZWl0YSBGZWRlcmFs\r\nIGRvIEJyYXNpbCAtIFJGQjEXMBUGA1UEAxMOQUMgTElOSyBSRkIgdjIwHhcNMjIwNzE4MjA1NDQx\r\nWhcNMjMwNzE4MjA1NDQxWjCB8TELMAkGA1UEBhMCQlIxEzARBgNVBAoTCklDUC1CcmFzaWwxCzAJ\r\nBgNVBAgTAkRGMREwDwYDVQQHEwhCUkFTSUxJQTEXMBUGA1UECxMOMjE2MTIwMDMwMDAxNTYxNjA0\r\nBgNVBAsTLVNlY3JldGFyaWEgZGEgUmVjZWl0YSBGZWRlcmFsIGRvIEJyYXNpbCAtIFJGQjEWMBQG\r\nA1UECxMNUkZCIGUtQ05QSiBBMTEZMBcGA1UECxMQdmlkZW9jb25mZXJlbmNpYTEpMCcGA1UEAxMg\r\nQ09MRUdJTyBFU1BVIExUREE6MDA2NjUxNDMwMDAxMTIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAw\r\nggEKAoIBAQDCoJD42LjnJDtsYxE48F3ABNkTcfj8mJRWav6DIzVE8ZLbqIwqSWydfo1rcmBh3DUa\r\nVqJQeay77eSM54tmlLihb9a+fHlsNNU5SI5xMwxALO3+l7BP+sfMf6zB8xKBZAMNlUH3PjXY6iW9\r\nEC6/DooRAZxrgOkmLNbCtifRyY4M6EktQTGnqi9qE63+DDLfDGld1kflgGZ7IuUprjaAI76sgwr2\r\nmXCswRcOEh4gxLewIyPwOiaBBAeEytVsbWGMCpIEzLBvwtFzP8QPrIITXwsDSDH6k/FvxwRzUyk2\r\niwT+aBV9pFkvCp2Zpu1wvpiUy2ukO265wlRChQljdkgmia85AgMBAAGjggKkMIICoDAfBgNVHSME\r\nGDAWgBQN39ZH9BNO5SJYMixmpucu5Fe8AjAOBgNVHQ8BAf8EBAMCBeAwbgYDVR0gBGcwZTBjBgZg\r\nTAECATswWTBXBggrBgEFBQcCARZLaHR0cDovL3JlcG9zaXRvcmlvLmxpbmtjZXJ0aWZpY2FjYW8u\r\nY29tLmJyL2FjLWxpbmtyZmIvYWMtbGluay1yZmItcGMtYTEucGRmMIGwBgNVHR8EgagwgaUwUKBO\r\noEyGSmh0dHA6Ly9yZXBvc2l0b3Jpby5saW5rY2VydGlmaWNhY2FvLmNvbS5ici9hYy1saW5rcmZi\r\nL2xjci1hYy1saW5rcmZidjUuY3JsMFGgT6BNhktodHRwOi8vcmVwb3NpdG9yaW8yLmxpbmtjZXJ0\r\naWZpY2FjYW8uY29tLmJyL2FjLWxpbmtyZmIvbGNyLWFjLWxpbmtyZmJ2NS5jcmwwYgYIKwYBBQUH\r\nAQEEVjBUMFIGCCsGAQUFBzAChkZodHRwOi8vcmVwb3NpdG9yaW8ubGlua2NlcnRpZmljYWNhby5j\r\nb20uYnIvYWMtbGlua3JmYi9hYy1saW5rcmZidjUucDdiMIG7BgNVHREEgbMwgbCBGlZJTklDSVVT\r\nQ0NPU1RBOTVAR01BSUwuQ09NoCQGBWBMAQMCoBsTGUlFREEgQ0FSVkFMSE8gTk9CUkUgQ09TVEGg\r\nGQYFYEwBAwOgEBMOMDA2NjUxNDMwMDAxMTKgOAYFYEwBAwSgLxMtMTAwNzE5NjQzMDg0ODE0ODEz\r\nNDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwoBcGBWBMAQMHoA4TDDAwMDAwMDAwMDAwMDAdBgNV\r\nHSUEFjAUBggrBgEFBQcDAgYIKwYBBQUHAwQwCQYDVR0TBAIwADANBgkqhkiG9w0BAQsFAAOCAgEA\r\nXTlg0wxx5rXFSZxazn7Jp64G2eceqXdSH1PYMQShiRb5SCzEKGIpjc5dnVO/oE7/K8VEutjPE9c1\r\nlo/BvIgNrBrLZtMvmfrX/zqxAF1tgoMVkyj6hcJqGlFfBS9ioxnJXoKNlj5YC3OMBmEorgjf8+Z8\r\nP4uZJ364d8+nMfnNWPCjjsgwN5v/Xfqs7uU7CrelPqaQcPrfG7nsRmSJfE52FGgvYoTb33RMg5C/\r\nIwL9CbaQ4gJIFga2JP9kUZIZKg0ndT82V82LCg66ex0A6Nb0nRGsDEQR9V/xlbwNieB2I6vdC4Zs\r\nLva+KZI5Jdykvx3IQe7FHeCQzjifU7liUdUfX62ndHXM8h1hjkQfJl1WUaoa0dEqtI38KvMC64yN\r\n0Npg2an2s16MimX4L+WQA5wh5wMLmqMAnDeIaXnzZM14vyiD+fPsD6XMqez7DSP81jJtzGO+sRDB\r\nn+bzjb65JtTp+nPt+9a9Y79vegeEQbKB7qn7AP3gL7aErxocwmZc6zpTxSKHjSXrFTq4PGOEsve/\r\n3lexnJyLq777pWi7eRfkAO7PdCPbNw+ZtR7JT7AVFRAynW5uVm7WHybDnITmv7+rrxurtnwKdP7C\r\n9VMFavxpDPMEomKz1nw/7iv0eiYZNRaobYjqZ7tGpRgPyBu7DNqrmAXc7Bi1KoLeoYp7cSv77C7=" # Alterado manualmente
                                    }
                                }
                            }
                        }
                    ]
                }
            },
            "dados": "53230500665143000112550017777740441235246385" # Alterado manualmente
        }

        requests.post = MagicMock(return_value=mock_response)

        # Chamando a Função:
        result = await nfe.emitir(token_emissor='token', token_secret_emissor='token-secret', objetoNfe=self.objeto, tipo_emissao='1', token_empresa="token_empresa", token_secret_empresa="token_secret_empresa")

        # Checando resultado:
        self.assertIn('status', result)
        self.assertIn('descricao', result)
        self.assertIn('retorno_sefaz', result)
        self.assertIn('dados', result)

        self.assertEqual(result['status'], 'Sucesso', )
        self.assertEqual(result['descricao'], 'Lote enviado com sucesso.')

    async def test_emitir_nota_ja_autorizada(self):
        """Função que simula a tentativa de emissão de uma nota fiscal já autorizada, utilizando dados falsos.

            O endpoint requer o número da nota fiscal como um dos parâmetro e
            se um número correspondente a uma nota fiscal autorizada for fornecido, a API retornará um erro.

            É importante observar que se trata de uma nota fiscal já **autorizada**,
            pois, é possível reenviar a mesma nota fiscal após ser rejeitada pela SEFAZ,
            permitindo ao usuário realizar alterações nos campos pertinentes e tentar emiti-la novamente.
        """

        # Mocking:
        mock_response = MagicMock()
        mock_response.status_code = 412
        mock_response.json.return_value = {
            "status": "Erro",
            "descricao": "Tentativa de retransmitir uma nota que não foi rejeitada.",
        }

        requests.post = MagicMock(return_value=mock_response)

         # Chamando a Função:
        result = await nfe.emitir(token_emissor='token', token_secret_emissor='token-secret', objetoNfe=self.objeto, tipo_emissao='1', token_empresa="token_empresa", token_secret_empresa="token_secret_empresa")

        # Checando resultado:
        self.assertIn('status', result)
        self.assertIn('descricao', result)

        self.assertEqual(result['status'], 'Erro')
        self.assertEqual(result['descricao'], 'Tentativa de retransmitir uma nota que não foi rejeitada.')

# =================================================================
# Models:
class ObjetoEmissaoNFeTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.endereco = Endereco (
            codigo_pais         = '1058',
            descricao_pais      = 'Brasil',
            uf                  = 'DF',
            codigo_municipio    = '5300108',
            descricao_municipio = 'Brasilia',
            cep                 = '70634300',
            bairro              = 'Zona Industrial',
            logradouro          = 'Quadra SOFN Quadra 3',
            numero              = '484',
            complemento         = 'Gerado por 4devs',
        )

        self.cliente  = Cliente(
            consumidor_final = '1',
            contribuinte     = '9',
            pessoa_fisica    = PessoaFisica(nome_completo="Vicente Marcos Samuel Nunes", cpf='44301337199'),
            endereco         = self.endereco,
        )

        self.impostos = nfe.ImpostosProduto(
            pis    = Pis (
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            cofins = Cofins(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            icms   = Icms (
                situacao_tributaria='102',
                aliquota_icms='0.0000',
                aliquota_icms_st='0.0000',
            ),
            ipi    = Ipi(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
        )

        self.produtos = [
            nfe.Produto(
                cfop                   = '5102',
                item                   = "1",
                nome                   = "UNIFORMES",
                codigo                 = "123456",
                ncm                    = "62069000",
                quantidade             = "2.0",
                unidade                = "UNID",
                subtotal               = "5.0",
                total                  = "10.0",
                impostos               = self.impostos,
                informacoes_adicionais = "Emitido pelo pySisnoAPI",
            ),
        ]

        self.pagamento = nfe.Pagamento(
            formas_pagamento = [
                nfe.FormaPagamento(
                    forma_pagamento='0',
                    meio_pagamento='01',
                    valor_pagamento='1.0'
                )
            ]
        )

        self.pedido   = nfe.Pedido(
            presenca='0',
            pagamento=self.pagamento,
            informacoes_complementares='Procon - 151 Endereço do Procon - Shopping Venâncio, Setor Comercial Sul Q. 6 - Brasilia, DF, CEP 70308-200nEMPRESA ENQUADRADA NO SIMPLES NACIONAL LC 123/2006n',
        )

        self.data = datetime(2023, 5, 19, 17, 25, 57)

    def test_todos_campos_obrigatorios(self):
        objeto = nfe.ObjetoEmissaoNFe (
            numero_nota_sequencial = '123456',
            serie                  = '1',
            operacao               = '1',
            natureza_operacao      = 'NATUREZA',
            modelo                 = '55',
            finalidade             = '1',
            ambiente               = '2',
            cliente                = self.cliente,
            produtos               = self.produtos,
            pedido                 = self.pedido,
            data_entrada_saida     = self.data,
            data_emissao           = self.data,
        )

        assert objeto.numero_nota_sequencial == "123456"
        assert objeto.serie                  == "1"
        assert objeto.operacao               == "1"
        assert objeto.natureza_operacao      == "NATUREZA"
        assert objeto.modelo                 == "55"
        assert objeto.finalidade             == "1"
        assert objeto.ambiente               == "2"
        assert objeto.cliente                == self.cliente
        assert objeto.produtos               == self.produtos
        assert objeto.pedido                 == self.pedido
        assert objeto.data_entrada_saida     == self.data
        assert objeto.data_emissao           == self.data

        assert objeto.numero_pedido            is None
        assert objeto.transporte               is None
        assert objeto.fatura                   is None
        assert objeto.parcelas                 is None
        assert objeto.exportacao               is None
        assert objeto.nfe_referenciada         is None
        assert objeto.retirada                 is None
        assert objeto.entrega                  is None
        assert objeto.compra                   is None
        assert objeto.indicador_intermediador  is None
        assert objeto.informacao_intermediador is None

    def test_campo_obrigatorio_numero_sequencial(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_serie(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_operacao(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_natureza_operacao(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_modelo(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_finalidade(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_ambiente(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_cliente(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_produtos(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_pedido(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                data_entrada_saida     = self.data,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_data_entrada_saida(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_emissao           = self.data,
            )

    def test_campo_obrigatorio_emissao(self):
        with self.assertRaises(ValidationError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial = '123456',
                serie                  = '1',
                operacao               = '1',
                natureza_operacao      = 'NATUREZA',
                modelo                 = '55',
                finalidade             = '1',
                ambiente               = '2',
                cliente                = self.cliente,
                produtos               = self.produtos,
                pedido                 = self.pedido,
                data_entrada_saida     = self.data,
            )

    def test_numero_nota_sequencial_menor_que_1_caracter(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '',
                serie                 = '1',
                operacao              = '1',
                natureza_operacao     = 'NATUREZA',
                modelo                = '55',
                finalidade            = '1',
                ambiente              = '2',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )

    def test_numero_nota_sequencial_maior_que_9_caracteres(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '0123456789',
                serie                 = '1',
                operacao              = '1',
                natureza_operacao     = 'NATUREZA',
                modelo                = '55',
                finalidade            = '1',
                ambiente              = '2',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )

    def test_operacao_invalida(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '123456',
                serie                 = '1',
                operacao              = '',
                natureza_operacao     = 'NATUREZA',
                modelo                = '55',
                finalidade            = '1',
                ambiente              = '2',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )

    def test_modelo_invalido(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '123456',
                serie                 = '1',
                operacao              = '1',
                natureza_operacao     = 'NATUREZA',
                modelo                = '',
                finalidade            = '1',
                ambiente              = '2',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )

    def test_finalidade_invalida(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '123456',
                serie                 = '1',
                operacao              = '1',
                natureza_operacao     = 'NATUREZA',
                modelo                = '55',
                finalidade            = '',
                ambiente              = '2',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )

    def test_ambiente_invalido(self):
        with self.assertRaises(ValueError):
            nfe.ObjetoEmissaoNFe (
                numero_nota_sequencial= '123456',
                serie                 = '1',
                operacao              = '1',
                natureza_operacao     = 'NATUREZA',
                modelo                = '55',
                finalidade            = '1',
                ambiente              = '',
                cliente               = self.cliente,
                produtos              = self.produtos,
                pedido                = self.pedido,
                data_entrada_saida    = self.data,
                data_emissao          = self.data,
            )

class PagamentoUnitTest(unittest.TestCase):
    def setUp(self) -> None:
        self.forma_pgto = nfe.FormaPagamento (
            forma_pagamento = '0',
            meio_pagamento  = '01',
            valor_pagamento = '1.00',
        )

    def test_todos_campos_obrigatorios(self):
        pagamento = nfe.Pagamento (
            formas_pagamento = [
                self.forma_pgto,
                self.forma_pgto,
            ]
        )

        self.assertEqual(len(pagamento.formas_pagamento), 2)

class FormaPagamentoUnitTest(unittest.TestCase):
    def test_todos_campos_obrigatorios(self):
        forma_pgto = nfe.FormaPagamento (
            forma_pagamento = '0',
            meio_pagamento  = '01',
            valor_pagamento = '1.00',
        )

        self.assertEqual(forma_pgto.forma_pagamento, '0')
        self.assertEqual(forma_pgto.meio_pagamento , '01')
        self.assertEqual(forma_pgto.valor_pagamento, '1.00')

    def test_campo_obrigatorio_forma_pagamento(self):
        with self.assertRaises(ValidationError):
            nfe.FormaPagamento(
                meio_pagamento  = '01',
                valor_pagamento = '1.00',
            )

    def test_campo_obrigatorio_meio_pagamento(self):
        with self.assertRaises(ValidationError):
            nfe.FormaPagamento(
                forma_pagamento = '0',
                valor_pagamento = '1.00',
            )

    def test_campo_obrigatorio_valor_pagamento(self):
        with self.assertRaises(ValidationError):
            nfe.FormaPagamento(
                forma_pagamento = '0',
                meio_pagamento  = '01',
            )

    def test_forma_pagamento_invalido(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento = '',
                meio_pagamento  = '01',
                valor_pagamento = '1.00',
            )

    def test_meio_pagamento_invalido(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento = '0',
                meio_pagamento  = '',
                valor_pagamento = '1.00',
            )

    def test_descricao_obrigatorio(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento = '0',
                meio_pagamento  = '99',
                valor_pagamento = '1.00'
            )

    def test_tamanho_descricao_menor_que_dois(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento          = '0',
                meio_pagamento           = '99',
                valor_pagamento          = '1.00',
                descricao_meio_pagamento = 'a',
            )

    def test_tamanho_descricao_maior_que_sessenta(self):
        with self.assertRaises(ValueError):
            nfe.FormaPagamento (
                forma_pagamento          = '0',
                meio_pagamento           = '99',
                valor_pagamento          = '1.00',
                descricao_meio_pagamento = 'x'*70,
            )

class ProdutoUnitTest(unittest.TestCase):
    """Testes da classe produtos"""

    def setUp(self) -> None:
        self.impostos = nfe.ImpostosProduto(
            pis    = Pis (
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            cofins = Cofins(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
            icms   = Icms (
                situacao_tributaria='102',
                aliquota_icms='0.0000',
                aliquota_icms_st='0.0000',
            ),
            ipi    = Ipi(
                situacao_tributaria='99',
                aliquota='0.0000',
            ),
        )

    def test_todos_campos_obrigatorios(self):
        produto = nfe.Produto(
            item       = "1",
            cfop       = '5102',
            nome       = "UNIFORMES",
            codigo     = "123456",
            ncm        = "62069000",
            quantidade = "2.0",
            unidade    = "UNID",
            subtotal   = "5.0",
            total      = "10.0",
            impostos   = self.impostos,
        )

        self.assertEqual(produto.cfop      , '5102')
        self.assertEqual(produto.item      , '1')
        self.assertEqual(produto.nome      , 'UNIFORMES')
        self.assertEqual(produto.codigo    , '123456')
        self.assertEqual(produto.ncm       , '62069000')
        self.assertEqual(produto.quantidade, '2.0')
        self.assertEqual(produto.unidade   , 'UNID')
        self.assertEqual(produto.subtotal  , '5.0')
        self.assertEqual(produto.total     , '10.0')
        self.assertEqual(produto.impostos  , self.impostos)

    def test_campo_obrigatorio_item(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (

                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "5.0",
                total      = "10.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_cfop(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",

                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "5.0",
                total      = "10.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_nome(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',

                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "5.0",
                total      = "10.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_codigo(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",

                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "5.0",
                total      = "10.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_ncm(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",

                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "5.0",
                total      = "10.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_quantidade(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",

                unidade    = "UNID",
                subtotal   = "5.0",
                total      = "10.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_unidade(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",

                subtotal   = "5.0",
                total      = "10.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_subtotal(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",

                total      = "10.0",
                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_total(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "5.0",

                impostos   = self.impostos,
            )

    def test_campo_obrigatorio_impostos(self):
        with self.assertRaises(ValidationError):
            nfe.Produto (
                item       = "1",
                cfop       = '5102',
                nome       = "UNIFORMES",
                codigo     = "123456",
                ncm        = "62069000",
                quantidade = "2.0",
                unidade    = "UNID",
                subtotal   = "5.0",
                total      = "10.0",

            )

# =================================================================
if __name__ == "__main__":
    unittest.main()

# =================================================================
