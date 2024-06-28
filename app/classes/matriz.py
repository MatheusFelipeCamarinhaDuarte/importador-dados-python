import os
import xml.etree.ElementTree as ET
from tkinter import messagebox
from app.classes.banco_de_dados import Banco_de_dados



class Matriz():
    def __init__(self, migracao:str='', sistema_origem:str='', sistema_destino:str='', extensao:str='', banco:Banco_de_dados = None, cod_filial:str = None):
        self.migracao = migracao
        self.sistema_origem = sistema_origem
        self.sistema_destino = sistema_destino
        self.extensao = extensao
        self.banco = banco
        self.cod_filial = cod_filial
    def filtro_de_importacao(self) -> list:
        """Função com o intuito de ser um filtro com base nas informações coletadas
        anteriormente, como o tipo de migração, o sistema de origem e destino e o
        sistema de destino e por fim a extensão

        Returns:
            list: retorna a matriz gerada pelo sistema
        """
        migracao = self.migracao
        sistema_origem = self.sistema_origem 
        extensao = self.extensao
        banco = self.banco
        mensagem = lambda: messagebox.showerror("Erro", f"Tipo de importação >>{migracao.upper()}<< ERRADA. Sistema de Origem >>{sistema_origem.upper()}<< ERRADO. Tipo de extenção >>{extensao.upper()}<< ERRADA.") 
        match sistema_origem:
            case 'Autosystem': mensagem()
            case 'Posto Fácil': return self.Posto_facil(migracao,extensao,banco,self.cod_filial).processar_dados()
            case 'Seller': return self.Seller(migracao,extensao,banco).processar_dados()
            case 'outros': mensagem()
            case _: mensagem()
    class Seller:
        def __init__(self, migracao:str = '', extensao:str = '', banco:Banco_de_dados = None):
            self.migracao = migracao
            self.extensao = extensao
            self.banco = banco

        def processar_dados(self):
            mensagem = lambda: messagebox.showerror("Erro", f"Tipo de importação {self.migracao} ERRADA. Sistema de Origem >>SELLER<< ERRADO. Tipo de extenção {self.extensao} ERRADA.")
            match self.migracao:
                case 'PRODUTOS': 
                    match self.extensao:
                        case '.xml': return self.produto_xml()
                        case _:       mensagem()
                case 'CLIENTES': 
                    match self.extensao:
                        case '.xml':  mensagem()
                        case '.csv':  mensagem()
                        case '.xls':  mensagem()
                        case 'banco': mensagem()
                        case _:       mensagem()
                case 'ESTOQUE': 
                    match self.extensao:
                        case '.xml':  mensagem()
                        case '.csv':  mensagem()
                        case '.xls':  mensagem()
                        case 'banco': mensagem()
                        case _:       mensagem()
                case _:               mensagem()

        def produto_xml(self) -> list[list]:
            """Função que recupera o arquivo temporário de produtos em xml
            e converte para o formato padrão de matriz, logo em seguida o excluindo.

            Returns:
                list[list]: Retorna a matriz básica.
            """
            from app.classes.correcoes import Correcao
            # Caminho completo para o arquivo XML
            correcao = Correcao()
            caminho_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            caminho_dados = os.path.join(caminho_app,'temp','dados')
            # Aqui preciso passar o arquivo recebido por XML    
            xml_file = os.path.join(caminho_dados,'arquivo_temporario.xml')
            try:
                # Parse o XML
                tree = ET.parse(xml_file)
                root = tree.getroot()
                # Inicializa a matriz para armazenar os dados
                matriz = []
                # Itera sobre os elementos 'Group'
                for group in root.findall('.//{urn:crystal-reports:schemas:report-detail}Group'):
                    row = []
                    # Itera sobre os elementos 'Field' dentro de 'GroupHeader'
                    for field in group.find('.//{urn:crystal-reports:schemas:report-detail}GroupHeader').iter('{urn:crystal-reports:schemas:report-detail}Field'):
                        value_element = field.find('{urn:crystal-reports:schemas:report-detail}Value')
                        value = value_element.text if value_element is not None else ' '  # Substitui por " " se não encontrar valor
                        row.append(value)
                    
                    # Itera sobre os elementos 'Field' dentro de cada 'Details'
                    for details in group.findall('.//{urn:crystal-reports:schemas:report-detail}Details'):
                        for field in details.iter('{urn:crystal-reports:schemas:report-detail}Field'):
                            value_element = field.find('{urn:crystal-reports:schemas:report-detail}Value')
                            value = value_element.text if value_element is not None else ' '  # Substitui por " " se não encontrar valor
                            row.append(value)
                    
                    # Substitui None por uma string vazia
                    row = [value if value is not None else '' for value in row]
                    # Adiciona a linha à matriz
                    matriz.append(row)
                # Matriz correta no formato padrão
                nova_matriz = []
                # Converter matriz para o formato padrao
                for linha in matriz:
                    linha_da_nova_matriz = []
                    linha_da_nova_matriz.append(linha[0]) # 0 - codigo barra
                    linha_da_nova_matriz.append(correcao.corrigir_nome_acentos(linha[1].strip())) # 1 - descricao do produto         
                    estrutura = linha[8]
                    lista = estrutura.split('/')
                    linha_da_nova_matriz.append(correcao.corrigir_nome_acentos(lista[0])) # 2 - grupo                
                    linha_da_nova_matriz.append(correcao.corrigir_nome_acentos(lista[1])) # 3 - subgrupo
                    linha_da_nova_matriz.append(linha[3]) # 4 - preço da venda
                    linha_da_nova_matriz.append(linha[5]) # 5 - preco de compra
                    linha_da_nova_matriz.append(correcao.corrigir_unidade(linha[4])) # 6 - unidade de medida de venda
                    linha_da_nova_matriz.append(correcao.corrigir_unidade(linha[6])) # 7 - Unidade de medida de compra
                    linha_da_nova_matriz.append(linha[9]) # 8 -fator de conversao
                    codigo = linha[2]
                    linha_da_nova_matriz.append(codigo[:4] + '.' + codigo[4:6] +'.' + codigo[6:]) # 9 - NCM
                    tributacao = linha[14]
                    if tributacao != '':
                        tributacao = tributacao.replace(" ","").split('-')
                        tributacao = '0'+tributacao[0]
                    linha_da_nova_matriz.append(tributacao) # 10 - Tributacao
                    linha_da_nova_matriz.append('99') # 11 - cst_pis (int)
                    linha_da_nova_matriz.append('99') # 12 - cst_cofins (int)
                    linha_da_nova_matriz.append('98') # 13 - cst_pis_entrada (int)
                    linha_da_nova_matriz.append('98') # 14 - cst_cofins_entrada (int)
                    linha_da_nova_matriz.append('') # 15 - Natureza de receita (int)
                    
                    nova_matriz.append(linha_da_nova_matriz)
                if os.path.exists(xml_file):
                    os.remove(xml_file)
                # Retorna nova a matriz
                return nova_matriz


            except:
                messagebox.showerror("Erro", f'O XML apontado não é válido! olha a aba "Como retirar relatórios no formato correto" para obter o arquivo certo.')
                if os.path.exists(xml_file):
                    os.remove(xml_file)

        def produto_banco(self):
            variavel = False
            if variavel:
                return
            else:
                if self.banco:
                    banco = self.banco
                    query = 'SELECT codigo_barra,nome,grupo_produto_id,XXX,preco_unit,XXX,unid_med,XXX,XXX,codigo_ncm FROM dataload.produto' 
                    """
                    - 0 - codigo de barras (str - número)
                    - 1 - descricao do produto (str)
                    - 2 - grupo (grid)
                    - 3 - subgrupo (grid) XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    - 4 - preço de venda (double)
                    - 5 - preço de compra (double) XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    - 6 - unidade de medida de compra (abreviação)
                    - 7 - unidade de medida de venda (abreviação) XXXXXXXXXXXXXXXXXXX
                    - 8 - fator de conversao (int) XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
                    - 9 - codigo ncm (xxxx.xx.xx)
                    - 10 - tributacao (int)
                    - 11 - cst_pis (int)
                    - 12 - cst_cofins (int)
                    - 13 - cst_pis_entrada (int)
                    - 14 - cst_cofins_entrada (int)
                    - 15 - natureza_de_receuta (int)

                    """ 
                    produtos = banco.executar_query(query)
                    
                else: return

    class Posto_facil:
        def __init__(self, migracao:str = '', extensao:str = '', banco:Banco_de_dados = None, cod_filial:str = None):
            self.migracao = migracao
            self.extensao = extensao
            self.banco = banco
            self.cod_filial = cod_filial

        def processar_dados(self):
            mensagem = lambda: messagebox.showerror("Erro", f"Tipo de importação {self.migracao} ERRADA. Sistema de Origem >>POSTO FÁCIL<< ERRADO. Tipo de extenção {self.extensao} ERRADA.")
            match self.migracao:
                case 'PRODUTOS': 
                    match self.extensao:
                        case '.xml':  mensagem()
                        case '.csv':  mensagem()
                        case '.xls':  mensagem()
                        case 'banco': return self.produto_banco()
                        case _:       mensagem()
                case 'CLIENTES': 
                    match self.extensao:
                        case '.xml':  mensagem()
                        case '.csv':  mensagem()
                        case '.xls':  mensagem()
                        case 'banco': mensagem()
                        case _:       mensagem()
                case 'ESTOQUE': 
                    match self.extensao:
                        case '.xml':  mensagem()
                        case '.csv':  mensagem()
                        case '.xls':  mensagem()
                        case 'banco': mensagem()
                        case _:       mensagem()
                case _:               mensagem()

        def produto_banco(self):
            try:
                if self.banco:
                    banco = self.banco        
                    query_empresa = f"SELECT EMPRESA_ID FROM EMPRESA where NOM_EMPRESA = '{self.cod_filial}'"
                    banco.cursor.execute(query_empresa)
                    resultado = banco.cursor.fetchall()
                    
                    query = (f"select CB.COD_BARRA, " +
                            "PP.DESCRICAO, " +
                            "PNN.DESCRICAO, " +
                            "PN.DESCRICAO, " +
                            "PE.PRC_VEN_VISTA, " +
                            "PE.PRC_CUSTO, " +
                            "PP.UND_VENDA, " +
                            "PP.UND_MEDIDA, " +
                            "PP.QTD_CAIXA, " +
                            "PP.CODIGO_NCM, " +
                            "PP.CT, " +
                            "PP.cst_pis_cofins, " +
                            
                            "PP.cst_pis_cofins_entrada, " +
                            "NR.codigo " +
                            "from PRODUTO_EMPRESA PE " +
                            "left join PRODUTO PP on PP.PRODUTO_ID = PE.PRODUTO_ID " +
                            "left join PRODUTO_NIVEL2 PN on PN.PRODUTO_NIVEL2_ID = PP.PRODUTO_NIVEL2_ID " +
                            "left join PRODUTO_NIVEL1 PNN on PNN.PRODUTO_NIVEL1_ID = PN.PRODUTO_NIVEL1_ID " +
                            "left join COD_BARRA_PRODUTO CB on CB.PRODUTO_ID = PP.PRODUTO_ID " +
                            "left join naturezas_receita NR ON NR.natureza_receita_id = PP.natureza_receita_id " +
                            f"where PE.EMPRESA_ID = {resultado[0][0]}")
                    banco.cursor.execute(query)
                    resultado = banco.cursor.fetchall()
                    matriz_nova =[]
                    from app.classes.correcoes import Correcao
                    corretor = Correcao()
                    
                    
                    
                    for item  in resultado:
                        linha_matriz = []
                        linha_matriz.append(corretor.corretor_codigo_barra(item[0])) # Codigo de barras
                        linha_matriz.append(corretor.corrigir_nome_acentos(item[1])) # Nome do produto
                        linha_matriz.append(corretor.corrigir_nome_acentos(item[2])) # Nome do grupo
                        linha_matriz.append(corretor.corrigir_nome_acentos(item[3])) # Nome do subgrupo
                        linha_matriz.append(item[4]) # preço de venda do produto
                        linha_matriz.append(item[5]) # preço de compra do produto
                        
                        unidade_venda = corretor.corrigir_unidade_posto_facil(item[6])
                        linha_matriz.append(unidade_venda) # Unidade de medida de compra

                        unidade_compra = corretor.corrigir_unidade_posto_facil(item[7])
                        linha_matriz.append(unidade_compra) # Unidade de medida de venda
                        
                        linha_matriz.append(item[8]) # Fator de conversao
                        
                        linha_matriz.append(item[9]) # Código NCM do produto
                        
                        tributacao = corretor.corrigir_tributacao_posto_facil(item[10])
                        linha_matriz.append(tributacao) # Tributacao
                        cst_pis_cofis = corretor.corrigir_cst_posto_facil(item[11])
                        linha_matriz.append(cst_pis_cofis) # cst_pis
                        linha_matriz.append(cst_pis_cofis) # cst_cofins

                        cst_pis_cofis_entrada = corretor.corrigir_cst_posto_facil(item[12], 'ENTRADA')
                        linha_matriz.append(cst_pis_cofis_entrada) # cst_pis_entrada
                        linha_matriz.append(cst_pis_cofis_entrada) # cst_cofins_entrada
                        linha_matriz.append(item[13]) # natureza_de_receita
                        matriz_nova.append(linha_matriz)
                    return matriz_nova
                    
            except Exception as e:
                messagebox.showerror('ERROR',e)
                return None