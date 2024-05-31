from app.classes.janela import Janela
from app.classes.banco_de_dados import Banco_de_dados
def conecatar_banco(janela_principal:Janela, banco:Banco_de_dados = Banco_de_dados()):
    """Função feita para ir para a tela de conexao do banco

    Args:
        janela_principal (Janela): Janela principal herdada de outras funções.
        banco (Banco_de_dados, optional): Após o carregamento desta página através
        do método layout_de_conexao, ele é substituido por um banco com informações de conexao. Defaults to Banco_de_dados().
    """
    import tkinter as tk
    from app.telas.tela_4_escolha_formato import escolha_formato
    from tkinter import messagebox
    janela_principal.limpar()
    # Criação da tela
    frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
    frame_conexao, frame_inserir = janela_principal.duplo_frame(frame_superior)
    frame_inserir.config(pady=20)
    janela_principal.rodape(frame_inferior,escolha_formato)
    matriz = janela_principal.matriz
    janela_principal.layout_de_conexao(frame_conexao,banco,conecatar_banco)    

    dicionario_botoes = {f'SUBISTITUIR {janela_principal.migracao}':lambda:[],f'ADICIONAR {janela_principal.migracao}':lambda:[]}
    substituir, adicionar = janela_principal.multi_botoes(dicionario_botoes,frame_inserir,20,1,10)
    substituir.config(state=tk.DISABLED)
    adicionar.config(state=tk.DISABLED)
    if banco.cursor:
        substituir.config(state=tk.NORMAL,command=lambda:[banco.cadastrar_produtos(matriz, janela_principal, substituir=True)])
        adicionar.config(state=tk.NORMAL,command=lambda:[messagebox.showerror('Error','Módulo ainda não implantado!')])