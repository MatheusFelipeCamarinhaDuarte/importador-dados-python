import csv
import os
from tkinter import filedialog
from tkinter import messagebox
def relatorio_erros_produto(relatorio_erro):
    # Nome do arquivo CSV
    caminho_app = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    nome_arquivo = os.path.join(caminho_app,'temp','relatorios', 'relatorio_erro_produto.csv')

    # Abre o arquivo em modo de escrita
    with open(nome_arquivo, mode="w", newline="") as arquivo_csv:
        escritor_csv = csv.writer(arquivo_csv, delimiter=';')
        cabecalho = ['ID','Nome', 'Código de barras', 'Preço de venda','Preço de custo','Foi importado?', 'Restrição']
        escritor_csv.writerow(cabecalho)
        for linha in relatorio_erro:
            linha[-1] = ", ".join(linha[-1])
            escritor_csv.writerow(linha)
    return 'relatorio_erro_produto'
    # with open(nome_arquivo, mode="r", newline="") as arquivo_csv:
    #     leitor_csv = csv.reader(arquivo_csv)
    #     matriz_lida = [linha for linha in leitor_csv]
    #     print(matriz_lida)
def baixar_arquivo_relatorio(lista_erros:list,tela,janela_principal,nome_cliente:str):
    nome_arquivo = relatorio_erros_produto(lista_erros)
    caminho_app = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    caminho_absoluto = os.path.join(caminho_app, 'temp','relatorios',nome_arquivo+'.csv')
    cliente = nome_cliente.replace(' ','_')
    destino = filedialog.asksaveasfilename(defaultextension='csv', initialfile="relatorio_restricoes_"+cliente.lower(), filetypes=[("Arquivos CSV", "*.csv")])
    print('Salvo em: '+destino)
    if destino:
        try:
        # Copia o arquivo para o destino usando o os
            os.system("copy \"" + caminho_absoluto + "\" \"" + destino + "\"")
        
            # print("Arquivo baixado com sucesso em:", destino)
            os.remove(caminho_absoluto)
            tela.destroy()
            messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
            resposta = messagebox.askyesno('Teste',"Deseja voltar ao menu?")
            if resposta:
                from app.telas.tela_2_escolha_tipo import escolha_tipo
                escolha_tipo(janela_principal)
            
        except PermissionError:
            # print("Erro: Permissão negada. Não é possível salvar o arquivo.")
            messagebox.showinfo("Erro", "Você não foi possui permissão para salvar nesta pasta!")
    else:
        messagebox.showerror("Erro", "Selecione um local válido para salvar o arquivo.")
