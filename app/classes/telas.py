from abc import ABC, abstractmethod

try:
    from app.classes.janela import Janela
except:
    from janela import Janela
class Telas(ABC):
    """Classe para importação de arquivos"""
    from app.classes.janela import Janela
    def __init__(self,janela:Janela = None,migracao:str = '',sistema_origem:str = '',sistema_destino:str = '',extensao:str = '', matriz:list = []):
        """Método de criação das telas de importacao"""
        # Tipo de migracao
        self.migracao = migracao
        # Sistema de origem
        self.sistema_origem = sistema_origem
        # Sistema de destino
        self.sistema_destino = sistema_destino
        # Tipo de extensão
        self.extensao = extensao
        # Janela
        self.matriz = matriz
        if janela:
            self.janela = janela
            self.carregar_pagina()
        else:
            self.janela = Janela()
        # Matriz
    @abstractmethod
    def carregar_pagina():
        raise NotImplementedError("Subclasses devem implementar este método.")
    @abstractmethod
    def ir_para_proxima_tela():
        raise NotImplementedError("Subclasses devem implementar este método.")



                
                
                
                
                
                
                