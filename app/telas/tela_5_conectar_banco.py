from app.classes.telas import Telas
from tkinter import messagebox
import tkinter as tk
from app.classes.banco_de_dados import Banco_de_dados

class Tela_5(Telas):
    def carregar_pagina(self):
        """Função feita para ir para a tela de conexao do banco

        Args:
            janela_principal (Janela): Janela principal herdada de outras funções.
            banco (Banco_de_dados, optional): Após o carregamento desta página através
            do método layout_de_conexao, ele é substituido por um banco com informações de conexao. Defaults to Banco_de_dados().
        """
        if not self.banco_destino.cursor:
            if self.janela.banco_provisorio.usuario:
                self.banco_origem = self.janela.banco_provisorio
                self.janela.banco_provisorio = Banco_de_dados()
                print("MEU USUARIO É "+self.banco_origem.usuario)
                print("MEU BANCO É "+self.banco_origem.banco)
            else:
                print("NÃO TENHO BANCO DE ORIGEM")
        
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
        carregar_aqui = lambda: [setattr(self,'banco_destino', janela_principal.banco_provisorio),self.carregar_pagina()]
        janela_principal.layout_de_conexao(frame_conexao,carregar_aqui)

        dicionario_botoes = {f'SUBISTITUIR {self.migracao}':lambda:[],f'ADICIONAR {self.migracao}':lambda:[]}
        substituir, adicionar = janela_principal.multi_botoes(dicionario_botoes,frame_inserir,20,1,10)
        substituir.config(state=tk.DISABLED)
        adicionar.config(state=tk.DISABLED)
        if self.banco_destino.cursor:
            substituir.config(state=tk.NORMAL,command=lambda:[self.ir_para_proxima_tela()])
            adicionar.config(state=tk.NORMAL,command=lambda:[messagebox.showerror('Error','Módulo ainda não implantado!')])

    def ir_para_proxima_tela(self):
        from app.classes.produto import Produto
        matriz = self.matriz
        substituir = True
        self.banco_destino = self.janela.banco_provisorio
        produto = Produto(matriz,self.banco_destino)
        # print(self.banco_destino.usuario,self.banco_origem.usuario)
        lista_erros, produtos_totais_adicionados,contador_produtos_totais, produtos_adicionados = produto.cadastrar_produtos(substituir=substituir)
        
        mensagem = tk.Toplevel()
        if lista_erros != []:
            from app.classes.relatorios import Relatorios
            xa = (mensagem.winfo_screenwidth() // 2) - (300 // 2)
            ya = (mensagem.winfo_screenheight() // 2) - (300 // 2)
            mensagem.geometry(f"{300}x{200}+{xa}+{ya}")            
            label = tk.Label(mensagem, text=f'Produtos totais: {contador_produtos_totais}')
            label.pack()
            if substituir:
                label1 = tk.Label(mensagem, text=f'Produtos adicionados: {produtos_totais_adicionados}')
                label1.pack()
                
            else:
                label1 = tk.Label(mensagem, text=f'Produtos adicionados: {produtos_adicionados-1}')
                label1.pack()
                label1 = tk.Label(mensagem, text=f'Produtos totais no banco: {produtos_totais_adicionados}')
                label1.pack()
            label3 = tk.Label(mensagem, text=f'Produtos não adicionados: {contador_produtos_totais - produtos_adicionados + 1}')
            label3.pack()
            label2 = tk.Label(mensagem, text=f'Produtos com restrições: {len(lista_erros)}')
            label2.pack()
        
            baixar_relatorio_de_importacao = lambda: [Relatorios().relatorio_erros_produto(lista_erros),mensagem.destroy(),self.voltar_tela_inicial()]
            botao = tk.Button(mensagem, text='Baixar relatório de importação', command=baixar_relatorio_de_importacao, font=("Arial", 10))
            botao.pack(pady=20)
            # app/temp/relatorios/relatorio_erro_produto.csv
        else:
            messagebox.showinfo('Sucesso',"Todos os dados foram inseridos com sucesso!")
            self.voltar_tela_inicial()
            # print("Todos os produtos foram adicionados com sucesso!!")

    def voltar_tela_inicial(self):
        resposta = messagebox.askyesno('Sucesso',"Deseja voltar ao menu?")
        if resposta:
            from app.telas.tela_2_escolha_tipo import Tela_2
            Tela_2(self.janela)
