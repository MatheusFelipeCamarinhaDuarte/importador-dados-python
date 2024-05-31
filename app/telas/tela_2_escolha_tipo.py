from app.classes.janela import Janela
def escolha_tipo(janela_principal:Janela):
    """Função para levar a tela de escolha do tipo de migração

    Args:
        janela_principal (Janela): Janela principal da aplicação.
    """
    # Importações
    from tkinter import messagebox
    from app.telas.tela_3_escolha_sistema import tela_de_escolha_sistema
    
    #Limpa a tela anterior
    janela_principal.limpar()
    janela_principal.title("Escolha o tipo de importação")  

    # Frame do botão de escolha
    frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
    frame_superior.configure(pady=40)
    # Menu de ação das telas de migração
    dicionario_de_botoes = {'PRODUTOS': lambda:[setattr(janela_principal, 'migracao', 'PRODUTOS'),tela_de_escolha_sistema(janela_principal)], 'ESTOQUE': lambda:[messagebox.showerror('Error','Módulo ainda não implantado!')], 'CLIENTES': lambda:[messagebox.showerror('Error','Módulo ainda não implantado!')]}
    janela_principal.multi_botoes(dicionario_de_botoes,frame_superior,20,2,20)

    # Rodapé dinâmico da tela
    janela_principal.rodape(frame_inferior)