import tkinter as tk
from tkinter import ttk



# Criar a janela principal
root = tk.Tk()
root.title("Aplicação Tkinter")
root.geometry("400x300")

# Adicionar um Label para instrução
label = tk.Label(root, text="Escolha uma das opções abaixo:")
label.pack(pady=10)

# Criar a Combobox
options = ["Pequeno", "Médio", "Grande"]
combobox = ttk.Combobox(root, values=options)
combobox.pack(pady=10)

result_label = tk.Label(root, text="", font=("Helvetica", 14))
result_label.pack(pady=10)

# Configurar evento de seleção
combobox.bind("<<ComboboxSelected>>", lambda event: result_label.config(text=f"Você selecionou: {combobox.get()}"))
combobox.set(options[1])
# Label para exibir a opção selecionada

# Iniciar o loop principal da aplicação
root.mainloop()
