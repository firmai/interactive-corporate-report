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



#def dict(firm_location, benchmark, bench_location, firm_location_options,benchmark_options,bench_location_options, code_start,a_small_names):

def dic(options_value_target_location_small_dd, option_value_bench_code_dd,
                 option_value_location_dd, options_target_locations,options_bench_code,options_bench_locations,
                 target_code, all_target_location_small_names, target_short_name, target_location_file_name):

    import _pickle as pickle
    import pandas as pd

    print(target_location_file_name)
    print(options_target_locations)

    closest = ld.dic(target_code, option_value_bench_code_dd, target_location_file_name)

    agg = pickle.load(open(path_in_ngrams + "figures_dict_agg.p", "rb"))

    fig_d_n=agg[target_code]

    fig_b_n=agg[option_value_bench_code_dd]

    # Local

    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_"+target_code+".p", "rb"))

    fig_d = figures_dict[target_code, target_location_file_name]


    figures_dict_b = pickle.load(open(path_in_ngrams + "figures_dict_"+option_value_bench_code_dd+".p", "rb"))

    fig_b = figures_dict_b[option_value_bench_code_dd,closest["name"]]


    for k in ["Number of Reviewers", "Total Network","Patrons","Connoisseur"]:
        if fig_d_n[k] > fig_b_n[k]:
            fig_d_n[k,"color"] = 'blue'
            fig_b_n[k,"color"] = 'red'
        else:
            fig_d_n[k,"color"] = 'red'
            fig_b_n[k,"color"] = 'blue'

        if fig_d[k] > fig_b[k]:
            fig_d[k,"color"] = 'blue'
            fig_b[k,"color"] = 'red'

        else:
            fig_d[k,"color"] = 'red'
            fig_b[k,"color"] = 'blue'

    info_layout_drop_downs =   html.Div([


        html.Div([
            html.H5(target_short_name),

        ], style={'background-color': "white", 'color': 'grey', 'float': 'left',
                  'padding-right': '0.6cm', 'width': '15%'}),

        html.Div([
            dcc.Dropdown(
                id='target_location_info',
                options=options_target_locations,
                value=options_value_target_location_small_dd,
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': "white", 'padding-right': '0.3cm', 'color': 'rgb(217, 224, 236)', 'float': 'left', 'width': '28%'}),

        html.Div([
            dcc.Dropdown(
                id='benchmark_code_info',
                options=options_bench_code,
                value=option_value_bench_code_dd,
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': 'white', 'padding-right': '0.3cm', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                  'width': '28%'}),

        html.Div([
            dcc.Dropdown(
                id='bench_location_info',
                options= options_bench_locations,
                value=option_value_location_dd,
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': 'white', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                  'width': '28%'})
        # , 'float': 'right', 'display': 'inline-block'
    ], style={'background-color': 'white','z-index':'0', 'clear': 'both', 'padding-top': '0.3cm','padding-bottom': '0.3cm'},
        className="double_drop")

    d = {}
    d["info_layout_drop_downs"] = info_layout_drop_downs


    return d

