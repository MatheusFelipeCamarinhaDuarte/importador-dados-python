from app.chave.conexao_firebase import conexao
from tkinter import messagebox
from app.telas.tela_1_inicial import tela_inicial

if __name__ == "__main__":
    
    # app = tela_inicial()
    # app.mainloop()
    conectado = conexao()
    if conectado == True:
        if conectado:
            app = tela_inicial()
            app.mainloop()
        else:
            # Mensagem para caso o certificado não seja válido
            messagebox.showerror("Erro", "Você não tem um certificado válido")
