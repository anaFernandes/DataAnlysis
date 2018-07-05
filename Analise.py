import pandas as pd


class Analise(object):

    # -----------------------------------------------------------
    # Funcionamento : Agupa todos os resultados, e os resultados que foram considerados interessantes.
    # Parâmetros : products
    # Retorno : Um dataframe de produtos somente com tipos de produtos que foram considerados interessantes pelo cliente
    def Agrupa_resultados (self, dados_minerados, tipos_produtos):
        produtos_por_tipo = {}

        print(dados_minerados)
        for tipo in tipos_produtos:
            produto = pd.read_csv("..relatorios/limpeza/treinamento/" + str(tipo) + '.csv', index_col=0)
            produtos_por_tipo[tipo] = pd.DataFrame.from_dict(produto)
            for dados_tipo in dados_minerados[tipo]:
                produtos_por_tipo[produto][dados_tipo] = pd.Series(dados_minerados[tipo][dados_tipo], index=produtos_por_tipo[tipo].index)

        print (produtos_por_tipo)

