import numpy as np
np.random.seed(0)
import math
import random 

from bokeh.io import curdoc
from bokeh.layouts import widgetbox, row, column, layout
from bokeh.models import ColumnDataSource, Select, Slider
from bokeh.palettes import Spectral6
from bokeh.io import output_notebook, show
from bokeh.plotting import figure, output_file, show
from sklearn import tree
from sklearn.cross_validation import train_test_split

from sklearn import neighbors, datasets
from sklearn.neighbors import NearestNeighbors
from sklearn import cluster, datasets
from sklearn.neighbors import kneighbors_graph
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import cross_val_score

import xlrd
from sklearn.cluster import KMeans
from bokeh.plotting import figure
from bokeh.models import HoverTool
from bokeh.models import BoxZoomTool
from bokeh.models import WheelZoomTool
from bokeh.models import PanTool


# In[2]:

def getAllTrafficData():
    file_location = "Lekagul_Sensor_Data.xlsx"
    TrafficFile = xlrd.open_workbook(file_location)
    t = TrafficFile.sheet_by_index(0)
    return t


# In[3]:

def getTimeStamp(traffic):
    v = []
    
    for r in range(1, traffic.nrows):
        v.append(traffic.cell_value(r, 0))
    
    return v


# In[4]:

def getCarID(traffic):
    v = []
    
    for r in range(1, traffic.nrows):
        v.append(traffic.cell_value(r, 1))
    
    return v


# In[5]:

def getCarType(traffic):
    v = []
    
    for r in range(1, traffic.nrows):
        v.append(traffic.cell_value(r, 2))
    
    return v


# In[6]:

def getGateName(traffic):
    v = []
    
    for r in range(1, traffic.nrows):
        v.append(traffic.cell_value(r, 3))
    
    return v


# In[7]:


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[8]:



# In[9]:
def createParkMap(timeStamps, carTypes, gateNames):
    gateSet = set(gateNames)
    carTypeSet = set(carTypes)

    newTime = []
    for date in timeStamps:
        newTime.append(math.floor(date/10))
    dateSet = set(newTime)

    parkMap = {}

    for gate1 in gateSet:
        for gate2 in gateSet:
            if gate1 != gate2:
                for date in dateSet:
                    for car in carTypeSet:
                        parkMap[date, car, gate1, gate2] = 0
                    
    return parkMap
#==========================================================================================================================================




def getSingleCarData(singleCarID, carIDs, timeStamps, carTypes, gateNames):
    singleCarDates = []
    singleCarType = []
    singleCarGateNames = []
    
    for i in range(0, len(carIDs)):
        if carIDs[i] == singleCarID:
            singleCarDates.append(timeStamps[i])
            singleCarType.append(carTypes[i])
            singleCarGateNames.append(gateNames[i])
            
    return singleCarDates, singleCarType, singleCarGateNames
#==========================================================================================================================================
    

    
    
def plotParkMap(parkMap, carType, startingGate):
    print("type(parkMap) = ", type(parkMap))
    print("type(carType) = ", type(carType))
    print("type(startingGate) = ", type(startingGate))
    
    denominator = 0
    subParkMap = {}
    for d, c, g1, g2 in parkMap.keys():
        if c == carType:
            if g1 == startingGate:
                print(d, c, g1, g2, parkMap[d, c, g1, g2])
                denominator += parkMap[d, c, g1, g2]
                subParkMap[c, g1, g2] = parkMap[d, c, g1, g2]
    
    
    
    print("denominator = ", denominator)
    
    sumTotal = 0
    for c, g1, g2 in subParkMap.keys():
        subParkMap[c, g1, g2] = subParkMap[c, g1, g2] / denominator
        sumTotal += subParkMap[c, g1, g2]

    print("sumTotal = ", sumTotal)
#========================================================================================================================================
    
    
traffic = getAllTrafficData()
timeStamps = getTimeStamp(traffic)
carIDs = getCarID(traffic)
carTypes = getCarType(traffic)
gateNames = getGateName(traffic)

parkMap = createParkMap(timeStamps, carTypes, gateNames)
#count = 1
#for k in parkMap.keys():
    #print(count, " ", k, " ", parkMap[k])
    #count += 1
#print()
    

    
    
        
uniqueCars = set(carIDs)
#print("len(uniqueCars) = ", len(uniqueCars))
count = 1
for singleCarID in uniqueCars:
    singleCarDates, singleCarType, singleCarGateNames = getSingleCarData(singleCarID, carIDs, timeStamps, carTypes, gateNames)
    #print(count)
    #count += 1
    
    if len(singleCarDates) != len(singleCarType) or len(singleCarDates) != len(singleCarGateNames) or len(singleCarType) != len(singleCarGateNames):
        print("there was a mismatch")
        
        
    for i in range(1, len(singleCarDates)):
        if singleCarGateNames[i-1] != singleCarGateNames[i]:
            parkMap[math.floor(singleCarDates[i]/10), singleCarType[i], singleCarGateNames[i-1], singleCarGateNames[i]] += 1
print()       
        
  

    
    
count = 1
sumOfPoints = 0
for k in parkMap.keys():
    #if parkMap[k] != 0:
        #print(k, " = ", parkMap[k])
    #print(count, " ", k, " ", parkMap[k])
    #count += 1
    sumOfPoints += parkMap[k]
print("sumOfPoints", sumOfPoints)

plotParkMap(parkMap, 1, "entrance3")
        
        
        
        
        
        
   