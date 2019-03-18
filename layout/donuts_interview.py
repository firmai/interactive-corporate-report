import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
# py.sign_in('snowde', 'm12EGGpG9bqMssuzLnjY')

from scipy import signal

from datetime import datetime, timedelta

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

from datetime import datetime
from dateutil.parser import parse
import os


my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_gdoor = os.path.join(my_path, "../data/glassdoor/")

#input_fields = pd.read_csv(path)

#code = input_fields["code_or_ticker"]

def donuts_fig(code):

    p = code

    inter = pd.read_csv(path_in_gdoor + p + "_interview.csv")

    for i in ["Experience","Offer", "Interview Type","Interview","Application","Interview Type"]:
        inter[i] = [ga[2:-2] for ga in inter[i].values]


    inter["Question"] = [ga[3:-2] for ga in inter["Question"].values]


    inter['Interview Date'] = inter['Interview Date'].apply(lambda x: parse(x))

    inter = inter.sort_values("Interview Date")


    inter["Experience"].value_counts()

    exp = inter["Experience"].value_counts()

    pos = exp[0]
    neu = exp[1]
    neg = exp[2]

    all_i = pos + neu + neg

    uno = (pos * 5 + neu * 2.5 + neg * 1) / (all_i * 5) * 5

    # Then we round it to 2 places
    uno = round(uno, 1)

    off = inter["Offer"].value_counts()

    of = off[0]
    no = off[1]
    de = off[2]

    inter["accepted"] = inter["Offer"].apply(lambda x: 1 if x == "Accepted Offer" else 0)

    inter["perc_acc"] = inter["accepted"].rolling(30).sum()

    inter["perc_acc"] = inter["perc_acc"].fillna(method="bfill")

    inter["perc_acc"] = inter["perc_acc"] / 30

    inter["perc_acc"] = inter["perc_acc"].round(2)

    inter["perc_acc"] = signal.savgol_filter(inter["perc_acc"], 31, 3)

    filter_f = inter["Interview Date"].max() - timedelta(365 * 5)

    inter = inter[inter["Interview Date"] > filter_f]

    # Get this figure: fig = py.get_figure("https://plot.ly/~snowde/43/")
    # Get this figure's data: data = py.get_figure("https://plot.ly/~snowde/43/").get_data()
    # Add data to this figure: py.plot(Data([Scatter(x=[1, 2], y=[2, 3])]), filename ="Plot 43", fileopt="extend")

    # Get figure documentation: https://plot.ly/python/get-requests/
    # Add data documentation: https://plot.ly/python/file-options/

    # If you're using unicode in your file, you may need to specify the encoding.
    # You can reproduce this figure in Python with the following code!

    # Learn about API authentication here: https://plot.ly/python/getting-started
    # Find your api_key here: https://plot.ly/settings/api


    trace1 = {
        "hole": 0.8,
        "labels": ["Offer Accepted", "No Offer", "Offer Decline"],
        "showlegend": False,
        "type": "pie",
        "values": [of, no, de],
        "text": ['Accepted', 'No Offer', 'Declined'],
        "textposition": 'outside'
    }


    inter_1 = inter[inter["Interview Date"] < (inter["Interview Date"].max() - timedelta(365*4.6))]
    print(inter_1["Interview Date"])
    trace2 = {
        "x": inter_1["Interview Date"],##
        "y": inter_1["perc_acc"],
        "line": {
            "color": "white",
            "width": 8
        },
        "mode": "lines",
        "name": "Accepted",
        "type": "scatter",
    }

    inter_2 = inter[inter["Interview Date"] > (inter["Interview Date"].max() - timedelta(365*4.6))]

    print(inter_2["Interview Date"])
    inter_2.iloc[-1,inter_2.columns.get_loc("Interview Date")] = inter_2.iloc[-1,inter_2.columns.get_loc("Interview Date")] + timedelta(180)

    trace3 = {
        "x": inter_2["Interview Date"],
        "y": inter_2["perc_acc"],
        "line": {
            "color": "black",
            "width": 8
        },
        "mode": "lines",
        "name": "Accepted",
        "type": "scatter",
    }

    data = Data([trace1, trace2, trace3])
    layout = {

        "showlegend": False,
        "xaxis": {
            "autorange": True,
            "type": "date",
            "showline": False,
            "ticks": False,
            "showgrid": False,
            "showticklabels": False

        },
        "margin": {
            "l": 227,
            "r": 240,
            'b': 300,
            "pad": -10},

        "title": "Accepted Job Offer",

        "yaxis": {
            "type": "linear",
            "range": [inter["perc_acc"].min() - .25, inter["perc_acc"].max() + .25],
            "showline": False,
            "ticks": False,
            "showgrid": False,
            "showticklabels": False
        },

        "autosize": False,
        "width": 700,
        "height": 700,
    }
    offer_fig = Figure(data=data, layout=layout)

    int_type = exp = inter["Interview Type"].value_counts()

    easy = int_type[0]
    avg = int_type[1]
    diff = int_type[2]

    trace1 = {
        "hole": 0.8,
        "labels": ["Easy", "Average", "Difficult"],
        'marker': {'colors': ['rgb(56, 75, 126)',
                              "red",
                              'green']},

        "showlegend": False,
        "type": "pie",

        "values": [easy, avg, diff],
        "text": ['Easy', 'Average', 'Difficult'],
        "textposition": 'outside'
    }
    trace2 = {
        "x": [1],
        "y": [easy],
        "name": 4,
        "type": "bar",
        "marker": {
            "color": 'rgb(56, 75, 126)'},
        "textposition": 'outside'
    }
    trace3 = {
        "x": [2],
        "y": [avg],
        "name": 6,
        "type": "bar",
        "marker": {
            "color": 'red'},
    }
    trace4 = {
        "x": [3],
        "y": [diff],
        "name": 8,
        "type": "bar",
        "marker": {
            "color": 'green'},
    }
    data = Data([trace1, trace2, trace3, trace4])
    layout = {
        "showlegend": False,
        "title": "Interview Difficulty",
        "xaxis": {
            "autorange": True,
            "domain": [0.33, 0.67],
            "range": [3, 9],
            "type": "linear",
            "showline": False,
            "ticks": False,
            "showgrid": False,
            "showticklabels": False
        },
        "yaxis": {
            "autorange": True,
            "domain": [0.33, 0.67],
            "range": [0, 28.0669856459],
            "type": "linear",
            "showline": False,
            "ticks": False,
            "showgrid": False,
            "showticklabels": False
        },

        "autosize": False,
        "width": 350,
        "height": 350,
    }

    difficulty_fig = Figure(data=data, layout=layout)

    # Interview Experience

    trace1 = {
        "hole": 0.8,
        "labels": ["Positive", "Neutral", "Negative"],
        "showlegend": False,
        "type": "pie",
        "values": [pos, neu, neg],
        "text": ['Positive', 'Neutral', 'Negative'],
        "textposition": 'outside'
    }

    data = Data([trace1])
    layout = {
        "annotations": [
            {
                "y": 0.5,
                "text": str(uno),
                "font": {
                    "size": 50
                },
                "showarrow": False,
                "x": 0.5
            }],

        "title": "Interview Experience",

        "yaxis": {
            "autorange": True,
            "domain": [0.33, 0.67],
            "range": [0, 28.0669856459],
            "title": "Avg MPG",
            "type": "linear"
        },

        "autosize": False,
        "width": 350,
        "height": 350,
    }

    experience_fig = Figure(data=data, layout=layout)
    return  difficulty_fig, experience_fig, offer_fig


