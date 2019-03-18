# coding: utf-8
import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from plotly import graph_objs as go
from datetime import datetime as dt
import json
import json
import pandas as pd
import os
from flask import Flask
from six.moves import cPickle as pickle #for performance
from os import listdir
from os.path import isfile, join
import numpy as np


import processing.input as inp

import layout.multiple_charts as mc
import layout.polar_figure as pf
import layout.polar_figure_2 as pf2
import layout.charting_words as cw
import layout.frequency_word_chart as fwc
import layout.glassdoor_chart as gc
import layout.chart_ratings as cr
import layout.language_layout as ll
import layout.compensation_layout as cl
import layout.infograph_layout as inl
import layout.treemap as tm
from processing.stock_narration import describe
import processing.frames as fm
from layout.figures import figs
import layout.donuts_interview as di
import layout.employee_layout as el

### It is important to note that there is no target firm. This is dynamic.

    #To Give Orientation

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv("input_fields.csv")

tick  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]

ticker_start = input_fields[input_fields["starting"]==1]["ticker"].reset_index(drop=True)[0]

bench_start = input_fields[input_fields["starting"]==2]["ticker"].reset_index(drop=True)[0]

location_start = "2231 State Hwy 6, Sugar Land, TX 77478"

small_loc = "Sugar-Land"
###############

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server
# -> This part is important for Heroku deployment
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')


def db_frame(url):
    url = url.replace("dl=0", "dl=1")  # dl=1 is important

    import urllib.request
    u = urllib.request.urlopen(url)
    data = u.read()
    u.close()

    def find_between_r(s, first, last):
        try:
            start = s.rindex(first) + len(first)
            end = s.rindex(last, start)
            return s[start:end]
        except ValueError:
            return ""

    filename = find_between_r(url, "/", "?")

    with open(filename, "wb") as f:
        f.write(data)

    ff = pd.read_excel(filename)
    return ff

#go
s_metrics_df = fm.s_metrics_df
c_metrics_df = fm.c_metrics_df


r = 5
if r>4:
    employee_sentiment = "happy"
else:
    employee_sentiment = "unhappy"

dict = {

    "title":"BJ’s Restaurant & Brewhouse",
    "location":"Jacksonville",
    "employees":"Employees are " + employee_sentiment + "." + "The company then bought 26.",
    "customers":"Customers are happy. The company then bought 26.",
    "shareholders":"Shareholders are happy. The company then bought 26.",
    "management":"Management is performing well. The company then bought 26."

}
#


from datetime import datetime, timedelta

now = datetime.now()

#stock_price_desc = describe


def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table

##
#df_perf_summary = pd.read_csv("17530.csv")

df_perf_summary = fm.fin_met(ticker_start,bench_start)

modifed_perf_table = make_dash_table(df_perf_summary)

modifed_perf_table.insert(
    0, html.Tr([
        html.Td([]),
        html.Td(['Company'], colSpan=4, style={'text-align': "center"}),
        html.Td(['Benchmark'], colSpan=4, style={'text-align': "center"})
    ], style={'background': 'white', 'font-weight': '600'}
    )
)

# Function To Import Dictionary and Open IT.
def load_dict(filename_):
    with open(filename_, 'rb') as f:
        ret_di = pd.read_pickle(f)
    return ret_di

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "data/financial/")

# And the specification of this table
dict_frames = load_dict(path + 'data.pkl') # Much rather use this one


df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544.csv')
df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542.csv')
df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540.csv')
df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538.csv')

##### Addition One

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "data/yelp/" + ticker_start + "/")

path_out = os.path.join(my_path, "data/ratings/")

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

path_in_ngrams = os.path.join(my_path, "data/cpickle/")

figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_"+ticker_start+".p", "rb"))

new_list = []
for of in onlyfiles:
    address = figures_dict[ticker_start, of[:-4]]["Response Data"]["location"]["display_address"]
    ak = ""
    for a in address:
        if ak == "":
            ak = ak + a
        else:
            ak = ak + ", " + a
    new_list.append(ak)

rat = ""
for li in onlyfiles:
    rat = rat + li + "-"

from collections import Counter
import re

coun = Counter(rat.split("-"))

ad = pd.DataFrame()

ad["word"] = list(coun.keys())
ad["number"] = list(coun.values())

ad = ad.sort_values("number", ascending=False)

ad = ad[~(np.abs(ad.number - ad.number.mean()) <= (3.2 * ad.number.std()))]

ad.reset_index(inplace=True, drop=True)
ad["word_1"] = "-" + ad["word"] + "-"
ad["word_2"] = ad["word"] + "-"
ad["word_3"] = "-" + ad["word"]

ad["final"] = ad["word_1"]

words = list(ad["final"].append(ad["word_2"]).append(ad["word_3"]).values)

full_names = []
small_names = []
a_small_names = []
for i in range(len(onlyfiles)):
    my_string = onlyfiles[i]
    full_names.append(my_string)
    li = my_string
    if len(li) > 4:
        li = re.sub(r'|'.join(map(re.escape, list(words))), '', li)
        small_names.append(li[:-4])

        ga  = li[:-4].title()
        a_small_names.append(ga)

codes_df = pd.DataFrame()
codes_df["file"]=onlyfiles
codes_df["address"] = new_list
codes_df["small"] = a_small_names
#print(codes_df[codes_df["small"]=="Glendale"]["address"].reset_index(drop=True)[0])

available_locations = new_list

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "input_fields.csv")

input_fields = pd.read_csv(path)
input_fields = pd.read_csv(path)


start_ticker = input_fields[input_fields["starting"]==1]["ticker"].reset_index(drop=True)[0]

available_benchmarks = list(input_fields["code_or_ticker"].values)

available_benchmarks.remove(start_ticker)

available_benchmarks = list(input_fields[input_fields["code_or_ticker"].isin(available_benchmarks)]["short_name"].values)

tickers_loca = {}
tickers_loca["All"] = ticker_start
for i in available_locations:
    tickers_loca[i] = ticker_start

tickers = list(input_fields[input_fields["short_name"].isin(available_benchmarks)]["ticker"].values)

tickers_bench = {}
for i, t in zip(available_benchmarks, tickers):
    tickers_bench[i] = t

###

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.config['suppress_callback_exceptions']=True
# Describe the layout, or the UI, of the app
app.layout = html.Div([

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate-value', style={'display': 'none'}),

    html.Div([  # page 1

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 1

            # Row 1 (Header)

            html.Div([

                html.Div([
                    #html.H5(
                    ##
                    #    dict["title"] + " 4-D Report lo"),
                    html.H5(id='title'),

                    html.H6(id='location',
                            style={'color': '#7F90AC'}),
                    html.Div([


                        html.Div([
                            dcc.Dropdown(
                                id='locas',
                                options=[{'label': r, 'value': i} for r,i in zip(available_locations,codes_df[codes_df["address"].isin(available_locations)]["small"])],
                                value="All",
                                clearable=False,
                                className="dropper",
                                placeholder="Type Location",


                            )
                        ], style={'background-color':'#a9a9a9','color':'rgb(217, 224, 236)','float':'left', 'padding-right': '0cm', 'width': '20%'}),

                        html.Div([
                            html.Button('SWAP', id='button_swap', n_clicks=0, style={'height': '3.3em', 'float': 'center', 'color':'rgb(217, 224, 236)'})
                        ], style={'padding-left': '0.8cm', 'padding-right': '0.8cm','float':'left'}),

                        html.Div([
                            dcc.Dropdown(
                                id='benchy',
                                options=[{'label': r, 'value': i} for r, i in tickers_bench.items()],
                                #value=bench_start,
                                clearable=False,
                                className="dropper",
                                placeholder="Select Benchmark"

                            )
                        ], style={'background-color':'#a9a9a9','color':'rgb(217, 224, 236)','width': '80%','float':'left','width': '20%'}),
                        html.Div([html.H3('3.6/5')],style={'padding-left': '1.2cm','float':'left'})
                        # , 'float': 'right', 'display': 'inline-block'
                    ], style={'padding-top': '0.3cm', 'padding-left': '0cm'},
                        className="double_drop"),

                ], className="nine columns padded"),

                html.Div([
                    html.H1(
                        [html.Span(str(now.month), style={'opacity': '0.5'}), html.Span(str(now.year)[2:])]),
                    html.H6('Monthly Interactive Update')
                ], className="three columns gs-header gs-accent-header padded", style={'float': 'right'}),

            ], className="row gs-header gs-text-header"),


            html.Br([]),

            html.Div([

                    html.Div([html.H6(["Executive Summary"], style={"float":"left","padding-right":"0.2cm"}),
                    html.A("info", href='http://4d.readthedocs.io/en/latest/text/executive_summary.html#executive-summary', target="_blank")
                        ],className="gs-header gs-table-header padded"),

                      html.P(inp.exec, style={"padding-top":"1mm"})]),


            # Row 2

            html.Div([

                html.Div([

                    html.H6(id="profile",className="gs-header gs-text-header padded"),

                    html.Strong("Employees pg 4"),
                    html.P(dict["employees"],
                           className='blue-text'),

                    html.Strong(
                        'Customers pg 6'),
                    html.P(dict["customers"],
                           className='blue-text'),

                    html.Strong('Shareholders pg 8'),
                    html.P(dict["shareholders"],
                           className='blue-text'),

                    html.Strong('Management pg 10'),
                    html.P(dict["management"],
                           className='blue-text'),

                ], className="four columns"),

                html.Div([
                    html.H6(["Shareholder Performance"],
                            className="gs-header gs-table-header padded"),
                    #html.Iframe(src="https://plot.ly/~snowde/36.embed?modebar=false&link=false&autosize=true", \
                    #            seamless="seamless", style={'border': '0', 'width': "100%", 'height': "250"}),

                dcc.Graph(
                    id='stock_plot',style={'border': '0', 'width': "100%", 'height': "250"},
                    config={'displayModeBar': False}
                )
                ], className="eight columns"),
            ], className="row "),

            # Row 2.5, s

            html.Div([

                html.Div([


                    html.H6('Stakeholder Metrics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(s_metrics_df), style={'marginBottom': 5},
                               className='tiny-header'),
                    html.P("E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average", style={'font-size': '60%', 'marginTop': 5}),
                    html.H6('Company Metrics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(c_metrics_df), style={'marginBottom': 5},
                               className='tiny-header'),
                ], className="four columns"),



                html.Div([
                    html.P(id='stock_plot_desc', style={"padding-top":"1.2mm"}),
                ], className="eight columns"),
                html.Div([

                    html.H6("Financial Performance",
                            className="gs-header gs-table-header padded"),
                    html.Table(modifed_perf_table,id="mgmt_perf", className="reversed")
                ], className="eight columns"),

            ], className="row "),

            # Row 3#


        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 2

                # Row 1 (Header)

                html.Div([
                    html.H6(["Executive Advice"],
                            className="gs-header gs-table-header padded"),

                        ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 1

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 1

                # Row 1 (Header)

                html.Br([]),

                html.Div([html.H6(["Trend Analysis"],
                                className="gs-header gs-table-header padded"),
                          html.P(inp.exec, style={"padding-top":"1mm"}),

                            html.Div([
                                dcc.Tabs(
                                    tabs=[{'label':"Overall" , 'value':"Overall" },
                                          {'label':"Employee" , 'value':"Employee" },
                                          {'label':"Management" , 'value':"Management" },
                                          {'label':"Shareholders" , 'value':"Shareholders" },
                                          {'label':"Customers" , 'value':"Customers" },
                                          {'label':"Search" , 'value':"Search" },
                                    ],
                                    value="Overall",
                                    id='tabs'
                                ),
                                html.Div(id='tab-output')
                            ], style={
                                'width': '100%',
                                'fontFamily': 'Sans-Serif',
                                'margin-left': 'auto',
                                'margin-right': 'auto'
                            })

                         ]),

                # Row 2
                # Row 2.5, s

                html.Div([

                    html.Div([


                        html.H6('Stakeholder Metrics',
                                className="gs-header gs-text-header padded"),
                        html.Table(make_dash_table(s_metrics_df), style={'marginBottom': 5},
                                   className='tiny-header'),
                        html.P("E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average", style={'font-size': '60%', 'marginTop': 5}),
                        html.H6('Financial Metrics',
                                className="gs-header gs-text-header padded"),
                        html.Table(make_dash_table(c_metrics_df), style={'marginBottom': 5},
                                   className='tiny-header'),
                    ], className="four columns"),


                    html.Div([

                        html.H6("Management Performance",
                                className="gs-header gs-table-header padded"),
                        html.Table(modifed_perf_table,id="mgmt_perf", className="reversed")
                    ], className="eight columns"),

                ], className="row "),

                # Row 3#


        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

                html.A(['Print PDF'],
                       className="button no-print",
                       style={'position': "absolute", 'top': '-40', 'right': '0'}),

                html.Div([  # subpage 2

                    # Row 1 (Header)

                    html.Div([
                        html.H6(["Sensitivity and Valuation Analysis"],
                                className="gs-header gs-table-header padded"),

                            ]),

        ], className="subpage"),

    ], className="page"),


    html.Div([  # page 3

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                    html.H6(["Competitor Analysis"],
                            className="gs-header gs-table-header padded") ]),

            dcc.Graph(figure=pf.figs_polar(ticker_start,"bench", ticker_start), config={'displayModeBar': False}, id='comp_plot',style={'border': '0', 'width': "100%", 'height': "250"}),


        ], className="subpage"),

            # Row 2

            html.Div(html.P(inp.exec, style={"padding-top":"1mm"}))

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Employee Analysis"],
                        className="gs-header gs-table-header padded")]),

            html.Br([]),

            html.Div([
                dcc.Tabs(
                    tabs=[{'label':"Interview" , 'value':"Interview" },
                          {'label':"Sentiment" , 'value':"Sentiment" },
                          {'label':"Compensation" , 'value':"Compensation" },
                          {'label':"Jobs Map" , 'value':"Jobs Map" },
                          {'label':"Search" , 'value':"Search" },
                    ],
                    value="Interview",
                    id='tabs-employee'
                ),
                html.Div(id='tab-output-employee'),

                    ], style={
                        'width': '100%',
                        'fontFamily': 'Sans-Serif',
                        'margin-left': 'auto',
                        'margin-right': 'auto'
                    }),


        ], className="subpage"),

    ], className="page"),

html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Customer Analysis"],
                        className="gs-header gs-table-header padded")]),

            html.Br([]),

            html.Div([
                dcc.Tabs(
                    tabs=[{'label':"Infographic" , 'value':"Infographic" },
                          {'label':"Map" , 'value':"Map" },
                          {'label':"Sentiment" , 'value':"Sentiment" },
                    ],
                    value="Infographic",
                    id='tabs-customer'
                ),
                html.Div(id='tab-output-customer'),

                    ], style={
                        'width': '100%',
                        'fontFamily': 'Sans-Serif',
                        'margin-left': 'auto',
                        'margin-right': 'auto'
                    }),


        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Shareholder Analysis"],
                        className="gs-header gs-table-header padded"),

                    ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Management Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Dimensional Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Appendix Analysis"],
                        className="gs-header gs-table-header padded"),

            ]),

        ], className="subpage"),

    ], className="page"),

    html.Div([  # page 3

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([

                # Data tables on this page:
                # ---
                # df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')
                # df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')
                # df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')
                # df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')

                # Column 1

                html.Div([
                    html.H6('Financial Information',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(df_fund_info), id="table1"),

                    html.H6('Fund Characteristics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(df_fund_characteristics)),

                    html.H6('Fund Facts',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(df_fund_facts)),

                ], className="four columns"),

                # Column 2##

                html.Div([
                    html.H6('Sector Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17560.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                    html.H6('Country Bond Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Table(make_dash_table(df_bond_allocation)),

                ], className="four columns"),

                # Column 3

                html.Div([
                    html.H6('Top 10 Currency Weights (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17555.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                    html.H6('Credit Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17557.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                ], className="four columns"),

            ], className="row"),

        ], className="subpage"),

    ], className="page"),
####
    html.Div([  # page 2

            html.A(['Print PDF'],
                   className="button no-print",
                   style={'position': "absolute", 'top': '-40', 'right': '0'}),

            html.Div([  # subpage 2

                # Row 1 (Header)

                html.Div([
                        html.H6(["Company Financials"],
                                className="gs-header gs-table-header padded")]),

                mc.layout,

                # Row ##

                html.Div([html.P(inp.exec, style={"padding-top":"1mm"}),

                          html.Div([dcc.Graph(
                              id='first_tree',
                              config={'displayModeBar': False},
                              style={'autosize': 'False', 'margin-top': '-100px', 'padding-right': '4cm', 'border': '0',
                                     'width': "20%", 'height': "20%"})

                          ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                                    'padding-right': '4cm', 'width': "20%", 'height': "20%"}),

                          html.Div([dcc.Graph(
                              id='third_tree',
                              config={'displayModeBar': False},
                              style={'autosize': 'False', 'margin-top': '-100px', 'padding-top': '0cm',
                                     'padding-left': '4cm', 'border': '0', 'width': "20%", 'height': "20%"})

                          ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                                    'padding-right': '0cm', 'width': "20%", 'height': "20%"}),
                          ],style={'z-index':'3'}),


        ], className="subpage" ),

    ],className="page")

])

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'https://cdn.rawgit.com/chriddyp/ca0d8f02a1659981a0ea7f013a378bbd/raw/e79f3f789517deec58f41251f7dbb6bee72c44ab/plotly_ga.js'
    })

#'https://codepen.io/chriddyp/pen/bWLwgP.css',##
# If you upload css you have to reapload it after github to git raw.
# fuckit i JUST STORED IT IN KERAS
#https://github.com/snowde/keras/blob/master/just.css

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                #"https://www.dropbox.com/s/7zx0pqn3eqql7b1/this.css?dl=1"
                "https://cdn.rawgit.com/snowde/keras/c59812f7/just.css",
                #"https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]

for css in external_css:
    app.css.append_css({"external_url": css})

external_js = [
               "https://code.jquery.com/jquery-3.2.1.min.js",
               "https://cdn.rawgit.com/snowde/keras/2b7d6742/new_java.js",
               "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js",
                ]

for js in external_js:
    app.scripts.append_script({"external_url": js})


#
# Call Backs


@app.callback(Output('intermediate-value', 'children'), [Input('dropdown', 'value')])
def clean_data(value):
     # some expensive clean data step
     cleaned_df = your_expensive_clean_or_compute_step(value)

     # more generally, this line would be
     # json.dumps(cleaned_df)
     return cleaned_df.to_json(date_format='iso', orient='split')



@app.callback(
    dash.dependencies.Output('stock_plot', 'figure'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_fig(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        if not all((the_benchmark, the_location)):
            the_benchmark = bench_start
            the_location = location_start
            fig = figs(ticker_start,bench_start,the_location, the_benchmark, False)
            print(ticker_start, bench_start, the_location, the_benchmark)
        else:
            print(ticker_start, bench_start, the_location, the_benchmark)
            fig = figs(ticker_start, bench_start, the_location, the_benchmark, False)
    else:
        fig = figs(ticker_start,bench_start,the_benchmark, the_location, True)
    return fig


@app.callback(
    dash.dependencies.Output('stock_plot_desc', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_desc(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        if not all((the_benchmark,the_location)):
            the_benchmark = bench_start
            the_location = location_start
            desc = describe(ticker_start,bench_start,the_location, the_benchmark, False)
        else:
            desc = describe(ticker_start,bench_start,the_location, the_benchmark, False)
    else:
        desc = describe(ticker_start,bench_start, the_location,the_benchmark, True)
    return desc


@app.callback(
    dash.dependencies.Output('title', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_title(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        title = dict["title"] + " 4-D Reports"
    else:
        title = str(the_benchmark) + " 4-D Report"
    return title


@app.callback(
    dash.dependencies.Output('location', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_title(the_location, the_benchmark, clicks):

    if clicks % 2 == 0:
        if not all((the_location)):
            the_benchmark = bench_start
            the_location = location_start
            #addy = codes_df[codes_df["small"] == the_location]["address"].reset_index(drop=True)[0]
            title = str(the_location) + " Location"
        else:
            addy = codes_df[codes_df["small"] == the_location]["address"].reset_index(drop=True)[0]
            title = str(addy) + " Location"


    else:
        title = str(the_benchmark) + " Location"
    return title

###
@app.callback(
    dash.dependencies.Output('profile', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_title(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        if not all((the_benchmark, the_location)):
            the_benchmark = bench_start
            the_location = location_start
            title = small_loc + " Profile"
        else:
            title = str(the_location) + " Profile"
    else:
        title = str(the_benchmark) + " Profile"
    return title

###
@app.callback(
    dash.dependencies.Output('mgmt_perf', 'children'),
    [dash.dependencies.Input('locas', 'value'),
     dash.dependencies.Input('benchy', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks'),
     ])

def update_table(the_location, the_benchmark, clicks):
    if clicks % 2 == 0:
        if not all((the_benchmark, the_location)):
            the_location = location_start
            the_benchmark = bench_start
            df_perf_summary = fm.fin_met(ticker_start, the_benchmark)
        else:

            df_perf_summary = fm.fin_met(ticker_start, the_benchmark)


    else:
        df_perf_summary = fm.fin_met(tickers_bench[the_benchmark], ticker_start)

    modifed_perf_table = make_dash_table(df_perf_summary)

    modifed_perf_table.insert(
        0, html.Tr([
            html.Td([]),
            html.Td(['Company'], colSpan=4, style={'text-align': "center"}),
            html.Td(['Benchmark'], colSpan=4, style={'text-align': "center"})
        ], style={'background': 'white', 'font-weight': '600'}
        )
    )
    return modifed_perf_table

@app.callback(
    Output('filtered-content', 'children'),
    [Input('category-filter', 'value'),
     Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter( var, req, stu, ben):

    df = dict_frames[ben, req, stu]

    highlight = list(df.drop("year",axis=1).columns.values)

    if stu in ["Normalised", "Original"]:
        highlight = list(df.ix[:, :5].columns.values)

    highlight = highlight + var
    figure = mc.create_figure(highlight,df,req, stu)

    for trace in figure['data']:
        trace['hoverinfo'] = 'text'

    return dcc.Graph(
        id='filtered-graph',
        figure=figure,config={'displayModeBar': False}
    )
###
@app.callback(
    Output('category-filter', 'options'),
    [Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter(req, stu, ben):
    # print(per, req, stu, ben)

    df = dict_frames[ben, req, stu]
    highlight = list(df.drop("year", axis=1).columns.values)

    return [{'label': i, 'value': i} for i in highlight]


@app.callback(
    Output('first_tree', 'figure'),
    [Input('request', 'value'),
     ])
def filter(req):
    df = dict_frames["BJRI", req, "Original"]
    return tm.treemap(df)
###
@app.callback(
    Output('third_tree', 'figure'),
    [Input('request', 'value'),
     ])
def filter(req):
    df = dict_frames[bench_start, req, "Original"]
    return tm.treemap(df)

@app.callback(
    Output('graphed', 'figure'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bencher', 'value')])
def filter2( goo, time, many, norm, bench):
    #print(per, req, stu, ben)

    figure = gc.chart_gd(goo, time, many, norm, bench)

##
    return figure

@app.callback(
    Output('text_sum', 'value'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bencher', 'value')])
def filter2( goo, time, many, norm, bench):
    #print(per, req, stu, ben)

    figure = gc.sum_gd(goo, time, many, norm, bench)
    return figure
###

@app.callback(Output('tab-output', 'children'), [Input('tabs', 'value')])
def display_content(value):

    layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_overall, config={'displayModeBar': False},
                                 style={"margin-top": "0mm"})])
    if value == "Overall":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_overall, config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Employee":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_emp, config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Management":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_mgm, config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Shareholders":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_sha, config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Customers":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_cus, config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Search":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_search, config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])


    return layout


@app.callback(Output('tab-output-employee', 'children'), [Input('tabs-employee', 'value')])
def display_content(value):

    layout = el.interview_layout

    if value== "Interview":
        layout = el.interview_layout
    elif value== "Sentiment":
        layout = ll.language_layout
    elif value== "Compensation":
        layout = cl.compensation_layout
    elif value== "Job Map":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_cus, config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])
    elif value== "Search":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cr.fig_search, config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])


    return layout

## Here

@app.callback(Output('tab-output-customer', 'children'), [Input('tabs-customer', 'value')])
def display_content(value):

    layout = inl.info_layout

    if value== "Infographic":
        layout = inl.info_layout
    elif value== "Map":
        layout = ll.language_layout
    elif value== "Sentiment":
        layout = cl.compensation_layout


    return layout



@app.callback(Output('tab-output-interview-bottom', 'children'), [Input('tabs-interview-bottom', 'value')])
def display_content(value):

    layout = el.interview_layout_accepted

    if value== "Accepted":
        layout = el.interview_layout_accepted
    elif value== "Positive":
        layout = el.interview_layout_positive
    elif value== "Negative":
        layout = el.interview_layout_negative
    elif value== "Difficult":
        layout = el.interview_layout_difficult
    elif value== "Easy":
        layout = el.interview_layout_easy

    return layout

@app.callback(Output('tab-output-language', 'children'), [Input('tabs-language', 'value')])
def display_content(value):

    layout = ll.four_figs_layout

    if value== "Noun":
        layout = ll.four_figs_layout
    elif value== "Phrase":
        layout = ll.phrase_layout
    elif value== "Sentiment":
        layout = el.interview_layout_negative
    elif value== "Map":
        layout = el.interview_layout_easy

    return layout

@app.callback(Output('tab-output-compensation', 'children'), [Input('tabs-compensation', 'value')])
def display_content(value):

    layout = ll.four_figs_layout

    if value== "Benefits":
        layout = cl.benefits_layout
    elif value== "Salaries":
        layout = cl.benefits_layout
    elif value== "Third":
        layout = cl.benefits_layout


    return layout




# Our main function
if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server()