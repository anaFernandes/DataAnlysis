import csv

import pandas as pd

#estração, transformação e carga
class Etl(object):


    #-----------------------------------------------------------
    # Funcionamento : Seleciona os produtos que foram considerados interessantes e verifica quais tipos de produtos são
    # interessantes para o cliente. A seguir os produtos que não foram considerados interessantes para os clientes são
    # eliminados do data frame.
    # Parâmetros : products
    # Retorno : Um dataframe de produtos somente com tipos de produtos que foram considerados interessantes pelo cliente
    # ----------------------------------------------------------
    def Limpeza_dados(self, produtos, produtos_interessantes):

        produtos_nao_interessantes = list()

        tipos_produtos_unicos = (produtos.TIPO_PRODUTO.drop_duplicates())
        tipos_produtos_interessantes_unicos = (produtos_interessantes.TIPO_PRODUTO.drop_duplicates())

        for tipo_produto_unico in tipos_produtos_unicos:
            var = 'nao interessante'
            for produto_interessante in tipos_produtos_interessantes_unicos:
                if (tipo_produto_unico == produto_interessante):
                    var = 'interessante'
                    break

            if var != 'interessante' :
                produtos_nao_interessantes.append(tipo_produto_unico)

        for produto in produtos_nao_interessantes:
            produtos = produtos[produtos.TIPO_PRODUTO != produto]

        return produtos, tipos_produtos_interessantes_unicos


    #-----------------------------------------------------------
    # Funcionamento : Nesta etapa são verificadas as colunas que possuem muitos valores nulos, determinado produto pode
    # ter um atributo importante para ele mas não para os outros também é feita uma verificação de acordo com o produto
    # Parâmetros : products
    # Retorno : dataframe de produtos
    # ----------------------------------------------------------
    def Limpeza_valores_perdidos(self, produtos, produtos_interessantes, teste):

        tipos_produtos_unicos = (produtos.TIPO_PRODUTO.drop_duplicates())

        produtos_por_tipo = {}
        miss_value_percent = {}
        miss_value_insteresting_percent = {}

        # Divide os valores dos produtos de acordo com tipo e os coloca dentro de um dict de dataframes
        # Cria um dataframe com a porcentagem de valores perdidos separados por tipo de produto e por caracteristicas
        for tipo_produto in tipos_produtos_unicos:
            produto_por_tipo = (produtos[produtos.TIPO_PRODUTO == tipo_produto])
            valores_perdidos = 100 * produto_por_tipo.isnull().sum() / len(produto_por_tipo)
            miss_value_percent.setdefault(tipo_produto, valores_perdidos)
            produtos_por_tipo[tipo_produto] = pd.DataFrame.from_dict(produto_por_tipo)

            produto_interessante_por_tipo = (produtos_interessantes[produtos_interessantes.TIPO_PRODUTO == tipo_produto])
            valores_perdidos_1 = 100 * produto_interessante_por_tipo.isnull().sum() / len(produto_interessante_por_tipo)
            miss_value_insteresting_percent.setdefault(tipo_produto, valores_perdidos_1)

        data_tipos_produtos_percent = pd.DataFrame.from_dict(miss_value_percent)
        data_insteresting_products = pd.DataFrame.from_dict(miss_value_insteresting_percent)
        data_insteresting_products_transpose = data_insteresting_products.T
        data_products_transpose = data_tipos_produtos_percent.T


        #Somente gera relatórios só para os arquivos de treinamento
        if (teste == 1):
            # Gera relatórios com base nos valores nulos de cada produto,
            # o primeiro relatório é relacionado com os produtos que o cliente manifestou interesse
            data_insteresting_products_transpose.to_csv('relatorios/porcentagem_de_valores_nulos_separados_pelo_tipo_so_nos_produtos_interessantes.csv', sep=',', encoding='utf-8')
            # o segundo é relacionado com todos os produtos
            data_products_transpose.to_csv('relatorios/porcentagem_de_valores_nulos_separados_pelo_tipo.csv', sep=',', encoding='utf-8')

        index_array = data_insteresting_products_transpose.index
        # Elimina as colunas por tipo de produto com valores perdidos maiores que 5%
        # Preenche as colunas linearmente de acordo com o tipo de produto
        for coluna_produto in data_insteresting_products_transpose:
            contador_index = 0
            for data1 in data_insteresting_products_transpose[coluna_produto]:
                for tipo_produto in tipos_produtos_unicos:
                    if (data1 >= 5 and tipo_produto == index_array[contador_index]):
                        produtos_por_tipo[index_array[contador_index]] = produtos_por_tipo[index_array[contador_index]].drop(coluna_produto, axis=1)
                    if (data1 <= 5 and tipo_produto == index_array[contador_index]):
                        produtos_por_tipo[index_array[contador_index]] = produtos_por_tipo[index_array[contador_index]].interpolate()
                produtos_por_tipo[index_array[contador_index]] = produtos_por_tipo[index_array[contador_index]].fillna(method='ffill')
                contador_index = contador_index + 1

        for produto in produtos_por_tipo:
            produtos_por_tipo[produto] = produtos_por_tipo[produto].dropna()

        # Elimina as colunas em que todos os elementos possuem o mesmo valor
        for produto in produtos_por_tipo:
            for coluna_produto in produtos_por_tipo[produto]:
                if (coluna_produto != 'INTERESTED'):
                    if (len(produtos_por_tipo[produto][coluna_produto].drop_duplicates()) == 1):
                        produtos_por_tipo[produto] = produtos_por_tipo[produto].drop(coluna_produto, axis=1)

        #Gera os relatórios
        for produto in produtos_por_tipo:
            if(teste == 1):
                produtos_por_tipo[produto].to_csv("relatorios/limpeza/treinamento/"+str(produto)+ '.csv', sep=',', encoding='utf-8')
            else:
                produtos_por_tipo[produto].to_csv("relatorios/limpeza/teste/"+str(produto)+'.csv', sep=',', encoding='utf-8')

        return produtos_por_tipo

    # -----------------------------------------------------------
    # Funcionamento : Aqui é feita a trasformação dos dados, strings são mudadas para inteiros
    # Parâmetros : produtos
    # Retorno : dataframe de produtos
    # ----------------------------------------------------------
    def arruma_valores(self, tipos_produtos):
        produtos_por_tipo = {}
        produtos_por_tipo_teste = {}
        for tipo in tipos_produtos:
            produto = pd.read_csv("relatorios/limpeza/treinamento/"+str(tipo)+'.csv', index_col = 0)
            produtos_por_tipo_teste[tipo] = pd.DataFrame.from_dict(produto)

        for tipo in tipos_produtos:
            produto = pd.read_csv("relatorios/limpeza/treinamento/" + str(tipo) + '.csv', index_col=0)
            produtos_por_tipo[tipo] = pd.DataFrame.from_dict(produto)

        sumario = {}
        #Tranformo os valores em string em inteiros
        for produto in produtos_por_tipo:
            for coluna_produto in produtos_por_tipo[produto]:
                tamanho = (produtos_por_tipo[produto][coluna_produto].drop_duplicates())
                if type(produtos_por_tipo[produto][coluna_produto].values[0]) == str:
                    contador_valor = 1
                    for valor in tamanho:
                        produtos_por_tipo_teste[produto][coluna_produto] = produtos_por_tipo_teste[produto][coluna_produto].replace(valor, contador_valor)
                        produtos_por_tipo[produto][coluna_produto] = produtos_por_tipo[produto][coluna_produto].replace(valor, contador_valor)
                        contador_valor = 1+contador_valor

        for produto in produtos_por_tipo:
            produtos_por_tipo_teste[produto].to_csv('relatorios/transformacao/teste/' + str(produto) + '.csv', sep=',', encoding='utf-8')
            produtos_por_tipo[produto].to_csv('relatorios/transformacao/treinamento/' + str(produto) + '.csv', sep=',', encoding='utf-8')

        return produtos_por_tipo, produtos_por_tipo_teste

    # -----------------------------------------------------------
    # Funcionamento : Nesta etapa são separados os atributos do conjuntos de dados das features, tanto para o teste,
    # Quanto para o treinamento
    # Parâmetros : tipos dos produtos, produto_teste, produtos_treinamento
    # Retorno : dataframe de produtos
    # ----------------------------------------------------------
    def Separa_dados_treinamento(self, tipos_produtos):

        produtos_por_tipo = {}
        produtos_por_tipo_teste = {}
        for tipo in tipos_produtos:
            produto = pd.read_csv("relatorios/transformacao/teste/" + str(tipo) + '.csv', index_col=0)
            produtos_por_tipo_teste[tipo] = produto

        for tipo in tipos_produtos:
            produto = pd.read_csv("relatorios/transformacao/treinamento/" + str(tipo) + '.csv', index_col=0)
            produtos_por_tipo[tipo] = produto

        produtos_cliente_teste = {}
        produtos_cliente = {}

        for produto in tipos_produtos:
            produtos_cliente[produto] = {}
            produtos_cliente_teste[produto] = {}
            produtos_cliente[produto] = produtos_por_tipo[produto].INTERESTED
            produtos_cliente[produto] = pd.DataFrame.from_dict(produtos_cliente[produto])
            produtos_cliente_teste[produto] = produtos_por_tipo_teste[produto].INTERESTED
            produtos_cliente_teste[produto] = pd.DataFrame.from_dict(produtos_cliente_teste[produto])
            produtos_por_tipo[produto] = produtos_por_tipo[produto].drop('INTERESTED', axis=1)
            produtos_por_tipo_teste[produto] = produtos_por_tipo_teste[produto].drop('INTERESTED', axis=1)


        return produtos_cliente, produtos_por_tipo, produtos_cliente_teste, produtos_por_tipo_teste
