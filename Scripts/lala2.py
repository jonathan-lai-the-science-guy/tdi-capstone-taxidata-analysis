import numpy as np
import scipy.ndimage.filters


print('Reading in pandas data')
import pandas as pd

bars = pd.read_csv('topPlaces4.csv',\
                   engine='c',\
                   dtype={'Index' : 'float',\
                          'Doing Business As (DBA)' : 'str',\
                          'Premises Name' : 'str',\
                          'LatGrid' : 'float',\
                          'LonGrid' : 'float',\
                          'price_level' : 'float',\
                          'weekday' : 'str'})

for h,i,j in zip(bars['Index'],bars['LatGrid'],bars['LonGrid']):
    if(np.isnan(i) or np.isnan(j)):
        print(h,i,j)
