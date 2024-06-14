import os

from tkinter import filedialog
from tkinter import messagebox
class Manipular_arquivos():

    def selecionar_arquivo(self,extensao_desejada:str='') -> bool | list:
        """Método para selecionar arquivo arquivo e verificar se está na extensão correta,
        caso o arquivo não esteja na extensão desejada, o programa alerta o usuário.

        método salva o arquivo (se houver) na pasta temporário para futura exclusão.
        
        Após isso, chama a próxima tela.

        Args:
            func_proxima_tela (Callable[[],None]): Função para prosseguir para a próxima tela
            extensao_desejada (str, optional): string da extenção desejada. Defaults to ''.
        """
        # Importações
        import os
        import shutil
        from tkinter import filedialog
        # Definindo a extensão pedida como padrão da Janela
        
        # Pede ao usuário o arquivo já na extensão destinada. Se não tiver, permite qualquer extensão
        arquivo_selecionado = filedialog.askopenfilename(filetypes=[(f"Arquivos {extensao_desejada.replace('.','').upper()}", f"*{extensao_desejada}")])
        
        # Verifica se o arquivo existe ou não. Se não existir, o programa alerta nenhuma caminho indicado
        if not arquivo_selecionado:
            messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
            return False
        
        # Recupero o nome e a extensão original do arquivo
        nome_arquivo = os.path.basename(arquivo_selecionado)
        extensao_arquivo = os.path.splitext(arquivo_selecionado)[1]
        
        # Verifico se o arquivo que me entregou está no formato pedido, caso a extensão não seja equivalente ao pedido, ele envia um aviso.
        if extensao_arquivo != extensao_desejada:
            messagebox.showerror("Erro", f"Extensão inválida, o arquivo precisa ser {extensao_desejada}.")
            return False
        
        # Uso para referenciar a pasta onde ficara temporariamente os dados. PODE MUDAR
        caminho_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # app > componentes > tela > este arquivo
        
        caminho_dados_temp = os.path.join(caminho_app, 'temp','dados')        
        # Capturo o nome antigo do arquivo e defino para um outro nome para ser o padrão
        antigo_nome = os.path.join(caminho_dados_temp,nome_arquivo)
        novo_nome = os.path.join(caminho_dados_temp,'arquivo_temporario'+extensao_arquivo)
        
        # Copio e renomeio o arquivo
        shutil.copy(arquivo_selecionado, caminho_dados_temp)
        shutil.move(antigo_nome,novo_nome)
        return True

    def deletar_arquivo_temp(self,caminho_arquivo):
        os.remove(caminho_arquivo)
    
    def baixar_arquivo(self,caminho_arquivo:str):        
        caminho_absoluto = caminho_arquivo
        destino = filedialog.asksaveasfilename(defaultextension='csv', initialfile="relatorio_restricoes_"+'produto', filetypes=[("Arquivos CSV", "*.csv")])
        print('Salvo em: '+destino)
        if destino:
            try:
            # Copia o arquivo para o destino usando o os
                os.system("copy \"" + caminho_absoluto + "\" \"" + destino + "\"")
            
                # print("Arquivo baixado com sucesso em:", destino)
                self.deletar_arquivo_temp(caminho_absoluto)
                messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
                return True
            except PermissionError:
                # print("Erro: Permissão negada. Não é possível salvar o arquivo.")
                messagebox.showinfo("Erro", "Você não foi possui permissão para salvar nesta pasta!")
        else:
            messagebox.showerror("Erro", "Selecione um local válido para salvar o arquivo.")