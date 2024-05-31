from app.classes.janela import Janela
def escolha_formato(janela_principal:Janela):
    """Função para abrir a tela de inserção de relatório ou banco para a migracao.

    Args:
        janela_principal (Janela): Janela principal vinda do tela de escolha de sistema
    """
    import tkinter as tk
    import webbrowser
    from tkinter import messagebox
    from app.telas.tela_3_escolha_sistema import tela_de_escolha_sistema
    from app.telas.tela_5_conectar_banco import conecatar_banco
    
    # Oculta a primeira janela e criar a nova
    janela_principal.limpar()
    
    # Define informações do sistema
    sistema_origem = janela_principal.sistema_origem
    
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
    
    button_selecionar = tk.Button(frame_arquivos, text="Selecionar Arquivo", command=lambda:[janela_principal.selecionar_arquivo(conecatar_banco,var_extensoes.get())] if (janela_principal.verifica_radio(var_extensoes.get())) else None)
    button_selecionar.pack()
    
    label_arquivos = tk.Label(frame_banco, text=f"Importação via Banco de dados:")
    label_arquivos.pack()
    button_selecionar = tk.Button(frame_banco, text="Conectar", command= lambda:messagebox.showerror("Erro","Módeulo ainda não implantado"))
    button_selecionar.pack()
    
    # Rodapé dinâmico 
    janela_principal.rodape(frame_inferior,tela_de_escolha_sistema)
    
    # Frame com link para tirar dúvidas
    sub_frame = tk.Frame(frame_inferior)
    sub_frame.pack(anchor=tk.S)
    texto = tk.Label(sub_frame, height=2, wraplength=250,text=f"como retirar relatorios no formato correto de dentro do {sistema_origem}?", )
    texto.pack(anchor=tk.S)
    link = "https://google.com"
    texto.config(foreground='blue', underline=True)
    texto.bind("<Button-1>", lambda event: webbrowser.open(link))
