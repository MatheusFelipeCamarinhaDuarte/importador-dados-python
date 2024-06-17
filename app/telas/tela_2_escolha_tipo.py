from app.classes.telas import Telas

class Tela_2(Telas):
    def carregar_pagina(self):
        """Função para levar a tela de escolha do tipo de migração

        Args:
            janela_principal (Janela): Janela principal da aplicação.
        """
        #Limpa a tela anterior
        janela_principal = self.janela
        janela_principal.limpar()
        janela_principal.title("Escolha o tipo de importação")  

        # Frame do botão de escolha
        frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
        frame_superior.configure(pady=40)
        # Menu de ação das telas de migração
        produto = lambda:[setattr(self, 'migracao', 'PRODUTOS'), self.ir_para_proxima_tela()]
        estoque = lambda:[self.erros('Error','Módulo ESTOQUE ainda não implantado!')]
        clientes = lambda:[self.erros('Error','Módulo CLIENTES ainda não implantado!')]
        # cliente = lambda:ir_para_proxima_tela(janela_principal, migracao="CLIENTES")
        # estoque = lambda:ir_para_proxima_tela(janela_principal, migracao="ESTOQUE")
        
        dicionario_de_botoes = {'PRODUTOS': produto, 'ESTOQUE': estoque, 'CLIENTES': clientes}
        janela_principal.multi_botoes(dicionario_de_botoes,frame_superior,20,2,20)

        # Rodapé dinâmico da tela
        janela_principal.rodape(frame_inferior)
        

    def ir_para_proxima_tela(self):
        from app.telas.tela_3_escolha_sistema import Tela_3
        migracao = self.migracao
        janela_principal = self.janela
        Tela_3(janela_principal,migracao)
