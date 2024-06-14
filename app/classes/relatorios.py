import csv
import os
try:
    from app.classes.manipular_arquivos import Manipular_arquivos
except:
    from app.classes.manipular_arquivos import Manipular_arquivos

class Relatorios(Manipular_arquivos):

    def relatorio_erros_produto(self,relatorio_erro):
        # Nome do arquivo CSV
        caminho_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        nome_arquivo = os.path.join(caminho_app,'temp','relatorios', 'relatorio_erro_produto.csv')

        # Abre o arquivo em modo de escrita
        with open(nome_arquivo, mode="w", newline="") as arquivo_csv:
            escritor_csv = csv.writer(arquivo_csv, delimiter=';')
            cabecalho = ['ID','Nome', 'Código de barras', 'Preço de venda','Preço de custo','Foi importado?', 'Restrição']
            escritor_csv.writerow(cabecalho)
            for linha in relatorio_erro:
                linha[-1] = ", ".join(linha[-1])
                escritor_csv.writerow(linha)
        Manipular_arquivos().baixar_arquivo(nome_arquivo)
        # nome_arquivo

        # with open(nome_arquivo, mode="r", newline="") as arquivo_csv:
        #     leitor_csv = csv.reader(arquivo_csv)
        #     matriz_lida = [linha for linha in leitor_csv]
        #     print(matriz_lida)
