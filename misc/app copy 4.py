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
from flask_caching import Cache
import layout.customer_bar as cb

### It is important to note that there is no target firm. This is dynamic.

    #To Give Orientation

# Initialize the Dash app #
app = dash.Dash(__name__)

app.config.suppress_callback_exceptions = True


cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})


server = app.server
# -> This part is important for Heroku deployment
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')


## Loading input fields
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv("input_fields.csv")
from datetime import datetime, timedelta

now = datetime.now()


###############

r = 5
if r > 4:
    employee_sentiment = "happy"
else:
    employee_sentiment = "unhappy"


dict = {

    "title": "BJ’s Restaurant & Brewhouse",
    "location": "Jacksonville",
    "employees": "Employees are " + employee_sentiment + "." + "The company then bought 26.",
    "customers": "Customers are happy. The company then bought 26.",
    "shareholders": "Shareholders are happy. The company then bought 26.",
    "management": "Management is performing well. The company then bought 26."

}
#
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

my_path = os.path.abspath(os.path.dirname('__file__'))

path = os.path.join(my_path, "data/cpickle/")

first_dict = pickle.load(open(path + "first_page.p", "rb"))

figure = pf.figs_polar(first_dict["first_option_target_code"], first_dict["first_option_bench_code"], first_dict["first_option_target_code"])

comp_plot_output = figure

fig = figs(first_dict["first_option_target_code"], first_dict["first_option_bench_code"])

stock_plot_output = fig

df_perf_summary = first_dict["df_perf_summary_output"]


def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


modifed_perf_table = make_dash_table(df_perf_summary)

modifed_perf_table.insert(
    0, html.Tr([
        html.Td([]),
        html.Td(['Company'], colSpan=4, style={'text-align': "center"}),
        html.Td(['Benchmark'], colSpan=4, style={'text-align': "center"})
    ], style={'background': 'white', 'font-weight': '600'}
    )
)
mgmt_perf_output = modifed_perf_table

mgmt_perf_output_1 = modifed_perf_table


#path = os.path.join(my_path, "data/cpickle/")

#ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))

@cache.memoize()
def roll():
    my_path = os.path.abspath(os.path.dirname('__file__'))

    path = os.path.join(my_path, "data/cpickle/")

    ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))
    return ext_info_dict

ext_info_dict = roll()


app.config['suppress_callback_exceptions']=True
# Describe the layout, or the UI, of the app
app.layout = html.Div([

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate_value', style={'display': 'none'}),
    html.Div(id='hidden_output', style={'display': 'none'}),
    html.Div(id='store_values', style={'display': 'none'}),

    html.Div([  # page 1

        html.A(['Print PDF'],
               className="button no-print",
               style={'position': "absolute", 'top': '-40', 'right': '0'}),

        html.Div([  # subpage 1

            # Row 1 (Header)

            html.Div(id='loading', children = [

                html.Div([
                    #html.H5(
                    ##
                    #    dict["title"] + " 4-D Report lo"),
                    html.H5(first_dict["title_output"], id='title'),

                    html.H6(first_dict["location_output"], id='location',
                            style={'color': '#7F90AC'}),
                    html.Div([


                        html.Div([
                            dcc.Dropdown(
                                id='target_location_small_drop_down',
                                options=first_dict["target_location_small_drop_down_options"],
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
                                id='bench_code_drop_down',
                                #value=bench_code,
                                options=first_dict["bench_code_drop_down_options"],
                                clearable=False,
                                className="dropper",
                                placeholder="Select Benchmark"

                            )
                        ], style={'background-color':'#a9a9a9','color':'rgb(217, 224, 236)','width': '80%','float':'left','width': '20%'}),
                        html.Div([html.Img(src='//logo.clearbit.com/spotify.com?size=80&greyscale=true'),

                            html.H3('3.6/5')],style={'padding-left': '1.2cm','float':'left'})
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

                    html.H6(first_dict["profile_output"], id="profile",className="gs-header gs-text-header padded"),

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

                dcc.Graph(figure = stock_plot_output,
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
                    html.Table(make_dash_table(first_dict["s_metrics_df_output"]), id="stakeholder_metrics_dataframe", style={'marginBottom': 5},
                               className='tiny-header'),
                    html.P("E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average", style={'font-size': '60%', 'marginTop': 5}),
                    html.H6('Company Metrics',
                            className="gs-header gs-text-header padded"),
                    html.Table(make_dash_table(first_dict["c_metrics_df_output"]), id="company_metrics_dataframe", style={'marginBottom': 5},
                               className='tiny-header'),
                ], className="four columns"),



                html.Div([
                    html.P(first_dict["stock_plot_desc_output"],id='stock_plot_desc', style={"padding-top":"1.2mm"}),
                ], className="eight columns"),
                html.Div([

                    html.H6("Financial Performance",
                            className="gs-header gs-table-header padded"),
                    html.Table(mgmt_perf_output,id="mgmt_perf", className="reversed")
                ], className="eight columns"),

            ], className="row "),

            # Row 3##


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
                        html.Table( id="stakeholder_metrics_dataframe_1", style={'marginBottom': 5},
                                   className='tiny-header'),
                        html.P("E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average", style={'font-size': '60%', 'marginTop': 5}),
                        html.H6('Financial Metrics',
                                className="gs-header gs-text-header padded"),
                        html.Table(id="company_metrics_dataframe_1", style={'marginBottom': 5},
                                   className='tiny-header'),
                    ], className="four columns"),


                    html.Div([

                        html.H6("Management Performance",
                                className="gs-header gs-table-header padded"),
                        html.Table(id="mgmt_perf_1", className="reversed")
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

            dcc.Graph(config={'displayModeBar': False}, id='comp_plot',style={'border': '0', 'width': "100%", 'height': "250"}),


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

            html.Br([]),

            html.Div([
                html.H6(["Customer Analysis"],
                        className="gs-header gs-table-header padded"),

            html.Div([

                dcc.Tabs(
                    tabs=[{'label':"Infographic" , 'value':"Infographic" },
                          {'label':"Map" , 'value':"Map" },
                          {'label':"Sentiment" , 'value':"Sentiment" },
                    ],
                    value="Infographic",
                    id='tabs-customer'
                ),
                    ], style={
                        'width': '100%',
                        'height': '10%',
                        'fontFamily': 'Sans-Serif',
                        'margin-left': 'auto',
                        'margin-right': 'auto'
                    }),
                html.Div(id='customer_bar'),

                html.Div(id='tab-output-customer'),

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
                    html.Table(id="df_fund_info"),

                    html.H6('Fund Characteristics',
                            className="gs-header gs-text-header padded"),
                    html.Table(id="df_fund_characteristics"),

                    html.H6('Fund Facts',
                            className="gs-header gs-text-header padded"),
                    html.Table(id="df_fund_facts"),

                ], className="four columns"),

                # Column 2##

                html.Div([
                    html.H6('Sector Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Iframe(src="https://plot.ly/~jackp/17560.embed?modebar=false&link=false&autosize=true", \
                                seamless="seamless", style={'border': '0'}, width="100%", height="300"),

                    html.H6('Country Bond Allocation (%)',
                            className="gs-header gs-table-header padded"),
                    html.Table(id="df_bond_allocation"),

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
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://codepen.io/chriddyp/pen/brPBPO.css"]

#
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




@app.callback(Output('intermediate_value', 'children'),
      [
     dash.dependencies.Input('bench_code_drop_down', 'value'),
     dash.dependencies.Input('button_swap', 'n_clicks')],
    [dash.dependencies.State('target_location_small_drop_down', 'value'),
     dash.dependencies.State('intermediate_value', 'children')])

def clean_data(bench_code_dd, clicks,target_location_small_dd,riffy):
     # some expensive clean data step

     target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

     target_long_name = input_fields[input_fields["code_or_ticker"]==target_code]["yelp_name"].reset_index(drop=True)[0]

     bench_code = input_fields[input_fields["starting"] == 2]["code_or_ticker"].reset_index(drop=True)[0]

     bench_long_name = input_fields[input_fields["code_or_ticker"]==bench_code]["yelp_name"].reset_index(drop=True)[0]

     ## Starting here

     #location_start = "2231 State Hwy 6, Sugar Land, TX 77478"

     #small_loc = "Sugar-Land"
     #first_option_coy.title()#

     if not all((bench_code_dd, target_location_small_dd)):
         print("none")
     else:

         if clicks % 2 == 0:
             if not all((bench_code_dd, target_location_small_dd)):
                 target_location_small_dd = first_dict["first_option_target_location_small_name"]
                 bench_code_dd = bench_code

             else:
                 loading = True
                 bench_code_dd = bench_code_dd

         else:
             temp = target_code  # The old switcheroo.#
             target_code = bench_code_dd
             bench_code_dd = temp
             target_long_name = input_fields[input_fields["code_or_ticker"] == target_code]["yelp_name"].reset_index(drop=True)[0]

         temp_df = pd.DataFrame()
         temp_df["All Target Location Full Addresses"] = ext_info_dict[target_code]["All Target Location Full Addresses"]
         temp_df["All Target Location Small Names"] = ext_info_dict[target_code]["All Target Location Small Names"]
         temp_df["All Target Location File Names"] = ext_info_dict[target_code]["All Target Location File Names"]

         # Needed to get a new value for dropdown after the swap button click.
         if clicks == 1:
             target_location_small_dd = temp_df["All Target Location Small Names"][0]

         # Needed to get the past state to see if the dropdown value should change
         brad = 0
         if clicks > 0:
             riffy = json.loads(riffy)
             brad = riffy["clicks"] - clicks

         # Needed to get a new value for dropdown after the swap button click.
         if brad != 0:
             target_location_small_dd = temp_df["All Target Location Small Names"][0]

         target_location_address = temp_df[temp_df["All Target Location Small Names"] == target_location_small_dd]["All Target Location Full Addresses"].reset_index(drop=True)[0]

         target_location_file_name = temp_df[temp_df["All Target Location Small Names"] == target_location_small_dd]["All Target Location File Names"].reset_index(drop=True)[0]

         target_short_name = input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

         ##bench_code_dd_small = temp_df[temp_df["all_target_location_full_addresses"] == bench_code_dd]["all_target_location_small_names"].reset_index(drop=True)[0]
         ##  "bench_code_dd_small":bench_code_dd_small,
         hidden_dict = {'target_short_name':target_short_name,'target_location_file_name':target_location_file_name, 'target_location_address':target_location_address,'bench_long_name':bench_long_name,"target_long_name":target_long_name,'target_location_small_dd':target_location_small_dd, 'bench_code_dd':bench_code_dd, 'target_code':target_code, 'clicks':clicks, }

         return json.dumps(hidden_dict)




@app.callback(Output('target_location_small_drop_down', 'options'),
     [dash.dependencies.Input('intermediate_value', 'children'),
      dash.dependencies.Input('button_swap', 'n_clicks')
     ])

def dadr(hidden_dict, clicks):
    hidden_dict = json.loads(hidden_dict)

    all_target_location_full_addresses = ext_info_dict[hidden_dict["target_code"]]["All Target Location Full Addresses"]
    all_target_location_small_names = ext_info_dict[hidden_dict["target_code"]]["All Target Location Small Names"]

    return [{'label': r, 'value': i} for r,i in zip(all_target_location_full_addresses,all_target_location_small_names)]



# Tables#
@app.callback(Output('stakeholder_metrics_dataframe', 'children'),
     [dash.dependencies.Input('intermediate_value', 'children'),
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    stakeholder_metrics_dataframe = ext_info_dict[hidden_dict["target_code"]]["Stakeholder Metrics"]
    return make_dash_table(stakeholder_metrics_dataframe)

@app.callback(Output('stakeholder_metrics_dataframe_1', 'children'),
     [dash.dependencies.Input('intermediate_value', 'children'),
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    stakeholder_metrics_dataframe = ext_info_dict[hidden_dict["target_code"]]["Stakeholder Metrics"]
    return make_dash_table(stakeholder_metrics_dataframe)


@app.callback(Output('company_metrics_dataframe', 'children'),
     [dash.dependencies.Input('intermediate_value', 'children'),
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    company_metrics_dataframe = ext_info_dict[hidden_dict["target_code"]]["Company Metrics"]
    return make_dash_table(company_metrics_dataframe)


@app.callback(Output('company_metrics_dataframe_1', 'children'),
     [dash.dependencies.Input('intermediate_value', 'children'),
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    company_metrics_dataframe = ext_info_dict[hidden_dict["target_code"]]["Company Metrics"]
    return make_dash_table(company_metrics_dataframe)


@app.callback(Output('df_fund_info', 'children'),
     [dash.dependencies.Input('intermediate_value', 'children'),
     ])
def dadr(hidden_dict):
    df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')

    return make_dash_table(df_fund_info)


@app.callback(Output('df_fund_characteristics', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')

    return make_dash_table(df_fund_characteristics)

##RRR
@app.callback(Output('df_fund_facts', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')

    return make_dash_table(df_fund_facts)


@app.callback(Output('df_bond_allocation', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')

    return make_dash_table(df_bond_allocation)


@app.callback(Output('comp_plot', 'figure'),
     [dash.dependencies.Input('intermediate_value', 'children'),
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    figure=pf.figs_polar(hidden_dict["target_code"], "bench_code_dd", hidden_dict["target_code"])

    return figure


@app.callback(
    dash.dependencies.Output('stock_plot', 'figure'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    fig = figs(hidden_dict["target_code"], hidden_dict["bench_code_dd"])
    return fig

## RR

@app.callback(
    dash.dependencies.Output('stock_plot_desc', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])

def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    desc = describe(hidden_dict["target_code"], hidden_dict["bench_code_dd"])
    return desc


@app.callback(
    dash.dependencies.Output('title', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])

def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    title = str(hidden_dict["target_long_name"]) + " 4-D Report"
    return title


@app.callback(
    dash.dependencies.Output('location', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])

def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    #print(hidden_dict["dict_comp"])
    #print(hidden_dict["target_location_small_dd"])
    title = str(hidden_dict["target_location_address"]) + " Location"

    return title



@app.callback(
    dash.dependencies.Output('profile', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])

def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    title = str(hidden_dict["target_code"]) + " Sentiment Profile"

    return title
### RR


@app.callback(
    dash.dependencies.Output('mgmt_perf', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    df_perf_summary = fm.fin_met(hidden_dict["bench_code_dd"], hidden_dict["target_code"])

    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

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
#

@app.callback(
    dash.dependencies.Output('mgmt_perf_1', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    df_perf_summary = fm.fin_met(hidden_dict["bench_code_dd"], hidden_dict["target_code"])
    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

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
    [dash.dependencies.Input('intermediate_value', 'children'),
     Input('category-filter', 'value'),
     Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter(hidden_dict ,var, req, stu, ben):
    hidden_dict = json.loads(hidden_dict)
    dict_frames = ext_info_dict[hidden_dict["target_code"]]["Stock Dictionary"]
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



@app.callback(
    Output('category-filter', 'options'),
    [dash.dependencies.Input('intermediate_value', 'children'),
     Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter(hidden_dict,req, stu, ben):
    # print(per, req, stu, ben)
    hidden_dict = json.loads(hidden_dict)
    dict_frames =  ext_info_dict[hidden_dict["target_code"]]["Stock Dictionary"]
    df = dict_frames[ben, req, stu]
    highlight = list(df.drop("year", axis=1).columns.values)

    return [{'label': i, 'value': i} for i in highlight]


@app.callback(
    Output('first_tree', 'figure'),
    [dash.dependencies.Input('intermediate_value', 'children'),
     Input('request', 'value'),
     ])
def filter(hidden_dict, req):
    hidden_dict = json.loads(hidden_dict)
    dict_frames =  ext_info_dict[hidden_dict["target_code"]]["Stock Dictionary"]
    df = dict_frames["BJRI", req, "Original"]
    return tm.treemap(df)
###
@app.callback(
    Output('third_tree', 'figure'),
    [dash.dependencies.Input('intermediate_value', 'children'),
    Input('request', 'value'),
     ])
def filter(hidden_dict, req):
    hidden_dict = json.loads(hidden_dict)
    bench_code = hidden_dict["bench_code_dd"]
    dict_frames = ext_info_dict[hidden_dict["target_code"]]["Stock Dictionary"]
    df = dict_frames[bench_code, req, "Original"]
    return tm.treemap(df)

@app.callback(
    Output('graphed', 'figure'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bench_code_dder', 'value')])
def filter2( goo, time, many, norm, bench_code_dd):
    #print(per, req, stu, ben)

    figure = gc.chart_gd(goo, time, many, norm, bench_code_dd)

###
    return figure

@app.callback(
    Output('text_sum', 'value'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bench_code_dder', 'value')])
def filter2( goo, time, many, norm, bench_code_dd):
    #print(per, req, stu, ben)

    figure = gc.sum_gd(goo, time, many, norm, bench_code_dd)
    return figure
####


@app.callback(Output('tab-output', 'children'),
              [Input('intermediate_value', 'children'),
               Input('tabs', 'value')])
def display_content(hidden_dict ,value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    d = cr.dic(target_code)
    layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_overall"], config={'displayModeBar': False},
                                 style={"margin-top": "0mm"})])
    if value == "Overall":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_overall"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Employee":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_emp"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Management":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_mgm"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Shareholders":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_sha"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Customers":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_cus"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])
    elif value == "Search":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_search"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm"})])


    return layout


@app.callback(Output('tab-output-employee', 'children'),
              [Input('intermediate_value', 'children'),
                Input('tabs-employee', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    d = el.dic(target_code)
    l = ll.dic(target_code)
    c = cl.dic(target_code)
    cra = cr.dic(target_code)
    layout = d["interview_layout"]

    if value== "Interview":
        layout = d["interview_layout"]
    elif value== "Sentiment":
        layout = l["language layout"]
    elif value== "Compensation":
        layout = c["compensation_layout"]
    elif value== "Job Map":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cra["fig_cus"], config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])
    elif value== "Search":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=cra["fig_search"], config={'displayModeBar': False},
                        style={"margin-top": "0mm"})])

    return layout




@app.callback(Output('customer_bar', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children')])

def display_content(hidden_dict):

    import layout.location_distance as ld

    print('hidden_output', 'children')

    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]

    bench_code_dd = hidden_dict["bench_code_dd"]
    target_location_small_dd = hidden_dict["target_location_small_dd"]
    target_short_name = hidden_dict["target_short_name"]

    bench_code_dd_ad_df = pd.DataFrame()

    all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
    all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
    all_target_location_full_addresses_b = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
    bench_code_dd_ad_df["all_target_location_file_names_b"] = all_target_location_file_names_b
    bench_code_dd_ad_df["all_target_location_small_names_b"] = all_target_location_small_names_b
    bench_code_dd_ad_df["all_target_location_full_addresses_b"] = all_target_location_full_addresses_b

    l = ll.dic(target_code)
    c = cl.dic(target_code)

    all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    options_target_locations =  [{'label': r, 'value': i} for r, i in zip(all_target_location_full_addresses, all_target_location_small_names)]

    all_benchmark_codes = ext_info_dict[target_code]["All Benchmark Codes"]
    all_benchmark_small_names = ext_info_dict[target_code]["All Benchmark Small Names"]
    options_bench_code  = [{'label': r, 'value': i} for r,i in zip(all_benchmark_small_names,all_benchmark_codes)]

    all_target_location_full_addresses_b = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
    all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
    options_bench_locations =  [{'label': r, 'value': i} for r, i in zip(all_target_location_full_addresses_b, all_target_location_small_names_b)]


    all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]

    #coy = target_code
    #city = target_location_small_dd
    #bench_code_dd = bench_code_dd


    print("This seems to be working here")

    comp_ad_df = pd.DataFrame()
    comp_ad_df["all_target_location_file_names"] = all_target_location_file_names
    comp_ad_df["all_target_location_small_names"] = all_target_location_small_names
    comp_ad_df["all_target_location_full_addresses"] = all_target_location_full_addresses

    print(comp_ad_df["all_target_location_small_names"])

    target_location_file_name = comp_ad_df[comp_ad_df["all_target_location_small_names"] == target_location_small_dd]["all_target_location_file_names"].reset_index(drop=True)[0]

    closest = ld.dict(target_code, bench_code_dd, target_location_file_name)

    option_value_bench_location_dd = bench_code_dd_ad_df[bench_code_dd_ad_df["all_target_location_file_names_b"] == closest["name"]]["all_target_location_small_names_b"].reset_index(drop=True)[0]


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


    #new_dict["Company City File"] = comp_ad_df["all_target_location_file_names"].reset_index(drop=True)[0]
    #new_dict["Benchmark City File"] = bench_code_dd_ad_df["all_target_location_file_names_b"].reset_index(drop=True)[0]

    new_dict["options_target_locations"] = options_target_locations
    new_dict["options_bench_code"] = options_bench_code
    new_dict["options_bench_locations"] = options_bench_locations

    options_value_target_location_small_dd = new_dict["options_value_target_location_small_dd"]

    option_value_bench_code_dd = bench_code_dd

    i = cb.dict(options_value_target_location_small_dd, option_value_bench_code_dd,
                 option_value_bench_location_dd, options_target_locations,options_bench_code,options_bench_locations,
                 target_code, all_target_location_small_names, target_short_name, target_location_file_name)


    return i["info_layout_drop_downs"]



@app.callback(
    dash.dependencies.Output('bench_location_info', 'value'),
    [dash.dependencies.Input('benchmark_code_info', 'value'),
     dash.dependencies.Input('target_location_info', 'value')],)

def dadr(bench_code_dd, city):
    import layout.location_distance as ld

    target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

    print('bench_location_info', 'value')

    all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
    all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]

    bench_code_df = pd.DataFrame()
    bench_code_df["all_target_location_file_names_b"] = all_target_location_file_names_b
    bench_code_df["all_target_location_small_names_b"] = all_target_location_small_names_b

    all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]

    target_code_df = pd.DataFrame()
    target_code_df["all_target_location_file_names"] = all_target_location_file_names
    target_code_df["all_target_location_small_names"] = all_target_location_small_names

    target_file_name = target_code_df[target_code_df["all_target_location_small_names"] == city][
        "all_target_location_file_names"].reset_index(drop=True)[0]

    closest = ld.dict(target_code, bench_code_dd, target_file_name)

    option_value_bench_code_dd = \
        bench_code_df[bench_code_df["all_target_location_file_names_b"] == closest["name"]][
            "all_target_location_small_names_b"].reset_index(drop=True)[0]

    return option_value_bench_code_dd


# This should work - If not create tab-input-customer as input
@app.callback(
    dash.dependencies.Output('bench_location_info', 'options'),
    [dash.dependencies.Input('benchmark_code_info', 'value')])
def dadr(bench_code_dd):

    all_target_location_full_addresses = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
    all_target_location_small_names = ext_info_dict[bench_code_dd]["All Target Location Small Names"]

    options_ben_loc =  [{'label': r, 'value': i} for r, i in zip(all_target_location_full_addresses, all_target_location_small_names)]


    return options_ben_loc


@app.callback(Output('hidden_output', 'children'),
              [Input('intermediate_value', 'children')])

def display_content(hidden_dict):
    import layout.location_distance as ld
    hidden_dict = json.loads(hidden_dict)

    target_code = hidden_dict["target_code"]
    target_short_name = hidden_dict["target_short_name"]

    bench_code_dd = hidden_dict["bench_code_dd"]
    target_location_small_dd = hidden_dict["target_location_small_dd"]

    l = ll.dic(target_code)
    c = cl.dic(target_code)


    all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    options_target_locations =  [{'label': r, 'value': i} for r, i in zip(all_target_location_full_addresses, all_target_location_small_names)]

    all_benchmark_codes = ext_info_dict[target_code]["All Benchmark Codes"]
    all_benchmark_small_names = ext_info_dict[target_code]["All Benchmark Small Names"]
    options_bench_code  = [{'label': r, 'value': i} for r,i in zip(all_benchmark_small_names,all_benchmark_codes)]

    all_target_location_full_addresses_b = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
    all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
    options_bench_locations =  [{'label': r, 'value': i} for r, i in zip(all_target_location_full_addresses_b, all_target_location_small_names_b)]


    all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
    all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
    all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
    all_target_location_full_addresses_b = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
    #coy = target_code
    #city = target_location_small_dd
    #bench_code_dd = bench_code_dd

    comp_ad_df = pd.DataFrame()
    comp_ad_df["all_target_location_file_names"] = all_target_location_file_names
    comp_ad_df["all_target_location_small_names"] = all_target_location_small_names
    comp_ad_df["all_target_location_full_addresses"] = all_target_location_full_addresses

    print("This seems to be working here")

    target_location_file_name = comp_ad_df[comp_ad_df["all_target_location_small_names"] == target_location_small_dd]["all_target_location_file_names"].reset_index(drop=True)[0]

    closest = ld.dict(target_code, bench_code_dd, target_location_file_name)

    print(closest)

    bench_code_dd_ad_df = pd.DataFrame()
    bench_code_dd_ad_df["all_target_location_file_names_b"] = all_target_location_file_names_b
    bench_code_dd_ad_df["all_target_location_small_names_b"] = all_target_location_small_names_b
    bench_code_dd_ad_df["all_target_location_full_addresses_b"] = all_target_location_full_addresses_b

    option_value_bench_location_dd = bench_code_dd_ad_df[bench_code_dd_ad_df["all_target_location_file_names_b"] == closest["name"]]["all_target_location_small_names_b"].reset_index(drop=True)[0]

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


    #new_dict["Company City File"] = comp_ad_df["all_target_location_file_names"].reset_index(drop=True)[0]
    #new_dict["Benchmark City File"] = bench_code_dd_ad_df["all_target_location_file_names_b"].reset_index(drop=True)[0]

    new_dict["options_target_locations"] = options_target_locations
    new_dict["options_bench_code"] = options_bench_code
    new_dict["options_bench_locations"] = options_bench_locations

    print("This Prints")

    return json.dumps(new_dict)


app.callback(
    dash.dependencies.Output('store_values', 'children'),
     [dash.dependencies.Input('bench_location_info', 'value'),
     dash.dependencies.Input('benchmark_code_info', 'value'),
     dash.dependencies.Input('target_location_info', 'value')])
def display_content( bench_location_info,benchmark_code_info,target_location_info):

    print("I am adjusting")
    return json.dumps({"bench_location_info": bench_location_info, "benchmark_code_info": benchmark_code_info,
                          "target_location_info": target_location_info})


##### From otehr sizde#

@app.callback(
    dash.dependencies.Output('tab-output-customer', 'children'),
    [Input('tabs-customer', 'value'),
    dash.dependencies.Input('button_versus', 'n_clicks'),
     dash.dependencies.Input('hidden_output', 'children')],
    [dash.dependencies.State('store_values', 'children'),])
def dadr(value,clicks,dar,store_values,):
    import layout.location_distance as ld
    print(clicks)
    new_dict = json.loads(dar)

    print("Clique")

    try:
        store_values = json.loads(store_values)

        print("Success")
        target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]
        target_short_name = input_fields[input_fields["code_or_ticker"]==target_code]["short_name"].reset_index(drop=True)[0]


        bench_code_dd = store_values["benchmark_code_info"]
        target_location_small_dd = store_values["target_location_info"]


        bench_code_dd_ad_df = pd.DataFrame()

        all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
        all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
        all_target_location_full_addresses_b = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
        bench_code_dd_ad_df["all_target_location_file_names_b"] = all_target_location_file_names_b
        bench_code_dd_ad_df["all_target_location_small_names_b"] = all_target_location_small_names_b
        bench_code_dd_ad_df["all_target_location_full_addresses_b"] = all_target_location_full_addresses_b

        l = ll.dic(target_code)
        c = cl.dic(target_code)

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

        i = inl.dict(options_value_target_location_small_dd, option_value_bench_code_dd,
                     option_value_bench_location_dd, options_target_locations, options_bench_code,
                     options_bench_locations,
                     target_code, all_target_location_small_names, target_short_name, target_location_file_name)

        l = ll.dic(target_code)
        c = cl.dic(target_code)

        if value == "Infographic":
            layout = i["info_layout"]
        elif value == "Map":
            layout = l["language_layout"]
        elif value == "Sentiment":
            layout = c["compensation_layout"]

        return layout


    except:

        all_target_location_file_names_b = new_dict["all_target_location_file_names_b"]
        all_target_location_small_names_b = new_dict["all_target_location_small_names_b"]
        all_target_location_small_names = new_dict["all_target_location_small_names"]
        target_short_name = new_dict["target_short_name"]
        target_code = new_dict["target_code"]
        bench_code_dd = new_dict["bench_code_dd"]
        options_value_target_location_small_dd = new_dict["options_value_target_location_small_dd"]
        target_location_file_name = new_dict["target_location_file_name"]


        option_value_bench_location_dd = new_dict["option_value_bench_location_dd"]

        # new_dict["Company City File"] = comp_ad_df["all_target_location_file_names"].reset_index(drop=True)[0]
        # new_dict["Benchmark City File"] = bench_code_dd_ad_df["all_target_location_file_names_b"].reset_index(drop=True)[0]

        options_target_locations = new_dict["options_target_locations"]
        options_bench_code = new_dict["options_bench_code"]
        options_bench_locations = new_dict["options_bench_locations"]

        all_target_location_small_names = new_dict["all_target_location_small_names"]

        option_value_bench_code_dd = bench_code_dd

        i = inl.dict(options_value_target_location_small_dd, option_value_bench_code_dd,
                     option_value_bench_location_dd, options_target_locations,options_bench_code,options_bench_locations,
                     target_code,all_target_location_small_names,target_short_name,target_location_file_name)

        l = ll.dic(target_code)
        c = cl.dic(target_code)

        if value == "Infographic":
            layout = i["info_layout"]
        elif value == "Map":
            layout = l["language_layout"]
        elif value == "Sentiment":
            layout = c["compensation_layout"]

        return layout




@app.callback(Output('tab-output-interview-bottom', 'children'),
              [Input('intermediate_value', 'children'),
              Input('tabs-interview-bottom', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    d = el.dic(target_code)
    layout = d["interview_layout_accepted"]

    if value== "Accepted":
        layout = d["interview_layout_accepted"]
    elif value== "Positive":
        layout = d["interview_layout_positive"]
    elif value== "Negative":
        layout = d["interview_layout_negative"]
    elif value== "Difficult":
        layout = d["interview_layout_difficult"]
    elif value== "Easy":
        layout = d["interview_layout_easy"]

    return layout

@app.callback(Output('tab-output-language', 'children'),
              [Input('intermediate_value', 'children'),
               Input('tabs-language', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    d = el.dic(target_code)
    l = ll.dic(target_code)
    c = cl.dic(target_code)

    layout = l["four_figs_layout"]

    if value== "Noun":
        layout = l["four_figs_layout"]
    elif value== "Phrase":
        layout = l["phrase_layout"]
    elif value== "Sentiment":
        layout = d["interview_layout_negative"]
    elif value== "Map":
        layout = d["interview_layout_easy"]

    return layout

@app.callback(Output('tab-output-compensation', 'children'),
              [Input('intermediate_value', 'children'),
               Input('tabs-compensation', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    l = ll.dic(target_code)
    c = cl.dic(target_code)

    layout = l["four_figs_layout"]

    if value== "Benefits":
        layout = c["benefits_layout"]
    elif value== "Salaries":
        layout = c["benefits_layout"]
    elif value== "Third":
        layout = c["benefits_layout"]


    return layout




# Our main function
if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server()