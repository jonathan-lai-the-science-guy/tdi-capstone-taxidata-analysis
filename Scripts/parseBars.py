

dtypeDictOld = { '' : 'str',\
              'License Serial Number' : 'int',\
              'License Type Name' : 'str',\
              'License Class Code' : 'float',\
              'License Type Code' : 'str',\
              'Agency Zone Office Name' : 'str',\
              'Agency Zone Office Number' : 'int',\
              'County Name (Licensee)' : 'str',\
              'Premises Name' : 'str',\
              'Doing Business As (DBA)' : 'str',\
              'Actual Address of Premises (Address1)' : 'str',\
              'Additional Address Information (Address2)' : 'str',\
              'City' : 'str',\
              'State' : 'str',\
              'Zip' : 'int',\
              'License Certificate Number' : 'int',\
              'License Original Issue Date' : 'str',\
              'License Effective Date' : 'str',\
              'License Expiration Date' : 'str',\
              'Latitude' : 'float',\
              'Longitude' : 'float',\
              'Location' : 'str',\
              'License_Type_Code' : 'str',\
              'Icons' : 'str',\
              'Colors' : 'str',\
              'LatGrid' : 'int',\
              'LonGrid' : 'int',\
              'numNormPickups' : 'float',\
              'absolutePickups' : 'float',\
              'gaussBlur' : 'float',\
              'pid' : 'str',\
              'rating' : 'float',\
              'price_level' : 'float',\
              'weekday' : 'str',\
              'website' : 'str',\
              'reviews' : 'str',\
              'lateClose' : 'float',\
              'earlyClose' : 'float',\
              'Sunday open' : 'float',\
              'Monday open' : 'float',\
              'Tuesday open' : 'float',\
              'Wednesday open' : 'float',\
              'Thursday open' : 'float',\
              'Friday open' : 'float',\
              'Saturday open' : 'float',\
              'Sunday close' : 'float',\
              'Monday close' : 'float',\
              'Tuesday close' : 'float',\
              'Wednesday close' : 'float',\
              'Thursday close' : 'float',\
              'Friday close' : 'float',\
              'Saturday close' : 'float'
}

dtypeDict = { '' : 'str',\
              'Premises Name' : 'str',\
              'Doing Business As (DBA)' : 'str',\
              'Latitude' : 'float',\
              'Longitude' : 'float',\
              'LatGrid' : 'int',\
              'LonGrid' : 'int',\
              'rating' : 'float',\
              'price_level' : 'float',\
              'Sunday close' : 'int',\
              'Monday close' : 'int',\
              'Tuesday close' : 'int',\
              'Wednesday close' : 'int',\
              'Thursday close' : 'int',\
              'Friday close' : 'int',\
              'Saturday close' : 'int',\
              'closeCounter' : 'int' }

import pandas as pd
tmp = pd.read_csv('../Data/topPlaces4.csv',\
                  engine='c',\
                  dtype=dtypeDict)

import sys
sys.path.append('../Custom_Libraries')

import GridLib as gl
bg = gl.BaseGrid(resolution=33)

xeLiquorOrig,yeLiquorOrig = bg.getGridIndex()

tmp['LatGrid'] = pd.cut(tmp['Latitude'],xeLiquorOrig,labels=False)
tmp['LonGrid'] = pd.cut(tmp['Longitude'],yeLiquorOrig,labels=False)

tmp['Sunday close'] = tmp['Sunday close'].astype(int)
tmp['Monday close'] = tmp['Monday close'].astype(int)
tmp['Tuesday close'] = tmp['Tuesday close'].astype(int)
tmp['Wednesday close'] = tmp['Wednesday close'].astype(int)
tmp['Thursday close'] = tmp['Thursday close'].astype(int)
tmp['Friday close'] = tmp['Friday close'].astype(int)
tmp['Saturday close'] = tmp['Saturday close'].astype(int)



tmp.dropna(inplace=True, subset=['LatGrid','LonGrid'])
tmp2 = tmp.loc[(tmp['LatGrid'] > 3) &\
               (tmp['LatGrid'] < (len(xeLiquorOrig) - 4)) &\
               (tmp['LonGrid'] > 3) &\
               (tmp['LonGrid'] < (len(yeLiquorOrig) - 4)) &\
               (tmp['closeCounter'] >= 1)
               ]

tmp2['Doing Business As (DBA)'].fillna(tmp2['Premises Name'], inplace=True)

tmp3 = tmp2[['Doing Business As (DBA)','Premises Name','LatGrid','LonGrid','Latitude','Longitude','rating','price_level','Sunday close','Monday close','Tuesday close','Wednesday close','Thursday close','Friday close','Saturday close']]
tmp3.to_csv('topPlaces5.csv')
