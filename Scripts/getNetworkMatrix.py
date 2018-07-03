import numpy as np
import scipy.ndimage.filters


########################################
# Initialize base matrices
########################################
import time
t0 = time.time()

import sys
sys.path.append('../Custom_Libraries')

import GridLib as gl
bg = gl.BaseGrid(resolution=33)

xeLiquorOrig,yeLiquorOrig = bg.getGridIndex()
data = np.zeros((len(xeLiquorOrig),len(yeLiquorOrig)))

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

barsDict = {}
for i,j,k in zip(bars['LatGrid'],bars['LonGrid'],bars['Index']):
    barsDict[(i,j)] = k
import gc

import pickle
for year in range(2009,2017):
    
    print('Loading hdf file')
    for month in range(1,13):
        networkDict = {}
        rides = pd.read_hdf('../Data/tripdata_{:d}-{:02d}-grid.hdf'.format(year,month),'table')
        rides.dropna(inplace=True)
    
        t1 = time.time()
        print("\t",t1 - t0,"seconds elapsed")
        t0 = t1
        print('Finished loading hdf file')
        print("Starting with year: {:d}, month: {:d}".format(year,month))

        for i,j,k,l in zip(rides['pGridLat'],\
                           rides['pGridLon'],\
                           rides['dGridLat'],\
                           rides['dGridLon']):
        
            if((i,j) in barsDict and (k,l) in barsDict):
                point = (barsDict[(i,j)],barsDict[(k,l)]) 
                if point in networkDict:
                    networkDict[point] += 1
                else:
                    networkDict[point] = 1
    
        del rides
        pickle.dump(networkDict, open("networkDict/networkDict-{:04d}-{:02d}.p".format(year,month),"wb"))
        del networkDict
        print("Cleaned up:",gc.collect(),"objects")
        
