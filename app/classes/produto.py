from app.classes.banco_de_dados import Banco_de_dados
class Produto():
    from typing import Callable, Optional, Tuple, List

    def __init__(self,matriz:list[list],banco:Banco_de_dados = Banco_de_dados()):
        """Aqui eu coloco os atributos inciais de Produto

        Args:
            matriz (list[list]): a matriz com os produtos a serem inseridos
            banco (Banco_de_dados): o banco de dados que vai ser usado para cadastrar
        """
        self.matriz = matriz
        self.banco = banco
    
    def cadastrar_produto(self,matriz:list[list]) -> list[list]:
        pass
    
    def tratamento_de_matriz(self):
        pass
    
    
    def cadastrar_produtos(self,substituir:bool=False) -> Tuple[list[list[any]],int,int,int]:
        """Método para cadastrar produtos a partir de uma matriz igual a todos. O formato desta matriz é:
        
        formato ideal:
            - 0 - codigo de barras (str - número)
            - 1 - descricao do produto (str)
            - 2 - grupo (grid)
            - 3 - subgrupo (grid)
            - 4 - preço de venda (double)
            - 5 - preço de compra (double)
            - 6 - unidade de medida de compra (abreviação)
            - 7 - unidade de medida de venda (abreviação)
            - 8 - fator de conversao (int)
            - 9 - codigo ncm (xxxx.xx.xx)
            - 10 - tributacao (int)
            - 11 - cst_pis (int)
            - 12 - cst_cofins (int)
            - 13 - cst_pis_entrada (int)
            - 14 - cst_cofins_entrada (int)
        
        Args:
            matriz (list): _description_
            janela_principal (_type_): _description_
            substituir (bool, optional): _description_. Defaults to False.
        """
        conexao = self.banco.conexao
        if conexao:
            id = self.banco.id(substituir, 'produto')        
            
            if not substituir:
                result1 = self.banco.executar_query(f"SELECT codigo_barra FROM produto")
                maior_numero = 0
                for i in result1:
                    numero = int(i[0])
                    if numero >= maior_numero:
                        maior_numero = numero
                id = maior_numero + 1
            
            # Inserção dos grupos e subgrupos, junto com a troca de seus nomes por grid
            matriz = self.troca_de_grupo(self.matriz)
            
            lista_erros = []
            lista_tributacoes = []
            contador_produtos_totais = 0
            result = self.banco.executar_query(f"SELECT * FROM tributacao WHERE tributacao = 0;")
            resultado_cd_tributacao = self.banco.executar_query(f"SELECT codigo FROM tributacao;")
            for item in resultado_cd_tributacao:
                lista_tributacoes.append(item[0])
            for produto in matriz:
                contador_produtos_totais += 1
                
                grupo,subgrupo,fator_conversao,codigo_ncm,cst_pis,cst_cofins,cst_pis_entrada,cst_cofins_entrada = produto[2],produto[3],produto[8],produto[9],produto[11],produto[12],produto[13],produto[14]

                codigo_barra, nome, preco_venda, custo_medio, unid_venda, unid_compra, importar, errado, motivo_erro = self.verificacao_erro_produto(produto[0],produto[1],produto[4],produto[5],produto[6],produto[7])
                try:
                    tributacao = produto[10]
                    if tributacao not in lista_tributacoes:
                        tributacao = result[0][0]
                    if tributacao == '':
                        tributacao = result[0][0]
                except:
                    tributacao = result[0][0]
                

                if importar:
                    try:
                        query = f"INSERT INTO produto(codigo, codigo_barra, nome, grupo, subgrupo, preco_unit, preco_custo, unid_med, unid_med_entrada, qtde_unid_entrada, codigo_ncm, tributacao, cst_pis, cst_cofins, cst_pis_entrada, cst_cofins_entrada) VALUES({id}, {codigo_barra}, '{nome}', {grupo}, {subgrupo}, {preco_venda}, {custo_medio}, '{unid_venda}', '{unid_compra}', {fator_conversao}, '{codigo_ncm}', '{tributacao}', '{cst_pis}', '{cst_cofins}', '{cst_pis_entrada}', '{cst_cofins_entrada}');"
                        self.banco.executar_query(query)
                        id += 1
                    except Exception as e:
                        motivo_erro.append(e)
                        errado = True
                        importar = False
                if errado:
                    if importar:
                        id_erro = id-1
                        importado = 'Importado com restrição'
                    else:
                        id_erro = '###'
                        importado = 'Não importado'
                    # print(f"Produto {nome} ERRADO!")
                    lista_erros.append([id_erro,nome,codigo_barra,preco_venda,custo_medio,importado,motivo_erro])            
            conexao.commit()
                        
            resultado_produtos_totais = self.banco.executar_query(f"SELECT codigo FROM produto;")
            self.banco.finalizar()
            return lista_erros, len(resultado_produtos_totais),contador_produtos_totais, id

    def troca_de_grupo(self, matriz:list[list]) -> list[list]:
        """Método para trocar o grupo pelo grid equivalente

        Args:
            matriz (list[list]): matriz antes

        Returns:
            list[list]: matriz depois da mudança
        """
        grupo_dict = {}
        for linha in matriz:
            grupo = linha[2]
            subgrupo = linha[3]
            if grupo in grupo_dict:
                grupo_dict[grupo].add(subgrupo)
            else:
                grupo_dict[grupo] = {subgrupo}
        for item in grupo_dict:
            grupo_dict[item] = list(grupo_dict[item])
        
        grupo_com_grid, subgrupo_com_grid = self.cadastrar_grupos_produtos(grupo_dict)
        
        for linha in matriz:
            linha[2] = grupo_com_grid[linha[2]]
            linha[3] = subgrupo_com_grid[linha[3]]
        return matriz

    def cadastrar_grupos_produtos(self,dicionario:dict) -> Tuple[dict,dict]:
        """Este métodos, de acordo com um dicionário onde os grupos são
        a chave e os subgrupos são os valores, faz a inserção dos grupos
        e sub grupos e devolve um grid

        Args:
            dicionario (dict): Dicionário pronto com grupos e subgrupos

        Returns:
            Tuple[dict,dict]: Envia 2 dicionário (um de grupo e outro de subgrupo). 
            cada dicionário tem o nome como chave e o grid como valor
        """
        self.banco.executar_query(f"DELETE FROM grupo_produto")
        self.banco.executar_query(f"DELETE FROM subgrupo_produto")
        id = 1
        id_sub = 1
        grupo_com_grid = {} 
        subgrupo_com_grid = {}
        for grupo, subgrupos in dicionario.items():
            self.banco.executar_query(f"INSERT INTO grupo_produto (codigo,nome,flag,estoque_negativo_deposito) VALUES ({id},'{grupo}','A',true);")
            result1 = self.banco.executar_query(f"SELECT * FROM grupo_produto WHERE codigo = {id};")
            grid_grupo = result1[0][3]
            grupo_com_grid[grupo] = grid_grupo
            for subgrupo in subgrupos:
                self.banco.executar_query(f"INSERT INTO subgrupo_produto (codigo,nome,grupo,flag) VALUES ({id_sub},'{subgrupo}',{grid_grupo},'A');")
                result1 = self.banco.executar_query(f"SELECT * FROM subgrupo_produto WHERE codigo = {id_sub};")
                grid_subgrupo = result1[0][4]
                subgrupo_com_grid[subgrupo] = grid_subgrupo
                id_sub += 1
            id += 1
        
        resultado = self.banco.executar_query(f"SELECT grid FROM deposito WHERE codigo = 100;")
        try:
            grid_depoisto = resultado[0][0]
            self.banco.executar_query(f"UPDATE deposito SET estoque_negativo = false WHERE codigo = 100;")
        except:
            self.banco.executar_query(f"INSERT INTO deposito (codigo,nome,empresa,flag) VALUES (100,'DEPOSITO LOJA',1,'A');")
            resultado = self.banco.executar_query(f"SELECT grid FROM deposito WHERE codigo = 100;")
            grid_depoisto = resultado[0][0]
        # self.cursor.execute("DELETE FROM deposito_grupo_produto WHERE codigo = 100;")
            self.banco.executar_query(f"DELETE FROM deposito_grupo_produto WHERE deposito = ({grid_depoisto});")
        for nome_grupo,grid_dos_grupos in grupo_com_grid.items():
            self.banco.executar_query(f"INSERT INTO deposito_grupo_produto (deposito,grupo) VALUES ({grid_depoisto},{grid_dos_grupos});")
        self.banco.conexao.commit()
        return grupo_com_grid, subgrupo_com_grid

    def verificacao_erro_produto(self, codigo_barra:str, nome:str, preco_venda:str, custo_medio:str, unid_venda:str, unid_compra:str) -> Tuple[str,str,str,str,str,str,bool,bool,list[str]]:
        """Método de verificacao de erros antes das importações.

        Args:
            unid_venda (str): unidade de venda
            unid_compra (str): unidade de compra
            codigo_barra (str): código de barras em string
            nome (str): nome do produto 
            preco_venda (str): o Preço de venda em string

        Returns:
            Tuple[bool,bool,str,list]: retorna o relatório se tem erro, se deve
            importar, como ficou o custo_medio e a lista de motivos de erro (se houver)
        """
        from app.classes.correcoes import Correcao
        correcao = Correcao
        motivo_erro = []
        errado = False
        importar = True
        if len(codigo_barra) < 5:
            motivo_erro.append('codigo de barras inválido')
            errado = True
            importar = True
        if custo_medio =='' or custo_medio == '0' or custo_medio == '0.0' or custo_medio == '0.00' or custo_medio == None:
            custo_medio = '0.10'
            motivo_erro.append('Falta preço custo - Adicionado padrão (0.10)')
            errado = True
            importar = True
        if preco_venda == '' or preco_venda == '0' or preco_venda == '0.0' or preco_venda == '0.00' or preco_venda == None:
            motivo_erro.append('Falta de preço de venda - Adicionado padrão (0.10)')
            preco_venda = '0.10'
            errado = True
            importar = True
        if not unid_venda:
            unid_venda = 'UN'
            motivo_erro.append('Unidade de medida de venda não encontrada - Adicionado padrão (UN)')
            errado = True
            importar = True            
        if not unid_compra:
            unid_compra = 'UN'
            motivo_erro.append('Unidade de medida de compra não encontrada - Adicionado padrão (UN)')
            errado = True
            importar = True
        if codigo_barra == '':
            motivo_erro.append('Falta de codigo de barras')
            errado = True
            importar = False
        if nome == '' :
            motivo_erro.append('Falta de nome')
            errado = True
            importar = False
        if correcao.identificar_kit(unid_venda) or correcao.identificar_kit(unid_compra):
            motivo_erro = ['Kit não importado, favor, verificar cadastro.']
            errado = True
            importar = False

        
        return codigo_barra, nome, preco_venda, custo_medio, unid_venda, unid_compra, importar, errado, motivo_erro

