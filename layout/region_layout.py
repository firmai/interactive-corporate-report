import layout.donuts_interview as di
import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html


import os
my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")
import layout.location_distance as ld
import dash_table_experiments as dt
import layout.region_layout_couny_fig as rlf



def dic(options_bench_code, target_code, benchmark_code_info ):
    import pandas as pd
    import _pickle as pickle
    import numpy as np
    import re

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")
    input_fields = pd.read_csv("input_fields.csv")

    bench_short_name = \
        input_fields[input_fields["code_or_ticker"] == benchmark_code_info]["short_name"].reset_index(drop=True)[0]

    target_short_name = \
        input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

    rating_type = "Average Rating"

    region_type = "State"


    target_fig = rlf.figs_county(target_short_name,rating_type )

    bench_fig = rlf.figs_county(bench_short_name, rating_type)


    region_layout =   html.Div([


        html.Br([]),

            html.Div(
                [dcc.Graph(figure = target_fig,
                id='fig_target',
                config={'displayModeBar': False}),

                  ],style={'margin-top':'-0.8cm','margin-bottom':'0.1cm','padding-top':'0.0cm','height':'80%','width':'300px'}),

        html.Div([

            html.Div([
                dcc.Dropdown(
                    id='benchmary_dd',
                    options=options_bench_code,
                    value=bench_short_name,
                    clearable=False,
                    className="dropper"
                )
            ], style={'background-color': 'white', 'margin-top': '0cm', 'padding-right': '0.3cm',
                      'color': 'rgb(217, 224, 236)',
                      'float': 'left',
                      'width': '33%'}),

            html.Div([
                dcc.Dropdown(
                    id='rating_dd',
                    options=[{'label': i, 'value': i} for i in
                             ["Average Rating", "Female Rating", "Male Rating", "Visual Importance", "Connectedness",
                              "Foreign Importance"]],
                    value=rating_type,
                    clearable=False,
                    className="dropper"
                )
            ], style={'background-color': "white", 'margin-top': '0cm', 'padding-right': '0.3cm',
                      'color': 'rgb(217, 224, 236)',
                      'float': 'left', 'width': '33%'}),

            html.Div([
                dcc.Dropdown(
                    id='county_state_dd',
                    options=[{'label': r, 'value': r} for r in ["County", "State"]],
                    value=region_type,
                    clearable=False,
                    className="dropper"
                )
            ], style={ 'background-color': 'white', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                      'width': '33%'})
            # , 'float': 'right', 'display': 'inline-block'
        ], style={'background-color': 'white','margin-top': '-0.3cm', 'z-index': '100', 'clear': 'both', 'min-width': '100%', 'display': 'inline-block',
                  'background-color': 'white'},
        ),

    html.Div(
                [dcc.Graph(figure = bench_fig,
                id='fig_bench',
                config={'displayModeBar': False}),

                  ],style={'margin-top':'0.1cm','padding-top':'0.0cm','height':'80%','width':'300px'}),

    ],style={'padding-top':'0.0cm'})

    d = {}
    d["region_layout"] = region_layout

    return d





