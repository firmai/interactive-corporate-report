# Get this figure: fig = py.get_figure("https://plot.ly/~1beb/3/")
# Get this figure's data: data = py.get_figure("https://plot.ly/~1beb/3/").get_data()
# Add data to this figure: py.plot(Data([Scatter(x=[1, 2], y=[2, 3])]), filename ="plot from API", fileopt="extend")

# Get figure documentation: https://plot.ly/python/get-requests/
# Add data documentation: https://plot.ly/python/file-options/

# If you're using unicode in your file, you may need to specify the encoding.
# You can reproduce this figure in Python with the following code!

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api


import pandas as pd
import numpy as np
import os
from datetime import datetime

str(datetime.now().year)

from plotly.graph_objs import *

def figs_polar(coy):
    ### This can be done elsewehere and loaded in as csv = first 10 lines

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "data/closure/")
    new_frame = pd.read_csv(path + "stakeholder_metrics.csv")
    new_frame = new_frame.set_index("ticker")
    print(new_frame)
    new_frame.columns = ['Customers', 'Management', 'Employees', 'Shareholders', "Mean"]

    go = -1
    for inde in list(new_frame.index):
        go = go + 1
        distances = (((new_frame[new_frame.index != inde].loc[:, :"Shareholders"] - new_frame.loc[inde,
                                                                                    :"Shareholders"]) ** 2).mean(
            axis=1)) ** (1 / 2)

        frmo = distances.to_frame()

        frmo.columns = [inde]

        if go == 0:
            fula = frmo
        else:
            fula = pd.merge(fula, frmo, left_index=True, right_index=True, how="left")

    del fula["Mean"]

    fula = fula.iloc[:-1,:]

    trace1 = {"type": "scatter"}
    trace2 = {
        "x": [0, 0],
        "y": [0, 0],
        "line": {
            "color": "#d3d3d3",
            "dash": "3px"
        },
        "showlegend": False,
        "type": "scatter"
    }

    four_dict = {}
    g = -1
    for inde in list(fula.sort_values(coy).head(4)[coy].index):
        g = g + 1
        bench = inde

        plots_dict = {}
        plots_dict[coy, "Employees"] = new_frame.loc[coy, "Employees"] / 5
        plots_dict[coy, "Managers"] = new_frame.loc[coy, "Management"] / 5
        plots_dict[coy, "Shareholders"] = new_frame.loc[coy, "Shareholders"] / 5
        plots_dict[coy, "Customers"] = new_frame.loc[coy, "Customers"] / 5

        plots_dict[bench, "Employees"] = new_frame.loc[bench, "Employees"] / 5 - (
        (1 + (new_frame.loc[coy, "Employees"] / 5) - (new_frame.loc[bench, "Employees"] / 5)) ** 2 - 1)
        plots_dict[bench, "Managers"] = new_frame.loc[bench, "Management"] / 5 - (
        (1 + (new_frame.loc[coy, "Management"] / 5) - (new_frame.loc[bench, "Management"] / 5)) ** 2 - 1)
        plots_dict[bench, "Shareholders"] = new_frame.loc[bench, "Shareholders"] / 5 - (
        (1 + (new_frame.loc[coy, "Shareholders"] / 5) - (new_frame.loc[bench, "Shareholders"] / 5)) ** 2 - 1)
        plots_dict[bench, "Customers"] = new_frame.loc[bench, "Customers"] / 5 - (
        (1 + (new_frame.loc[coy, "Customers"] / 5) - (new_frame.loc[bench, "Customers"] / 5)) ** 2 - 1)

        # plots_dict[coy, "Employees"] = 0.6
        # plots_dict[coy, "Managers"] = 0.6
        # plots_dict[coy, "Shareholders"] = 0.6
        # plots_dict[coy, "Customers"] = 0.6

        # plots_dict[bench, "Employees"] = 0.6
        # plots_dict[bench, "Managers"] = 0.6
        # plots_dict[bench, "Shareholders"] = 0.6
        # plots_dict[bench, "Customers"] = 0.6


        0.6

        key_tick = list(pd.DataFrame(np.array(list(plots_dict.keys())).reshape(-1, 2))[0].drop_duplicates().values)

        key_type = list(pd.DataFrame(np.array(list(plots_dict.keys())).reshape(-1, 2))[1].drop_duplicates().values)

        abso = {}
        for key, value in plots_dict.items():
            abso[key] = abs(value)

        max_value = {}
        for r in key_type:
            k = 0
            for i in key_tick:
                max_value[r] = abso[i, r]
                if max_value[r] < k:
                    max_value[r] = k
                else:
                    k = max_value[r]

        trace26 = {
            "x": [0, 1 * plots_dict[coy, "Customers"], 0, -1 * plots_dict[coy, "Managers"], 0],
            "y": [1 * plots_dict[coy, "Shareholders"], 0, -1 * plots_dict[coy, "Employees"], 0,
                  1 * plots_dict[coy, "Shareholders"]],
            "hoverinfo": "text",
            "marker": {"color": "#65201F"},
            "mode": "lines+markers",
            "name": coy,
            "text": ["Placeholder %", str(datetime.now().year) +" Customers {} %".format(round(plots_dict[coy, "Customers"],2)), str(datetime.now().year) +" Employees {} %".format(round(plots_dict[coy, "Employees"],2)), str(datetime.now().year) +" Managers {} %".format(round(plots_dict[coy, "Managers"],2)),str(datetime.now().year) +" Shareholders {} %".format(round(plots_dict[coy, "Shareholders"],2))],
            "type": "scatter"
        }
        trace27 = {
            "x": [0, 1 * plots_dict[bench, "Customers"], 0, -1 * plots_dict[bench, "Managers"], 0],
            "y": [1 * plots_dict[bench, "Shareholders"], 0, -1 * plots_dict[bench, "Employees"], 0,
                  1 * plots_dict[bench, "Shareholders"]],
            "hoverinfo": "text",
            "marker": {"color": "#8a9ea5"},
            "mode": "lines+markers",
            "name": bench,
            "text": ["Placeholder %", str(datetime.now().year) +" Customers {} %".format(round(plots_dict[bench, "Customers"],2)), str(datetime.now().year) +" Employees {} %".format(round(plots_dict[bench, "Employees"],2)), str(datetime.now().year) +" Managers {} %".format(round(plots_dict[bench, "Managers"],2)),str(datetime.now().year) +" Shareholders {} %".format(round(plots_dict[bench, "Shareholders"],2))],
            "type": "scatter"
        }
        trace28 = {
            "x": [0, 0.16 + max_value["Customers"], 0, -.15 - max_value["Managers"], 0],
            "y": [0.7 + max_value["Shareholders"], 0, -.10 - max_value["Employees"], 0,
                  0.1 + max_value["Shareholders"]],
            "hoverinfo": "none",
            "line": {
                "color": "white",
                "dash": "30px",
                "shape": "spline"
            },
            "mode": "lines+text",
            "showlegend": False,
            "text": ["Shareholders", "Customers", "Employees", "Managers", "Shareholders"],
            "textposition": "top middle",
            "type": "scatter"
        }

        data = Data([trace1, trace2, trace26, trace27, trace28])
        layout = {
            "autosize": True,
            "height": 210,
            "annotations": [
            dict(
                x=0,
                y=0,
                xref='x',
                yref='y',
                text='MSE: '
                     ' {}'.format(round((((plots_dict[coy, "Customers"]- plots_dict[bench, "Customers"])**2 +
                                          (plots_dict[coy, "Shareholders"] - plots_dict[bench, "Shareholders"])**2 +
                                          (plots_dict[coy, "Employees"]- plots_dict[bench, "Employees"])**2 +
                                          (plots_dict[coy, "Managers"] - plots_dict[bench, "Managers"])**2))**(1/2),2)),
                showarrow=False,
                ax=0,
                ay=0
            )],
            "hovermode": "closest",
            "width": 290,
            "margin": {
                "r": 0,
                "t": 10,
                "b": 10,
                "l": 0,
                "pad": 0
            },
            "xaxis": {
                "range": [-1.25, 1.25],
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False
            },
            "yaxis": {
                "range": [-1.25, 1.25],
                "showgrid": False,
                "showticklabels": False,
                "zeroline": False
            }
        }
        fig = Figure(data=data, layout=layout)
        four_dict[g] = fig

    # plot_url = py.plot(fig)
    # return fig
    #plot_url = py.plot(fig)
    return four_dict