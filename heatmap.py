from bokeh.io import show, curdoc
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
    LinearColorMapper
)
from bokeh.palettes import OrRd9 as palette
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, row, column
from time import sleep
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment
import pandas
from bokeh.models.widgets import Button
import numpy 

# data = np.load('cardict.npy').item()
coor = pandas.read_csv('points.csv')
data = pandas.read_csv('sensorDataTest.csv')
print(data.keys())
palette.reverse()
color_mapper = LogColorMapper(palette=palette)

source = ColumnDataSource(data=dict(
    x=list(coor['x']),
    y=list(coor['y']),
    voldata = [1]*len(coor['x']),
    address = list(coor['location']),
))
# print(source.data['address'])
TOOLS = "pan,wheel_zoom,reset,hover,save"
p = figure(
    title="Traffic Volume",
    x_axis_location=None, y_axis_location=None, tools = TOOLS, x_axis_label='Location of Checkpoint', y_axis_label='Location of Checkpoint'
)
p.circle(x='x',y='y',
    fill_color={'field': 'voldata', 'transform': color_mapper}, 
    size = 15, source=source)
p.image_url(url=['https://i.imgur.com/FjKKNLz.png'], x=0, y=100, w = 100, h= 100, global_alpha = 0.2)

hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Volume", "@voldata"),
    ("Address", "@address"),
]
button1 = Button(label="Run Total Footprint", button_type="success")
button2 = Button(label="Run Realtime", button_type="success")

#this streams in the data and counts every car that has been to the node thus far. 
def update1():
    nodeVolume = [0 for i in coor['location']]
    for number, row in data.iterrows():
        # print(source.data['address'])
        theIndex = source.data['address'].index(row['gate-name'])
        nodeVolume[theIndex] += 1
        if number % 1000 == 0:
            print(number)
            tuplist = []
            for i in range(len(nodeVolume)):
                tuplist.append((i, nodeVolume[i]))

            patch = {'voldata' : tuplist}
            source.patch(patch)
        # time.sleep(0.05)
        
    print('done!!')
#this streams in the data and counts every car currently at that node. This is finally useful yay!!!
def update2():
    nodeVolume = [0 for i in coor['location']]
    seen = {}
    exited = None 

    for number, row in data.iterrows():
        sleep(.5)
        # print(source.data['voldata'])
        # print(source.data['address'])
        if row['car-id'] in seen:
            # print("prev:{} to:{}".format(seen[row['car-id']],row['gate-name']))
            theMinusIndex = source.data['address'].index(seen[row['car-id']])
            nodeVolume[theMinusIndex] -= 1
            if 'entrance' in row['gate-name']:
                print("prev:{} to:{}".format(seen[row['car-id']],row['gate-name']))
            if 'entrance' in row['gate-name'] and 'entrance' not in seen[row['car-id']]:
                exited = row['gate-name']
                # print(row['gate-name'])
                print(exited)

        else:
            pass
            # print('new car!!!')
        seen[row['car-id']] = row['gate-name']

        thePlusIndex = source.data['address'].index(row['gate-name'])
        nodeVolume[thePlusIndex] += 1

        #this deals with exit node pile ups   
        if exited is not None:
            theMinusIndex = source.data['address'].index(exited)
            nodeVolume[theMinusIndex] -= 1
            exited = None
        # if number % 1 == 0:
            # print(number)
        tuplist = []
        for i in range(len(nodeVolume)):
            tuplist.append((i, nodeVolume[i]))

        patch = {'voldata' : tuplist}
        source.patch(patch)
        # time.sleep(0.05)
        
    print('done!!')

button1.on_click(update1)
button2.on_click(update2)

show(p)
layout = column(p,widgetbox(button1,button2))
curdoc().add_root(layout)
curdoc().title = "Heatmap"