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




#def dict(firm_location, benchmark, bench_location, firm_location_options,benchmark_options,bench_location_options, code_start,a_small_names):

def dic(target_code, target_location_add_info,benchmark_code_info,  bench_location_add_info ):
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

    df = pickle.load(open(path_in_ngrams + "map_dict.p", "rb"))

    df['text'] = df['target_small_name'] + '<br>Location ' + (df.index).astype(str) + \
                 '<br>Number of Reviewers ' + (df['Number of Reviewers']).astype(str) + \
                 '<br>Average Rating ' + (df['Female']).astype(str)

    df["Rate"] = df["Female"] ** 5

    limits = [(0, 2), (3, 10), (11, 20), (21, 50), (50, 3000)]

    colors = ["rgb(0,116,217)", "rgb(255,65,54)", "rgb(133,20,75)", "rgb(255,133,27)", "lightgrey", "purple", "green","magenta","lime"]
    cities = []
    scale = 8

    ra = -1
    for i in list(df["target_small_name"].unique()):
        ra = ra + 1
        df_sub = df[df["target_small_name"] == i].reset_index(drop=True)
        city = dict(
            type='scattergeo',
            locationmode='USA-states',
            lon=df_sub['lon'],
            lat=df_sub['lat'],
            text=df_sub['text'],
            marker=dict(
                size=df_sub['Rate'] / scale,
                color=colors[ra],
                line={'width':'0.5', 'color':'rgb(40,40,40)'},
                sizemode='area'
            ),
            name='{}'.format(i))
        cities.append(city)

    layout = dict(
        title='Competitive Map<br>(Size Indicates Rating)',
        showlegend=True,
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showland=True,
            landcolor='rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"
        ),
    )

    fig = dict(data=cities, layout=layout)


    path_in_ngrams = os.path.join(my_path, "data/cpickle/")
    map_df = pickle.load(open(path_in_ngrams + "map_dict.p", "rb"))



    map_layout =   html.Div([
                    html.Br([]),

                        html.Div(
                            [dcc.Graph(figure = fig,
                            id='map_fig',
                            config={'displayModeBar': False}),

                              ],style={'margin-top':'-0.90cm','padding-top':'0.0cm','height':'80%'}),
                    html.Div([
                        dt.DataTable(
                            rows=map_df.to_dict('records'),
                            row_selectable=True,
                            filterable=True,
                            sortable=True,
                            # optional - sets the order of columns
                            #selected_row_indices=[0],
                            id='map_table',
                            min_height='440px'
                        ),
                    ],style={'margin-top':'-2cm','height':'440px','padding-bottom':'1cm'}),

    ])

    d = {}
    d["map_layout"] = map_layout

    return d





