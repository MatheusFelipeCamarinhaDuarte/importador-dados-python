import tkinter as tk
from tkinter import messagebox

class Janela(tk.Tk):
    """Janela principal da nossa aplicação que herda tk.Tk do Tkinter,
    com o objetivo de ser uma single-page aplication e adiciona funções
    extras como o Limpar
    
    A janela principal já inicia com nome fixo e icone de nossa aplicação,
    além de fixar a largura e altura, e realizar um protocolo correto de quit()
    caso alguém delete a janela pelo botao.
    """
    from typing import Callable, Optional, Tuple, List
    from app.classes.banco_de_dados import Banco_de_dados
    def __init__(self):
        """Método de criação de tela personalizada"""
        import os
        super().__init__()
        # Titulo inicial
        self.title("Matheus Solutions")
        # Icone
        diretorio_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        caminho_icone = os.path.join(diretorio_app, "icons", "selltech.ico")
        self.iconbitmap(caminho_icone)
        # Travando as dimensões da janela
        self.resizable(False, False)
        # Protocolo de encerramento correto
        self.protocol("WM_DELETE_WINDOW", lambda: self.quit())
        self.migracao = ''
        self.sistema_origem = ''
        self.sistema_destino = ''
        self.extensao = ''
        self.matriz = []
        self.banco = ''

    def limpar(self) -> None:
        """Método para limpar todos os widgets

        Returns:
            Janela: retorna a janela limpa
        """
        for widget in self.winfo_children():
            widget.destroy()
        return self

    def duplo_frame(self,frame_pai:tk.Frame, orientacao: str = 'Y') -> Tuple[tk.Frame, tk.Frame]:
        """Cria um frame duplo na orientação especificada.
        X para Frame esqueda e direita, Y para frames superiores e inferiores

        Args:
            orientacao (str): Deve ser 'X' ou 'Y'. Defalts to 'Y'.

        Raises:
            ValueError: Se a orientação não for 'X' ou 'Y'.
    
        Returns:
            Tuple[tk.Frame, tk.Frame]: Retorna uma tupla contendo os dois frames criados.
        """
        if orientacao not in ("X", "Y"):
            raise ValueError("A orientação deve ser 'X' ou 'Y'.")
        # Fazendo a verificação da orientação da tela.
        if orientacao == "X":
            # Implementação para orientação X
            frame_esquerdo = tk.Frame(frame_pai)
            frame_esquerdo.pack(side=tk.LEFT)
            frame_direito = tk.Frame(frame_pai)
            frame_direito.pack(side=tk.RIGHT)          
            return frame_esquerdo, frame_direito
        else:
            # Implementação para orientação Y (superior e inferior)
            frame_superior = tk.Frame(frame_pai)
            frame_superior.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
            frame_inferior = tk.Frame(frame_pai)
            frame_inferior.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
            return frame_superior, frame_inferior

    def rodape(self, frame_inferior:tk.Frame, func_tela_anterior:Optional[Callable[[], None]] = None) -> tk.Frame:
        """Método que chame e adiciona um frame de rodapé com funções voltar e sair.

        Args:
            frame_inferior (tk.Frame): Frame em que se localiza a parte de baixo da janela.
            func_tela_anterior (function, optional): Aqui fica a função da geração da tela 
            anterior, sem ela, o código não adiciona o botão voltar. Defaults to False.

        Returns:
            tk.Frame: Frame equivalente ao rodape da janela.
        """        
        
        # A partir do frame inferior, cria um outro frame destinado ao rodapé
        frame_rodape = tk.Frame(frame_inferior)
        frame_rodape.pack(anchor=tk.S,expand=True, fill=tk.X)
        
        # Caso tenha a função da tela anterior, adiciona a tela voltar
        if func_tela_anterior:
            voltar = tk.Button(frame_rodape, text="Voltar", command=lambda: [func_tela_anterior(self)])
            voltar.pack(side=tk.LEFT, pady=10, padx=10)
        
        # Adiciona o botão de sair da aplicação com o devido
        sair = tk.Button(frame_rodape, text="Sair", command=lambda: self.quit())
        sair.pack(side=tk.RIGHT, pady=10, padx=10)
        
        # Retorna o frame do rodape (Já ligado ao frame inferior)
        return frame_rodape

    def multi_botoes(self, dicionario_botoes:dict, frame_pertencente:tk.Frame, largura_botao:int = 20, altura_botao:int = 1, espacamento:int=5, orientacao=tk.CENTER) -> list[tk.Button]:
        """Método para criar multiplos botões em sequência um do outro.

        Args:
            dicionario_botoes (dict): um dicionario onde a chave é o text do
            botao e o valor é a função passada por meio de lambda.
            frame_pertencente (tk.Frame): Frame onde o botão será colocado
            largura_botao (int, optional): largura padrão do botão. Defaults to 20.
            orientacao (optional): Orientação do botão (padrão é centro). Defaults to tk.CENTER.

        Returns:
            list[tk.Button]: Retorna uma lista de botões para caso queria modificar algo nele
        """
        # Gera uma lista vazia
        todos = []
        # Para cada nome gerado, cria um botao com a respectiva funcao dele e adiciona na lista
        for texto, funcao in dicionario_botoes.items():
            button = tk.Button(frame_pertencente, text=texto, width=largura_botao,height=altura_botao, command=funcao)
            button.pack(anchor=orientacao, pady=espacamento, padx=10)
            todos.append(button)
        return todos

    def multi_radios(self,lista_radio:list, frame_pertencente:tk.Frame,lista:bool=False) -> Tuple[tk.StringVar,List[tk.Radiobutton]]:
        """Método para criar multiplos botões radios em sequência um do outro e 
        retorna-los junto com a variável.
        
        O método conta também com um label que exibe em baixo a opção selecionada.

        Args:
            lista_radio (list): Lista dos radios que quer de valores
            frame_pertencente (tk.Frame): Frame em que quer adicionar os radios
            lista (bool, optional): disposição em lista ao invés de coluna. 
            Defaults to False.

        Returns:
            Tuple[tk.StringVar,List[tk.Radiobutton]]: Devolve 2 variáveis, uma é 
            a string var do que está escrito no Radio button, e a outra é uma lista
            de todos os tk.RadioButton 
        """
        # Definição da variável que indica o radio_button
        var_opcao = tk.StringVar(value='Nenhuma opção selecionada')
        
        # Criação do subframe para o radio button
        frame_dos_radio_buttons = tk.Frame(frame_pertencente)
        frame_dos_radio_buttons.pack()
        
        #Definição de 
        lado = tk.TOP
        orientacao=tk.W
        if lista:
            lado = tk.RIGHT
            orientacao=tk.CENTER
        lista_radio_buttons = []
        # Criação de radio_button versionada de acordo com a lista passada
        for texto in lista_radio:
            radio_button = tk.Radiobutton(frame_dos_radio_buttons, text=texto, variable=var_opcao, value=texto, command=lambda: opcao.config(text=var_opcao.get()))
            radio_button.pack(anchor=orientacao,side=lado)
            lista_radio_buttons.append(radio_button)

        # Label para mostrar a opção selecionada
        opcao = tk.Label(frame_pertencente, text=var_opcao.get())
        opcao.pack(anchor=orientacao)
        
        # Retorna a variável que mantém o valor selecionado
        return var_opcao, lista_radio_buttons

    def desativar_radio(self,*args: Tuple[tk.Radiobutton]) -> None:
        """Métodos para desativar múltiplos radios para não serems clicáveis
        
        Args:
            *args (Tuple[tk.Radiobutton]): Lista de todos os radios a serem desativados
        """
        for i, arg in enumerate(args):
            arg.config(state=tk.DISABLED)

    def verifica_radio(self,*args: Tuple[str]) -> bool:
        """Método para verificar se algum radio está selecionado
        
        Args:
            funcao_proxima_tela (Callable): funcao para prosseguir para a proxima tela
            *args (Tuple[tk.StringVar]): Lista de todos os radios a serem verificados
        Returns:
            (str | Callable): Devolve uma mensagem de errado ou a função para a próxima tela
        """
        for i, arg in enumerate(args):
            if arg == 'Nenhuma opção selecionada':
                messagebox.showerror("Erro","Você precisa escolher o campo antes de prosseguir!")
                return False 
        return True

    def selecionar_arquivo(self,func_proxima_tela: Callable[[],None],extensao_desejada:str='') -> None:
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
            return messagebox.showerror("Erro", "Nenhum arquivo selecionado.")
        
        # Recupero o nome e a extensão original do arquivo
        nome_arquivo = os.path.basename(arquivo_selecionado)
        extensao_arquivo = os.path.splitext(arquivo_selecionado)[1]
        
        # Verifico se o arquivo que me entregou está no formato pedido, caso a extensão não seja equivalente ao pedido, ele envia um aviso.
        if extensao_arquivo != extensao_desejada:
            return messagebox.showerror("Erro", f"Extensão inválida, o arquivo precisa ser {extensao_desejada}.")
        
        # Uso para referenciar a pasta onde ficara temporariamente os dados. PODE MUDAR
        caminho_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # app > componentes > tela > este arquivo
        
        caminho_dados_temp = os.path.join(caminho_app, 'temp','dados')        
        # Capturo o nome antigo do arquivo e defino para um outro nome para ser o padrão
        antigo_nome = os.path.join(caminho_dados_temp,nome_arquivo)
        novo_nome = os.path.join(caminho_dados_temp,'arquivo_temporario_'+self.migracao.lower().replace(' ','_')+extensao_arquivo)
        
        # Copio e renomeio o arquivo
        shutil.copy(arquivo_selecionado, caminho_dados_temp)
        shutil.move(antigo_nome,novo_nome)
        self.extensao = extensao_arquivo
        
        matriz = self.filtro_de_importacao()
        if matriz:
            func_proxima_tela(self)

    def filtro_de_importacao(self) -> list:
        """Função com o intuito de ser um filtro com base nas informações coletadas
        anteriormente, como o tipo de migração, o sistema de origem e destino e o
        sistema de destino e por fim a extensão

        Returns:
            list: retorna a matriz gerada pelo sistema
        """
        from app.componentes.arquivo.seller import xml_to_matriz_produto
        migracao = self.migracao
        sistema_origem = self.sistema_origem 
        # sistema_destino = self.sistema_destino 
        extensao = self.extensao
        match migracao:
            case 'PRODUTOS':
                match sistema_origem:
                    case 'Autosystem':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'EMsys':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Posto Fácil':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Seller':
                        match extensao:
                            case '.xml':
                                self.matriz = xml_to_matriz_produto()
                                
                                return self.matriz
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Outros':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
            case 'ESTOQUE':
                match sistema_origem:
                    case 'Autosystem':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'EMsys':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Posto Fácil':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Seller':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Outros':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
            case 'CLIENTES':
                match sistema_origem:
                    case 'Autosystem':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'EMsys':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Posto Fácil':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Seller':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                    case 'Outros':
                        match extensao:
                            case '.xml':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.csv':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
                            case '.xls':
                                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")
            case _:
                messagebox.showerror("Erro", f"Tipo de importação {migracao} ERRADA. Sistema de Origem {sistema_origem} ERRADO. Tipo de extenção {extensao} ERRADA.")

    def layout_de_conexao(self,frame_pertencente:tk.Frame,banco:Banco_de_dados,func_proxima_tela: Callable[[],None]) -> tk.Entry:
        """Método com o intuito de realizar o layout de conexao
        com o banco de dados (Nome do banco,usuário, senha).add()

        Args:
            frame_pertencente (tk.Frame): Frame em que o layot irá ficar.
            banco (Banco_de_dados): Banco de dados criado pela tela
            func_proxima_tela (Callable[[],None]): funcao_que retorna para a mesma tela ou apra a tela psoterior
        Returns:
            Tuple[tk.Entry]: retorna os 3 inputs
        """
        frame_conjunto = tk.Frame(frame_pertencente)
        frame_conjunto.pack()
        frame_nome_banco = tk.Frame(frame_conjunto)
        frame_nome_banco.pack(expand=True, fill=tk.X)
        frame_usuario = tk.Frame(frame_conjunto)
        frame_usuario.pack(expand=True, fill=tk.X)
        frame_senha = tk.Frame(frame_conjunto)
        frame_senha.pack(expand=True, fill=tk.X)
        # Input de nome do banco
        label_nome_banco = tk.Label(frame_nome_banco, text="Nome do Banco")
        label_nome_banco.pack(side=tk.LEFT, pady=10, padx=10)
        input_nome_banco = tk.Entry(frame_nome_banco, width=20)
        input_nome_banco.pack(side=tk.RIGHT, pady=10, padx=10)
        input_nome_banco.insert(0, banco.banco)
        # Input de usuário do banco
        label_usuario = tk.Label(frame_usuario, text="Usuario do banco")
        label_usuario.pack(side=tk.LEFT, pady=10, padx=10)
        input_usuario = tk.Entry(frame_usuario, width=20)
        input_usuario.pack(side=tk.RIGHT, pady=10, padx=10)
        input_usuario.insert(0, banco.usuario)
        # Input de senha do banco
        label_senha = tk.Label(frame_senha, text="Senha do banco")
        label_senha.pack(side=tk.LEFT, pady=10, padx=10)
        input_senha = tk.Entry(frame_senha, width=20)
        input_senha.pack(side=tk.RIGHT, pady=10, padx=10)
        input_senha.insert(0, banco.senha)
        # Botão para conectar com o banco de dados
        botao_conexao = tk.Button(frame_conjunto,text="CONECTAR AO BANCO", command=lambda:[banco.iniciar(input_usuario.get(),input_senha.get(),input_nome_banco.get()),func_proxima_tela(self,banco)])
        botao_conexao.pack()
        return input_nome_banco, input_usuario, input_senha


