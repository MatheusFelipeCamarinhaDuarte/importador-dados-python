from app.classes.telas import Telas
from app.classes.janela import Janela

class Tela_intermediaria(Telas):
    def carregar_pagina(self):
        """Janela aberta para escolha de qual filial deve ser selecionada no Posto Fácil

        Returns:
            None
        """
        
        # Importações
        import tkinter as tk
        from tkinter import ttk,messagebox
        
        try:
            # Criação da janela principal
            janela_principal = Janela()
            janela_principal.title("Escolha a Filial")

            # Colocando as dimensões iniciais (e fixas) da tela
            altura = 400
            largura = 550
            x = (janela_principal.winfo_screenwidth() // 2) - (largura // 2)
            y = (janela_principal.winfo_screenheight() // 2) - (altura // 2)
            janela_principal.geometry(f"{largura}x{altura}+{x}+{y}")
            
            # Colocando a linha de apresentação do projeto
            apresentacao = tk.Label(janela_principal, text="Projeto de importação de dados entre sistemas")
            apresentacao.pack(anchor=tk.CENTER, expand=True)
            
            # Colocando a linha de inícia do código em si. Uma vez colocado, ele não volta para cá
            iniciar = lambda: self.ir_para_proxima_tela()
            button = tk.Button(janela_principal, text="INICIAR", width=10,height=1, command=iniciar)
            button.pack(anchor=tk.CENTER, expand=True)
            
            # Retornando a primeira tela criada
            if self.banco_origem.cursor:
                banco = self.banco_origem.cursor
                
                query_empresa = 'SELECT NOM_EMPRESA FROM EMPRESA'
                self.banco_origem.cursor.execute(query_empresa)
                resultado = self.banco_origem.cursor.fetchall()
                # Adicionar um Label para instrução
                label = tk.Label(janela_principal, text="Escolha uma das opções abaixo:")
                label.pack(pady=10)

                # Criar a Combobox
                options = []
                resultado = ['frango', 'calabresa']
                for nome in resultado:
                    options.append(nome)

                combobox = ttk.Combobox(janela_principal, values=options, width=20)
                combobox.pack(pady=10)

                result_label = tk.Label(janela_principal, text="", font=("Helvetica", 14))
                result_label.pack(pady=10)

                # Configurar evento de seleção
                combobox.set(options[0])


                # Iniciar o loop principal da aplicação
                proxima_tela = lambda:[janela_principal.destroy(),self.ir_para_proxima_tela(combobox.get())]
                advance_button = tk.Button(janela_principal, text="Avançar", command=proxima_tela)
                advance_button.pack(pady=10)
                janela_principal.mainloop()
        except Exception as e:
            messagebox.showerror('ERROR',e)

    def ir_para_proxima_tela(self,combobox):
        from app.telas.tela_5_conectar_banco import Tela_5
        from app.classes.matriz import Matriz
        nome_filial = combobox
        self.matriz = Matriz(self.migracao,self.sistema_origem,self.sistema_destino,self.extensao,self.banco_origem,nome_filial).filtro_de_importacao()
        if self.matriz:
            Tela_5(self.janela,self.migracao,self.sistema_origem, self.sistema_destino, self.extensao, self.matriz, self.banco_origem)
        else:
            self.erros("Erro", f"Este módulo ainda não foi implantado.")
