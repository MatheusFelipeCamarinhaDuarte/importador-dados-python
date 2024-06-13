from app.classes.janela import Janela
from app.classes.telas import Telas
class Tela_1(Telas):
    def carregar_pagina(self) -> Janela:
        """Janela Principal da aplicação, com o intuito de inciar aplicação e não retornar a está tela novamente.

        Returns:
            tk.Tk: Retorna uma tela Tk.
        """
        
        # Importações
        import tkinter as tk    
        # Criação da janela principal
        janela_principal = self.janela
        # Colocando as dimensões iniciais (e fixas) da tela
        altura = 400
        largura = 550
        x = (janela_principal.winfo_screenwidth() // 2) - (largura // 2)
        y = (janela_principal.winfo_screenheight() // 2) - (altura // 2)
        janela_principal.geometry(f"{largura}x{altura}+{x}+{y}")
        
        # Colocando a linha de apresentação do projeto
        apresentacao = tk.Label(janela_principal, text="Projeto de importação de dados entre sistemas")
        apresentacao.pack(anchor=tk.CENTER, expand=True)
        
        # Colocando a linha de inícia do código em si. Uma vez colocado, ele não volta para cá
        iniciar = lambda: self.ir_para_proxima_tela()
        button = tk.Button(janela_principal, text="INICIAR", width=10,height=1, command=iniciar)
        button.pack(anchor=tk.CENTER, expand=True)
        
        # Retornando a primeira tela criada
        return janela_principal


    def ir_para_proxima_tela(self):
        from app.telas.tela_2_escolha_tipo import Tela_2
        janela_principal = self.janela
        Tela_2(janela_principal)
