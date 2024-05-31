from app.classes.janela import Janela

def tela_de_escolha_sistema(janela_principal:Janela):
    """Função para a escolha do sistema de origem e o sistema de destino

    Args:
        janela_principal (Janela): Janela principal vinda da tela de escolha
    """
    import tkinter as tk
    from app.telas.tela_2_escolha_tipo import escolha_tipo
    from app.telas.tela_4_escolha_formato import escolha_formato
    
    #Limpa a tela anterior
    janela_principal.limpar()
    migracao = janela_principal.migracao
    # Título da nova tela
    janela_principal.title("Escolha o sistema")  
    
    # PAREI AQUI
    frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
    
    # Título do frame superior
    label_titulo_pagina = tk.Label(frame_superior, text=f"Importação de {migracao.lower()}:")
    label_titulo_pagina.pack()

    # Criação do frame esquerdo e direito para separa sistema de origem e sistema de destino
    frame_sistema_origem, frame_sistema_destino = janela_principal.duplo_frame(frame_superior, 'X')
    frame_sistema_origem.config(padx=20)
    frame_sistema_destino.config(padx=20)
    
    # Criação dos labels explicando qual é o sistema de origem e qual o sistema de destino
    label_titulo_origem = tk.Label(frame_sistema_origem, text="Escolha o sistema de origem:")
    label_titulo_origem.pack(side=tk.TOP,anchor=tk.NW)
    label_titulo_destino = tk.Label(frame_sistema_destino, text="Escolha o sistema de destino:")
    label_titulo_destino.pack(side=tk.TOP,anchor=tk.NW)

    # Criação dos radio botões de sistema de origem e sistema de destino
    sistemas_origem = ["Autosystem","EMsys","Posto Fácil", "Seller", "Outros"]
    var_origem, lista_radio_origem = janela_principal.multi_radios(sistemas_origem,frame_sistema_origem)
    as_or,em_or,pf_or,seller_or,outros_or = lista_radio_origem
    
    sistemas_destino = ["Autosystem","EMsys","Posto Fácil", "Seller"]
    var_destino, lista_radio_destino = janela_principal.multi_radios(sistemas_destino,frame_sistema_destino)
    as_des, em_des, pf_des, seller_des = lista_radio_destino
    
    janela_principal.desativar_radio(as_or,em_or,pf_or,outros_or,em_des, pf_des,seller_des) # Desativando radios ainda não implementados
    
    # Criando botão e rodapé dinâmico do frame inferior
    button_submit = tk.Button(frame_inferior, text="Proximo", command=lambda: [setattr(janela_principal,'sistema_origem',var_origem.get()),setattr(janela_principal,'sistema_destino',var_destino.get()),escolha_formato(janela_principal)] if janela_principal.verifica_radio(var_origem.get(),var_destino.get()) else None)
    button_submit.pack() # Inserindo o botão de próximo
    janela_principal.rodape(frame_inferior,escolha_tipo) # Rodapé dinâmico



