from app.classes.telas import Telas

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
            janela_principal = tk.Toplevel(self.janela)
            janela_principal.title("Escolha a Filial")

            # Colocando as dimensões iniciais (e fixas) da tela
            altura = 300
            largura = 300
            x = (janela_principal.winfo_screenwidth() // 2) - (largura // 2)
            y = (janela_principal.winfo_screenheight() // 2) - (altura // 2)
            janela_principal.geometry(f"{largura}x{altura}+{x}+{y}")
            # Retornando a primeira tela criada
            if self.banco_origem.cursor:
                query_empresa = 'SELECT NOM_EMPRESA FROM EMPRESA'
                self.banco_origem.cursor.execute(query_empresa)
                resultado = self.banco_origem.cursor.fetchall()
                # Adicionar um Label para instrução
                label = tk.Label(janela_principal, text="Escolha uma das opções abaixo:")
                label.pack(pady=10)

                # Criar a Combobox
                options = []
                for nome in resultado:
                    options.append(str(nome[0]).replace('{','').replace('}',''))

                lista_nomes_empresas = ttk.Combobox(janela_principal, values=options, width=20)
                lista_nomes_empresas.pack(pady=10)

                # Configurar evento de seleção
                lista_nomes_empresas.set(options[0])


                # Iniciar o loop principal da aplicação
                proxima_tela = lambda:[self.ir_para_proxima_tela(lista_nomes_empresas.get()),janela_principal.destroy()]
                advance_button = tk.Button(janela_principal, text="Avançar", command=proxima_tela)
                advance_button.pack(pady=10)
                janela_principal.mainloop()
        except Exception as e:
            messagebox.showerror('ERROR',e)

    def ir_para_proxima_tela(self,nome_empresa:str):
        from app.telas.tela_5_conectar_banco import Tela_5
        from app.classes.matriz import Matriz
        nome_filial = nome_empresa
        self.matriz = Matriz(self.migracao,self.sistema_origem,self.sistema_destino,self.extensao,self.banco_origem,nome_filial).filtro_de_importacao()
        if self.matriz:
            Tela_5(self.janela,self.migracao,self.sistema_origem, self.sistema_destino, self.extensao, self.matriz, self.banco_origem)
        else:
            self.erros("Erro", f"Este módulo ainda não foi implantado.")
