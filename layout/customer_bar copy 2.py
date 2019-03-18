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
import pandas as pd

import layout.location_distance as ld

print('hidden_output', 'children')

my_path = os.path.abspath(os.path.dirname('__file__'))

path = os.path.join(my_path, "data/cpickle/")

ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))

input_fields = pd.read_csv("input_fields.csv")


target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

bench_code_dd = input_fields[input_fields["starting"] == 2]["code_or_ticker"].reset_index(drop=True)[0]

target_short_name = target_short_name = input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

temp_df = pd.DataFrame()
temp_df["All Target Location Small Names"] = ext_info_dict[target_code]["All Target Location Small Names"]


target_location_small_dd = temp_df["All Target Location Small Names"][0]


bench_code_dd_ad_df = pd.DataFrame()

all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
all_target_location_full_addresses_b = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
bench_code_dd_ad_df["all_target_location_file_names_b"] = all_target_location_file_names_b
bench_code_dd_ad_df["all_target_location_small_names_b"] = all_target_location_small_names_b
bench_code_dd_ad_df["all_target_location_full_addresses_b"] = all_target_location_full_addresses_b


all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
options_target_locations = [{'label': r, 'value': i} for r, i in
                            zip(all_target_location_full_addresses, all_target_location_small_names)]

all_benchmark_codes = ext_info_dict[target_code]["All Benchmark Codes"]
all_benchmark_small_names = ext_info_dict[target_code]["All Benchmark Small Names"]
options_bench_code = [{'label': r, 'value': i} for r, i in zip(all_benchmark_small_names, all_benchmark_codes)]

all_target_location_full_addresses_b = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
options_bench_locations = [{'label': r, 'value': i} for r, i in
                           zip(all_target_location_full_addresses_b, all_target_location_small_names_b)]

all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]
all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]

# coy = target_code
# city = target_location_small_dd
# bench_code_dd = bench_code_dd


print("This seems to be working here")

comp_ad_df = pd.DataFrame()
comp_ad_df["all_target_location_file_names"] = all_target_location_file_names
comp_ad_df["all_target_location_small_names"] = all_target_location_small_names
comp_ad_df["all_target_location_full_addresses"] = all_target_location_full_addresses

print(comp_ad_df["all_target_location_small_names"])

target_location_file_name = comp_ad_df[comp_ad_df["all_target_location_small_names"] == target_location_small_dd][
    "all_target_location_file_names"].reset_index(drop=True)[0]

closest = ld.dict(target_code, bench_code_dd, target_location_file_name)

option_value_bench_location_dd = \
bench_code_dd_ad_df[bench_code_dd_ad_df["all_target_location_file_names_b"] == closest["name"]][
    "all_target_location_small_names_b"].reset_index(drop=True)[0]

all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]

new_dict = {}
new_dict["all_target_location_file_names_b"] = all_target_location_file_names_b
new_dict["all_target_location_small_names_b"] = all_target_location_small_names_b
new_dict["all_target_location_small_names"] = all_target_location_small_names
new_dict["target_short_name"] = target_short_name
new_dict["target_code"] = target_code
new_dict["bench_code_dd"] = bench_code_dd
new_dict["options_value_target_location_small_dd"] = target_location_small_dd
new_dict["target_location_file_name"] = target_location_file_name
new_dict["option_value_bench_location_dd"] = option_value_bench_location_dd

# new_dict["Company City File"] = comp_ad_df["all_target_location_file_names"].reset_index(drop=True)[0]
# new_dict["Benchmark City File"] = bench_code_dd_ad_df["all_target_location_file_names_b"].reset_index(drop=True)[0]

new_dict["options_target_locations"] = options_target_locations
new_dict["options_bench_code"] = options_bench_code
new_dict["options_bench_locations"] = options_bench_locations

options_value_target_location_small_dd = new_dict["options_value_target_location_small_dd"]

option_value_bench_code_dd = bench_code_dd


closest = ld.dict(target_code, option_value_bench_code_dd, target_location_file_name)

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

    html.Div(id='store_values', style={'display': 'none'}),

    html.Div([
        html.H5(target_short_name),

    ], style={'background-color': "white", 'color': 'grey', 'float': 'left',
              'padding-right': '0.6cm', 'width': '10%'}),

    html.Div([
        dcc.Dropdown(
            id='target_location_info',
            options=options_target_locations,
            value=options_value_target_location_small_dd,
            clearable=False,
            className="dropper"
        )
    ], style={'background-color': "white", 'padding-right': '0.2cm', 'color': 'rgb(217, 224, 236)', 'float': 'left', 'width': '25%'}),

    html.Div([
        html.Button('Set', id='button_versus', n_clicks=0,
                    style={'height': '3.3em', 'float': 'center', 'color': 'rgb(217, 224, 236)'})
    ], style={'width': '15%', 'padding-right': '0.2cm', 'float': 'left', 'font-size':'14'}),

    html.Div([
        dcc.Dropdown(
            id='benchmark_code_info',
            options=options_bench_code,
            value=option_value_bench_code_dd,
            clearable=False,
            className="dropper"
        )
    ], style={'background-color': 'white', 'padding-right': '0.6cm', 'color': 'rgb(217, 224, 236)', 'float': 'left',
              'width': '23%'}),

    html.Div([
        dcc.Dropdown(
            id='bench_location_info',
            options= options_bench_locations,
            value=option_value_bench_location_dd,
            clearable=False,
            className="dropper"
        )
    ], style={'background-color': 'white', 'color': 'rgb(217, 224, 236)', 'float': 'left',
              'width': '25%'})
    # , 'float': 'right', 'display': 'inline-block'
], style={'background-color': 'white', 'clear': 'both', 'padding-top': '0.3cm'},
    className="double_drop")


