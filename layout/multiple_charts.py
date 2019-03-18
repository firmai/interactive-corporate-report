# -*- coding: utf-8 -*-
from __future__ import print_function

import pandas as pd

import numpy as np
import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import colorlover as cl
import numpy as np
from flask import Flask
## -*- coding: utf-8 -*-
import pandas as pd
#import stock_df_dict as sd

import dash
from dash import Dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import colorlover as cl
import numpy as np
from flask import Flask
####
from six.moves import cPickle as pickle
import processing.input as inp

##############

def create_figure(highlight, data_frame, req, stu):

    traces = []
    annotations = []
    scale = cl.scales['5']['div']['RdBu']
    x = data_frame["year"]
    num = data_frame["year"].shape[0]

    data_frame = data_frame.fillna(value=0.00)
    data_frame = data_frame.replace(0.01, 0.00)


    for fundamental in data_frame.drop("year",axis=1).columns:
        #print(data_frame[fundamental])
        growth = data_frame[fundamental].iloc[-1]-data_frame[fundamental].iloc[0]
        y = data_frame[fundamental]
        #print(y.iloc[-1])

        if growth > 0:
            color = scale[4]
            legendgroup = 'positive growth'
        else:
            color = scale[1]
            legendgroup = 'negative growth'

        hoverinfo = None
        width = 1

        hoverinfo = None


        if fundamental not in highlight:
            color = 'lightgrey'

        if highlight and fundamental in highlight:
            width = 2
            if color == 'lightgrey':
                color = 'grey'
            hoverinfo = None

        else:
            width = 0.2
            hoverinfo = None

        traces.append({
            'x': x,
            'y': y,
            'mode': 'line',
            'line': {
                'color': color,
                'width': width
            },
            'text':
                ('<b>{}   </b><br>'
                 '<b>{} : {:,}   </b>'
                 '<b>{} : {:,}</b>').format(
                    fundamental,x[0],round(y[0], 2),x.iloc[-1], round(y.iloc[-1], 2)

                ) if fundamental in highlight else None,



            'legendgroup': legendgroup,
            'name': fundamental,
            'hoverinfo': hoverinfo,
            'showlegend': (
                False if legendgroup in [t['legendgroup'] for t in traces]
                else True
            )

        })

        if (highlight and fundamental in highlight):
            annotations.append({
                'x': traces[-1]['x'].iloc[-1], 'xref': 'x', 'xanchor': 'left',
                'y': traces[-1]['y'].iloc[-1], 'yref': 'y', 'yanchor': 'top',
                'showarrow': False,
                'text': fundamental,
                'font': {'size': 12},
                'bgcolor': 'rgba(255, 255, 255, 0.5)'
            })

            # reorder traces to reorder legend items
        if not highlight:
            def get_trace_index(traces, legendgroup):
                for i, trace in enumerate(traces):
                    if trace['showlegend'] and trace['legendgroup'] == legendgroup:
                        return i

            traces.insert(0, traces.pop(get_trace_index(traces, 'positive growth')))
            traces.insert(0, traces.pop(get_trace_index(traces, 'negative growth')))
        else:
            # move highlighted traces to the end
            for i, trace in enumerate(traces):
                if trace['line']['width'] != 2.5:
                    traces.insert(0, traces.pop(i))

        if not highlight:
            annotations = [{
                'x': 0.8, 'xref': 'paper', 'xanchor': 'left',
                'y': 0.95, 'yref': 'paper', 'yanchor': 'bottom',
                'text': '<b>Variable Growth</b>',
                'showarrow': False
            }]


    layout = {
        'xaxis': {
            'showgrid': False,
            'showline': False,
            'zeroline': False,
            'showticklabels': True,
            'ticks': ''
        },
        'yaxis': {
            'showgrid': False,
            'showticklabels': False,
            'zeroline': False,
            'ticks': '',
            'title': 'Fundamentals'
        },
        'showlegend': not bool(highlight),
        'hovermode': 'closest',
        'legend': {
            'x': 0.8,
            'y': 0.95,
            'xanchor': 'left'
        },
        'annotations': annotations,
        'margin': {'t': 20, 'b': 60, 'r': 0, 'l': 20},
        'font': {'size': 12}
    }

    return {'data': traces, 'layout': layout}

server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname='/dash/gallery/recession-report/', csrf_protect=False)
app.css.append_css({
    'external_url': (
        'https://cdn.rawgit.com/chriddyp/0247653a7c52feb4c48437e1c1837f75'
        '/raw/a68333b876edaf62df2efa7bac0e9b3613258851/dash.css'
    )
})


def load_dict(filename_):
    with open(filename_, 'rb') as f:
        ret_di = pd.read_pickle(f)
    return ret_di

import os

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")


input_fields = pd.read_csv(path)

short  = input_fields["short_name"]
codes = input_fields["code_or_ticker"]


layout = html.Div ([

            html.Div([

                html.Div([
                    dcc.Dropdown(
                        id='request',
                        options=[{'label': r, 'value': v} for r, v in zip(["Calculations", "Income Statement", "Cash Flow Statement","Balance Sheet"],
                                                                          ["calculations", "income_statement", "cash_flow","balance_sheet"])],
                        value="calculations",
                        clearable=False,
                        className="dropper"
                    )
                ], style={'background-color':"white", 'color': 'rgb(217, 224, 236)', 'float': 'left',
                          'padding-right': '1cm', 'width': '30%'}),

                html.Div([
                    dcc.Dropdown(
                        id='study',
                        options=[{'label': i, 'value': i} for i in ["Normalised", "Original", "Correlated Fundamentals"
                            ,"Price Correlated","Principal Component","Better Than Bench","Worse Than Bench","Volatile","Stable"]],
                        value="Normalised",
                        clearable=False,
                        className="dropper"
                    )
                        ], style={'background-color':'white','padding-right': '1cm','color':'rgb(217, 224, 236)','float':'left','width': '30%'}),

                html.Div([
                    dcc.Dropdown(
                        id='bench',
                        options=[{'label': r, 'value': v} for r, v in zip(short, codes)],
                        value="BJRI",
                        clearable=False,
                        className="dropper"
                    )
                ], style={'background-color': 'white', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                          'width': '26%'})
                # , 'float': 'right', 'display': 'inline-block'
            ], style={'background-color': 'white', 'padding-left': '1.8cm','clear':'both', 'padding-top': '0.3cm'},
                className="double_drop"),
    html.Div(id='filtered-content', style={'clear':'both', 'height':'250px'}),

    html.Div([
        dcc.Dropdown(
            multi=True,
            value=["rnnoa", "earningsyield"],
            id='category-filter',
            className='dropper')
    ], style={'background-color': 'white','padding-top': '0cm', 'color': 'rgb(217, 224, 236)', 'clear':'both', 'padding-right': '0cm',
              'width': '100%'}),


        ],style={'background-color': 'white'})


