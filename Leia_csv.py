# !-*- conding: utf8

import pandas as pd

class Leia_csv(object):

    #-----------------------------------------------------------
    # Funcionaento : recebe um arquivo e transforma em dataframe
    # Parâmetros : (void)
    # Retorno : dataframe de produtos
    # ----------------------------------------------------------
    def leia(self):

        produtos = pd.read_csv('problem1_dataset.csv')

        # exit()
        return produtos