import sys
sys.path.append('../Custom_Libraries')

import GridLib as gl
bg = gl.BaseGrid(resolution=33)

xeLiquorOrig,yeLiquorOrig = bg.getGridIndex()

import gc
from subprocess import call
import pandas as pd

for i in range(2009,2016):

    print("Looping over csv files")
    PATH = '../Data/tripdata_{:d}-{:s}.hdf'.format(i,'01')
    arr = pd.read_hdf(PATH,'table')
    arr.sort_values('pickup_datetime',inplace=True,kind='quicksort')
    for jj in range(2,13):
        PATH = '../Data/tripdata_{:d}-{:02d}.hdf'.format(i,jj)
        print("\tProcessing: {:s}".format(PATH))
        arr2 = pd.read_hdf(PATH,'table')
        arr2.sort_values('pickup_datetime',inplace=True,kind='quicksort')
        arr = arr.append(arr2)
        print(len(arr))
        del arr2
#        tmp2 = pd.read_csv(PATH,engine='c',\
#                           dtype={ '' : 'int',\
#                                   'pickup_datetime' : 'str',\
#                                   'pickup_longitude' : 'float',\
#                                   'pickup_latitude' : 'float',\
#                                   'dropoff_datetime' : 'str',\
#                                   'dropoff_longitude' : 'float',\
#                                   'dropoff_latitude' : 'float',\
#                                   'passenger_count' : 'int' },\
#                           parse_dates = ['pickup_datetime', 'dropoff_datetime'])
        
        print("\tFinished".format(PATH))
#        arr.append(tmp2)
#    tmp = pd.concat(arr)
#    del arr
#    del tmp2
    gc.collect()
    print("Sorting files")

    print("Computing local grids")
#    arr['pGridLat'] = pd.cut(arr['pickup_latitude'],xeLiquorOrig,labels=False)
#    arr['pGridLon'] = pd.cut(arr['pickup_longitude'],yeLiquorOrig,labels=False)
#    arr['dGridLat'] = pd.cut(arr['dropoff_latitude'],xeLiquorOrig,labels=False)
#    arr['dGridLon'] = pd.cut(arr['dropoff_longitude'],yeLiquorOrig,labels=False)
    print("Writing file to disk")

    newFile = '../Data/tripdata_{:d}.hdf'.format(i)
    arr.to_hdf(newFile,"table")
    del arr
    gc.collect()
