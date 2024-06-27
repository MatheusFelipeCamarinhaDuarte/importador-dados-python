from tkinter import messagebox

class Banco_de_dados():
    """Classe de banco de dados e suas operações"""
    from typing import Callable, Optional, Tuple, List

    def __init__(self, usuario:str = '',senha:str = '', banco:str = '',porta:int = '5432', host:str = 'localhost'):
        self.usuario = usuario
        self.senha = senha
        self.banco = banco
        self.porta = porta
        self.host = host
        self.conexao = None
        self.cursor = None
        if banco != '':
            self.iniciar(self.usuario,self.senha,self.banco,self.porta,self.host)

    def iniciar(self,usuario:str,senha:str,banco:str,porta:int = '5432', host:str = 'localhost') -> None:
        """Método para inciar o banco de dados a partir de usuáriom senha e nome do banoc de dados

        Args:
            janela_principal (Janela): Janela principal da aplicação
            usuario (str): Nome do usuário passado por meio de input
            senha (str): senha do usuário passado por meio de input
            banco (str): Nome do banco passado por meio de input

        Returns:
            conecao: retorna uma conexão com o banco de dados especificado.
        """
        import psycopg2
        self.usuario = usuario
        self.senha = senha
        self.banco = banco
        self.porta = porta
        self.host = host
        try:
            conn1 = psycopg2.connect(
                host=host,
                port=porta,
                user=usuario,
                password=senha,
                database=banco
            )
            cur1 = conn1.cursor()
            self.cursor = cur1 
            self.conexao = conn1
            messagebox.showinfo("Sucesso", "Conexão estabelecida com sucesso")
        except:
            self.cursor = None 
            self.conexao = None
            self.usuario = ''
            self.senha = ''
            self.banco = ''
            self.porta = ''
            self.host = ''
            messagebox.showerror("Erro", "Os dados passados de usuário, senha ou banco estão incorretos.")

    def iniciar_firebird(self,usuario:str,senha:str,banco:str) -> None:
        """Método para inciar o banco de dados a partir de usuáriom senha e nome do banoc de dados

        Args:
            janela_principal (Janela): Janela principal da aplicação
            usuario (str): Nome do usuário passado por meio de input
            senha (str): senha do usuário passado por meio de input
            banco (str): Nome do banco passado por meio de input

        Returns:
            conecao: retorna uma conexão com o banco de dados especificado.
        """
        import fdb
        self.usuario = usuario
        self.senha = senha
        self.banco = banco

        try:
            dns = 'localhost:'+banco.replace("\\", "\\\\")
            conn1 = fdb.connect(
                user=usuario,
                password=senha,
                dsn=dns
            )
            cur1 = conn1.cursor()
            self.cursor = cur1 
            self.conexao = conn1
            messagebox.showinfo("Sucesso", "Conexão estabelecida com sucesso")
        except:
            self.cursor = None 
            self.conexao = None
            self.usuario = ''
            self.senha = ''
            self.banco = ''
            self.porta = ''
            self.host = ''
            messagebox.showerror("Erro", "Os dados passados de usuário, senha ou banco estão incorretos.")

    def finalizar(self) -> None:
        """Método para o fechamento correto do banco de dados."""
        self.conexao.commit()
        self.cursor.close()
        self.conexao.close()
        self.cursor = None
        self.conexao = None

    def executar_query(self, query):
        """Método para executar uma query no banco de dados"""
        cursor = self.cursor
        try:
            cursor.execute(query)
            self.conexao.commit()
        except Exception as e:
            print(e)
        try:
            resultado = cursor.fetchall()
            print(resultado)
        except:
            resultado = None
        return resultado

    def id(self,substituir, tabela):
        id = 1
        if substituir:
            self.cursor.execute(f"DELETE FROM {tabela}")
        else:
            self.cursor.execute(f"SELECT * FROM {tabela}")
            result1 = self.cursor.fetchall()
            maior_numero = 0
            for i in result1:
                numero = int(i[0])
                if numero >= maior_numero:
                    maior_numero = numero
            id = maior_numero + 1
        return id
