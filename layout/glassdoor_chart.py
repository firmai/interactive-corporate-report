import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import numpy as np

from flask import Flask
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
import os

#Change Over Time

my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_ngrams = os.path.join(my_path, "../data/ngrams/")

input_fields = pd.read_csv(path_2)



def sum_gd(k, time_s, many, norm, bench):
    print("lgffd")
    print(k, time_s, many, norm, bench)

    print(many)
    if many=="3":
        print("lolooo")
        print(path_in_ngrams + bench + "_review_" + k + "_" + time_s + "_" + "1" + ".txt")
        with open(path_in_ngrams + bench + "_review_" + k + "_" + time_s + "_" + "1" + ".txt", 'r') as myfile:
            data = myfile.read().replace('\n', '')
    elif time_s=="rvp":
        with open(path_in_ngrams + bench + "_review_" + k + "_" + "alltime" + "_" + "1" + ".txt", 'r') as myfile:
            data = myfile.read().replace('\n', '')
    else:
        with open(path_in_ngrams + bench + "_review_" + k + "_" + time_s + "_" + str(many) + ".txt", 'r') as myfile:
            data = myfile.read().replace('\n', '')

    return str(data)


def chart_gd(k, time_s, many, norm, bench):

    print("lgffd")
    print(k, time_s, many, norm, bench)
    if time_s=="rvp":
        # Also if bench Compare, remember to change the filters, norm should also change.
        # I think compare should be added in the time dropdown.
        print(path_in_ngrams + bench +"_review_" + k + "_" + "three_years" + "_" + str(many) + ".csv")
        ras_3 = pd.read_csv(path_in_ngrams + bench +"_review_" + k + "_" + "three_years" + "_" + str(many) + ".csv").head(10)

        ras_5 = pd.read_csv(path_in_ngrams + bench +"_review_" + k + "_" + "five_years_ago" + "_" + str(many) + ".csv")

        ras_5 = ras_5[["name", "norm"]]

        ras_3 = ras_3[["name", "norm"]].head(10)

        thus = pd.merge(ras_3, ras_5, on="name", how="left")
        thus["norm_y"] = np.where(thus["norm_y"].isnull(),(thus["norm_x"] - (thus["norm_x"].mean() - thus["norm_x"].mean())), thus["norm_y"])
        month = list(thus["name"].values)
        good = list(thus["norm_x"].values)

        trace1 = go.Scatter(
            x=month,
            y=good,
            name='Recent',
            line=dict(
                color=('rgb(205, 12, 24)'),
                width=4,
                dash='dash')  # dash options include 'dash', 'dot', and 'dashdot'
        )

        good = list(thus["norm_y"].values)

        trace2 = go.Scatter(
            x=month,
            y=good,
            name='Past',
            line=dict(
                color=('blue'),
                width=4,
                dash='dash')  # dash options include 'dash', 'dot', and 'dashdot'
        )

        data = [trace1, trace2]
    else:
        ras = pd.read_csv(path_in_ngrams + bench + "_review_" + k + "_" + time_s + "_" + str(many) + ".csv").head(10)
        month = list(ras["name"].values)

        if norm == "True":
            good = list(ras["count"].values)
        else:
            good = list(ras["norm"].values)

        # Create and style traces

        trace1 = go.Scatter(
            x=month,
            y=good,
            name='positive nouns',
            line=dict(
                color=('rgb(205, 12, 24)'),
                width=4,
                dash='dash')  # dash options include 'dash', 'dot', and 'dashdot'
        )

        data = [trace1]

    # Edit the layout
    layout = dict(title = 'Frequency of ' + k + ' Terms',
                  yaxis = dict(title = 'Frequency'),
                  )

    fig = dict(data=data, layout=layout)
    return fig

def layout(code):
    return html.Div([

    html.Div([

    html.Div([
        dcc.Dropdown(
            id='goo_ba',
            options=[{'label': r, 'value': v} for r, v in zip(["Good", "Great", "Bad", "Severe"],
                                                              ["good", "great", "bad", "severe"])],
            value="good",
            clearable=False,
            className="dropper"
        )
    ], style={'background-color': "white", 'color': 'rgb(217, 224, 236)', 'float': 'left',
              'padding-right': '1cm', 'width': '19%'}),

    html.Div([
        dcc.Dropdown(
            id='time',
            options=[{'label': r, 'value': v} for r, v in zip(["All Observations","Recent vs Past","Last Six Month", "Last Year","Last Three Years", "Last Five Years","First Five Years"], ["alltime","rvp","six month","year","three_years", "five_years","five_years_ago"])],
            value="alltime",
            clearable=False,
            className="dropper"
        )
    ], style={'background-color': 'white', 'color': 'rgb(217, 224, 236)', 'float': 'left', 'padding-right': '1cm',
              'width': '19%'}),



    html.Div([
        dcc.Dropdown(
            id='many',
            options=[{'label': r, 'value': v} for r, v in zip(["One Noun","Two Words","Phrase"],["1","2","3"])],
            value="3",
            clearable=False,
            className="dropper"
        )
    ], style={'background-color': 'white', 'padding-right': '1cm', 'color': 'rgb(217, 224, 236)', 'float': 'left',
              'width': '19%'}),

        html.Div([
            dcc.Dropdown(
                id='norm',
                options=[{'label': r, 'value': v} for r, v in
                         zip(["Relative", "Count"], ["False","True"])],
                value="True",
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': 'white', 'padding-right': '1cm', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                  'width': '19%'}),

        html.Div([
            dcc.Dropdown(
                id='bencher',
                options=[{'label': r, 'value': v} for r, v in
                         zip(input_fields["short_name"], input_fields["code_or_ticker"])],
                value="BJRI",
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': 'white', 'padding-right': '1cm', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                  'width': '19%'}),

    # , 'float': 'right', 'display': 'inline-block'
], style={'background-color': 'white', 'padding-left': '1.8cm', 'clear': 'both', 'padding-top': '0.3cm'},
    className="double_drop"),

html.Div([dcc.Graph(id='graphed',config={'displayModeBar': False})], style={'clear':'both'}),
html.Div([dcc.Textarea(id='text_sum', placeholder='Summary', value='Component', style={'width': '100%', 'height':'140px'}
                        )], style={'padding-top':'25px','clear':'both'})

])

