import pickle
with open('networkDict-2009.p','rb') as pickle_file:
    networkDict = pickle.load(pickle_file)

import pandas as pd
bars = pd.read_csv('topPlaces5.csv',\
                   engine='c',\
                   dtype={'Index' : 'float',\
                          'Doing Business As (DBA)' : 'str',\
                          'Premises Name' : 'str',\
                          'LatGrid' : 'float',\
                          'LonGrid' : 'float',\
                          'Latitude' : 'float',\
                          'Longitude' : 'float',\
                          'price_level' : 'float',\
                          'weekday' : 'str'})

import networkx as nx
G=nx.DiGraph()

for tmpIndx,dba in zip(bars['Index'],bars['Doing Business As (DBA)']):
    indx = int(tmpIndx)
    G.add_node(indx,attr_dict = {'name':dba})

pos = {}
for tmpIndx,tmpLat,tmpLon in zip(bars['Index'],\
                                 bars['LatGrid'],\
                                 bars['LonGrid']):
    pos[tmpIndx] = (tmpLat,tmpLon)

print("Number of nodes: %d" % G.number_of_nodes())

for i in networkDict:
    a,b = (int(i[0])),(int(i[1]))
    G.add_edge(a,b,weight = networkDict[i])

#print("radius: %d" % radius(G))
#print("diameter: %d" % diameter(G))
#print("eccentricity: %s" % eccentricity(G))
#print("center: %s" % center(G))
#print("periphery: %s" % periphery(G))
#print("density: %s" % density(G))

import matplotlib.pyplot as plt
limits=plt.axis('off')
nx.draw_networkx(G,pos=pos)
plt.show()
