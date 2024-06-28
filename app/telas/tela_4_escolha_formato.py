from app.classes.telas import Telas

class Tela_4(Telas):
    
    def carregar_pagina(self):
        """Função para abrir a tela de inserção de relatório ou banco para a migracao.

        Args:
            janela_principal (Janela): Janela principal vinda do tela de escolha de sistema
        """
        from app.telas.tela_3_escolha_sistema import Tela_3
        
        janela_principal = self.janela
        # Oculta a primeira janela e criar a nova
        janela_principal.limpar()
        
        # Define informações do sistema
        
        # Separando frame superior de frame inferior
        frame_superior, frame_inferior = janela_principal.duplo_frame(janela_principal)
        frame_superior.config(pady=25)

        frame_banco, frame_arquivos = janela_principal.duplo_frame(janela_principal)

        
        # Campo do banco de dados 
        lista_com_banco = ['Posto Fácil']
        if self.sistema_origem in lista_com_banco:    
            label_arquivos = self.tk.Label(frame_banco, text=f"Importação via Banco de dados de origem:", font=2)
            label_arquivos.pack()
            proxima_tela_com_banco = lambda: [setattr(self,'extensao','banco'),self.ir_para_proxima_tela()]
            dba = 'postgres'
            if self.sistema_origem == "Posto Fácil":
                dba = 'firebird'
            
            janela_principal.layout_de_conexao(frame_banco,proxima_tela_com_banco,self.banco_origem,dba)
        
        
        # Campo via relatórios
        label_arquivos = self.tk.Label(frame_arquivos, text=f"Importação via relatório:", font=2)
        label_arquivos.pack(pady=(7,0))
        # Criando os radio buttons para extensões
        extensoes_aceitas = ['.xml', '.xls', '.csv']
        var_extensoes,lista_radio_extensoes = janela_principal.multi_radios(extensoes_aceitas, frame_arquivos,True,False)   
        xml,xls,csv = lista_radio_extensoes
        
        if self.sistema_origem.upper() == "SELLER":
            janela_principal.desativar_radio(xls,csv) # Desativando opções ainda não implantadas
        if self.sistema_origem.upper() == "POSTO FÁCIL":
            janela_principal.desativar_radio(xml,xls,csv) # Desativando opções ainda não implantadas
        # Botão de selecionar arquivos
        proximo = lambda:[setattr(self,'extensao',var_extensoes.get()),self.ir_para_proxima_tela()]
        button_selecionar = self.tk.Button(frame_arquivos, text="Selecionar Arquivo", command=proximo)
        button_selecionar.pack()

        
        # Frame com link para tirar dúvidas
        sub_frame = self.tk.Frame(frame_inferior)
        sub_frame.pack(anchor=self.tk.S)
        texto = self.tk.Label(sub_frame, height=2, wraplength=250,text=f"como retirar relatorios no formato correto de dentro do {self.sistema_origem}?", )
        texto.pack(anchor=self.tk.S)
        link = "https://google.com"
        self.janela.link(texto,link)        
        
        # Rodapé dinâmico
        tela_anterior = lambda:Tela_3(janela_principal,self.migracao)
        janela_principal.rodape(frame_inferior,tela_anterior)

    def ir_para_proxima_tela(self):
        from app.telas.tela_5_conectar_banco import Tela_5
        from app.telas_intermediarias.tela_4 import Tela_intermediaria
        from app.classes.manipular_arquivos import Manipular_arquivos
        from app.classes.matriz import Matriz

        janela_principal = self.janela
        if self.extensao != 'banco':        # Verifica se a importação é feita via banco ou arquivo.
            if (janela_principal.verifica_radio(self.extensao)):
                Manipular_arquivos().selecionar_arquivo(self.extensao)  # Captura o arquivo.
                self.matriz = Matriz(self.migracao,self.sistema_origem,self.sistema_destino,self.extensao, self.banco_origem).filtro_de_importacao() # Gera uma matriz a depender da extensão
                if self.matriz:
                    # Se tiver a matriz, vai para a próxima tela.
                    Tela_5(janela_principal,self.migracao,self.sistema_origem,self.sistema_destino,self.extensao,self.matriz)
                else:
                    self.erros("Erro", f"Este módulo ainda não foi implantado.")
            else: return None
        
            
        else:
            if self.banco_origem.cursor:
                Tela_intermediaria(self.janela,self.migracao,self.sistema_origem, self.sistema_destino, self.extensao, self.matriz, self.banco_origem)
            else:
                self.erros("Erro", f"Nenhum banco foi encontrado.")