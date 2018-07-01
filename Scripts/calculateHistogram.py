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
data = np.zeros((len(xeLiquorOrig),len(yeLiquorOrig)))

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

import gc
day = 0
#result = np.zeros((365*8,(len(bars))),dtype='float32')
results = []

t1 = time.time()
print("\t",t1 - t0,"seconds elapsed")
t0 = t1
print('Finished loading pandas')
for year in range(2009,2016):

    for month in range(1,12):
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

        for k in datetimes:
            tmp = rides.loc[rides['date'] == k]
            for l,m,n in zip(tmp['pGridLat'],tmp['pGridLon'],tmp['passenger_count']):
                numRides = 1
                if(not np.isnan(n)):
                    numRides = n

                data[int(l),int(m)] += numRides
    

            ########################################
            # Normalize matrix
            ########################################
            data *= 1.0/normalizedBar

            counter = 0
            tmpDict = { 'Date' : k }
            for gg,hh,ii,jj in zip(bars['Index'],bars['Doing Business As (DBA)'],bars['LatGrid'],bars['LonGrid']):
                i,j = int(ii),int(jj)
                sample = data[i-2:i+3,j-2:j+3]
                if(sample.shape != blurHist.shape):
                    print(gg,hh,ii,jj)
                    raise ValueError
                tmpDict[hh] = (np.sum(blurHist * sample))
                counter += 1

            results.append(pd.DataFrame(tmpDict,columns=bars['Doing Business As (DBA)'],index=[k]))

            day += 1
            data *= 0
        
        print("\tDays analyzed:",day)
        print("\tThere are now",len(results),"records in database")
    
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

        for k in datetimes:
            tmp = rides.loc[rides['date'] == k]
            for l,m in zip(tmp['pGridLat'],tmp['pGridLon']):
                data[int(l),int(m)] += 1
    
            counter = 0
            tmpDict = { 'Date' : k }
            for gg,hh,ii,jj in zip(bars['Index'],bars['Doing Business As (DBA)'],bars['LatGrid'],bars['LonGrid']):
                i,j = int(ii),int(jj)
                sample = data[i-2:i+3,j-2:j+3]
                if(sample.shape != blurHist.shape):
                    print(gg,hh,ii,jj)
                    raise ValueError
                tmpDict[hh] = (np.sum(blurHist * sample))
                counter += 1

            results.append(pd.DataFrame(tmpDict,columns=bars['Doing Business As (DBA)'],index=[k]))

            day += 1
            data *= 0
        
        print("\tDays analyzed:",day)
        print("\tThere are now",len(results),"records in database")
    
        gc.collect()
        t1 = time.time()
        print("\t",t1 - t0,"seconds elapsed")
        t0 = t1
        print("Finished with year: {:d}".format(year),flush=True)
########################################

df = pd.concat(results)
s = df.columns.to_series()
df.columns = s + s.groupby(s).cumcount().astype(str).replace({'0':''})
df.to_hdf('histResult.hdf','table')
#np.save('result.npy',result)

