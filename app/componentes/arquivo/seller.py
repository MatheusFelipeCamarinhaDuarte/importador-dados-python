import os
import xml.etree.ElementTree as ET
from tkinter import messagebox

def xml_to_matriz_produto() -> list[list]:
    """Função que recupera o arquivo temporário de produtos em xml
    e converte para o formato padrão de matriz, logo em seguida o excluindo.

    Returns:
        list[list]: Retorna a matriz básica.
    """
    from app.classes.correcoes import Correcao
    # Caminho completo para o arquivo XML
    correcao = Correcao()
    caminho_app = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    caminho_dados = os.path.join(caminho_app,'temp','dados')
    
    # Aqui preciso passar o arquivo recebido por XML    
    xml_file = os.path.join(caminho_dados,'arquivo_temporario_produtos.xml')
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
            linha_da_nova_matriz.append('99') # 13 - cst_pis_entrada (int)
            linha_da_nova_matriz.append('99') # 14 - cst_cofins_entrada (int)
            
            nova_matriz.append(linha_da_nova_matriz)
        os.remove(xml_file)
        # Retorna nova a matriz
        return nova_matriz


    except:
        os.remove(xml_file)
        messagebox.showerror("Erro", f'O XML apontado não é válido! olha a aba "Como retirar relatórios no formato correto" para obter o arquivo certo.')

if __name__ == "__main__":
    xml_to_matriz_produto()
