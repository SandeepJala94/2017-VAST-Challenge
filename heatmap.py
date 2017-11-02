from bokeh.io import show, curdoc
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
    LinearColorMapper
)
from bokeh.palettes import Greys256 as palette
from bokeh.plotting import figure
from bokeh.layouts import widgetbox, row, column
import time
from bokeh.sampledata.us_counties import data as counties
from bokeh.sampledata.unemployment import data as unemployment
import pandas
from bokeh.models.widgets import Button
import numpy 

# data = np.load('cardict.npy').item()
coor = pandas.read_csv('points.csv')
data = pandas.read_csv('sensorData.csv')
print(data.keys())
palette.reverse()
color_mapper = LogColorMapper(palette=palette)

source = ColumnDataSource(data=dict(
    x=list(coor['x']),
    y=list(coor['y']),
    voldata = [1]*len(coor['x']),
    address = list(coor['location']),
))
print(source.data['address'])
TOOLS = "pan,wheel_zoom,reset,hover,save"
p = figure(
    title="Traffic Volume",
    x_axis_location=None, y_axis_location=None, tools = TOOLS, x_axis_label='Location of Checkpoint', y_axis_label='Location of Checkpoint'
)
p.circle(x='x',y='y',
    fill_color={'field': 'voldata', 'transform': color_mapper}, 
    size = 10, source=source)
hover = p.select_one(HoverTool)
hover.point_policy = "follow_mouse"
hover.tooltips = [
    ("Volume", "@voldata"),
    ("Address", "@address"),
]
button = Button(label="Run", button_type="success")


def update():
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

button.on_click(update)
show(p)
layout = column(p,widgetbox(button))
curdoc().add_root(layout)
curdoc().title = "Heatmap"