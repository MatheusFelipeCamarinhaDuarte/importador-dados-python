import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
from app.classes.janela import Janela


class Arquivos():
    def manipular_arquivos_dados(janela_principal:Janela):
        pass

    def deletar_arquivo_temp(extensao_desejada):
        
        caminho_app = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        caminho_absoluto = os.path.join(caminho_app,'temp', 'dados')
        caminho_do_arquivo = os.path.join(caminho_absoluto, "arquivo_temporario"+extensao_desejada)
        os.remove(caminho_do_arquivo)