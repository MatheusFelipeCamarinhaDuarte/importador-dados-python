from abc import ABC, abstractmethod

try:
    from app.classes.janela import Janela
    from app.classes.banco_de_dados import Banco_de_dados
except:
    from janela import Janela
    
class Telas(ABC):
    """Classe para importação de arquivos"""
    from app.classes.janela import Janela
    def __init__(self,janela:Janela = None,migracao:str = '',sistema_origem:str = '',sistema_destino:str = '',extensao:str = '', matriz:list = [], banco_origem:Banco_de_dados = Banco_de_dados(),banco_destino:Banco_de_dados = Banco_de_dados()):
        """Método de criação das telas de importacao"""
        super().__init__()
        # Tipo de migracao
        self.migracao = migracao
        # Sistema de origem
        self.sistema_origem = sistema_origem
        # Sistema de destino
        self.sistema_destino = sistema_destino
        # Tipo de extensão
        self.extensao = extensao
        # Matriz
        self.matriz = matriz
        #Banco de dados de origem
        self.banco_origem = banco_origem
        #Banco de dados de destino
        self.banco_destino = banco_destino
        # Janela
        if janela:
            self.janela = janela
            self.carregar_pagina()
        else:
            self.janela = Janela()
    @abstractmethod
    def carregar_pagina():
        raise NotImplementedError("Subclasses devem implementar este método.")
    @abstractmethod
    def ir_para_proxima_tela():
        raise NotImplementedError("Subclasses devem implementar este método.")



                
                
                
                
                
                
                