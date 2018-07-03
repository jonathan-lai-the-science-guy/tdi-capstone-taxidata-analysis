import folium # MIT license
from folium import plugins, IFrame
from folium.map import *
from folium.plugins import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt,mpld3
import seaborn as sns
########################################

MIN_SHOW = 5
MIN_SHOW_CHART = 120

########################################


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

########################################
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
import matplotlib.pyplot as plt, mpld3

points2 = []
tmpArray = []
for i,j,lat,lon in zip(dbas,averagePickups,lats,lons):

    if(j > MIN_SHOW_CHART):
        print(lat,lon)
        points2.append((lat,lon))

#        tmpDF = pd.DataFrame({ "dates" : tmpData.index, "pickups" : tmpData[i] })
#        tmpDF.index = tmpDF.index.values.astype('M8[D]')

        fig = plt.figure(figsize=(3,5))
        ax = fig.add_subplot(2,1,1)
#add_subplot(1,1,1)
        ax.plot(tmpData[i])
#tmpData[i][::7])
        ax.set_xlabel('Date')
        ax.set_ylabel('Average number of pickups')
        popup = IFrame(html=mpld3.fig_to_html(fig,template_type="simple"), width=600, height=450)
        plt.tight_layout()
        plt.close(fig)

        tmpArray.append(popup)

cluster2 = MarkerCluster(locations=points2,\
                         popups=tmpArray).add_to(map_of_nyc)
cluster2.layer_name = "Locations with more than {:d} daily pickups".format(MIN_SHOW_CHART)

########################################
map_of_nyc.add_child(folium.LayerControl())
map_of_nyc.save('map.html')

