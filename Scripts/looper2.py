import sys
sys.path.append('../Custom_Libraries')

import GridLib as gl
bg = gl.BaseGrid(resolution=33)

xeLiquorOrig,yeLiquorOrig = bg.getGridIndex()

import gc
from subprocess import call
import pandas as pd

for i in range(2016,2017):

    print("Looping over csv files")
    PATH = '../Data/tripdata_{:d}-{:s}.hdf'.format(i,'01')
    for jj in range(1,7):
        PATH = '../Data/tripdata_{:d}-{:02d}.hdf'.format(i,jj)
        print("\tProcessing: {:s}".format(PATH))
        arr = pd.read_hdf(PATH,'table')
        print("\tSorting files")
        arr.sort_values('pickup_datetime',inplace=True,kind='quicksort')
        print("\tComputing local grids")
        arr['pGridLat'] = pd.cut(arr['pickup_latitude'],xeLiquorOrig,labels=False)
        arr['pGridLon'] = pd.cut(arr['pickup_longitude'],yeLiquorOrig,labels=False)
        arr['dGridLat'] = pd.cut(arr['dropoff_latitude'],xeLiquorOrig,labels=False)
        arr['dGridLon'] = pd.cut(arr['dropoff_longitude'],yeLiquorOrig,labels=False)
        print("\tWriting file to disk")
        newFile = '../Data/tripdata_{:d}-{:02d}-grid.hdf'.format(i,jj)
        arr.to_hdf(newFile,"table")
        del arr        
        print("\tFinished".format(PATH))
    gc.collect()
