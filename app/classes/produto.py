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
        self.substituir = None
        
        self.lista_tributacoes = []
        
        self.lista_codigo_barra = []
        self.lista_nome_grupo = []
        self.lista_nome_subgrupo = []
    
    
    def tratamento_de_matriz(self):
        pass
    
    
    def cadastrar_produto(self,substituir:bool=False) -> Tuple[list[list[any]],int,int,int]:
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
            - 15 - natureza_de_receuta (int)

        
        Args:
            matriz (list): _description_
            janela_principal (_type_): _description_
            substituir (bool, optional): _description_. Defaults to False.
        """
        conexao = self.banco.conexao
        self.substituir = substituir
        if conexao:
            # Declarando listas e contadores
            lista_erros = []
            lista_nome_produtos_sendo_adicionados = []
            contador_produtos_totais = 0
            contador_produtos_adicionados = 0
            contador_multi_codigo_barra = 0
            id = self.banco.id(substituir, 'produto') # Pega o último ID ou o ID 1 para iniciar, a depender da variável substituir
            self.verificar_substituicao()
            print(len(self.lista_nome_grupo))
            print(len(self.lista_nome_subgrupo))



            # Inserção dos grupos e subgrupos, junto com a troca de seus nomes por grid
            matriz = self.troca_de_grupo()
            
            resultado_tributacao_padrao = self.banco.executar_query(f"SELECT codigo FROM tributacao WHERE tributacao = 0;")
            tributacao_padrao = resultado_tributacao_padrao[0][0]
            resultado_cd_tributacao = self.banco.executar_query(f"SELECT codigo FROM tributacao;")
            for item in resultado_cd_tributacao:
                self.lista_tributacoes.append(item[0])
            for produto in matriz:
                contador_produtos_totais += 1
                
                grupo,subgrupo,fator_conversao,codigo_ncm,cst_pis,cst_cofins,cst_pis_entrada,cst_cofins_entrada = produto[2],produto[3],produto[8],produto[9],produto[11],produto[12],produto[13],produto[14],

                codigo_barra, nome, preco_venda, custo_medio, unid_venda, unid_compra, natureza_receita,importar, errado, motivo_erro = self.verificacao_erro_produto(id,produto[0],produto[1],produto[4],produto[5],produto[6],produto[7],produto[15])
                if codigo_barra in self.lista_codigo_barra:
                    errado = True
                    importar = False
                    motivo_erro = [f'codigo barra {codigo_barra} já existe dentro do banco de dados (não foi adicionado novamente)']
                # print(len(self.lista_codigo_barra))
                try:
                    tributacao = produto[10]
                    if tributacao not in self.lista_tributacoes:
                        tributacao = tributacao_padrao
                    if tributacao == '':
                        tributacao = tributacao_padrao
                except:
                    tributacao = tributacao_padrao

                if importar:
                    try:
                        if nome in lista_nome_produtos_sendo_adicionados:
                            query = f"SELECT grid FROM produto Where nome = '{nome}'"
                            resultado = self.banco.executar_query(query)
                            grid_certa = resultado[0][0]
                            query = f"INSERT INTO produto_codigo_barra(produto,codigo_barra) Values({grid_certa},{codigo_barra})"
                            self.banco.executar_query(query)
                            self.lista_codigo_barra.append(codigo_barra)
                            
                            contador_multi_codigo_barra += 1
                        else:
                            query = f"INSERT INTO produto(codigo, codigo_barra, nome, grupo, subgrupo, preco_unit, preco_custo, unid_med, unid_med_entrada, qtde_unid_entrada, codigo_ncm, tributacao, cst_pis, cst_cofins, cst_pis_entrada, cst_cofins_entrada, natureza_receita) VALUES({id}, {codigo_barra}, '{nome}', {grupo}, {subgrupo}, {preco_venda}, {custo_medio}, '{unid_venda}', '{unid_compra}', {fator_conversao}, '{codigo_ncm}', '{tributacao}', '{cst_pis}', '{cst_cofins}', '{cst_pis_entrada}', '{cst_cofins_entrada}', {natureza_receita});"
                            self.banco.executar_query(query)
                            lista_nome_produtos_sendo_adicionados.append(nome)
                            self.lista_codigo_barra.append(codigo_barra)
                            contador_produtos_adicionados += 1
                            id += 1
                    except Exception as e:
                        motivo_erro.append(e)
                        errado = True
                        importar = False
                        self.banco.iniciar(self.banco.usuario,self.banco.senha,self.banco.banco,self.banco.porta,self.banco.host)

                if errado:
                    if importar:
                        id_erro = id-1
                        importado = 'Importado com restrição'
                    else:
                        id_erro = '###'
                        importado = 'Não importado'
                    lista_erros.append([id_erro,nome,codigo_barra,preco_venda,custo_medio,importado,motivo_erro])
            conexao.commit()
                        
            resultado_produtos_totais_no_banco = self.banco.executar_query(f"SELECT codigo FROM produto;")
            self.banco.finalizar()
            return lista_erros, contador_produtos_adicionados,contador_produtos_totais,len(resultado_produtos_totais_no_banco), contador_multi_codigo_barra

    def troca_de_grupo(self) -> list[list]:
        """Método para trocar o grupo pelo grid equivalente

        Args:
            matriz (list[list]): matriz antes

        Returns:
            list[list]: matriz depois da mudança
        """
        from app.classes.correcoes import Correcao
        matriz  = self.matriz
        corretor = Correcao()
        grupo_dict = {}
        for linha in matriz:
            grupo = corretor.corrigir_nome_acentos(linha[2])
            subgrupo = corretor.corrigir_nome_acentos(linha[3])
            if grupo in grupo_dict:
                grupo_dict[grupo].add(subgrupo)
            else:
                grupo_dict[grupo] = {subgrupo}
        for item in grupo_dict:
            grupo_dict[item] = list(grupo_dict[item])
        grupo_com_grid, subgrupo_com_grid = self.cadastrar_grupo_produto(grupo_dict)
        
        for linha in matriz:
            linha[2] = grupo_com_grid[corretor.corrigir_nome_acentos(linha[2])]
            linha[3] = subgrupo_com_grid[corretor.corrigir_nome_acentos(linha[3])]
        return matriz

    def cadastrar_grupo_produto(self,dicionario:dict) -> Tuple[dict,dict]:
        """Este métodos, de acordo com um dicionário onde os grupos são
        a chave e os subgrupos são os valores, faz a inserção dos grupos
        e sub grupos e devolve um grid

        Args:
            dicionario (dict): Dicionário pronto com grupos e subgrupos

        Returns:
            Tuple[dict,dict]: Envia 2 dicionário (um de grupo e outro de subgrupo). 
            cada dicionário tem o nome como chave e o grid como valor
        """
        # De acordo com a variável substituir, deleta os bancos anteriores, ou pega o id de acordo com a coluna codigo         
        id = self.banco.id(self.substituir,'grupo_produto')
        id_sub = self.banco.id(self.substituir,'subgrupo_produto')
        grupo_com_grid = {} 
        subgrupo_com_grid = {}
        if self.substituir:
            pass

        # Para cada um dos grupos, vai pegar também a lista de subgrupos associada a ele
        for grupo, subgrupos in dicionario.items():
            if grupo in self.lista_nome_grupo:
                resultado_grid_grupo_existente = self.banco.executar_query(f"SELECT grid FROM grupo_produto WHERE nome = '{grupo}'")
                grid_do_grupo_atual = resultado_grid_grupo_existente[0][0]
            else:
                self.banco.executar_query(f"INSERT INTO grupo_produto (codigo,nome,flag,estoque_negativo_deposito) VALUES ({id},'{grupo}','A',true);")
                resulltado_grid_do_grupo_atual = self.banco.executar_query(f"SELECT grid FROM grupo_produto WHERE codigo = {id};")
                grid_do_grupo_atual = resulltado_grid_do_grupo_atual[0][0]
                id += 1

            grupo_com_grid[grupo] = grid_do_grupo_atual
            
            for subgrupo in subgrupos:
                if subgrupo in self.lista_nome_subgrupo:
                    resultado_grid_subgrupo_existente = self.banco.executar_query(f"SELECT grid FROM subgrupo_produto WHERE nome = '{subgrupo}'")
                    grid_do_subgrupo_atual = resultado_grid_subgrupo_existente[0][0]
                else:
                    self.banco.executar_query(f"INSERT INTO subgrupo_produto (codigo,nome,grupo,flag) VALUES ({id_sub},'{subgrupo}',{grid_do_grupo_atual},'A');")
                    resultado_grid_do_subgrupo_atual = self.banco.executar_query(f"SELECT grid FROM subgrupo_produto WHERE codigo = {id_sub};")
                    grid_do_subgrupo_atual = resultado_grid_do_subgrupo_atual[0][0]
                    id_sub += 1
                    
                subgrupo_com_grid[subgrupo] = grid_do_subgrupo_atual

        resultado_banco_deposito = self.banco.executar_query(f"SELECT grid FROM deposito WHERE codigo = 100;")
        if resultado_banco_deposito:
            grid_depoisto = resultado_banco_deposito[0][0]
            self.banco.executar_query(f"UPDATE deposito SET estoque_negativo = false WHERE codigo = 100;")
        else:
            self.banco.executar_query(f"INSERT INTO deposito (codigo,nome,empresa,flag) VALUES (100,'DEPOSITO LOJA',1,'A');")
            resultado_banco_deposito_padrao = self.banco.executar_query(f"SELECT grid FROM deposito WHERE codigo = 100;")
            grid_depoisto = resultado_banco_deposito_padrao[0][0]
        if self.substituir:
            self.banco.executar_query(f"DELETE FROM deposito_grupo_produto WHERE deposito = ({grid_depoisto});")
        for nome_grupo, grid_grupo in grupo_com_grid.items():
            self.banco.executar_query(f"DELETE FROM deposito_grupo_produto WHERE grupo = ({grid_grupo});")
            self.banco.executar_query(f"INSERT INTO deposito_grupo_produto (deposito,grupo) VALUES ({grid_depoisto},{grid_grupo});")
        self.banco.conexao.commit()
        return grupo_com_grid, subgrupo_com_grid


    def verificar_substituicao(self) -> Tuple[list,list,list]:
        if self.substituir:
            # Se for pra substituir, deleta a tabela de produto com código de barras
            self.banco.executar_query(f"DELETE FROM produto_codigo_barra")
        else:
            # Se for apenas para adicionar, ele irá fazer uma lista com os códigos de barras com os produtos atuais
            resultado_codigo_barra = self.banco.executar_query(f"SELECT codigo_barra FROM produto UNION all SELECT codigo_barra FROM produto_codigo_barra")
            for codigo in resultado_codigo_barra:
                self.lista_codigo_barra.append(codigo[0])            
            resultado_nome_grupos = self.banco.executar_query(f"SELECT nome FROM grupo_produto")
            for nome in resultado_nome_grupos:
                self.lista_nome_grupo.append(nome[0])
            
            resultado_nome_subgrupos = self.banco.executar_query(f"SELECT nome FROM subgrupo_produto")
            for nome in resultado_nome_subgrupos:
                self.lista_nome_subgrupo.append(nome[0])

    def verificacao_erro_produto(self, id_do_produto:int,codigo_barra:str, nome:str, preco_venda:str, custo_medio:str, unid_venda:str, unid_compra:str, natureza_receita:str) -> Tuple[str,str,str,str,str,str,str,bool,bool,list[str]]:
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
        correcao = Correcao()
        motivo_erro = []
        errado = False
        importar = True
        if codigo_barra:
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
        if not natureza_receita:
            natureza_receita = 'null'
            # motivo_erro.append('Falta natureza de receita')
            # errado = True
            importar = True
        if codigo_barra == '' or not codigo_barra:
            motivo_erro.append(f'Falta de codigo de barras. Foi replicado o ID do produto ({id_do_produto}) no código de barra')
            codigo_barra = id_do_produto
            errado = True
            importar = True
        if nome == '' :
            motivo_erro.append('Falta de nome')
            errado = True
            importar = False
        if correcao.identificar_kit(unid_venda) or correcao.identificar_kit(unid_compra):
            motivo_erro.append('Kit não importado, favor, verificar cadastro.')
            errado = True
            importar = False
        if codigo_barra in self.lista_codigo_barra:
            errado = True
            importar = False
            motivo_erro = [f'codigo barra {codigo_barra} já existe dentro do banco de dados (não foi adicionado novamente)']
        else:
            self.lista_codigo_barra.append(codigo_barra)
            
        return codigo_barra, nome, preco_venda, custo_medio, unid_venda, unid_compra, natureza_receita, importar, errado, motivo_erro

