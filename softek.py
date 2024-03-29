# -*- coding: utf-8 -*-
"""Softek.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GRaKQWHG1WARTiPkc30yV5LqCQsVmfCf
"""

import pandas as pd
pd.__version__
pd.DataFrame
import numpy as np
import random

#Declarar un Pandas Series
mylist = list("abcdefghijklmnñopqrstuvwxyz")
df=pd.DataFrame(mylist)
df[0]

#Combinar dos series
mylist = [x for x in "abcdefghijklmnñopqrstuvwxyz"]
myarr = list(range(0,len(mylist)))
ser = pd.DataFrame({"col1:": mylist,"col2": myarr})
ser

#Filtrar elementos que no esten en un Series
ser1 = pd.Series([1,2,3,4,5])
ser2 = pd.Series([4,5,6,7,8])

result = ser1.isin(ser2)
res = ser1[~result]
res

