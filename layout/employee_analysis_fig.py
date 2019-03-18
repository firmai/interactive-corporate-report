import plotly.plotly as py
import plotly.graph_objs as go
import colorlover as cl
import os
import _pickle as pickle
import pandas as pd
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")


input_fields = pd.read_csv(path)

short  = input_fields["short_name"]
codes = input_fields["code_or_ticker"]
my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/data/linkedin/"

dop_dict = pickle.load(open(path_out +"employee.p", "rb"))

colors_all = cl.scales['11']["qual"]["Paired"]

# Add data
# Create and style traces

ga = -1
data = []
for coy in list(codes):
    ga = ga + 1
    data.append(go.Scatter(
        x = dop_dict["insights"][coy]["date"],
        y = dop_dict["insights"][coy]["employee_count"],
        name = coy,
        opacity=0.8,
        line = dict(
            color = colors_all[ga],
            width = 4)
    ))

# Edit the layout
layout = dict(
            xaxis = dict(
                                      showgrid=False,
            zeroline=False,
            showline=False,),
              yaxis = dict(
                                      showgrid=False,
            zeroline=False,
            showline=False,),
              margin=go.Margin(
                  l=0,
                  r=0,
                  b=25,
                  t=0,
                  pad=0
              ),
              )
fig_level = dict(data=data, layout=layout)

import plotly.plotly as py
import plotly.graph_objs as go

import colorlover as cl
from IPython.display import HTML

colors_all = cl.scales['11']["qual"]["Paired"]

# Add data
# Create and style traces

ga = -1
data = []

for coy in list(codes):
    ga = ga + 1

    data.append(go.Scatter(
        x=dop_dict["insights"][coy]["date"],
        y=dop_dict["insights"][coy]["employee_add"],
        name=coy + " Net",
        legendgroup=coy,
        opacity=1,
        line=dict(
            color=colors_all[ga],
            width=3)
    ))

    data.append(go.Scatter(
        x=dop_dict["insights"][coy]["date"],
        y=dop_dict["insights"][coy]["allEmployeeHireCount"],
        name=coy + " Hired",
        legendgroup=coy,
        opacity=0.4,
        line=dict(
            color="green",
            width=0.5)
    ))

    data.append(go.Scatter(
        x=dop_dict["insights"][coy]["date"],
        y=dop_dict["insights"][coy]["employee_left"],
        name=coy + " Left",
        legendgroup=coy,
        opacity=0.4,
        line=dict(
            color="red",
            width=0.5)
    ))

# Edit the layout
layout = dict(
              xaxis=dict(
                         showgrid=False,
                         zeroline=False,
                         showline=False, ),
              yaxis=dict(
                         showgrid=False,
                         zeroline=False,
                         showline=False, ),
            margin=go.Margin(
                l=0,
                r=0,
                b=25,
                t=0,
                pad=0
            ),
                          )

fig_month = dict(data=data, layout=layout)