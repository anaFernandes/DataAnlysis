from Mineracao import Mineracao
from Leia_csv import Leia_csv
from Etl import Etl
from Split_dataframe import Split_dataframe


def start():
    #transforma o arquivo em dataframe
    leitor_csv = Leia_csv()
    todos_produtos = leitor_csv.leia()

    separa_dados = Split_dataframe()
    dados_treinamento, dados_teste = separa_dados.separa(todos_produtos)

    #realiza a limpeza dos dados
    dados_etl = Etl()
    produtos_interessantes = (dados_treinamento[dados_treinamento.INTERESTED == 1.0])
    produtos, tipos_produtos_interessantes_unicos = dados_etl.Limpeza_dados(dados_treinamento, produtos_interessantes)
    produtos_treinamento, tipos_produtos_interessantes_unicos = dados_etl.Limpeza_dados(dados_teste, produtos_interessantes)

    # teste = 1
    # dados_etl.Limpeza_valores_perdidos(produtos, produtos_interessantes, teste)
    # teste = 2
    # dados_etl.Limpeza_valores_perdidos(produtos_treinamento, produtos_interessantes, teste)
    dados_etl.arruma_valores(tipos_produtos_interessantes_unicos)

    #previsão dos dados
    dados_cliente, produtos_treino, dados_cliente_teste, produtos_teste = dados_etl.Separa_dados_treinamento(tipos_produtos_interessantes_unicos)

    #mineração dos dados
    Mineracao().Classificacao(dados_cliente, produtos_treino, dados_cliente_teste, produtos_teste)


    exit()



start()