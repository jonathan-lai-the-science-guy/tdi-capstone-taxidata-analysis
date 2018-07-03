import numpy as np
import scipy.ndimage.filters


########################################
# Initialize base matrices
########################################
import time
t0 = time.time()
print('Initializing code')
SPREAD = np.zeros((5,5))
SPREAD[2,2] = 1
blurHist = np.abs(scipy.ndimage.filters.gaussian_filter(SPREAD,sigma=1))
blurHist = blurHist/np.max(blurHist)


import sys
sys.path.append('../Custom_Libraries')

import GridLib as gl
bg = gl.BaseGrid(resolution=33)

xeLiquorOrig,yeLiquorOrig = bg.getGridIndex()
data = np.zeros((len(xeLiquorOrig),len(yeLiquorOrig),8)).astype(int)

########################################
# Read data
########################################
import numpy as np

normalizedBar = np.load('../Data/normalizedBar.npy')

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

barsDict = {}
for i,j,k in zip(bars['LatGrid'],bars['LonGrid'],bars['Index']):
    barsDict[(i,j)] = k

import gc
day = 0

dictConvert = { 22:0, 23:1, 0:2 , 1:3 , 2:4 , 3:5 , 4:6 }
results = []

t1 = time.time()
print("\t",t1 - t0,"seconds elapsed")
t0 = t1
print('Finished loading pandas')
for year in range(2009,2016):

    for month in range(1,13):
        print('Loading hdf file')
        rides = pd.read_hdf('../Data/tripdata_{:d}-{:02d}-grid.hdf'.format(year,month),'table')
        rides.dropna(inplace=True)
        print("There are {:d} number of NYC rides".format(len(rides)))
        rides['date'] = pd.DatetimeIndex(rides['pickup_datetime']).hour
        datetimes = rides['date'].unique()

        t1 = time.time()
        print("\t",t1 - t0,"seconds elapsed")
        t0 = t1
        print('Finished loading hdf file')
        print("Starting with year: {:d}".format(year))

        for kk in datetimes:
            tmp = rides.loc[rides['date'] == kk]
            k = dictConvert[kk]
            for pLat,pLon,dLat,dLon,numP in zip(tmp['pGridLat'],\
                                                tmp['pGridLon'],\
                                                tmp['dGridLat'],\
                                                tmp['dGridLon'],\
                                                tmp['passenger_count']):
        
                if((pLat,pLon) in barsDict):
                    numRides = 1
                    if(not np.isnan(numP)):
                        numRides = numP

                    data[int(pLat),int(pLon),k] += int(numRides)
        
        gc.collect()
        t1 = time.time()
        print("\t",t1 - t0,"seconds elapsed")
        t0 = t1
        print("Finished with year: {:d}".format(year),flush=True)

########################################
for year in [2016]:

    for month in range(1,7):
        print('Loading hdf file')
        rides = pd.read_hdf('../Data/tripdata_{:d}-{:02d}-grid.hdf'.format(year,month),'table')
        rides.dropna(inplace=True)
        print("There are {:d} number of NYC rides".format(len(rides)))
#        rides['date'] = pd.DatetimeIndex(rides['pickup_datetime']).normalize()
#        datetimes = rides['date'].unique()
        rides['date'] = pd.DatetimeIndex(rides['pickup_datetime']).hour
        datetimes = rides['date'].unique()
        
        t1 = time.time()
        print("\t",t1 - t0,"seconds elapsed")
        t0 = t1
        print('Finished loading hdf file')
        print("Starting with year: {:d}".format(year))

        for kk in datetimes:
            tmp = rides.loc[rides['date'] == kk]
            k = dictConvert[kk]
            for pLat,pLon,dLat,dLon,numP in zip(tmp['pGridLat'],\
                                                tmp['pGridLon'],\
                                                tmp['dGridLat'],\
                                                tmp['dGridLon'],\
                                                tmp['passenger_count']):
        
                if((pLat,pLon) in barsDict):
                    numRides = 1
                    if(not np.isnan(numP)):
                        numRides = numP

                    data[int(pLat),int(pLon),k] += int(numRides)
        
        print("\tDays analyzed:",day)
        print("\tThere are now",len(results),"records in database")
    
        gc.collect()
        t1 = time.time()
        print("\t",t1 - t0,"seconds elapsed")
        t0 = t1
        print("Finished with year: {:d}".format(year),flush=True)
########################################
np.save('whereArePeopleGoing.npy',data)
