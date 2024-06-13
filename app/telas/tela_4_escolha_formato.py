from app.classes.janela import Janela
from app.classes.telas import Telas

class Tela_4(Telas):
    
    def carregar_pagina(self):
        """Função para abrir a tela de inserção de relatório ou banco para a migracao.

        Args:
            janela_principal (Janela): Janela principal vinda do tela de escolha de sistema
        """
        import tkinter as tk
        import webbrowser
        from tkinter import messagebox
        from app.telas.tela_3_escolha_sistema import Tela_3
        janela_principal = self.janela
        # Oculta a primeira janela e criar a nova
        janela_principal.limpar()
        
        # Define informações do sistema
        
        # Separando frame superior de frame inferior
        frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
        frame_superior.config(pady=25)

        frame_arquivos, frame_banco = janela_principal.duplo_frame(janela_principal)

        label_arquivos = tk.Label(frame_arquivos, text=f"Importação via relatório:")
        label_arquivos.pack()
        # Criando os radio buttons para extensões
        extensoes_aceitas = ['.xml', '.xls', '.csv']
        var_extensoes,lista_radio_extensoes = janela_principal.multi_radios(extensoes_aceitas, frame_arquivos,True)   
        xml,xls,csv = lista_radio_extensoes   
        janela_principal.desativar_radio(xls,csv) # Desativando opções ainda não implantadas
        
        # Botão de selecionar arquivos
        proximo = lambda:[setattr(self,'extensao',var_extensoes.get()),self.ir_para_proxima_tela()]
        button_selecionar = tk.Button(frame_arquivos, text="Selecionar Arquivo", command=proximo)
        button_selecionar.pack()
        
        label_arquivos = tk.Label(frame_banco, text=f"Importação via Banco de dados:")
        label_arquivos.pack()
        conectar = lambda:messagebox.showerror("Erro","Módulo ainda não implantado")
        button_selecionar = tk.Button(frame_banco, text="Conectar", command=conectar )
        button_selecionar.pack()
        
        # Rodapé dinâmico
        tela_anterior = lambda:Tela_3(janela_principal,self.migracao)
        janela_principal.rodape(frame_inferior,tela_anterior)
        
        # Frame com link para tirar dúvidas
        sub_frame = tk.Frame(frame_inferior)
        sub_frame.pack(anchor=tk.S)
        texto = tk.Label(sub_frame, height=2, wraplength=250,text=f"como retirar relatorios no formato correto de dentro do {self.sistema_origem}?", )
        texto.pack(anchor=tk.S)
        link = "https://google.com"
        texto.config(foreground='blue', underline=True)
        texto.bind("<Button-1>", lambda event: webbrowser.open(link))

    def ir_para_proxima_tela(self):
        from app.telas.tela_5_conectar_banco import Tela_5
        janela_principal = self.janela
        migracao = self.migracao
        sistema_origem = self.sistema_origem
        sistema_destino = self.sistema_destino
        extensao = self.extensao
        if (janela_principal.verifica_radio(extensao)):
            matriz = janela_principal.selecionar_arquivo(migracao,sistema_origem,sistema_destino,extensao)
            if matriz:
                Tela_5(janela_principal,migracao,sistema_origem,sistema_destino,extensao,matriz)