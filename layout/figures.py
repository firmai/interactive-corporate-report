import pandas as pd

from datetime import datetime, timedelta

import plotly.plotly as py
from plotly.graph_objs import *
import os
import _pickle as pickle
#


def figs(code_start,bench_start):
    print("loooooook")
    print(code_start)
    print(bench_start)

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "input_fields.csv")
    input_fields = pd.read_csv(path)

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../data/stock/")

    company = input_fields[input_fields["code_or_ticker"] == code_start]["short_name"].reset_index(drop=True)[0]

    tick = " (" + input_fields[input_fields["code_or_ticker"] == code_start]["ticker"].reset_index(drop=True)[0] + ") "

    not_listed = input_fields[input_fields["listed"] == "No"].reset_index(drop=True)["code_or_ticker"]

    if code_start not in list(not_listed):
        df_com_sim = pd.read_csv(path + code_start + "_sim_tick_df.csv")
        df_com_sim["date"] = pd.to_datetime(df_com_sim["date"], format="%Y-%m-%d")
        df_com_sim = df_com_sim[df_com_sim["date"] < "01-18-2018"]

    df_com = pd.read_csv(path + code_start + "_tick_df.csv")

    df_ben = pd.read_csv(path + bench_start + "_tick_df.csv")

    df2 = pd.read_csv(path + "bench" + "_tick_df.csv")

    df_ben["date"] = pd.to_datetime(df_ben["date"], format="%Y-%m-%d")
    df_com["date"] = pd.to_datetime(df_com["date"], format="%Y-%m-%d")
    df2["date"] = pd.to_datetime(df_com["date"], format="%Y-%m-%d")

    trace1 = {
        "x": df_com["date"],
        "y": df_com["close"],
        "line": {
            "color": "rgb(140, 15, 7)",
            "width": 3
        },
        "mode": "lines",
        "name": company,
        "type": "scatter",
        "uid": "4cd1a4"
    }
    trace2 = {
        "x": df_ben["date"],
        "y": df_ben["close"],
        "connectgaps": True,
        "line": {
            "color": "rgb(22, 60, 109)",
            "width": 3
        },
        "mode": "lines",
        "name": bench_start,
        "type": "scatter",
        "uid": "f7fed3"
    }

    trace3 = {
        "x": df2["date"],
        "y": df2["mean"],
        "connectgaps": True,
        "line": {
            "color": "rgb(10, 45, 90)",
            "width": 0.3
        },
        "mode": "lines",
        "showlegend": False,
        "name": "Ind Perf.",
        "type": "scatter",
        "uid": "f7fed3"
    }

    data = Data([trace1, trace2, trace3])


    try:
        if len(df_com_sim) > 0:
            trace4 = {
                "x": df_com_sim["date"],
                "y": df_com_sim["close"],
                "connectgaps": True,
                "line": {
                    "color": "rgb(120, 8, 14)",
                    "width": 0.3
                },
                "mode": "lines",
                "name": "AI Pred.",
                "showlegend": False,
                "type": "scatter",
                "uid": "f7fed3"
            }

            data = Data([trace1, trace2, trace3, trace4])
    except:
        print("fail")

    if code_start not in list(not_listed):
        maxos = [int(min([df_ben["close"].min(),df2["mean"].min(), df_com_sim["close"].min(), df_com["close"].min()]) - 40),
                          int(max([df_ben["close"].max(),df2["mean"].max(),df_com_sim["close"].min(), df_com["close"].max()]) + 10)]
    else:
        maxos = [
            int(min([df_ben["close"].min(), df2["mean"].min(), df_com["close"].min()]) - 40),
            int(max([df_ben["close"].max(), df2["mean"].max(), df_com["close"].max()]) + 10)]

    layout = {
        "autosize": True,
        "font": {"family": "Raleway"},
        "hovermode": "compare",
        "legend": {
            "x": 0.45,
            "y": 0.05,
            "bgcolor": "rgba(255, 255, 255, 0.5)",
            "orientation": "v"
        },
        "margin": {
            "r": 0,
            "t": 10,
            "b": 30,
            "l": 35,
            "pad": 0
        },
        "plot_bgcolor": "rgb(217, 224, 236)",
        "showlegend": True,
        "title": "",
        "titlefont": {
            "family": "Raleway",
            "size": 12
        },
        "xaxis": {
            "autorange": False,
            "gridcolor": "rgb(255, 255, 255)",
            "range": [str(min([df_ben["date"].min(), df_com["date"].min()]))[:10],
                      str(max([df_ben["date"].max() + timedelta(days=200), df_com["date"].max() + timedelta(days=200)]))[:10]],
            "showline": True,
            "tickfont": {"color": "rgb(68, 68, 68)"},
            "tickformat": "%b %Y",
            "ticks": "outside",
            "title": "",
            "type": "date"
        },
        "yaxis": {
            "autorange": False,
            "gridcolor": "rgb(255, 255, 255)",
            "nticks": 11,
            "range": maxos,
            "showline": True,
            "ticks": "outside",
            "title": "",
            "type": "linear"
        }
    }
    fig = Figure(data=data, layout=layout)
    return fig