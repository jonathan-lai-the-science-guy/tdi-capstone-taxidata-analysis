"""BaseGrid.py is a module to help setup a geographically aware grid."""

__author__      = "Jonathan Lai"
__copyright__   = "Copyright 2018, Jonathan Lai"
__version__ = 0.1
__credits__ = __author__
__license__ = "Copyrighted, give me money to use"
__version__ = "0.1"
__email__ = "jonathan.lai@mg.thedataincubator.com"
__status__ = "Prototype"

import geopy.distance
import pandas as pd
import numpy as np
from numba import jit
import gc

class BaseGrid:
    """
    BaseGrid : Class to setup a geographically aware grid
    """
    EAST_BOUND = -73.750
    SOUTH_BOUND = 40.550
    WEST_BOUND = -74.150
    NORTH_BOUND = 40.900

    LON_CENTER = -73.95
    LAT_CENTER = 40.70

    # Dummy declarations
    # self.xeLiquorOrig = np.array([])
    # self.yeLiquorOrig = np.array([])
    # self.xeLiquor = np.array([])
    # self.yeLiquor = np.array([])

    def __init__(self,\
                 resolution = 33,\
                 EAST_BOUND = -73.750,\
                 SOUTH_BOUND = 40.550,\
                 WEST_BOUND = -74.150,\
                 NORTH_BOUND = 40.900):

        # Cleanup everything
        gc.collect()

        # Check to make sure that the input is okay:
        assert(EAST_BOUND > WEST_BOUND)
        assert(NORTH_BOUND > SOUTH_BOUND)
        assert(resolution > 0)
        assert(EAST_BOUND <= 180. and WEST_BOUND >= -180.)
        assert(NORTH_BOUND <= 90. and SOUTH_BOUND >= -90.)

        # Precompute the dimensionality of the geographical space
        LON_BOUND = EAST_BOUND - WEST_BOUND
        LAT_BOUND = NORTH_BOUND - SOUTH_BOUND 
        
        # Precompute the center of hte geographical space
        LON_CENTER = (EAST_BOUND + WEST_BOUND)/2.0
        LAT_CENTER = (SOUTH_BOUND + NORTH_BOUND)/2.0

        # Compute a rough bounding box for the grid space
        COORDS_1 = (LAT_CENTER + 0.5,LON_CENTER)
        COORDS_2 = (LAT_CENTER - 0.5,LON_CENTER)
        COORDS_3 = (LAT_CENTER,LON_CENTER + 0.5)
        COORDS_4 = (LAT_CENTER,LON_CENTER - 0.5)

        # Compute the conversion of degrees to 
        latDeg2m = (geopy.distance.vincenty(COORDS_1, COORDS_2).km)
        lonDeg2m = (geopy.distance.vincenty(COORDS_3, COORDS_4).km)

        # 100 = 10 m resolution
        # 50 = 20 m resolution
        # 33 = ~30 m resolution ~100 ft
        # 25 = 40 m resolution
        # 20 = 50 m resolution
        latBins = int(np.round(LAT_BOUND * latDeg2m,2) * 33)
        lonBins = int(np.round(LON_BOUND * lonDeg2m,2) * 33)

        # Compute iterable range for the space
        latRange = np.linspace(SOUTH_BOUND,NORTH_BOUND,latBins)
        lonRange = np.linspace(WEST_BOUND,EAST_BOUND,lonBins)
        
        # [ JLai ] Works but needs to be rewritten
        histLiquor,self.xeLiquor,self.yeLiquor = np.histogram2d([0],[0],\
                                                      bins=(latRange,lonRange))

        # Deletes variable, we don't need it
        del histLiquor

        # Store internal variables
        self.xeLiquorOrig = np.copy(self.xeLiquor)
        self.yeLiquorOrig = np.copy(self.yeLiquor)

        # Compute midpoint of grid and store internal variables
        self.xeLiquor = (self.xeLiquor[1:] + self.xeLiquor[:-1])/2.0 
        self.yeLiquor = (self.yeLiquor[1:] + self.yeLiquor[:-1])/2.0 
        
        # Cleanup function
        gc.collect()
        return None

    @jit
    def griddify(self,lon,lat):
        """
        Returns a single grid index given a tuple of longitude and latitude
        """

        # This is SLOW code
        X = np.abs(self.xeLiquor-lat).argmin()
        Y = np.abs(self.yeLiquor-lon).argmin()    
        return(X,Y)
        
    def getGridIndex(self):
        """
        Returns tuple of (longitude, latitude grid indices) in THAT order
        because longitudes are X coordinates and latitudes are Y coordinates
        in scatterplot space
        """
        return(self.getLatGridIndex(),self.getLonGridIndex())

    def getLatGridIndex(self):
        """
        Returns an array of the latitude grid indices
        """
        return(self.xeLiquor)

    def getLonGridIndex(self):
        """
        Returns an array of the longitude grid indices
        """
        return(self.yeLiquor)

