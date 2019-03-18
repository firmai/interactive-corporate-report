import layout.donuts_interview as di
import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html
import _pickle as pickle
import os
my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")
import layout.location_distance as ld
import dash_table_experiments as dt

#import plotly.plotly as py
#from plotly.graph_objs import *

import numpy as np

import plotly.plotly as py
from plotly.graph_objs import *

def dic(bench_short_name, options_value_target_location_small_dd, option_value_bench_code_dd,
                 option_value_location_dd, options_target_locations,options_bench_code,options_bench_locations,
                 target_code, all_target_location_small_names, target_short_name, target_location_file_name):

    import pandas as pd


    import _pickle as pickle
    import pandas as pd


    RECORDS = [
        {'Input': '', 'Output': ''}
        for i in range(10)
    ]

    input_fields = pd.read_csv("input_fields.csv")
    codes = input_fields["code_or_ticker"]


    agg = pickle.load(open(path_in_ngrams + "figures_dict_agg.p", "rb"))

    fig_d_n=agg[target_code]

    fig_b_n=agg[option_value_bench_code_dd]

    to = -1
    for target_coder in codes:
        to = to + 1
        fig_d_n = agg[target_coder]

        lat = pd.DataFrame.from_dict(fig_d_n, orient="index")
        lat.columns = [target_coder]
        if to == 0:
            gr = lat
        else:
            gr = pd.concat((gr, lat), axis=1)
    gr["Bench"] = gr.mean(axis=1)

    # Local



    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_"+target_code+".p", "rb"))

    fig_d = figures_dict[target_code, target_location_file_name]


    figures_dict_b = pickle.load(open(path_in_ngrams + "figures_dict_"+option_value_bench_code_dd+".p", "rb"))

    closest = ld.dic(target_code, option_value_bench_code_dd, target_location_file_name)

    fig_b = figures_dict_b[option_value_bench_code_dd,closest["name"]]


    big_small = pd.read_csv("big_small_add.csv")

    # add your google maps api key here
    my_google_maps_api_key = 'xxxxxxx'


    import googlemaps
    def route(address_start, address_end, zoom=3, endpt_size=6):
        # start = (supercharger_locations[address_start]['latitude'], supercharger_locations[address_start]['longitude'])
        # end = (supercharger_locations[address_end]['latitude'], supercharger_locations[address_end]['longitude'])

        start = (address_start["latitude"], address_start["longitude"])
        end = (address_end["latitude"], address_end["longitude"])

        directions = gmaps.directions(start, end)
        steps = []
        steps.append(start)  # add starting coordinate to trip

        for index in range(len(directions[0]['legs'][0]['steps'])):
            start_coords = directions[0]['legs'][0]['steps'][index]['start_location']
            steps.append((start_coords['lat'], start_coords['lng']))

            if index == len(directions[0]['legs'][0]['steps']) - 1:
                end_coords = directions[0]['legs'][0]['steps'][index]['end_location']
                steps.append((end_coords['lat'], end_coords['lng']))

        steps.append(end)  # add ending coordinate to trip

        mapbox_access_token = "xxxxxxxxxxxx"

        data = Data([
            Scattermapbox(
                lat=[item_x[0] for item_x in steps],
                lon=[item_y[1] for item_y in steps],
                mode='markers+lines',
                marker=Marker(
                    size=[endpt_size] + [4 for j in range(len(steps) - 2)] + [endpt_size]
                ),
            )
        ])
        layout = Layout(
            autosize=True,
            hovermode='closest',
            margin=dict(
                t=0,
                b=0,
                r=0,
                l=0
            ),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                style='streets',
                center=dict(
                    lat=np.mean([float(step[0]) for step in steps]),
                    lon=np.mean([float(step[1]) for step in steps]),
                ),
                pitch=0,
                zoom=zoom
            ),
        )

        fig = dict(data=data, layout=layout)
        return fig

    server_key = my_google_maps_api_key
    gmaps = googlemaps.Client(key=server_key)


    targo = target_location_file_name

    #bencho = "applebees-neighborhood-grill-and-bar-minneapolis-30"

    address_start = {}
    address_end = {}
    address_start["latitude"] = \
    big_small[big_small["All Target Location File Names"] == targo].reset_index(drop=True)["lat"].values[0]
    address_start["longitude"] = \
    big_small[big_small["All Target Location File Names"] == targo].reset_index(drop=True)["lon"].values[0]
    address_end["latitude"] = closest["lat"]
    address_end["longitude"] = closest["lon"]

    zoom = 12.2
    endpt_size = 20

    fig_map = route(address_start, address_end, zoom=10, endpt_size=20)



    for k in ["Number of Reviewers", "Total Network","First Visit","Connoisseur","Food Aestheticist"]:
        if fig_d_n[k] > fig_b_n[k]:
            fig_d_n[k,"color"] = '#5380ba'
            fig_b_n[k,"color"] = '#65201F'
        else:
            fig_d_n[k,"color"] = '#65201F'
            fig_b_n[k,"color"] = '#5380ba'

        if fig_d[k] > fig_b[k]:
            fig_d[k,"color"] = '#5380ba'
            fig_b[k,"color"] = '#65201F'

        else:
            fig_d[k,"color"] = '#65201F'
            fig_b[k,"color"] = '#5380ba'

    info_layout = html.Div([


        html.Div([

            html.Div([
                html.Br([]),
                html.Br([]),
                #html.Hr(style={'padding-top': '0.15cm', 'padding-bottom': '0.0cm', 'margin-top': '-0.2cm'}),


            ]),

            html.Div([

                html.Div([
                    html.Hr(style={'padding-top': '0.15cm', 'padding-bottom': '0.0cm', 'margin-top': '-0.0cm'}),

                ], ),

            ]),

            html.Div([




                html.Div([

                    html.H5("Description",style={'font-size': '20px'}),
                    html.Div([

                        html.Div([
                            html.Br([]),
                            html.Br([]),
                            html.H5("Reviewers", id='info_1', title="All Reviewers",
                                    style={'margin-top': '8px', 'font-size': '16px', 'color': 'gray'}),
                            html.H5("Network", style={'font-size': '16px', 'color': 'gray'},title="Network of Friends."),
                            html.H5("Average", style={'font-size': '16px', 'color': 'gray'}, title="Average Customer Rating"),
                            html.H5("Connoisseur", style={'font-size': '16px', 'color': 'gray'}, title="Rating of Sophisticated Customers"),
                            html.H5("Aestheticist", style={'font-size': '16px', 'color': 'gray'}, title="Rating of customers who takes alot of photos.")

                        ])

                    ], ),
                ], style={'display': 'table-cell', 'width': '145px'}),

                html.Div([

                    html.H5("Local",style={'font-size': '20px'}),
                    html.Div([

                        html.Div([
                            html.H5(target_code, style={'color': 'gray','font-size': '20px'}),

                            html.H5("{:,}".format(fig_d["Number of Reviewers"]), id='info_1',
                                    style={'font-size': '16px', 'color': fig_d["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5("{:,}".format(fig_d["Total Network"]), id='info_1',
                                    style={'font-size': '16px', 'color': fig_d["Total Network", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_d["First Visit"], 2)),
                                    style={'font-size': '16px', 'color': fig_d["First Visit", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_d["Connoisseur"], 2)),
                                    style={'font-size': '16px', 'color': fig_d["Connoisseur", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_d["Food Aestheticist"], 2)),
                                    style={'font-size': '16px', 'color': fig_d["Food Aestheticist", "color"],
                                           "font-weight": "bold"})

                        ], style={'display': 'table-cell', 'width': '145px'}),

                        html.Div([
                            html.H5(bench_short_name, style={'color': 'gray','font-size': '20px'}),
                            html.H5("{:,}".format(fig_b["Number of Reviewers"]), id='info_1',
                                    style={'font-size': '16px', 'color': fig_b["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5("{:,}".format(fig_b["Total Network"]), id='info_1',
                                    style={'font-size': '16px', 'color': fig_b["Total Network", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_b["First Visit"], 2)),
                                    style={'font-size': '16px', 'color': fig_b["First Visit", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_b["Connoisseur"], 2)),
                                    style={'font-size': '16px', 'color': fig_b["Connoisseur", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_b["Food Aestheticist"], 2)),
                                    style={'font-size': '16px', 'color': fig_b["Food Aestheticist", "color"],
                                           "font-weight": "bold"})

                        ], style={'display': 'table-cell'}),

                    ], style={'display': 'table'}),
                ], style={'display': 'table-cell', 'width': '160px'}),

                html.Div([

                    html.H5(""),
                    html.Div([

                        html.Div([
                            html.H5(""),

                        ], style={'display': 'table-cell', 'width': '145px'}),

                        html.Div([

                        ], style={'display': 'table-cell'}),

                    ], style={'display': 'table'}),
                ], style={'display': 'table-cell', 'width': '40px'}),

                html.Div([

                    html.H5("National",style={'font-size': '20px'}),
                    html.Div([

                        html.Div([
                            html.H5(target_code, style={'color': 'gray','font-size': '20px'}),
                            html.H5("{:,}".format(int(fig_d_n["Number of Reviewers"])), id='info_1',
                                    style={'font-size': '16px', 'color': fig_d_n["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5("{:,}".format(int(fig_d_n["Total Network"])), id='info_1',
                                    style={'font-size': '16px', 'color': fig_d_n["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_d_n["First Visit"], 2)),
                                    style={'font-size': '16px', 'color': fig_d_n["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_d_n["Connoisseur"], 2)),
                                    style={'font-size': '16px', 'color': fig_d_n["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_d_n["Food Aestheticist"], 2)),
                                    style={'font-size': '16px', 'color': fig_d_n["Food Aestheticist", "color"],
                                           "font-weight": "bold"})

                        ], style={'display': 'table-cell', 'width': '110px'}),

                        html.Div([
                            html.H5(bench_short_name, style={'color': 'gray','font-size': '20px'}),
                            html.H5("{:,}".format(int(fig_b_n["Number of Reviewers"])), id='info_1',
                                    style={'font-size': '16px', 'color': fig_b_n["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5("{:,}".format(int(fig_b_n["Total Network"])), id='info_1',
                                    style={'font-size': '16px', 'color': fig_b_n["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_b_n["First Visit"], 2)),
                                    style={'font-size': '16px', 'color': fig_b_n["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_b_n["Connoisseur"], 2)),
                                    style={'font-size': '16px', 'color': fig_b_n["Number of Reviewers", "color"],"font-weight": "bold"}),
                            html.H5(str(round(fig_b_n["Food Aestheticist"], 2)),
                                    style={'font-size': '16px', 'color': fig_b_n["Food Aestheticist", "color"],
                                           "font-weight": "bold"})

                        ], style={'display': 'table-cell', 'width': '120px'}),

                        html.Div([
                            html.H5("Bench", style={'color': 'gray', 'font-size': '20px'}),
                            html.H5("{:,}".format(int(gr["Bench"]["Number of Reviewers"])), id='info_1',
                                    style={'font-size': '16px', 'color': "rgb(192,192,192)",
                                           "font-weight": "bold"}),
                            html.H5("{:,}".format(int(gr["Bench"]["Total Network"])), id='info_1',
                                    style={'font-size': '16px', 'color': "rgb(192,192,192)",
                                           "font-weight": "bold"}),
                            html.H5(str(round(gr["Bench"]["First Visit"], 2)),
                                    style={'font-size': '16px', 'color': "rgb(192,192,192)",
                                           "font-weight": "bold"}),
                            html.H5(str(round(gr["Bench"]["Connoisseur"], 2)),
                                    style={'font-size': '16px', 'color': "rgb(192,192,192)",
                                           "font-weight": "bold"}),
                            html.H5(str(round(gr["Bench"]["Food Aestheticist"], 2)),
                                    style={'font-size': '16px', 'color': "rgb(192,192,192)",
                                           "font-weight": "bold"})

                        ], style={'display': 'table-cell', 'width': '120px'}),

                    ], style={'display': 'table'}),
                ], style={'display': 'table-cell'}),

                html.Div([
                ], style={'display': 'table-cell'}),


            ], style={'display': 'table', 'margin-top': '-1cm'})

        ], style={'margin-top': '0.5cm','margin-bottom': '0.5cm'}),

        dcc.Graph(figure=fig_map,
                  id='gif_map', style={'border': '0', 'width': "100%", 'height': "100"},
                  config={'displayModeBar': False}
                  ),


        html.Div([

            dcc.Tabs(
                tabs=[{'label': "All " + target_code+" Locations", 'value': "Company"},
                      {'label': "All " + option_value_bench_code_dd+" Locations", 'value': "Bench"},
                      {'label': "Surrounding Locations", 'value': "Area"},
                      ],
                value="Company",
                id='tabs-areas'
            ),
        ], style={
            'width': '100%',
            'height': '10%',
            'fontFamily': 'Sans-Serif',
            'margin-left': 'auto',
            'margin-top': '0.4cm',
            'margin-bottom': '-0.5cm',
            'margin-right': 'auto'
        }),

        html.Div([
        dt.DataTable(
            rows=[{}],
            row_selectable=True,
            filterable=True,
            sortable=True,
            # optional - sets the order of columns
            selected_row_indices=[0],
            id='datatable'),

                ],style={'margin-top': '0.5cm','height':'550px'}),

        html.Div([

            html.Div([
                html.Hr(style={'padding-top': '0.26cm', 'padding-bottom': '0.0cm', 'margin-top': '-0.0cm'}),
                html.H5(
                    (
                    "Try using Filter -> and try, >, <, >=, <=, =, 0-x, etc. Use multiple filters for trend spotting, For example filter, female >3 and male <2.8").title(),
                    style={'font-size': '14px', 'margin-top': '-1.1cm'}),
                html.Hr(style={'padding-top': '0.15cm', 'padding-bottom': '0.26cm', 'margin-top': '-0.0cm'})
            ], ),

        ]),

    ])

    d = {}
    d["info_layout"] = info_layout

    return d





