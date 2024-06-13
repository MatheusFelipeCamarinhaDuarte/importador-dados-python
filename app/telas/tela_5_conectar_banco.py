from app.classes.janela import Janela
from app.classes.telas import Telas


class Tela_5(Telas):
    def carregar_pagina(self):
        """Função feita para ir para a tela de conexao do banco

        Args:
            janela_principal (Janela): Janela principal herdada de outras funções.
            banco (Banco_de_dados, optional): Após o carregamento desta página através
            do método layout_de_conexao, ele é substituido por um banco com informações de conexao. Defaults to Banco_de_dados().
        """
        import tkinter as tk
        from app.telas.tela_4_escolha_formato import Tela_4
        from tkinter import messagebox
        
        janela_principal = self.janela
        janela_principal.limpar()
        # Criação da tela
        frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
        frame_conexao, frame_inserir = janela_principal.duplo_frame(frame_superior)
        frame_inserir.config(pady=20)
        # Rodape
        tela_anterior = lambda:Tela_4(janela_principal,self.migracao,self.sistema_origem,self.sistema_destino)
        janela_principal.rodape(frame_inferior,tela_anterior)
        
        matriz = self.matriz
        janela_principal.layout_de_conexao(frame_conexao,self.carregar_pagina)

        dicionario_botoes = {f'SUBISTITUIR {self.migracao}':lambda:[],f'ADICIONAR {self.migracao}':lambda:[]}
        substituir, adicionar = janela_principal.multi_botoes(dicionario_botoes,frame_inserir,20,1,10)
        substituir.config(state=tk.DISABLED)
        adicionar.config(state=tk.DISABLED)
        if janela_principal.banco.cursor:
            substituir.config(state=tk.NORMAL,command=lambda:[janela_principal.banco.cadastrar_produtos(matriz, janela_principal, substituir=True)])
            adicionar.config(state=tk.NORMAL,command=lambda:[messagebox.showerror('Error','Módulo ainda não implantado!')])
    def ir_para_proxima_tela(self):
        pass