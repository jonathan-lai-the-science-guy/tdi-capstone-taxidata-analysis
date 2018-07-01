import folium # MIT license
from folium import plugins, IFrame
from folium.map import *
from folium.plugins import *
import matplotlib.pyplot as plt

########################################

MIN_SHOW = 0
MIN_SHOW_CHART = 120

########################################

import pandas as pd
import numpy as np
tmpData = pd.read_hdf('result.hdf','table')
averagePickups2 = tmpData.mean(axis=0)

width, height = 310,180
nycCenLat,nycCenLon = 40.733274040,-73.992807073
# 40.729861,-73.988
NYC = (nycCenLat,nycCenLon)
f = folium.Figure()
f.html.add_child(\
                 folium.Element("<h1>Which bars are worth a taxi ride?</h1>"))

map_of_nyc = folium.Map(location=NYC,\
                        zoom_start=15,\
                        max_zoom=18,\
                        tiles='Stamen Toner')

TDI_marker = folium.Marker([nycCenLat,nycCenLon],\
                           popup='TDI NYC',\
                           icon=folium.Icon(icon_color='orange')).add_to(map_of_nyc)

import pandas as pd
topPlaces = pd.read_csv('topPlaces5.csv')
topPlaces['averagePickups'] = averagePickups2
topPlaces.sort_values(inplace=True,by='averagePickups')
lats,lons = topPlaces["Latitude"],topPlaces["Longitude"]
latGrid,lonGrid = topPlaces["LatGrid"],topPlaces["LonGrid"]
dbas = topPlaces["Doing Business As (DBA)"]
ratings = topPlaces["rating"]
priceLevels = topPlaces["price_level"]
averagePickups = topPlaces["averagePickups"].values

ubers_to_patrons = np.load('../Data/uber_to_patrons.npy')

########################################
table = """
<!DOCTYPE html>
<html>
<head>
<style>
table {{
    width:100%;
}}
table, th, td {{
    border: 1px solid black;
    border-collapse: collapse;
}}
th, td {{
    padding: 3px;
    text-align: left;
}}
table#t01 tr:nth-child(odd) {{
    background-color: #eee;
}}
table#t01 tr:nth-child(even) {{
   background-color:#fff;
}}
</style>
</head>
<body>

<table id="t01">
  <tr>
    <td>Name</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>Avg. Daily Pickup</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>Avg. Google review</td>
    <td>{}</td>
  </tr>
  <tr>
    <td>Price ($ - $$$$$)</td>
    <td>{}</td>
  </tr>
</table>
</body>
</html>
""".format
########################################

def get_colors(inp, colormap, vmin=None, vmax=None):
    norm = plt.Normalize(vmin, vmax)
    return colormap(norm(inp))

colorArray = []
B = get_colors(averagePickups,plt.cm.jet,vmin=MIN_SHOW_CHART)
A = B*255
A = A.astype(int)

for i in A:
    a = hex(i[0])[2:].zfill(2)
    b = hex(i[1])[2:].zfill(2)
    c = hex(i[2])[2:].zfill(2)
    colorArray.append("#{:s}{:s}{:s}".format(a,b,c))

for i,j,k,l in zip(lats,\
                   lons,\
                   averagePickups,\
                   colorArray):

    if(k >= MIN_SHOW_CHART):
        folium.Circle(location=[i,j],\
                      radius=10*int(np.log10(k+1)),\
                      color=l,\
                      fill=True).add_to(map_of_nyc)

########################################

points = []
popups = []

for lat,lon,dba,rating,priceLevel,pickup,latG,lonG in zip(lats,\
                                                          lons,\
                                                          dbas,\
                                                          ratings,\
                                                          priceLevels,\
                                                          averagePickups,\
                                                          latGrid,\
                                                          lonGrid):

    if(pickup > MIN_SHOW): 
        print(dba)

        if np.isnan(priceLevel):
            priceLevel = '-'
        else:
            priceLevel = '$'*int(priceLevel)
            
        points.append((lat,lon))
        iframe = IFrame(table(dba,\
                              np.around(pickup),\
                              rating,\
                              priceLevel),
                        width=width,\
                        height=height)
    
        popups.append(iframe)
    
cluster = MarkerCluster(locations=points,\
                         popups=popups).add_to(map_of_nyc)

cluster.layer_name = "Bars with at least {:d} pickups".format(MIN_SHOW)

import vincent, json
import numpy as np

tmpArray = []
points2 = []
#for i,j,p in zip(dbas,averagePickups,points):
#
#    if(j > MIN_SHOW_CHART):
#        points2.append(p)
#
#        tmpFrame = pd.DataFrame({
#            'index' : tmpData.index,\
#            'values' : tmpData[i].values()\
#                             })

#        lineChart = vincent.Line(tmpData[i].values(),
#                                 iter_idx='index',
#                                 width=600,
#                                 height=300)
#        lineChart.axis_titles(x='Dates', y='Average number of pickups')
#        popup = folium.Popup(max_width=800)        
#        folium.Vega(lineChart, height=350, width=650).add_to(popup)
#        tmpArray.append(popup)
#
#cluster2 = MarkerCluster(locations=points2,\
#                         popups=tmpArray).add_to(map_of_nyc)
#cluster2.layer_name = "Locations with more than {:d} daily pickups".format(MIN_SHOW_CHART)

map_of_nyc.add_child(folium.LayerControl())
map_of_nyc.save('map.html')

