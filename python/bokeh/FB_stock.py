import pandas as pd
import numpy as np
from datetime import date, datetime

import bokeh
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Select, DateRangeSlider
from bokeh.plotting import figure,show

# column: Date,Open,High,Low,Close,Volume
stock = pd.read_csv('FB_Historical_Data.csv', parse_dates=['Date'])

axis_map = {
   "Date": "Date",
   "Open": "Open",
   "High": "High",
   "Low": "Low",
   "Close": "Close",
   "Volume": "Volume",
}

# Create Input controls
Date = DateRangeSlider(title="Date Range: ", start=date(2012, 5, 18), end=date(2021, 11, 26), value=(date(2012, 5, 18), date(2021, 11, 26)), step=1)
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Open")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Close")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[], Date=[]))

TOOLTIPS=[('Date', '@Date')]

p = figure(height=600, width=700, title="FB Stock", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="scale_both")
p.circle(x="x", y="y", source=source, size=7, line_color=None)

def select_stock():
    try:
        Date_min = datetime.fromtimestamp(Date.value[0]/1000).date()
        Date_max = datetime.fromtimestamp(Date.value[1]/1000).date()
    except:
        Date_min = Date.value[0]
        Date_max = Date.value[1]

    selected = stock[(stock["Date"].dt.date>=Date_min) & (stock["Date"].dt.date<=Date_max)]   

    return selected 

def update():
    df = select_stock()
    x_name = axis_map[x_axis.value]
    y_name = axis_map[y_axis.value]

    p.xaxis.axis_label = x_axis.value
    p.yaxis.axis_label = y_axis.value
    p.title.text = "FB Stocks"
    source.data = dict(
       x=df[x_name],
       y=df[y_name],
       Date=df["Date"],
    )

controls = [Date, x_axis, y_axis]

for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320)

l = column(row(inputs, p), sizing_mode="scale_both")

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "FB Stocks"


