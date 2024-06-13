from app.keys.conexao_versao import conexao
from tkinter import messagebox
from app.telas.tela_1_inicial import Tela_1


def main():
    # app = tela_inicial()
    # app.mainloop()

    conectado = conexao()
    if conectado == True:
        app = Tela_1()
        janela = app.carregar_pagina()
        janela.mainloop()
    else:
        # Mensagem para caso o certificado não seja válido
        messagebox.showerror("Erro", "Você está em uma versão desatualizada.\nFavor entrar em contato com o administrador para atualizar.")

    
if __name__ == "__main__":
    main()