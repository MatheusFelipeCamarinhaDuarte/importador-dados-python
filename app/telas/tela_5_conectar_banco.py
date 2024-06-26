from app.classes.telas import Telas
class Tela_5(Telas):
    def carregar_pagina(self):
        """Função feita para ir para a tela de conexao do banco

        Args:
            janela_principal (Janela): Janela principal herdada de outras funções.
            banco (Banco_de_dados, optional): Após o carregamento desta página através
            do método layout_de_conexao, ele é substituido por um banco com informações de conexao. Defaults to Banco_de_dados().
        """
        if not self.banco_destino.cursor:
            if self.banco_origem.cursor:
                print("MEU USUARIO É "+self.banco_origem.usuario)
                print("MEU BANCO É "+self.banco_origem.banco)
                
                
            else:
                print("NÃO TENHO BANCO DE ORIGEM")
        
        from app.telas.tela_4_escolha_formato import Tela_4
        janela_principal = self.janela
        janela_principal.limpar()
        # Criação da tela
        frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
        frame_conexao, frame_inserir = janela_principal.duplo_frame(frame_superior)
        frame_inserir.config(pady=20)

        # Rodape
        tela_anterior = lambda:Tela_4(janela_principal,self.migracao,self.sistema_origem,self.sistema_destino)
        janela_principal.rodape(frame_inferior,tela_anterior)
        
        # Conectar com o banco
        carregar_aqui = lambda: [self.carregar_pagina()]
        janela_principal.layout_de_conexao(frame_conexao,carregar_aqui, self.banco_destino)

        # Inserção de dados no banco
        dicionario_botoes = {f'SUBISTITUIR {self.migracao}':lambda:[],f'ADICIONAR {self.migracao}':lambda:[]}
        substituir, adicionar = janela_principal.multi_botoes(dicionario_botoes,frame_inserir,20,1,10)
        substituir.config(state=self.tk.DISABLED)
        adicionar.config(state=self.tk.DISABLED)
        if self.banco_destino.cursor:
            substituir.config(state=self.tk.NORMAL,command=lambda:[self.ir_para_proxima_tela(True)])
            adicionar.config(state=self.tk.NORMAL,command=lambda:[self.ir_para_proxima_tela(False)])
            # adicionar.config(state=self.tk.NORMAL,command=lambda:[self.erros('Error','Módulo ainda não implantado!')])

    def ir_para_proxima_tela(self,substituir:bool):
        from app.classes.produto import Produto
        from app.telas.tela_4_escolha_formato import Tela_4
        produto = Produto(self.matriz,self.banco_destino)
        lista_erros, produtos_totais_adicionados,contador_produtos_totais,resultado_produtos_totais_no_banco, contador_multi_barra = produto.cadastrar_produto(substituir)
        Tela_4(self.janela,self.migracao,self.sistema_origem, self.sistema_destino)
        
        mensagem = self.tk.Toplevel()
        if lista_erros != []:
            from app.classes.relatorios import Relatorios
            xa = (mensagem.winfo_screenwidth() // 2) - (400 // 2)
            ya = (mensagem.winfo_screenheight() // 2) - (300 // 2)
            mensagem.geometry(f"{400}x{300}+{xa}+{ya}")            
            label = self.tk.Label(mensagem, text=f'Produtos totais identificados na base de origem: {contador_produtos_totais - contador_multi_barra}')
            label.pack()
            label1 = self.tk.Label(mensagem, text=f'Produtos adicionados: {produtos_totais_adicionados}')
            label1.pack()
            label3 = self.tk.Label(mensagem, text=f'Produtos não adicionados: {contador_produtos_totais - produtos_totais_adicionados - contador_multi_barra}')
            label3.pack()
            label2 = self.tk.Label(mensagem, text=f'Produtos com restrições: {len(lista_erros)}')
            label2.pack()
            if not substituir:
                label1 = self.tk.Label(mensagem, text=f'Produtos totais atualmente na base de destino: {resultado_produtos_totais_no_banco}')
                label1.pack()
        
            baixar_relatorio_de_importacao = lambda: [Relatorios().relatorio_erros_produto(lista_erros),mensagem.destroy(),self.voltar_tela_inicial()]
            botao = self.tk.Button(mensagem, text='Baixar relatório de importação', command=baixar_relatorio_de_importacao, font=("Arial", 10))
            botao.pack(pady=20)
            # app/temp/relatorios/relatorio_erro_produto.csv
        else:
            self.infos('Sucesso',"Todos os dados foram inseridos com sucesso!")
            self.voltar_tela_inicial()
    def voltar_tela_inicial(self):
        resposta = self.askyesno('Sucesso',"Deseja voltar ao menu?")
        if resposta:
            from app.telas.tela_2_escolha_tipo import Tela_2
            Tela_2(self.janela)
