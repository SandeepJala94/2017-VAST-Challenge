from bokeh.io import show, curdoc
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LogColorMapper,
    LinearColorMapper
)
from bokeh.palettes import Viridis6 as palette
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
data = pandas.read_csv('Lekagul Sensor Data.csv')
print(coor.keys())
palette.reverse()
color_mapper = LinearColorMapper(palette=palette)

source = ColumnDataSource(data=dict(
    x=coor['x'],
    y=coor['y'],
    voldata = [1]*len(coor['x']),
    address = coor['location'],
))
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
	nodeVolume = {}
	for i in coor['location']:
		nodeVolume[i] = 0
	for index, row in data.iterrows():
		nodeVolume[row['car-id']] +=1
	patch = {'bar' : [nodeVolume]}




show(p)
# layout = column(p,widgetbox(button))
# curdoc().add_root(layout)
# curdoc().title = "Heatmap"