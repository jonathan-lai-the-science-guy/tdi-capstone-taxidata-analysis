import folium # MIT license
from folium import plugins, IFrame
from folium.map import *
from folium.plugins import *
import matplotlib.pyplot as plt

########################################

MIN_SHOW = 5
MIN_SHOW_CHART = 120

########################################

import pandas as pd
import numpy as np
tmpData = pd.read_hdf('result.hdf','table')
tmpDict = {}
for i in tmpData.columns:
    tmpDict[i] = tmpData[i].mean(axis=0)

histData = pd.read_hdf('reducedHistResult.hdf','table')

width, height = 310,180
nycCenLat,nycCenLon = 40.733274040,-73.992807073
# 40.729861,-73.988
NYC = (nycCenLat,nycCenLon)
f = folium.Figure()
f.html.add_child(\
                 folium.Element("<h1>Which bars are worth a taxi ride?</h1>"))

map_of_nyc = folium.Map(location=NYC,\
                        zoom_start=16,\
                        max_zoom=18,\
                        tiles='Stamen Toner')

TDI_marker = folium.Marker([nycCenLat,nycCenLon],\
                           popup='TDI NYC',\
                           icon=folium.Icon(icon_color='orange')).add_to(map_of_nyc)

import pandas as pd
topPlaces = pd.read_csv('topPlaces5.csv').drop_duplicates()
topPlaces['averagePickups'] = topPlaces["Doing Business As (DBA)"].map(tmpDict)
topPlaces.sort_values(inplace=True,by='averagePickups')
lats,lons = topPlaces["Latitude"],topPlaces["Longitude"]
latGrid,lonGrid = topPlaces["LatGrid"],topPlaces["LonGrid"]
dbas = topPlaces["Doing Business As (DBA)"]
ratings = topPlaces["rating"]
priceLevels = topPlaces["price_level"]
averagePickups = topPlaces["averagePickups"].values
ubers_to_patrons = np.load('../Data/uber_to_patrons.npy')

########################################
import vincent, json
import numpy as np



points2 = []
tmpArray = []
for i,j,lat,lon in zip(dbas,averagePickups,lats,lons):

    if(j > MIN_SHOW_CHART):
        print(lat,lon)
        points2.append((lat,lon))

        tmpDF = pd.DataFrame({ "dates" : tmpData.index, "pickups" : tmpData[i] })
        tmpDF.index = tmpDF.index.values.astype('M8[D]')

        lineChart = vincent.Line(tmpDF,
                                 width=500,
                                 height=200)
        lineChart.axis_titles(x='Dates', y='Average number of pickups')

        barChart = vincent.Bar(histData[i],
                                width=500,
                                height=200)
        barChart.axis_titles(x='Hours', y='Average number of pickups')

        popup = folium.Popup(max_width=800)        
        folium.Vega(lineChart, height=300, width=700).add_to(popup)
        folium.Vega(barChart, height=300, width=700).add_to(popup)
        tmpArray.append(popup)

cluster2 = MarkerCluster(locations=points2,\
                         popups=tmpArray).add_to(map_of_nyc)
cluster2.layer_name = "Locations with more than {:d} daily pickups".format(MIN_SHOW_CHART)

########################################

#nb = np.load('../Data/normalizedBar.npy').tolist()
#HeatMap(nb).add_to(map_of_nyc)
########################################


map_of_nyc.add_child(folium.LayerControl())
map_of_nyc.save('map.html')

