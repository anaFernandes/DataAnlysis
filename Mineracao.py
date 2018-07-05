import pandas as pd
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC


class Mineracao(object):

    # -----------------------------------------------------------
    # Funcionamento : Classifica o produto entre 'interessante' e 'não interessante' dados os atributos do mesmo
    # Parâmetros : dados_cliente, produtos_treino, dados_cliente_teste, produtos_teste
    # Retorno : Um dataframe com a classificacao dos produtos (0 ou 1)
    def Classificacao(self, dados_cliente, produtos_treino, dados_cliente_teste, produtos_teste):
        dado={}
        dado_cliente={}
        precisao = {}
        for produto in produtos_treino:
            dado[produto] = pd.DataFrame.from_dict(dados_cliente[produto])
            dado_cliente[produto] = pd.DataFrame.from_dict(dados_cliente_teste[produto])
            dados_teste = dados_cliente_teste[produto].values
            dados_teste = dados_teste.astype(float)
            dados_teste = dados_teste.astype(int)

            modelo = MultinomialNB()
            modelo.fit(produtos_treino[produto], dado[produto].values.ravel())
            produto_previsto_MNB = modelo.predict(produtos_teste[produto])
            produto_previsto_MNB = produto_previsto_MNB.astype(int)
            precisao_media = average_precision_score(dados_teste, produto_previsto_MNB)
            dados_cliente_teste[produto]['MultinomialNB'] = pd.Series(produto_previsto_MNB, index=dados_cliente_teste[produto].index)
            precisao[produto] = precisao_media


            model = SVC()
            model.fit(produtos_treino[produto], dado[produto].values.ravel())
            produto_previsto_SVC = model.predict(produtos_teste[produto])
            produto_previsto_SVC = produto_previsto_SVC.astype(int)
            precisao_media = average_precision_score(dados_teste, produto_previsto_SVC)
            dados_cliente_teste[produto]['SVC'] = pd.Series(produto_previsto_MNB, index=dados_cliente_teste[produto].index)
            precisao[produto] = precisao_media
            dados_cliente_teste[produto] = pd.DataFrame(produto_previsto_SVC, dtype='str', index=dados_cliente_teste[produto].index)

