from app.classes.telas import Telas

class Tela_3(Telas):
    def carregar_pagina(self):
        """Função para a escolha do sistema de origem e o sistema de destino

        Args:
            janela_principal (Janela): Janela principal vinda da tela de escolha
        """
        from app.telas.tela_2_escolha_tipo import Tela_2
        janela_principal = self.janela
        #Limpa a tela anterior
        janela_principal.limpar()
        migracao = self.migracao
        # Título da nova tela
        janela_principal.title("Escolha o sistema")  
        
        # PAREI AQUI
        frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
        
        # Título do frame superior
        label_titulo_pagina = self.tk.Label(frame_superior, text=f"Importação de {migracao.lower()}:")
        label_titulo_pagina.pack()

        # Criação do frame esquerdo e direito para separa sistema de origem e sistema de destino
        frame_sistema_origem, frame_sistema_destino = janela_principal.duplo_frame(frame_superior, 'X')
        frame_sistema_origem.config(padx=20)
        frame_sistema_destino.config(padx=20)
        
        # Criação dos labels explicando qual é o sistema de origem e qual o sistema de destino
        label_titulo_origem = self.tk.Label(frame_sistema_origem, text="Escolha o sistema de origem:")
        label_titulo_origem.pack(side=self.tk.TOP,anchor=self.tk.NW)
        label_titulo_destino = self.tk.Label(frame_sistema_destino, text="Escolha o sistema de destino:")
        label_titulo_destino.pack(side=self.tk.TOP,anchor=self.tk.NW)

        # Criação dos radio botões de sistema de origem e sistema de destino
        sistemas_origem = ["Autosystem","Posto Fácil", "Seller", "Outros"]
        var_origem, lista_radio_origem = janela_principal.multi_radios(sistemas_origem,frame_sistema_origem)
        as_or,pf_or,seller_or,outros_or = lista_radio_origem
        
        sistemas_destino = ["Autosystem","Posto Fácil"]
        var_destino, lista_radio_destino = janela_principal.multi_radios(sistemas_destino,frame_sistema_destino)
        as_des, pf_des = lista_radio_destino
        
        janela_principal.desativar_radio(as_or,outros_or,pf_des) # Desativando radios ainda não implementados
        
        # Criando botão e rodapé dinâmico do frame inferior
        proximo = lambda:[setattr(self,'sistema_origem',var_origem.get()), setattr(self,'sistema_destino',var_destino.get()),self.ir_para_proxima_tela()]
        button_submit = self.tk.Button(frame_inferior, text="Proximo", command=proximo)
        button_submit.pack() # Inserindo o botão de próximo
        tela_anterior = lambda:Tela_2(janela_principal)
        janela_principal.rodape(frame_inferior,tela_anterior) # Rodapé dinâmico

    def ir_para_proxima_tela(self):
        from app.telas.tela_4_escolha_formato import Tela_4
        janela_principal = self.janela
        migracao = self.migracao
        sistema_origem = self.sistema_origem
        sistema_destino = self.sistema_destino
        if janela_principal.verifica_radio(sistema_origem,sistema_destino):
            Tela_4(janela_principal,migracao,sistema_origem,sistema_destino)

