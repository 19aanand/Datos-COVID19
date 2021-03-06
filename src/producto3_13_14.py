'''
MIT License

Copyright (c) 2020 Sebastian Cornejo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import csv
import pandas as pd
from os import listdir
from os.path import isfile, join

# product3 simplemente es una compilacion de los casos confirmados por dia en una tabla.
# Todos estos productos dependen del webscrapping

if __name__ == '__main__':

    mypath = "../output/producto4/"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    cumulativoCasosNuevos = pd.DataFrame({'Region':[],
                               'Casos nuevos':[]})
    cumulativoCasosTotales = pd.DataFrame({'Region': [],
                                          'Casos totales': []})
    cumulativoFallecidos = pd.DataFrame({'Region': [],
                                           'Fallecidos': []})


    print(onlyfiles.sort())
    for eachfile in onlyfiles:
        date = eachfile.replace("-CasosConfirmados-totalRegional", "").replace(".csv", "")
        dataframe = pd.read_csv(mypath + eachfile)
        # sanitize headers
        dataframe.rename(columns={'Región': 'Region'}, inplace=True)
        dataframe.rename(columns={'Casos  nuevos': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={' Casos nuevos': 'Casos nuevos'}, inplace=True)
        dataframe.rename(columns={'Casos  totales': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={' Casos totales': 'Casos totales'}, inplace=True)
        dataframe.rename(columns={' Casos fallecidos': 'Fallecidos'}, inplace=True)

        if cumulativoCasosNuevos['Region'].empty:
            cumulativoCasosNuevos[['Region', 'Casos nuevos']] = dataframe[['Region', 'Casos nuevos']]
            cumulativoCasosNuevos.rename(columns={'Casos nuevos': date}, inplace=True)
            cumulativoCasosTotales[['Region', 'Casos totales']] = dataframe[['Region', 'Casos totales']]
            cumulativoCasosTotales.rename(columns={'Casos totales': date}, inplace=True)
        else:
            cumulativoCasosNuevos[date] = dataframe['Casos nuevos']
            cumulativoCasosTotales[date] = dataframe['Casos totales']

        if 'Fallecidos' in dataframe.columns:
            if cumulativoFallecidos['Region'].empty:
                cumulativoFallecidos[['Region', 'Fallecidos']] = dataframe[['Region', 'Fallecidos']]
                cumulativoFallecidos.rename(columns={'Fallecidos': date}, inplace=True)
            else:
                cumulativoFallecidos[date] = dataframe['Fallecidos']

    #print(cumulativoCasosNuevos.columns)
    #print(cumulativoCasosTotales.columns)
    print(cumulativoFallecidos.columns)
    cumulativoCasosNuevos_T = cumulativoCasosNuevos.transpose()
    cumulativoCasosTotales_T = cumulativoCasosTotales.transpose()
    cumulativoFallecidos_T = cumulativoFallecidos.transpose()

    cumulativoCasosNuevos.to_csv('../output/producto13/CasosNuevosCumulativo.csv', index=False)
    cumulativoCasosNuevos_T.to_csv('../output/producto13/CasosNuevosCumulativo_T.csv', header=False)

    cumulativoCasosTotales.to_csv('../output/producto3/CasosTotalesCumulativo.csv', index=False)
    cumulativoCasosTotales_T.to_csv('../output/producto3/CasosTotalesCumulativo_T.csv', header=False)

    cumulativoFallecidos.to_csv('../output/producto14/FallecidosCumulativo.csv', index=False)
    cumulativoFallecidos_T.to_csv('../output/producto14/FallecidosCumulativo_T.csv', header=False)


