# !-*- conding: utf8
import numpy as np
import pandas as pd

class Split_dataframe(object):

    # -----------------------------------------------------------
    # Funcionaento : Divide o dataframe products em 2 partes, 2/3 serão utilzados no treinamento dos classificadores
    # e um terço será utilizado na fase de validação do classificadores
    # Parâmetros : products
    # Retorno : train_model, test
    # ----------------------------------------------------------
    def separa(self, products):

        #Verifico o tamanho máximo do data frame
        len_products = len(products.index)

        #divido esse tamanho em 3 pedaços, 2/3 serão utilizados no treinamento e 1/3 na validação
        len_train = int(len_products*2/3)

        #seleciono os dados para o treinamento
        test = products.loc[1:len_train]

        #seleciono os dados para a validação
        train_model = products.loc[len_train+1:]

        return train_model, test