import numpy as np
import scipy.ndimage.filters


########################################
# Initialize base matrices
########################################
import time
t0 = time.time()
print('Initializing code')
SPREAD = np.zeros((7,7))
SPREAD[3,3] = 1
blurHist = np.abs(scipy.ndimage.filters.gaussian_filter(SPREAD,sigma=1))
blurHist = blurHist/np.max(blurHist)


import sys
sys.path.append('../Custom_Libraries')

import GridLib as gl
bg = gl.BaseGrid(resolution=33)

xeLiquorOrig,yeLiquorOrig = bg.getGridIndex()
data = np.zeros((len(xeLiquorOrig),len(yeLiquorOrig)))

########################################
# Read data
########################################
t1 = time.time()
print("\t",t1 - t0,"seconds elapsed")
t0 = t1
print('Reading in pandas data')
import pandas as pd

bars = pd.read_csv('topPlaces5.csv',\
                   engine='c',\
                   dtype={'Index' : 'float',\
                          'Doing Business As (DBA)' : 'str',\
                          'Premises Name' : 'str',\
                          'LatGrid' : 'float',\
                          'LonGrid' : 'float',\
                          'Latitude' : 'float',\
                          'Longitude' : 'float',\
                          'price_level' : 'float',\
                          'weekday' : 'str'})

import gc
day = 0
result = np.zeros((365*8,(len(bars))),dtype='float32')

t1 = time.time()
print("\t",t1 - t0,"seconds elapsed")
t0 = t1
print('Finished loading pandas')
for year in range(2009,2017):

    print('Loading hdf file')
    rides = pd.read_hdf('../Data/tripdata_{:d}.hdf'.format(year),'table')
    rides.dropna(inplace=True)
    rides['date'] = pd.DatetimeIndex(rides['pickup_datetime']).normalize()
    datetimes = rides['date'].unique()
    
    t1 = time.time()
    print("\t",t1 - t0,"seconds elapsed")
    t0 = t1
    print('Finished loading hdf file')
    print("Starting with year: {:d}".format(year))

    for k in datetimes:
        tmp = rides.loc[rides['date'] == k]
        for l,m in zip(tmp['pGridLat'],tmp['pGridLon']):
            data[int(l),int(m)] += 1
    
        counter = 0
        for gg,hh,ii,jj in zip(bars['Index'],bars['Doing Business As (DBA)'],bars['LatGrid'],bars['LonGrid']):
            i,j = int(ii),int(jj)
            sample = data[i-3:i+4,j-3:j+4]
            if(sample.shape != blurHist.shape):
                print(gg,hh,ii,jj)
                raise ValueError
            result[day,counter] = np.sum(sample * blurHist)
            counter += 1

        day += 1
        data *= 0
    
    gc.collect()
    t1 = time.time()
    print("\t",t1 - t0,"seconds elapsed")
    t0 = t1
    print("Finished with year: {:d}".format(year),flush=True)


np.save('result.npy',result)

