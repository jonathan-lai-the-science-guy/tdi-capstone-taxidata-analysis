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
bg = gl.BaseGrid(resolution=33)

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

def prettifyAddress(addressStr):
    addressStr = " " + addressStr + " "
    addressStr = addressStr.replace(' STREET ',' ST ')
    addressStr = addressStr.replace(' AVENUE ',' AVE ')
    addressStr = addressStr.replace(' LANE ',' LN ')
    addressStr = addressStr.replace(' DRIVE ',' DR ')
    return(addressStr.strip())


import geopy.distance
def getBarOutput(indx,lat,lon):
    output = ["<body>"]
    colors = ['"#ffffff"','"#444444"']
    for counter,val in enumerate(indx):
        output.append("<table bgcolor={:s}>".format(colors[counter % 2]))
        tmp = bars.loc[bars["Index"] == val]

        # Print out bar name
        output.append("\t\t<th>{:d}&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</th>".format(counter + 1))
        output.append("\t<tr>")
        output.append("\t\t<th>&nbsp</th>")
        output.append("\t\t<th>Name</th>")
        output.append("\t\t<th>&nbsp&nbsp&nbsp&nbsp</th>")
        output.append("\t\t<th>{:s}</th>".format(tmp["Doing Business As (DBA)"].values[0]))
        output.append("\t</tr>")

        # Print out address
        address = prettifyAddress(tmp["Address"].values[0])
        output.append("\t<tr>")
        output.append("\t\t<th>&nbsp</th>")
        output.append("\t\t<th>Address</th>")
        output.append("\t\t<th>&nbsp&nbsp&nbsp&nbsp</th>")
        output.append("\t\t<th>{:s}</th>".format(address))
        output.append("\t</tr>")
        
        # Calculate the distance from your home to bar
        c1 = (lat,lon)
        c2 = (tmp["Latitude"].values[0],tmp["Longitude"].values[0])
        dist = geopy.distance.vincenty(c1,c2).mi
        print(c1,c2,dist)
        output.append("\t<tr>")
        output.append("\t\t<th>&nbsp</th>")
        output.append("\t\t<th>Distance</th>")
        output.append("\t\t<th>&nbsp&nbsp&nbsp&nbsp</th>")
        if(dist >= 0.5):
            output.append("\t\t<th>{:1.2f} miles</th>".format(dist))
        else:
            dist = geopy.distance.vincenty(c1,c2).ft
            output.append("\t\t<th>{:1.2f}ft</th>".format(dist))
        output.append("\t</tr>")
        
        # Print out price
        price = int(tmp["price_level"].values)
        if(price > 0):
            output.append("\t<tr>")
            output.append("\t\t<th>&nbsp</th>")
            output.append("\t\t<th>Price</th>")
            output.append("\t\t<th>&nbsp&nbsp&nbsp&nbsp</th>")
            output.append("\t\t<th>{:s}</th>".format('$'*price))
            output.append("\t</tr>")

        # Print out review
        rating = str(tmp["rating"].values[0])
        if(len(rating) > 0):
            output.append("\t<tr>")
            output.append("\t\t<th>&nbsp</th>")
            output.append("\t\t<th>Rating</th>")
            output.append("\t\t<th>&nbsp&nbsp&nbsp&nbsp</th>")
            output.append("\t\t<th>{:s}\u2606</th>".format(rating))
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
    StreetNum = IntegerField(default=41,validators=[validators.InputRequired])
    StreetAddress = TextField(default="East 11st",validators=[validators.InputRequired])
    ZipCode = IntegerField(default=10003,validators=[validators.InputRequired])
#    latitude = DecimalField(default=40.733274040,validators=[validators.InputRequired])
#    longitude = DecimalField(default=-73.99280703,validators=[validators.InputRequired])
    numPeopleGoing = SelectField(u'numPeopleGoing',\
                                 default='Single', \
                                 choices=[('Group', 'Group'), ('Single', 'Single')])
    
import json
from ediblepickle import checkpoint
@checkpoint(work_dir='/tmp/geoLookup', refresh=False)
def lookUpSub(inputStr):
    tmp = inputStr.split('|')
    streetNum = tmp[0]
    streetAddress = tmp[1]
    zipCode = tmp[2]
    tmpStr = "https://api.cityofnewyork.us/geoclient/v1/address.json?houseNumber={:s}&street={:s}&zip={:s}".format(streetNum,streetAddress,zipCode)
    tmpStr += "&app_id={:s}&app_key={:s}".format(nyc_project_id,nyc_api_key)
    tmpJSON = requests.get(tmpStr).json()
    return(tmpJSON)


def lookUp(streetNum,streetAddress,zipCode):
    inputStr = streetNum + '|' + streetAddress + '|' + zipCode
    cache_path = '/tmp/geoLookup/' + inputStr
    
#    try:
#        os.stat(cache_path)
#    except:
#        ll,mm,rr = cache_path.rpartition('/')
#        print(ll)
#        try:
#            os.makedirs(ll)
#        except:
#            pass
#        f= open(cache_path,"w+")
#        f.close()

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
        # lat = float(request.form['latitude'])
        # lon = float(request.form['longitude'])
        streetNum = (request.form['StreetNum'])
        streetAddress = (request.form['StreetAddress']).replace(' ','+')
        zipCode = (request.form['ZipCode'])
        try:
            JSON = lookUp(streetNum,streetAddress,zipCode)
            lat,lon = decodeJSON(JSON['address'])
        except:
            lat,lon = 0,0
        latGrid,lonGrid = bg.griddify(lon,lat)
        prediction = ckr.predict([[latGrid,lonGrid,1]],method='all')
        indx = np.argsort(prediction)[0][-1:-6:-1]
        script = getBarOutput(indx,lat,lon)

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
