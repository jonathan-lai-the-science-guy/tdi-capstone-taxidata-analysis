import sys
sys.path.append('../Custom_Libraries')


# Initialize gridding object
import GridLib
gridObj = GridLib.BaseGrid(resolution=33)

# Initialize grid of variables
import numpy as np
X,Y = gridObj.getGridIndex()

minX,maxX = 0,len(X)-1
minY,maxY = 0,len(Y)-1

gridMap = np.zeros((len(X),len(Y))).astype(int)
shapeMap = np.zeros((len(X),len(Y))).astype(int)

# Define helper function to populate a map
def graph_processor(graph,i):

    assert(isinstance(i,int))

    nodes = graph.nodes(data=True)
    edges = graph.edges(data=True)

    addVar = 2**i

    for ii in edges:
        N1 = nodes[ii[0]]
        N2 = nodes[ii[1]]
        N1x,N1y = gridObj.griddify(N1['x'],N1['y'])
        N2x,N2y = gridObj.griddify(N2['x'],N2['y'])
        gX = np.linspace(N1x,N2x,1000).astype(int)
        gY = np.linspace(N1y,N2y,1000).astype(int)
        
        gY[np.where(gY > (maxY - 7))] = (maxY - 7)
        gX[np.where(gX > (maxX - 7))] = (maxX - 7)
        gY[np.where(gY < 7)] = 7
        gX[np.where(gX < 7)] = 7

        gridMap[gX,gY] = addVar

        shapeMap[gX,gY] = addVar

        for j in range(7):
            shapeMap[gX+j,gY] = addVar
            shapeMap[gX-j,gY] = addVar
            shapeMap[gX,gY+j] = addVar
            shapeMap[gX,gY-j] = addVar

import osmnx as ox
for i,boro in enumerate(['Manhattan County, New York',\
                         'Kings County, New York',\
                         'Queens County, New York',\
                         'Bronx County, New York',\
                         'Richmond County, New York',\
                         'Nassau County, New York',\
                         'Bergen County, New Jersey',\
                         'Hudson County, New Jersey',\
                         'Essex County, New Jersey',\
                         'Union County, New Jersey',\
                         'Passaic County, New Jersey'
                        ]):
    print('Processing:',i,boro)
    graph = ox.graph_from_place('{:s}, USA'.format(boro), network_type='drive')
    graph_processor(graph,i)

np.save('../Data/StreetMap.npy',gridMap)
np.save('../Data/BoroMap.npy',shapeMap)

