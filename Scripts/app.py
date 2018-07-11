################################################################################
import os
try:
    nyc_api_key = os.environ["NYC_API_KEY"]
    nyc_project_id = os.environ["NYC_PROJECT_ID"]
except:
    print("NYC keys not defined")
    print("Failing as loudly as possible")
    print("DEFINE NYC_API_KEY AND NYC_PROJECT_ID BEFORE RERUNNING")
    raise(KeyError)
################################################################################
import sys
sys.path.append('/home/vagrant/Capstone/Custom_Libraries/')

import GridLib as gl
bg = gl.BaseGrid(resolution=33,scaleFactor=33)

xeLiquorOrig,yeLiquorOrig = bg.getGridIndex()

################################################################################
import pandas as pd
bars = pd.read_csv('topPlaces6.csv',\
                   engine='c',\
                   dtype={'Index' : 'float',\
                          'Doing Business As (DBA)' : 'str',\
                          'Premises Name' : 'str',\
                          'Address' : 'str',\
                          'LatGrid' : 'float',\
                          'LonGrid' : 'float',\
                          'Latitude' : 'float',\
                          'Longitude' : 'float',\
                          'rating' : 'float',\
                          'price_level' : 'float',\
                          'Sunday open' : 'int',\
                          'Monday open' : 'int',\
                          'Tuesday open' : 'int',\
                          'Wednesday open' : 'int',\
                          'Thursday open' : 'int',\
                          'Friday open' : 'int',\
                          'Saturday open' : 'int',\
                          'Sunday close' : 'int',\
                          'Monday close' : 'int',\
                          'Tuesday close' : 'int',\
                          'Wednesday close' : 'int',\
                          'Thursday close' : 'int',\
                          'Friday close' : 'int',\
                          'Saturday close' : 'int',\
                          'averagePickups' : 'float'})

bars['LatGrid'] = pd.cut(bars['Latitude'],xeLiquorOrig,labels=False)
bars['LonGrid'] = pd.cut(bars['Longitude'],yeLiquorOrig,labels=False)
bars.fillna(0,inplace=True)
################################################################################
outputElem = ["Doing Business As (DBA)","Address","price_level","rating"]
outputName = ["Name","Address","Price","Rating"]

#def getGoogleMap(x,y):
#    return("""function myMap() {
#    var mapOptions = {
#        center: new google.maps.LatLng({:1.2f},{:1.2f}),
#        zoom: 10,
#        mapTypeId: google.maps.MapTypeId.HYBRID
#    }
#var map = new google.maps.Map(document.getElementById("map"), mapOptions);
#}""".format(x,y))

def prettifyName(Name):
    return(Name[:30].strip())


def prettifyAddress(addressStr):
    addressStr = " " + addressStr + " "
    addressStr = addressStr.replace(' STREET ',' ST ')
    addressStr = addressStr.replace(' AVENUE ',' AVE ')
    addressStr = addressStr.replace(' LANE ',' LN ')
    addressStr = addressStr.replace(' DRIVE ',' DR ')
    return(addressStr.strip())


import geopy.distance
def getBarOutput(indx,vals,lat,lon):
    output = ["<body>"]
    output = ["<style> th {padding-right: 10px;} td {padding-right: 5px}</style>"]
    colors = ['"#ffffff"','"#444444"']
    for counter,val in enumerate(indx):
        output.append("<table bgcolor={:s}>".format(colors[counter % 2]))
        tmp = bars.loc[bars["Index"] == val]

        # Print out bar name
        output.append("\t<tr>")
        output.append("\t\t<th>{:d}&nbsp&nbsp&nbsp</th>".format(counter + 1))
        output.append('\t\t<th colspan="3"><i>{:1.2f}% of social taxi-rides home came from this bar</i></th>'.format(100*vals[counter]))
        output.append("\t<tr>")
        output.append("\t\t<th>&nbsp</th>")
        output.append("\t\t<th>Name</th>")
        output.append("\t\t<th>&nbsp&nbsp</th>")
        output.append("\t\t<td>{:s}</td>".format(prettifyName(tmp["Doing Business As (DBA)"].values[0])))
        output.append("\t</tr>")

        # Print out address
        address = prettifyAddress(tmp["Address"].values[0])
        output.append("\t<tr>")
        output.append("\t\t<th>&nbsp</th>")
        output.append("\t\t<th>Address</th>")
        output.append("\t\t<th>&nbsp&nbsp</th>")
        output.append("\t\t<td>{:s}</td>".format(address))
        output.append("\t</tr>")
        
        # Calculate the distance from your home to bar
        c1 = (lat,lon)
        c2 = (tmp["Latitude"].values[0],tmp["Longitude"].values[0])
        dist = geopy.distance.vincenty(c1,c2).mi
        output.append("\t<tr>")
        output.append("\t\t<th>&nbsp</th>")
        output.append("\t\t<th>Distance</th>")
        output.append("\t\t<th>&nbsp&nbsp</th>")
        if(dist >= 0.5):
            output.append("\t\t<td>{:1.2f} miles</td>".format(dist))
        else:
            dist = geopy.distance.vincenty(c1,c2).ft
            output.append("\t\t<td>{:1.2f}ft</td>".format(dist))
        output.append("\t</tr>")
        
        # Print out price
        price = int(tmp["price_level"].values)
        if(price > 0):
            output.append("\t<tr>")
            output.append("\t\t<th>&nbsp</th>")
            output.append("\t\t<th>Price</th>")
            output.append("\t\t<th>&nbsp&nbsp</th>")
            output.append("\t\t<td>{:s}</td>".format('$'*price))
            output.append("\t</tr>")

        # Print out review
        rating = str(tmp["rating"].values[0])
        if(len(rating) > 0):
            output.append("\t<tr>")
            output.append("\t\t<th>&nbsp</th>")
            output.append("\t\t<th>Avg. Google Rating</th>")
            output.append("\t\t<th>&nbsp&nbsp</th>")
            output.append("\t\t<td>{:s}\u2606</td>".format(rating))
            output.append("\t</tr>")

        output.append("</table>")
        output.append("<br/>")
    output.append("</body")
    return("".join(output))

################################################################################
from sklearn.neighbors import KNeighborsRegressor
import numpy as np

class customKNNRegressor():   
    
    def __init__(self):
        self.localRegressor = KNeighborsRegressor(n_neighbors=5,\
                                                  weights='uniform',\
                                                  algorithm='auto',\
                                                  leaf_size=30)
        self.distantRegressor = KNeighborsRegressor(n_neighbors=11,\
                                                    weights='distance',\
                                                    algorithm='auto',\
                                                    leaf_size=30)

    def fit(self,X,y):
        self.localRegressor.fit(X,y)
        self.distantRegressor.fit(X,y)
        
    def predict(self,X,method='all'):
        if(method=='all'):
            return(self.localRegressor.predict(X) \
                    + self.distantRegressor.predict(X))
        elif(method=='distant'):
            return(self.distantRegressor.predict(X))
        elif(method=='local'):
            return(self.localRegressor.predict(X))
        else:
            raise Exception("Wrong method attribute")
    
    def score(self,X,y):
        if(np.max(y) != 1):
            y[y >= 1] = 1
        localScore = self.localRegressor.score(X,y)
        distantScore = self.distantRegressor.score(X,y)
        avgScore = (localScore + distantScore)/2.0
        return((localScore,distantScore,avgScore))
            
################################################################################
import pickle
filename = "bar_ML_model.sav"
ckr = pickle.load(open(filename, 'rb'))
################################################################################
from flask import Flask, render_template, request
from wtforms import Form, DecimalField, IntegerField, SelectField, TextField, validators
import requests

app = Flask(__name__)

class InputForm(Form):
    StreetAddress = TextField(default="41 East 11st 10003",validators=[validators.InputRequired])
    numPeopleGoing = SelectField('Going by yourself or with a group?',\
                                 default='Single', \
                                 choices=[(1,'Single'),(0,'Group')])
    
import json
from ediblepickle import checkpoint
@checkpoint(work_dir='/tmp/geoLookup', refresh=False)
def lookUpSub(inputStr):
    tmpStr = "https://api.cityofnewyork.us/geoclient/v1/search.json?input={:s}".format(inputStr)
    tmpStr += "&app_id={:s}&app_key={:s}".format(nyc_project_id,nyc_api_key)
    tmpJSON = requests.get(tmpStr).json()
    return(tmpJSON)


def lookUp(inputStr):
    cache_path = '/tmp/geoLookup/'
    try: 
        os.stat(cache_path)
    except:
        try:
            os.makedirs(cache_path)
        except:
            pass

    strJSON = lookUpSub(inputStr) 
    return(strJSON)

def decodeJSON(JSON):
    return(float(JSON['latitude']),float(JSON['longitude']))

@app.route('/',methods=['GET','POST'])
def getBar():
    form = InputForm(request.form)
    script = None
    requestMethod = request.method
    if (requestMethod == 'POST'):
        streetAddress = (request.form['StreetAddress']).replace(' ','+')
        numPeopleGoing = request.form['numPeopleGoing']
        try:
            JSON = lookUp(streetAddress)
            lat,lon = decodeJSON(JSON['results'][0]['response'])
        except:
            lat,lon = 0,0
        latGrid,lonGrid = bg.griddify(lon,lat)
        prediction = ckr.predict([[latGrid,lonGrid,numPeopleGoing]],method='distant')
        indx = np.argsort(prediction)[0][-1:-6:-1]
        total = np.nansum(prediction[0])
        vals = (prediction[0] / total)[indx]
        script = getBarOutput(indx,vals,lat,lon)

    elif (requestMethod == 'GET'):
        numPeopleGoing = ['Group','Single']
        lat = 40.733
        lon = -73.993
    else:
        pass

    return(render_template("predictor.html",\
                           form=form,\
                           script=script,\
                           latitude=lat,\
                           longitude=lon))
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=33507)
