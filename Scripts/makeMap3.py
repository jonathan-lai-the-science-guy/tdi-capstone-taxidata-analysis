import folium # MIT license
from folium import plugins, IFrame
from folium.map import *
from folium.plugins import *
import matplotlib
matplotlib.use('Agg')

from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
import matplotlib.pyplot as plt,mpld3
import seaborn as sns
########################################

MIN_SHOW = 0
MIN_SHOW_CHART = 5

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

tableHeader = """<html>
<head>
<style>
table, th, td {
    border-spacing: 1px;
}
th, td {
    padding: 1px;
}
table#t01 tr:nth-child(even) {
    background-color: #888888;
}
table#t01 tr:nth-child(odd) {
    background-color: #ffffff;
}
</style>
</head>
<body>"""

tableCounter = 1
def buildTable(tmpList,tableCounter=1):
    htmlTable = tableHeader
    htmlTable += '<table id="t{:d}">'.format(tableCounter)
    for i in tmpList:
        htmlTable += '<tr>'
        if(isinstance(i[1],float)):
            htmlTable += '<td>{:s}&nbsp&nbsp&nbsp&nbsp</td>\n<td>{:1.1f}</td>'.format(str(i[0]),i[1])
        else:
            htmlTable += '<td>{:s}&nbsp&nbsp&nbsp&nbsp</td>\n<td>{:s}</td>'.format(str(i[0]),str(i[1][:25]))
        htmlTable += '</tr>'
    htmlTable += '</table>\n' #</body>\n'
    tableCounter += 1
    return(htmlTable)

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

import re
word_finder = re.compile('\w+')
def make_names_pretty(name):
    new_name = ""
    for i in word_finder.findall(name):
        if(i not in {'LLC','CORP','INC'}):
            new_name += i.lower().capitalize() + " "
    return(new_name.strip())
########################################

def get_colors(inp, colormap, vmin=None, vmax=None):
    norm = plt.Normalize(vmin, vmax)
    return colormap(norm(inp))

def get_color_array(listInput):
    colorArray = []
    B = get_colors(listInput,plt.cm.jet,vmin=MIN_SHOW_CHART)
    A = B*255
    A = A.astype(int)

    for i in A:
        a = hex(i[0])[2:].zfill(2)
        b = hex(i[1])[2:].zfill(2)
        c = hex(i[2])[2:].zfill(2)
        colorArray.append("#{:s}{:s}{:s}".format(a,b,c))
    return(colorArray)
########################################
import vincent, json
import numpy as np
import matplotlib.table

priceDict = { 1:'$', 2:'$$', 3:'$$$', 4:'$$$$', 5:'$$$$$' }

points2 = []
pickupList = []
tmpArray = []
for i,j,lat,lon,rating,priceLevel in zip(dbas,
                                         averagePickups,
                                         lats,
                                         lons,
                                         ratings,
                                         priceLevels):


          ##############################
    avgPickups = np.average(tmpData[i].values)

          ##############################
    if(avgPickups >= MIN_SHOW_CHART):
        points2.append((lat,lon))
        pickupList.append(avgPickups)
        print("{:s},({:1.2f},{:1.2f})".format(make_names_pretty(i),lat,lon))
        fig = plt.figure(figsize=(3,3))
 
        new_name = make_names_pretty(i)
        markerPopup = [["Business:", new_name],["Average pickups:",j]]
        if not np.isnan(priceLevel):
            markerPopup.append(["Price:",priceDict[priceLevel]])
        if not np.isnan(rating):
            markerPopup.append(["Rating:","{:1.1f}\u2606".format(rating)])
        tmpHtml = "<html>\n" + buildTable(markerPopup)

        ax = fig.add_subplot(2,1,1)
        #ax.plot(tmpData[i].index[::10],tmpData[i][::10],color='gray')
        y = tmpData[i]
        y = np.convolve(y,np.ones(30)/30.0)[14:-15]
        ax.plot(tmpData[i].index[15:-15:20],y[15:-15:20],lw=3,zorder=10)
        ax.set_title('Average number of pickups')

        ax = fig.add_subplot(2,1,2)
        bar = histData[i]
        ax.bar(bar.index,bar/np.sum(bar),color='gray')
        ax.plot(bar.index,bar/np.sum(bar),lw=3,zorder=10)
        ax.set_xticks(np.arange(-2,6)-0.5)
        ax.set_xticklabels(['10PM','11PM','12AM','1AM','2AM','3AM','4AM','5AM'])

        ax.set_yticks([])
        ax.set_title('Relative vehicular traffic')
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        plt.tight_layout()

        tmpHtml += mpld3.fig_to_html(fig,template_type="simple") + "\n</html>"
        popup = IFrame(html=tmpHtml, width=350, height=400)
        plt.close(fig)

        tmpArray.append(popup)

cluster2 = MarkerCluster(locations=points2,\
                         popups=tmpArray).add_to(map_of_nyc)

tmpColorArray = get_color_array(pickupList)
for pts,pickup,color in zip(points2,pickupList,tmpColorArray):

    if(pickup >= MIN_SHOW_CHART):
        folium.Circle(location=pts,\
                      radius=20*int(np.log10(pickup+1)),\
                      color=color,\
                      fill=True).add_to(map_of_nyc)

cluster2.layer_name = "Locations with more than {:d} daily pickups".format(MIN_SHOW_CHART)

# Overlay the image
import scipy
from scipy.ndimage.filters import gaussian_filter
wherePeopleLive = np.flipud(np.load('whereArePeopleGoing.npy')[:,:,-2]).astype(float)
wherePeopleLive = scipy.ndimage.filters.gaussian_filter(wherePeopleLive,sigma=4)
wherePeopleLive = np.log10(wherePeopleLive + 1)
wherePeopleLive[np.where(wherePeopleLive == 0)] = np.nan

whereArePeopleGoing = plugins.ImageOverlay(wherePeopleLive, opacity=0.8, \
                                           bounds =[[40.550, -74.150],\
                                                    [40.900, -73.750]],\
                                           colormap=plt.cm.inferno,\
                                           attr = 'Where do young people live?')
whereArePeopleGoing.layer_name = "Where do young people live?"
whereArePeopleGoing.add_to(map_of_nyc)

########################################
from folium.plugins import *
folium.plugins.MeasureControl(position='topright', primary_length_unit='miles', secondary_length_unit='meters')

########################################
map_of_nyc.add_child(folium.LayerControl())
map_of_nyc.save('map.html')
################################################################################
