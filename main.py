# coding: utf-8
import dash
from dash.dependencies import Input, Output
# import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
from plotly import graph_objs as go
from datetime import datetime as dt
import json
import plotly

plotly.tools.set_credentials_file(username='xxxxx', api_key='xxxxxxx')
import layout.key_stats_layout as ksl
import flask
import pandas as pd
import os
from flask import Flask
from six.moves import cPickle as pickle  # for performance
from os import listdir
from os.path import isfile, join
import numpy as np

import processing.input as inp
import processing.customer_area_dataframe as cad

import layout.multiple_charts as mc
import layout.polar_figure as pf
import layout.charting_words as cw
import layout.frequency_word_chart as fwc
import layout.glassdoor_chart as gc
import layout.chart_ratings as cr
import layout.language_layout as ll
import layout.compensation_layout as cl
import layout.infograph_layout as inl
import layout.treemap as tm
from processing.stock_narration import describe
import layout.frames_layout as fm
from layout.figures import figs
import layout.donuts_interview as di
import layout.employee_layout as el
from flask_caching import Cache
import layout.customer_bar as cb
import dash_table_experiments as dt
import layout.map_layout as ml
import layout.region_layout as rl
import layout.yelp_extra_info_layout as yeil
import layout.sentiment_customer_layout as scl
import layout.tastes_layout_callback as tlcw
import layout.tastes_layout_callback_sans as tlcs
import layout.social_layout as sola
import layout.employee_analysis as ea
import layout.employee_analysis_fig as eaf
import layout.snapshot_layout as snl
import processing.social_media as som

### It is important to note that there is no target firm. This is dynamic.

# To Give Orientation#

# Initialize the Dash app #
app = dash.Dash('FirmAI 4D Interactive Report')

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'statics')


@app.server.route('/statics/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)


app.config.suppress_callback_exceptions = True
app.scripts.config.serve_locally = True
app.scripts.config.serve_locally = False

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

dict_info = {

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

from string import digits

remove_digits = str.maketrans('', '', digits)

for i in range(len(first_dict["target_location_small_drop_down_options"])):
    dar = first_dict["target_location_small_drop_down_options"][i]["label"]

    res = dar.translate(remove_digits)
    try:
        full = res.lstrip().split(",")[1] + " - " + res.lstrip().split(",")[0]
        full = full.lstrip()
    except:
        full = res.lstrip()
    first_dict["target_location_small_drop_down_options"][i]["label"] = full

figure = pf.figs_polar(first_dict["first_option_target_code"])

dict_info = first_dict["dict_info_output"]

comp_plot_output = figure

fig = figs(first_dict["first_option_target_code"], first_dict["first_option_bench_code"])

stock_plot_output = fig

df_perf_summary = first_dict["df_perf_summary_output"]


def make_dash_table_white_2(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    bas = -1
    for index, row in df.iterrows():
        bas = bas + 1
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]], style={"padding-right": "8px"}))
        if bas == 0:
            table.append(
                html.Tr(html_row, style={"font-weight":"bold","background-color": "white", 'border-bottom': '1px solid WhiteSmoke'}))
        else:
            table.append(html.Tr(html_row, style={"background-color": "white"}))
    return table



def make_dash_table_white(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    bas = -1
    for index, row in df.iterrows():
        bas = bas + 1
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]], style={"padding-right": "8px"}))
        if bas == 0:
            table.append(
                html.Tr(html_row, style={"background-color": "white", 'border-bottom': '1px solid WhiteSmoke'}))
        else:
            table.append(html.Tr(html_row, style={"background-color": "white"}))
    return table


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
        html.Td([first_dict["first_option_target_code"]], colSpan=4, style={'text-align': "center"}),
        html.Td([first_dict["first_option_bench_code"]], colSpan=4, style={'text-align': "center"})
    ], style={'background': 'white', 'font-weight': '600'}
    )
)
mgmt_perf_output = modifed_perf_table

mgmt_perf_output_1 = modifed_perf_table

### Logo

import base64

image_filename = 'transparent_logo.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())


# path = os.path.join(my_path, "data/cpickle/")

# ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))

@cache.memoize()
def roll():
    my_path = os.path.abspath(os.path.dirname('__file__'))

    path = os.path.join(my_path, "data/cpickle/")

    ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))
    return ext_info_dict


ext_info_dict = roll()

app.config['suppress_callback_exceptions'] = True
# Describe the layout, or the UI, of the app

DF_SIMPLE = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E', 'F'],
    'y': [4, 3, 1, 2, 3, 6],
    'z': ['a', 'b', 'c', 'a', 'b', 'c']
}).to_dict('records')

shareholder = html.Div([  # page 5

    html.A(['Print PDF'],
           className="button no-print", href="javascript:window.print()",
           style={'position': "absolute", 'top': '-40', 'right': '0'}, title='Only Works on Safari'),

    html.Div([  # subpage 2

        # Row 1 (Header)

        html.Div([
            html.H6(["Shareholder Analysis"],
                    className="gs-header gs-table-header padded")]),

        html.Br([]),

        html.Div([
            dcc.Tabs(
                tabs=[{'label': "Key Stats", 'value': "Key Stats"},
                      {'label': "Industry Peers", 'value': "Competitors"},
                      ],
                value="Key Stats",
                id='tabs-shareholder'
            ),
            html.Div(id='tab-output-shareholder'),

        ], style={
            'width': '100%',
            'fontFamily': 'Sans-Serif',
            'margin-left': 'auto',
            'margin-right': 'auto'
        }),

    ], className="subpage"),

], className="page", id="page-7")

innards = html.Div([

    html.Div([

        html.Div([html.H6(["Executive Summary"], style={"float": "left", "padding-right": "0.2cm"}),
                  html.A("info",
                         href='www.firmai.org',
                         target="_blank")
                  ], className="gs-header gs-table-header padded"),

        html.P(inp.exec, style={"padding-top": "1mm"})]),

    # Row 2

    html.Div([

        html.Div([

            html.H6(first_dict["profile_output"], className="gs-header gs-text-header padded", id="profile"),

            html.Strong("Employees"),
            html.P(dict_info["employees"], title=dict_info["employees_r"],
                   className='blue-text'),

            html.Strong(
                'Customers'),
            html.P(dict_info["customers"], title=dict_info["customers_r"],
                   className='blue-text'),

            html.Strong('Shareholders'),
            html.P(dict_info["shareholders"], title=dict_info["shareholders_r"],
                   className='blue-text'),

            html.Strong('Management'),
            html.P(dict_info["management"], title=dict_info["management_r"],
                   className='blue-text'),

        ], className="four columns", id="stakeholder_description", ),

        html.Div([
            html.H6(["Shareholder Performance"],
                    className="gs-header gs-table-header padded",
                    title="This chart compares the past shareholder financial performance of the target company and the "
                          "benchmark company. The chart further includes an industry benchmark chart - Ind Perf in light blue. Furthermore the thin red line "
                          "identifies an AI predicted value of the firm. This is done by comparing multiple qualitative and other variables against "
                          "36 publicly trading companies and more than 5 million available datapoints to identify a fairvalue trajectory in shareholder "
                          "growth. Very importantly, where the company is not traded publicly the AI driven prediction method is used to estimate the "
                          "shareholder growth trajectory.  "),
            # html.Iframe(src="https://plot.ly/~snowde/36.embed?modebar=false&link=false&autosize=true", \
            #            seamless="seamless", style={'border': '0', 'width': "100%", 'height': "250"}),

            dcc.Graph(figure=stock_plot_output,
                      id='stock_plot', style={'border': '0', 'width': "100%", 'height': "250"},
                      config={'displayModeBar': False}
                      )
        ], className="eight columns"),
    ], className="row ", style={'width': "104%"}),

    # Row 2.5, s#

    html.Div([

        html.Div([
            html.H6('Stakeholder Metrics',
                    className="gs-header gs-text-header padded",
                    title="The Stajeholder Metrics identified the 4 most important stakeholder dimensions and their "
                          "aggregate ratings. Compring the average - A against the Benchmark - B can give the reader "
                          "an indication of the overall stakeholder sentiment versus the benchmark average."),
            html.Table(make_dash_table(first_dict["s_metrics_df_output"]), id="stakeholder_metrics_dataframe",
                       style={'marginBottom': 5},
                       className='tiny-header'),
            html.P(
                "E - Employees; C - Customer; S - Shareholders; M - Management; A - Average; BA - Benchmark Average",
                style={'font-size': '60%', 'marginTop': 5}),
            html.H6('Company Metrics',
                    className="gs-header gs-text-header padded", title="Company Metrics identifies the"
                                                                       "general trend of groups of financial variables relative to "
                                                                       "the other groups by using two mathematical techniques known "
                                                                       "as PCA and normalisation. The directional arrows therefore gives the "
                                                                       "reader an indication of the general trend over a five year period."),
            html.Table(make_dash_table(first_dict["c_metrics_df_output"]), id="company_metrics_dataframe",
                       style={'marginBottom': 5},
                       className='tiny-header'),
            html.P(
                "All metrics in this report is quarterly based unless otherwise specified. This report is "
                "for informational purposes only. It should not be considered financial advice. FirmAI "
                " does not make any guarantee nor does it take on any liability. ",
                style={'font-size': '80%', 'marginTop': '8', 'font-weight': 'bold', 'text-align': 'justify'}),
        ], className="four columns"),

        html.Div([
            html.P(first_dict["stock_plot_desc_output"], id='stock_plot_desc', style={"padding-top": "1.2mm"}),
        ], className="eight columns"),
        html.Div([

            html.H6("Financial Performance",
                    className="gs-header gs-table-header padded",
                    title="This financial performance table looks at essential metrics in averages accross 1,2,3 and 5 years starting with the "
                          "last financial year, Yr 1. If the company is private this information "
                          "is estimates with an AI prediction tool. This part is still experimental. The benchmark is the company "
                          "as selected in the header.  "),
            html.Table(mgmt_perf_output, id="mgmt_perf", className="reversed")
        ], className="eight columns"),

    ], className="row ", style={'width': "104%"}),

    # Row 3##
], style={'width': "100%"})

page_1 = html.Div([  # page 1

    html.A(['Print PDF'],
           className="button no-print", href="javascript:window.print()",
           style={'position': "absolute", 'top': '-40', 'right': '0'}, title='Only Works on Safari'),

    html.Div([  # subpage 1

        # Row 1 (Header)

        html.Div(id='loading', children=[

            html.Div([

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
                    ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                              'padding-right': '0cm', 'width': '20%'}),

                html.Div([
                    html.Div([
                        html.Button('SWAP', id='button_swap', n_clicks=0,
                                    style={'height': '3.3em', 'float': 'center', 'color': 'rgb(217, 224, 236)'})
                    ], style={'padding-left': '0.8cm', 'padding-right': '0.8cm', 'float': 'left'}),
                        ], id="SWAPS"),

                    html.Div([
                        dcc.Dropdown(
                            id='bench_code_drop_down',
                            # value=bench_code,
                            # options=first_dict["bench_code_drop_down_options"],
                            clearable=False,
                            className="dropper",
                            placeholder="Select Benchmark"

                        )
                    ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'width': '80%',
                              'float': 'left', 'width': '20%'}),
                    html.Div([

                        html.H3('3.6/5', id="final_rating")], style={'padding-left': '1.2cm', 'float': 'left'})
                    # , 'float': 'right', 'display': 'inline-block'
                ], style={'padding-top': '0.3cm', 'padding-left': '0cm'},
                    className="double_drop"),

            ], className="nine columns padded"),

            html.Div([
                html.Div([
                    html.H1(
                        [html.Span(str("1"), style={'opacity': '0.5'}), html.Span(str(now.year)[2:])]),

                    html.H6('Monthly Interactive Update'),
                    html.Div([
                        html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                 style={'width': '80px', 'margin-top': '3px', 'margin-left': '-5px'})
                    ]),
                ], className="three columns gs-header gs-accent-header padded", style={'float': 'right'}),
                html.Div([
                    html.Img(src="//logo-core.clearbit.com/bjsrestaurants.com?size=60"),
                ], style={'float': 'left', 'margin-left': "-0.86cm", "margin-top": "-0.0cm"}, id="img_logo"),

            ])

        ], className="row gs-header gs-text-header"),

        html.Br([]),

        html.Div([
            html.Div([

                innards,

            ], className="blor")
        ], id="blorring")

    ], className="subpage"),

], className="page", id="page-1")
###
other_layout = html.Div([

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print", href="javascript:window.print()",
               style={'position': "absolute", 'top': '-40', 'right': '0'}, title='Only Works on Safari'),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Quarterly Snapshot"],
                        className="gs-header gs-table-header padded"),

                ### Snapping Callback

            ], id="snap_layout"),

        ], className="subpage"),

    ], className="page", id="page-2"),

    html.Div([  # page 3

        html.A(['Print PDF'],
               className="button no-print", href="javascript:window.print()",
               style={'position': "absolute", 'top': '-40', 'right': '0'}, title='Only Works on Safari'),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.H6(["Competitor Map"],
                    className="gs-header gs-table-header padded", title="Five dimensions are used to isolate the "
                                                                        "true benchmaks of the target firm. Similarities in "
                                                                        "website, management, customers, location, news and "
                                                                        "employees are used to algorithmically filter the benchmarks down to 7 firms."),
            html.P("Five dimensions are used to isolate the "
                   "true benchmaks of the target firm. Similarities in "
                   "website, management, customers, location, news and "
                   "employees are used to algorithmically filter the benchmarks down to 7 firms. "
                   "The website algorithm tracks the cookies of users to calculate audience overlap using two independent tools. The management algorithm "
                   "uses Linkedin data to identify companies that "
                   "compete for the same cohort of managers. The customer algorithm uses Facebook and Yelp data to identify firms that have an overlapping customer base as. "
                   "The before mentioned as well as geolocation metrics are then further used to identify firms "
                   "that tend to be in close vicinity to the target company. The news algorithm looks at similarities in Twitter and Google mentions. And finally,"
                   " the employee algorithm looks at firms that compete for a similar cohort of lower level employees using Glassdoor data.  ",
                   style={"padding-top": "0.3cm"}),

            html.Div(id="competitor")

        ], className="subpage"),

        # Row 2

        html.Div(html.P(inp.exec, style={"padding-top": "1mm"}))

    ], className="page", id="page-3"),

    html.Div([  # page 1

        html.A(['Print PDF'],
               className="button no-print", href="javascript:window.print()",
               style={'position': "absolute", 'top': '-40', 'right': '0'}, title='Only Works on Safari'),

        html.Div([  # subpage 1

            # Row 1 (Header)

            html.Br([]),

            html.Div([html.H6(["Trend Analysis"],
                              className="gs-header gs-table-header padded"),
                      html.P(inp.trends, style={"padding-top": "2mm"}),
                      html.Hr([], style={"margin": "1mm"}),
                      html.Table(make_dash_table_white(pd.read_csv("data/ratings/corr_mat.csv")),
                                 style={"background-color": "white"}),
                      html.Div([
                          dcc.Tabs(
                              tabs=[{'label': "Overall", 'value': "Overall"},
                                    {'label': "Employee", 'value': "Employee"},
                                    {'label': "Management", 'value': "Management"},
                                    {'label': "Shareholders", 'value': "Shareholders"},
                                    {'label': "Customers", 'value': "Customers"},
                                    {'label': "Search", 'value': "Search"},
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
                html.Div([html.H6(["Social Stats"],
                                  className="gs-header gs-table-header padded"),

                          ]),

                # som.lt

            ], style={"margin-top": "0.0cm"}, id="soma_media"),

            # Row 3#

        ], className="subpage"),

    ], className="page", id="page-4"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print", href="javascript:window.print()",
               style={'position': "absolute", 'top': '-40', 'right': '0'}, title='Only Works on Safari'),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Employee Analysis"],
                        className="gs-header gs-table-header padded")]),

            html.Br([]),

            html.Div([
                dcc.Tabs(
                    tabs=[{'label': "Interview", 'value': "Interview"},
                          {'label': "Key Stats", 'value': "Key Stats"},
                          {'label': "Sentiment", 'value': "Sentiment"},
                          {'label': "Compensation", 'value': "Compensation"},

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

    ], className="page", id="page-5"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print", href="javascript:window.print()",
               style={'position': "absolute", 'top': '-40', 'right': '0'}, title='Only Works on Safari'),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Br([]),

            html.Div([
                html.H6(["Customer Analysis"],
                        className="gs-header gs-table-header padded"),

                html.Div([

                    dcc.Tabs(
                        tabs=[{'label': "Food", 'value': "Food"},
                              {'label': "Convenience", 'value': "Convenience"},

                              {'label': "Map", 'value': "Map"},
                              {'label': "State", 'value': "State"},
                              {'label': "Area", 'value': "Area"},

                              {'label': "Sentiment", 'value': "Sentiment"},
                              {'label': "Sent Score", 'value': "Sent Score"},

                              ],
                        value="Food",
                        id='tabs-customer'
                    ),
                ], style={
                    'width': '100%',
                    'height': '10%',
                    'fontFamily': 'Sans-Serif',
                    'margin-left': 'auto',
                    'margin-top': '0.5cm',
                    'margin-right': 'auto'
                }),

                html.Div(id='customer_bar'),

                html.Div(id='tab-output-customer'),

            ]),

        ], className="subpage"),

    ], className="page", id="page-6"),

    html.Div([

        shareholder

    ], id="shares"),

    html.Div([  # page 5

        html.A(['Print PDF'],
               className="button no-print", href="javascript:window.print()",
               style={'position': "absolute", 'top': '-40', 'right': '0'}, title='Only Works on Safari'),

        html.Div([  # subpage 2

            # Row 1 (Header)

            html.Div([
                html.H6(["Appendix"],
                        className="gs-header gs-table-header padded")]),

            html.Br([]),

            html.Div([
                dcc.Tabs(
                    tabs=[
                          {'label': "Website", 'value': "Website"},
                          {'label': "Finance Pattern", 'value': "Finance Pattern"},
                          {'label': "Report", 'value': "Report"},
                          ],
                    value="Website",
                    id='tabs-social'
                ),
                html.Div(id='tab-output-social'),

            ], style={
                'width': '100%',
                'fontFamily': 'Sans-Serif',
                'margin-left': 'auto',
                'margin-right': 'auto'
            }),

        ], className="subpage"),

    ], className="page", id="page-8"),

    ######
])

app.layout = html.Div([

    # Hidden div inside the app that stores the intermediate value
    html.Div(id='intermediate_value', style={'display': 'none'}),
    html.Div(id='hidden_output', style={'display': 'none'}),
    html.Div(id='store_values', style={'display': 'none'}),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    html.Div(id='map_hidden', style={'display': 'none'}),

    # html.Div(id='store_values', style={'display': 'none'})

    # Loading page 1 layout


    # other_layout
    html.Div(page_1, id="conditional_output_first"),

    html.Div(id="conditional_output")

])

if 'DYNO' in os.environ:
    app.scripts.append_script({
        'external_url': 'statics/plotly_ga.js'
    })

# 'https://codepen.io/chriddyp/pen/bWLwgP.css',##
# If you upload css you have to reapload it after github to git raw.
# fuckit i JUST STORED IT IN KERAS
# https://github.com/snowde/keras/blob/master/just.css

my_path = os.path.abspath(os.path.dirname('__file__'))

external_css = ["/statics/normalize.min.css",
                "/statics/skeleton.min.css",
                "/statics/fonts_google.css",
                # "https://www.dropbox.com/s/7zx0pqn3eqql7b1/this.css?dl=1"
                "/statics/just.css",
                # "https://cdn.rawgit.com/plotly/dash-app-stylesheets/5047eb29e4afe01b45b27b1d2f7deda2a942311a/goldman-sachs-report.css",
                "/statics/font-awesome.min.css",
                "/statics/brPBPO.css"]

#
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = [
    my_path + "/statics/jquery-3.2.1.min.js",
    my_path + "/statics/new_java.js",
    my_path + "/statics/dash-goldman-sachs-report-js.js",
]

for js in external_js:
    app.scripts.append_script({"external_url": js})


#
# Call Backs



@app.callback(Output('button_swap', 'children'),
              [dash.dependencies.Input('button_swap', 'n_clicks'),
               dash.dependencies.Input('bench_code_drop_down', 'value'),
               dash.dependencies.Input('target_location_small_drop_down', 'value')],
              [dash.dependencies.State('button_swap', 'children')], )
def do(clicks,bench_code_dd, target_location_small_dd, state):
    print("one")
    if clicks==0:
        return "SWAP"
    elif state == "SWAP":
        return "BACK"
    else:
        return "SWAP"


@app.callback(Output('bench_code_drop_down', 'options'),
              [dash.dependencies.Input('button_swap', 'children')],
              [dash.dependencies.State('target_location_small_drop_down', 'value')],
              )
def signal(bs, f):
    print("two")

    print("ringle")
    print(f)
    if f != "All":
        return first_dict["bench_code_drop_down_options"]
    else:
        return [{'label': "First Type Location!", 'value': None}]



@app.callback(Output('conditional_output', 'children'),
              [dash.dependencies.Input('bench_code_drop_down', 'options')],
              [dash.dependencies.State('bench_code_drop_down', 'value'),])
def signal(ins, f):
    print("three")
    print("signal")
    print(f)
    if f != None:
        return other_layout


@app.callback(Output('blorring', 'children'),
              [dash.dependencies.Input('conditional_output', 'children')],
              [dash.dependencies.State('bench_code_drop_down', 'value')])

def signal(trigs, f):
    print("signal")
    print(f)
    print("four")

    if f != None:

        return html.Div([

            innards,

        ])
    else:
        return html.Div([

            innards,

        ], className="blor")

@app.callback(Output('intermediate_value', 'children'),
              [dash.dependencies.Input('blorring', 'children')],
              [dash.dependencies.State('button_swap', 'n_clicks'),
               dash.dependencies.State('bench_code_drop_down', 'value'),
               dash.dependencies.State('target_location_small_drop_down', 'value'),
               dash.dependencies.State('intermediate_value', 'children')])
def clean_data(blor, clicks, bench_code_dd, target_location_small_dd, riffy):
    # some expensive clean data step
    print("five")

    if bench_code_dd != None:

        target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

        target_long_name = \
        input_fields[input_fields["code_or_ticker"] == target_code]["yelp_name"].reset_index(drop=True)[
            0]

        bench_code = input_fields[input_fields["starting"] == 2]["code_or_ticker"].reset_index(drop=True)[0]

        bench_long_name = \
        input_fields[input_fields["code_or_ticker"] == bench_code]["yelp_name"].reset_index(drop=True)[0]

        ## Starting here

        # location_start = "2231 State Hwy 6, Sugar Land, TX 77478"

        # small_loc = "Sugar-Land"#
        # first_option_coy.title()#

        ### Deleted Below - Can this solve it.

        #if not all((bench_code_dd, target_location_small_dd)):
        #    print("none")
        #else:

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
            target_long_name = \
                input_fields[input_fields["code_or_ticker"] == target_code]["yelp_name"].reset_index(drop=True)[0]

        temp_df = pd.DataFrame()
        temp_df["All Target Location Full Addresses"] = ext_info_dict[target_code][
            "All Target Location Full Addresses"]
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

        target_location_address = temp_df[temp_df["All Target Location Small Names"] == target_location_small_dd][
            "All Target Location Full Addresses"].reset_index(drop=True)[0]

        target_location_file_name = temp_df[temp_df["All Target Location Small Names"] == target_location_small_dd][
            "All Target Location File Names"].reset_index(drop=True)[0]

        target_short_name = \
            input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

        ##bench_code_dd_small = temp_df[temp_df["all_target_location_full_addresses"] == bench_code_dd]["all_target_location_small_names"].reset_index(drop=True)[0]
        ##  "bench_code_dd_small":bench_code_dd_small,
        hidden_dict = {'target_short_name': target_short_name,
                       'target_location_file_name': target_location_file_name,
                       'target_location_address': target_location_address, 'bench_long_name': bench_long_name,
                       "target_long_name": target_long_name, 'target_location_small_dd': target_location_small_dd,
                       'bench_code_dd': bench_code_dd, 'target_code': target_code, 'clicks': clicks, }

        print("Bladder")
        print(hidden_dict)

        return json.dumps(hidden_dict)



# Don't delete, this is the first page load dynamic.##


@app.callback(Output('target_location_small_drop_down', 'options'),
              [dash.dependencies.Input('intermediate_value', 'children')
               ])
def dadr(hidden_dict):
    print("six")

    hidden_dict = json.loads(hidden_dict)

    all_target_location_full_addresses = ext_info_dict[hidden_dict["target_code"]][
        "All Target Location Full Addresses"]
    all_target_location_small_names = ext_info_dict[hidden_dict["target_code"]]["All Target Location Small Names"]

    for i in range(len(all_target_location_full_addresses)):
        dar = all_target_location_full_addresses[i]

        res = dar.translate(remove_digits)
        try:
            full = res.lstrip().split(",")[1] + " - " + res.lstrip().split(",")[0]
            full = full.lstrip()
        except:
            full = res.lstrip()
        all_target_location_full_addresses[i] = full

    return [{'label': r, 'value': i} for r, i in
            zip(all_target_location_full_addresses, all_target_location_small_names)]


# Tables####
@app.callback(Output('stakeholder_metrics_dataframe', 'children'),
                [dash.dependencies.Input('intermediate_value', 'children'),])
def dadr(hidden_dict):

    print("seven")
    hidden_dict = json.loads(hidden_dict)
    stakeholder_metrics_dataframe = ext_info_dict[hidden_dict["target_code"]]["Stakeholder Metrics"]

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "data/closure/")
    new_frame = pd.read_csv(path + "stakeholder_metrics.csv")
    new_frame = new_frame.set_index("ticker")

    s_metrics_df = pd.DataFrame([["Sentiment", "E", "C", "S", "M", "A", "BA"],
                                 [hidden_dict["target_code"],
                                  new_frame[new_frame.index == hidden_dict["target_code"]].round(1)["Employees"].values[
                                      0],
                                  new_frame[new_frame.index == hidden_dict["target_code"]].round(1)["Customers"].values[
                                      0],
                                  new_frame[new_frame.index == hidden_dict["target_code"]].round(1)[
                                      "Valuation Part"].values[0],
                                  new_frame[new_frame.index == hidden_dict["target_code"]].round(1)[
                                      "Management"].values[0],
                                  new_frame[new_frame.index == hidden_dict["target_code"]].round(1)["Mean"].values[0],
                                  round(new_frame["Mean"].mean(), 1)],
                                 [hidden_dict["bench_code_dd"],
                                  new_frame[new_frame.index == hidden_dict["bench_code_dd"]].round(1)[
                                      "Employees"].values[
                                      0],
                                  new_frame[new_frame.index == hidden_dict["bench_code_dd"]].round(1)[
                                      "Customers"].values[
                                      0],
                                  new_frame[new_frame.index == hidden_dict["bench_code_dd"]].round(1)[
                                      "Valuation Part"].values[0],
                                  new_frame[new_frame.index == hidden_dict["bench_code_dd"]].round(1)[
                                      "Management"].values[0],
                                  new_frame[new_frame.index == hidden_dict["bench_code_dd"]].round(1)["Mean"].values[0],
                                  round(new_frame["Mean"].mean(), 1)],
                                 ["Bench",
                                  new_frame[new_frame.index == "Mean"].round(1)["Employees"].values[0],
                                  new_frame[new_frame.index == "Mean"].round(1)["Customers"].values[0],
                                  new_frame[new_frame.index == "Mean"].round(1)["Valuation Part"].values[0],
                                  new_frame[new_frame.index == "Mean"].round(1)["Management"].values[0],
                                  new_frame[new_frame.index == "Mean"].round(1)["Mean"].values[0],
                                  round(new_frame["Mean"].mean(), 1)]

                                 ])

    return make_dash_table(s_metrics_df)


@app.callback(Output('stakeholder_description', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    print("eight")

    print("This is running!")
    hidden_dict = json.loads(hidden_dict)
    ##dict_info = ext_info_dict[hidden_dict["target_code"]]["Stakeholder Description"]

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "data/closure/")

    overall = pd.read_csv(path + "overall.csv")
    overall = overall.rename(columns={"Unnamed: 0": "ticker"})
    overall_r = pd.read_csv(path + "overall_r.csv")
    overall_r = overall_r.rename(columns={"Unnamed: 0": "ticker"})

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "data/closure/")

    new_frame = pd.read_csv(path + "stakeholder_metrics.csv").set_index("ticker")

    bench = hidden_dict["bench_code_dd"]

    true_frame = new_frame.copy()

    larger = true_frame.iloc[0:-1, :] > true_frame.loc[bench, :] + 0.10

    smaller = true_frame.iloc[0:-1, :] < true_frame.loc[bench, :] - 0.10

    similar = smaller == larger

    similar = similar.replace(True, "Similar")

    for col in similar.columns:
        for row in similar.index:
            if similar.loc[row, col] == "Similar":
                larger.loc[row, col] = "Similar"

    larger.columns = ['Customers', 'Management', 'Employees', 'Shareholder', 'Overall']

    larger_shift = larger.copy()

    for col in larger_shift.columns:
        larger_shift[col] = larger_shift[col].apply(lambda x:
                                                    " and lower than " + bench + "'s"
                                                    if x == False else
                                                    (" and higher than " + bench + "'s"
                                                     if x == True else
                                                     (" and similar to " + bench + "'s"
                                                      if x == "Similar" else x)))

    overall = overall.set_index("ticker") + larger_shift
    overall = overall.reset_index()
    overall_tick = overall[overall["ticker"] == hidden_dict["target_code"]]
    overall_r_tick = overall_r[overall_r["ticker"] == hidden_dict["target_code"]]

    dict_info = {

        "title": "BJ’s Restaurant & Brewhouse",
        "location": "Jacksonville",
        "employees": overall_tick["Employees"].values[0],
        "customers": overall_tick["Customers"].values[0],
        "shareholders": overall_tick["Shareholder"].values[0],
        "management": overall_tick["Management"].values[0],
        "employees_r": overall_r_tick["Employees"].values[0],
        "customers_r": overall_r_tick["Customers"].values[0],
        "shareholders_r": overall_r_tick["Shareholder"].values[0],
        "management_r": overall_r_tick["Management"].values[0]

    }

    lt = html.Div([
        html.H6(str(hidden_dict["target_code"]) + " Sentiment Profile", className="gs-header gs-text-header padded"),

        html.A(html.Strong("Employees"), href='#page-5', style={"text-decoration": "none", "color": "inherit"}),

        html.P(dict_info["employees"], title=dict_info["employees_r"],
               className='blue-text'),

        html.A(html.Strong(
            'Customers'), href='#page-6', style={"text-decoration": "none", "color": "inherit"}),

        html.P(dict_info["customers"], title=dict_info["customers_r"],
               className='blue-text'),

        html.A(html.Strong('Shareholders'), href='#page-7', style={"text-decoration": "none", "color": "inherit"}),

        html.P(dict_info["shareholders"], title=dict_info["shareholders_r"],
               className='blue-text'),

        html.A(html.Strong('Management'), href='#page-2', style={"text-decoration": "none", "color": "inherit"}),

        html.P(dict_info["management"], title=dict_info["management_r"],
               className='blue-text'),

    ])

    return lt


###### stakeholder_metrics_dataframe_1  you can basically engineer this one, add stuff to app processing again

"""

@app.callback(Output('img_logo', 'src'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    logo = input_fields[input_fields["code_or_ticker"]==hidden_dict["target_code"]]["logo"].reset_index(drop=True).iloc[0]
    logo = "//logo.clearbit.com/"+logo+"?size=60"

    return logo
"""


@app.callback(Output('stakeholder_metrics_dataframe_1', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    print("nine")

    hidden_dict = json.loads(hidden_dict)
    stakeholder_metrics_dataframe = ext_info_dict[hidden_dict["target_code"]]["Stakeholder Metrics"]
    return make_dash_table(stakeholder_metrics_dataframe)


@app.callback(Output('company_metrics_dataframe', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    print("ten")

    hidden_dict = json.loads(hidden_dict)
    company_metrics_dataframe = ext_info_dict[hidden_dict["target_code"]]["Company Metrics"]
    return make_dash_table(company_metrics_dataframe)


@app.callback(Output('company_metrics_dataframe_1', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    print("eleven")
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


@app.callback(Output('competitor', 'children'),
              [dash.dependencies.Input('intermediate_value', 'children'),
               ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    fg = pf.figs_polar(hidden_dict["target_code"])

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_out = my_path + "/data/input/"
    rad = pickle.load(open(path_out + "comps.p", "rb"))
    names = input_fields["fake_yelp_name"]
    print("rad")
    lat = html.Div([

        html.Table(make_dash_table_white_2(rad[hidden_dict["target_code"]]), id="competitor_table"),

        html.P("This Report Has Automatically Isolated The Following Firms:"),

        html.Div([

            html.Div([
                html.Ul([

                    html.Li([names[0]]),
                    html.Li([names[1]]),

                ]
                ),

            ], style={"float": "left", "width": "25%"}),

            html.Div([
                html.Ul([

                    html.Li([names[2]]),
                    html.Li([names[3]]),

                ]
                ),

            ], style={"float": "left", "width": "25%"}),

            html.Div([
                html.Ul([

                    html.Li([names[4]]),
                    html.Li([names[5]]),

                ]
                ),
            ], style={"float": "left", "width": "25%"}),

            html.Div([
                html.Ul([

                    html.Li([names[6]]),

                ]
                ),
            ], style={"float": "left", "width": "24%"}),
        ], style={"width": "100%", "display": "inline-block"}),

        html.Div([

            html.H6(["Competitor Metrics"],
                    className="gs-header gs-table-header padded", style={"margin-top": "0.1cm"}),

            # html.H6(["Competitor Metrics"],
            # className="gs-header gs-table-header padded", style={"text-align": "left"}),

            html.H6(["Top Four Competitors"], style={"padding-top": "0.3cm"}),
            html.P("This section identifies the MSE (Marginal Squared Errors) between "
                   "4 overarching components to identify the 4 most similar firms to the target company by identifying"
                   " similarities in firm characteristic, the smaller the distance (MSE) the more similar these firms are "
                   "to each other.  ", title="This is the second method to filter down"
                                             " to the core competitors. The target-benchmark combination"

                                             " with the smallest distance (MSE) are the most similar. "),

            html.Div([
                html.Div([
                    html.Div([
                        dcc.Graph(figure=fg[0], config={'displayModeBar': False}, id='comp_plot',
                                  style={'border': '0', 'width': "50%", 'height': '6%'}),

                    ], style={"float": "left"}),

                    html.Div([
                        dcc.Graph(figure=fg[1], config={'displayModeBar': False}, id='rff',
                                  style={'border': '0', 'width': "50%", 'height': '6%'}),

                    ], style={"float": "left"}),

                ], style={"padding": "0cm"}),
                html.Div([
                    html.Div([
                        dcc.Graph(figure=fg[2], config={'displayModeBar': False}, id='dss',
                                  style={'border': '0', 'width': "50%", 'height': '6%'}),

                    ], style={"float": "left"}),
                    html.Div([
                        dcc.Graph(figure=fg[3], config={'displayModeBar': False}, id='comp_ggsplot',
                                  style={'border': '0', 'width': "50%", 'height': '6%'}),

                    ], style={"float": "left"}),

                ], style={"padding": "0cm"}),

            ], style={"margin-left": "1.5cm", "margin-bottom": "-1cm", "padding": "0cm", 'height': '100%'}),

        ]),

    ])

    return lat


@app.callback(
    dash.dependencies.Output('stock_plot', 'figure'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    fig = figs(hidden_dict["target_code"], hidden_dict["bench_code_dd"])
    return fig


## RR#

@app.callback(
    dash.dependencies.Output('stock_plot_desc', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    print("describe")
    print(hidden_dict["target_code"], hidden_dict["bench_code_dd"])
    desc, df_com = describe(hidden_dict["target_code"], hidden_dict["bench_code_dd"])
    ## Here I can add to the text

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "data/stock/")

    listed = \
    input_fields[input_fields["code_or_ticker"] == hidden_dict["target_code"]]["listed"].reset_index(drop=True).values[
        0]

    listed_bench = input_fields[input_fields["code_or_ticker"] == hidden_dict["bench_code_dd"]]["listed"].reset_index(
        drop=True).values[0]

    if listed == "Yes":
        df_com_sim = pd.read_csv(path + hidden_dict["target_code"] + "_sim_tick_df.csv")
        if df_com_sim["close"].iloc[-1] > df_com["close"].iloc[-1]:
            if listed_bench == "No":

                desc = "Note, as a result of " + hidden_dict[
                    "bench_code_dd"] + " not being publicly traded, the change in value over time as well as the financial performance ratios below are predicted using algorithms. " + desc + " The AI prediction model, represented by the thin red line, further estimates that the " \
                                                                                                                                                                                               "current value of the firm is undervalued"
            else:
                desc = desc + " The AI prediction model, represented by the thin red line, estimates that the " \
                              "current value of the firm is undervalued"

        elif df_com_sim["close"].iloc[-1] < df_com["close"].iloc[-1]:
            if listed_bench == "No":
                desc = "Note, as a result of " + hidden_dict[
                    "bench_code_dd"] + " not being publicly traded, the change in value over time as well as the financial performance ratios below are predicted using algorithms. " + desc + " The AI prediction model, represented by the thin red line, further estimates that the " \
                                                                                                                                                                                               "current value of the firm is overvalued"
            else:
                desc = desc + " The AI prediction model, represented by the thin red line, estimates that the " \
                              "current value of the firm is overvalued"

    path = os.path.join(my_path, "data/stock/")
    df2 = pd.read_csv(path + "bench" + "_tick_df.csv")

    if listed == "No":
        if df2["mean"].iloc[-1] > df_com["close"].iloc[-1]:
            desc = "Note, as a result of " + hidden_dict[
                "target_code"] + " not being publicly traded, the change in value over time as well as the financial performance ratios below are predicted using algorithms.  " + desc + " The AI predicted value growth is higher than the industry benchmark."
        elif df2["mean"].iloc[-1] < df_com["close"].iloc[-1]:
            desc = "Note, as a result of " + hidden_dict[
                "target_code"] + " not being publicly traded, the change in value over time as well as the financial performance ratios below are predicted using algorithms.  " + desc + "  The AI predicted value growth is lower than the industry benchmark."

    desc = desc + ". Throughout this report the firms are referred to by their tickers or a 4 letter substitute. The terms Bench and Inds are used to describe the metrics " \
                  "of all 6 benchmark companies in aggregate."

    return desc


@app.callback(
    dash.dependencies.Output('snap_layout', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    layout = html.Div([
        html.H6(["Quarterly Snapshot"],
                className="gs-header gs-table-header padded"),

        snl.snap_dic(hidden_dict["target_code"], hidden_dict["bench_code_dd"])

    ], id="snap_layout"),

    return layout


@app.callback(
    dash.dependencies.Output('soma_media', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    layout = html.Div([
        html.Div([html.H6(["Social Stats"],
                          className="gs-header gs-table-header padded"),
                  ], style={"margin-bottom": "0.3cm"}),

        inp.social,
        html.Div([
            html.Br([], style={"margin": "0mm"}),
            som.social_dic(hidden_dict["target_code"], hidden_dict["bench_code_dd"])
        ], style={"margin": "1mm"}),
    ], style={"margin-top": "0.0cm"}, id="soma_media"),

    return layout

#
@app.callback(
    dash.dependencies.Output('title', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    title = str(hidden_dict["target_long_name"]) + " 4-D Report"
    return title
#

@app.callback(
    dash.dependencies.Output('location', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    # print(hidden_dict["dict_comp"])
    # print(hidden_dict["target_location_small_dd"])
    title = str(hidden_dict["target_location_address"]) + " Location"

    return title


"""
@app.callback(
    dash.dependencies.Output('profile', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    title = str(hidden_dict["target_code"]) + " Sentiment Profile"

    return title

"""


### RR

@app.callback(
    dash.dependencies.Output('final_rating', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    path = os.path.join(my_path, "data/closure/")

    fullar = pd.read_csv(path + "overall_rank_ts.csv")

    rating = round(fullar[fullar["ticker"] == hidden_dict["target_code"]]["Overall Rating"].iloc[-1], 1)
    rating = str(rating) + "/5"

    return rating


@app.callback(
    dash.dependencies.Output('mgmt_perf', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children')
     ])
def dadr(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    df_perf_summary = fm.fin_met(hidden_dict["target_code"], hidden_dict["bench_code_dd"])

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
            html.Td([hidden_dict["target_code"]], colSpan=4, style={'text-align': "center"}),
            html.Td([hidden_dict["bench_code_dd"]], colSpan=4, style={'text-align': "center"})
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
            html.Td([hidden_dict["target_code"]], colSpan=4, style={'text-align': "center"}),
            html.Td([hidden_dict["bench_code_dd"]], colSpan=4, style={'text-align': "center"})
        ], style={'background': 'white', 'font-weight': '600'}
        )
    )
    return modifed_perf_table


##
@app.callback(
    Output('filtered-content', 'children'),
    [dash.dependencies.Input('intermediate_value', 'children'),
     Input('category-filter', 'value'),
     Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter(hidden_dict, var, req, stu, ben):
    hidden_dict = json.loads(hidden_dict)

    print("POEEEE")
    dict_frames = ext_info_dict[hidden_dict["target_code"]]["Stock Dictionary"]
    df = dict_frames[ben, req, stu]

    highlight = list(df.drop("year", axis=1).columns.values)

    if stu in ["Normalised", "Original"]:
        highlight = list(df.ix[:, :5].columns.values)

    highlight = highlight + var
    figure = mc.create_figure(highlight, df, req, stu)

    for trace in figure['data']:
        trace['hoverinfo'] = 'text'

    return dcc.Graph(
        id='filtered-graph',
        figure=figure, config={'displayModeBar': False},
        style={'height': '250px'}
    )


@app.callback(
    Output('category-filter', 'options'),
    [dash.dependencies.Input('intermediate_value', 'children'),
     Input('request', 'value'),
     Input('study', 'value'),
     Input('bench', 'value')])
def filter(hidden_dict, req, stu, ben):
    # print(per, req, stu, ben)
    hidden_dict = json.loads(hidden_dict)

    dict_frames = ext_info_dict[hidden_dict["target_code"]]["Stock Dictionary"]
    df = dict_frames[ben, req, stu]
    highlight = list(df.drop("year", axis=1).columns.values)

    return [{'label': i, 'value': i} for i in highlight]


@app.callback(
    Output('graphed', 'figure'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bencher', 'value')])
def filter2(goo, time, many, norm, bench_code_dd):
    # print(per, req, stu, ben)

    figure = gc.chart_gd(goo, time, many, norm, bench_code_dd)

    ###
    return figure


@app.callback(
    Output('text_sum', 'value'),
    [Input('goo_ba', 'value'),
     Input('time', 'value'),
     Input('many', 'value'),
     Input('norm', 'value'),
     Input('bencher', 'value')])
def filter2(goo, time, many, norm, bench_code_dd):
    # print(per, req, stu, ben)

    figure = gc.sum_gd(goo, time, many, norm, bench_code_dd)
    return figure


######


@app.callback(Output('tab-output', 'children'),
              [Input('intermediate_value', 'children'),
               Input('tabs', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    d = cr.dic(target_code, hidden_dict["target_location_small_dd"])

    layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_overall"], config={'displayModeBar': False},
                                 style={"margin-top": "0mm", "height": "250px"})])
    if value == "Overall":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_overall"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm", "height": "250px"})])
    elif value == "Employee":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_emp"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm", "height": "250px"})])
    elif value == "Management":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_mgm"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm", "height": "250px"})])
    elif value == "Shareholders":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_sha"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm", "height": "250px"})])
    elif value == "Customers":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_cus"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm", "height": "250px"})])
    elif value == "Search":
        layout = html.Div([dcc.Graph(id='rating_chart', figure=d["fig_search"], config={'displayModeBar': False},
                                     style={"margin-top": "0mm", "height": "250px"})])

    return layout


@app.callback(Output('shares', 'children'),
              [Input('intermediate_value', 'children')])
def display_content(hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    listed = \
        input_fields[input_fields["code_or_ticker"] == hidden_dict["target_code"]]["listed"].reset_index(
            drop=True).values[
            0]
    if listed == "Yes":
        return shareholder
    else:
        return html.Div([])


@app.callback(Output('tab-output-shareholder', 'children'),
              [Input('intermediate_value', 'children'),
               Input('tabs-shareholder', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]

    if value == "Key Stats":
        layout = ksl.drad(hidden_dict["target_code"])
    elif value == "Competitors":
        layout = ksl.comp(hidden_dict["target_code"])

    return layout


@app.callback(Output('tab-output-social', 'children'),
              [Input('intermediate_value', 'children'),
               Input('tabs-social', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]

    lt, _ = sola.bra(target_code)

    if value == "Website":
        layout = lt
    elif value == "Finance Pattern":
        layout = mc.layout
    elif value == "Report":
        layout = inp.drop_steun

    else:
        layout = lt

    return layout


@app.callback(Output('tab-output-employee', 'children'),
              [Input('intermediate_value', 'children'),
               Input('tabs-employee', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    d = el.dic(target_code)
    l = ll.dic(target_code)
    c = cl.dic(target_code, hidden_dict["target_location_small_dd"])
    ###cra = cr.dic(target_code)
    layout = d["interview_layout"]
    # .bra(target_code)
    if value == "Interview":
        layout = d["interview_layout"]
    if value == "Key Stats":
        layout = ea.employ_an(target_code, hidden_dict["bench_code_dd"])
    elif value == "Sentiment":
        layout = gc.layout(target_code)

    elif value == "Compensation":
        layout = c["compensation_layout"]

    return layout


###
@app.callback(Output('fig_social', 'figure'),
              [dash.dependencies.Input('selector_dd', 'value')])
def display_content(value):
    _, fig = sola.bra(value)

    return fig


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

    ##l = ll.dic(target_code)
    ##c = cl.dic(target_code,hidden_dict["target_location_small_dd"])

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

    closest = ld.dic(target_code, bench_code_dd, target_location_file_name)

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

    i = cb.dic(options_value_target_location_small_dd, option_value_bench_code_dd,
               option_value_bench_location_dd, options_target_locations, options_bench_code, options_bench_locations,
               target_code, all_target_location_small_names, target_short_name, target_location_file_name)

    return i["info_layout_drop_downs"]


@app.callback(
    dash.dependencies.Output('bench_location_info', 'value'),
    [dash.dependencies.Input('benchmark_code_info', 'value'),
     dash.dependencies.Input('target_location_info', 'value'),
     dash.dependencies.Input('intermediate_value', 'children')], )
def dadr(bench_code_dd, city, hidden_dict):
    import layout.location_distance as ld

    # target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

    hidden_dict = json.loads(hidden_dict)

    target_code = hidden_dict["target_code"]

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

    closest = ld.dic(target_code, bench_code_dd, target_file_name)

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

    options_ben_loc = [{'label': r, 'value': i} for r, i in
                       zip(all_target_location_full_addresses, all_target_location_small_names)]

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
    print("target_location_small_dd")
    print(hidden_dict["target_location_small_dd"])

    ##l = ll.dic(target_code)
    ##c = cl.dic(target_code,hidden_dict["target_location_small_dd"])

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
    all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
    all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
    all_target_location_full_addresses_b = ext_info_dict[bench_code_dd]["All Target Location Full Addresses"]
    # coy = target_code
    # city = target_location_small_dd
    # bench_code_dd = bench_code_dd

    comp_ad_df = pd.DataFrame()
    comp_ad_df["all_target_location_file_names"] = all_target_location_file_names
    comp_ad_df["all_target_location_small_names"] = all_target_location_small_names
    comp_ad_df["all_target_location_full_addresses"] = all_target_location_full_addresses

    print("This seems to be working here")

    target_location_file_name = comp_ad_df[comp_ad_df["all_target_location_small_names"] == target_location_small_dd][
        "all_target_location_file_names"].reset_index(drop=True)[0]

    closest = ld.dic(target_code, bench_code_dd, target_location_file_name)

    print(closest)

    bench_code_dd_ad_df = pd.DataFrame()
    bench_code_dd_ad_df["all_target_location_file_names_b"] = all_target_location_file_names_b
    bench_code_dd_ad_df["all_target_location_small_names_b"] = all_target_location_small_names_b
    bench_code_dd_ad_df["all_target_location_full_addresses_b"] = all_target_location_full_addresses_b

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

    print("This Prints")

    return json.dumps(new_dict)


##
import layout.region_layout_couny_fig as rlf
import layout.region_layout_state_fig as rsl


@app.callback(
    dash.dependencies.Output('fig_target', 'figure'),
    [dash.dependencies.Input('rating_dd', 'value'),
     dash.dependencies.Input('county_state_dd', 'value'),
     dash.dependencies.Input('intermediate_value', 'children')
        , ])
def dadr(rating_dd, county_state_dd, hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    if county_state_dd == "County":

        target_code = hidden_dict["target_code"]

        target_short_name = \
            input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

        fig_target = rlf.figs_county(target_short_name, rating_dd)
        return fig_target
    else:
        target_code = hidden_dict["target_code"]
        target_short_name = \
            input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

        fig_target = rsl.figs_state(target_short_name, rating_dd)
        return fig_target


@app.callback(
    dash.dependencies.Output('fig_bench', 'figure'),
    [dash.dependencies.Input('benchmary_dd', 'value'),
     dash.dependencies.Input('rating_dd', 'value'),
     dash.dependencies.Input('county_state_dd', 'value'),
     dash.dependencies.Input('intermediate_value', 'children')
        , ])
def dadr(benchmary_dd, rating_dd, county_state_dd, hidden_dict):
    print("DDDDFDFF")
    hidden_dict = json.loads(hidden_dict)

    if county_state_dd == "County":

        print("DDDDFDFF")
        target_code = hidden_dict["target_code"]
        target_short_name = \
            input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

        bench_target = rlf.figs_county(benchmary_dd, rating_dd)
        return bench_target

    else:
        fig_target = rsl.figs_state(benchmary_dd, rating_dd)
        return fig_target


##
@app.callback(
    dash.dependencies.Output('tab-output-customer', 'children'),
    [Input('tabs-customer', 'value'),
     dash.dependencies.Input('hidden_output', 'children'),
     dash.dependencies.Input('bench_location_info', 'value'),
     dash.dependencies.Input('benchmark_code_info', 'value'),
     dash.dependencies.Input('target_location_info', 'value'),
     dash.dependencies.Input('intermediate_value', 'children')
        , ])
def dadr(value, dar, bench_location_info, benchmark_code_info, target_location_info, hidden_dict):
    import layout.location_distance as ld
    new_dict = json.loads(dar)

    hidden_dict = json.loads(hidden_dict)

    target_code = hidden_dict["target_code"]
    print("Enter")
    target_location_small_dd = target_location_info

    # target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

    bench_code_dd = benchmark_code_info

    all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]

    comp_ad_df = pd.DataFrame()  #
    comp_ad_df["all_target_location_file_names"] = all_target_location_file_names
    comp_ad_df["all_target_location_small_names"] = all_target_location_small_names
    comp_ad_df["all_target_location_full_addresses"] = all_target_location_full_addresses

    print(comp_ad_df["all_target_location_small_names"])

    target_location_file_name = \
        comp_ad_df[comp_ad_df["all_target_location_small_names"] == target_location_small_dd][
            "all_target_location_file_names"].reset_index(drop=True)[0]

    bench_code_dd_ad_df = pd.DataFrame()

    all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
    all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
    all_target_location_full_addresses_b = ext_info_dict[bench_code_dd][
        "All Target Location Full Addresses"]
    bench_code_dd_ad_df["all_target_location_file_names_b"] = all_target_location_file_names_b
    bench_code_dd_ad_df["all_target_location_small_names_b"] = all_target_location_small_names_b
    bench_code_dd_ad_df["all_target_location_full_addresses_b"] = all_target_location_full_addresses_b

    bench_location_file_name = \
        bench_code_dd_ad_df[bench_code_dd_ad_df["all_target_location_small_names_b"] == bench_location_info][
            "all_target_location_file_names_b"].reset_index(drop=True)[0]

    closest = ld.dic(target_code, bench_code_dd, target_location_file_name)

    option_value_bench_location_dd = \
        bench_code_dd_ad_df[bench_code_dd_ad_df["all_target_location_file_names_b"] == closest["name"]][
            "all_target_location_small_names_b"].reset_index(drop=True)[0]

    if value == "Area":
        try:
            print("Success")
            target_short_name = \
                input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

            bench_code_dd = benchmark_code_info
            target_location_small_dd = target_location_info

            bench_code_dd_ad_df = pd.DataFrame()

            all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
            all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
            all_target_location_full_addresses_b = ext_info_dict[bench_code_dd][
                "All Target Location Full Addresses"]
            bench_code_dd_ad_df["all_target_location_file_names_b"] = all_target_location_file_names_b
            bench_code_dd_ad_df["all_target_location_small_names_b"] = all_target_location_small_names_b
            bench_code_dd_ad_df["all_target_location_full_addresses_b"] = all_target_location_full_addresses_b

            ##l = ll.dic(target_code)
            ##c = cl.dic(target_code,hidden_dict["target_location_small_dd"])

            all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
            all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
            options_target_locations = [{'label': r, 'value': i} for r, i in
                                        zip(all_target_location_full_addresses, all_target_location_small_names)]

            all_benchmark_codes = ext_info_dict[target_code]["All Benchmark Codes"]
            all_benchmark_small_names = ext_info_dict[target_code]["All Benchmark Small Names"]
            options_bench_code = [{'label': r, 'value': i} for r, i in
                                  zip(all_benchmark_small_names, all_benchmark_codes)]

            all_target_location_full_addresses_b = ext_info_dict[bench_code_dd][
                "All Target Location Full Addresses"]
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

            comp_ad_df = pd.DataFrame()  #
            comp_ad_df["all_target_location_file_names"] = all_target_location_file_names
            comp_ad_df["all_target_location_small_names"] = all_target_location_small_names
            comp_ad_df["all_target_location_full_addresses"] = all_target_location_full_addresses

            print(comp_ad_df["all_target_location_small_names"])

            target_location_file_name = \
                comp_ad_df[comp_ad_df["all_target_location_small_names"] == target_location_small_dd][
                    "all_target_location_file_names"].reset_index(drop=True)[0]

            closest = ld.dic(target_code, bench_code_dd, target_location_file_name)

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

            bench_short_name = \
                input_fields[input_fields["code_or_ticker"] == bench_code_dd]["short_name"].reset_index(drop=True)[
                    0]

            option_value_bench_code_dd = bench_code_dd

            i = inl.dic(bench_short_name, options_value_target_location_small_dd, option_value_bench_code_dd,
                        option_value_bench_location_dd, options_target_locations, options_bench_code,
                        options_bench_locations,
                        target_code, all_target_location_small_names, target_short_name, target_location_file_name)

            layout = i["info_layout"]

        except:

            all_target_location_file_names_b = new_dict["all_target_location_file_names_b"]
            all_target_location_small_names_b = new_dict["all_target_location_small_names_b"]
            all_target_location_small_names = new_dict["all_target_location_small_names"]
            target_short_name = new_dict["target_short_name"]
            target_code = hidden_dict["target_code"]
            bench_code_dd = hidden_dict["bench_code_dd"]
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

            bench_short_name = \
                input_fields[input_fields["code_or_ticker"] == bench_code_dd]["short_name"].reset_index(drop=True)[0]

            i = inl.dic(bench_short_name, options_value_target_location_small_dd, option_value_bench_code_dd,
                        option_value_bench_location_dd, options_target_locations, options_bench_code,
                        options_bench_locations,
                        target_code, all_target_location_small_names, target_short_name, target_location_file_name)

            layout = i["info_layout"]

    if value == "Convenience":
        try:
            print("Success")
            target_short_name = \
                input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

            bench_code_dd = benchmark_code_info
            target_location_small_dd = target_location_info

            bench_code_dd_ad_df = pd.DataFrame()

            all_target_location_file_names_b = ext_info_dict[bench_code_dd]["All Target Location File Names"]
            all_target_location_small_names_b = ext_info_dict[bench_code_dd]["All Target Location Small Names"]
            all_target_location_full_addresses_b = ext_info_dict[bench_code_dd][
                "All Target Location Full Addresses"]
            bench_code_dd_ad_df["all_target_location_file_names_b"] = all_target_location_file_names_b
            bench_code_dd_ad_df["all_target_location_small_names_b"] = all_target_location_small_names_b
            bench_code_dd_ad_df["all_target_location_full_addresses_b"] = all_target_location_full_addresses_b

            bench_location_file_name = \
                bench_code_dd_ad_df[bench_code_dd_ad_df["all_target_location_small_names_b"] == bench_location_info][
                    "all_target_location_file_names_b"].reset_index(drop=True)[0]

            ##l = ll.dic(target_code)
            ##c = cl.dic(target_code)

            all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
            all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
            options_target_locations = [{'label': r, 'value': i} for r, i in
                                        zip(all_target_location_full_addresses, all_target_location_small_names)]

            all_benchmark_codes = ext_info_dict[target_code]["All Benchmark Codes"]
            all_benchmark_small_names = ext_info_dict[target_code]["All Benchmark Small Names"]
            options_bench_code = [{'label': r, 'value': i} for r, i in
                                  zip(all_benchmark_small_names, all_benchmark_codes)]

            all_target_location_full_addresses_b = ext_info_dict[bench_code_dd][
                "All Target Location Full Addresses"]
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

            comp_ad_df = pd.DataFrame()  #
            comp_ad_df["all_target_location_file_names"] = all_target_location_file_names
            comp_ad_df["all_target_location_small_names"] = all_target_location_small_names
            comp_ad_df["all_target_location_full_addresses"] = all_target_location_full_addresses

            print(comp_ad_df["all_target_location_small_names"])

            target_location_file_name = \
                comp_ad_df[comp_ad_df["all_target_location_small_names"] == target_location_small_dd][
                    "all_target_location_file_names"].reset_index(drop=True)[0]

            closest = ld.dic(target_code, bench_code_dd, target_location_file_name)

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
            new_dict["bench_location_file_name"] = bench_location_file_name
            new_dict["option_value_bench_location_dd"] = option_value_bench_location_dd

            # new_dict["Company City File"] = comp_ad_df["all_target_location_file_names"].reset_index(drop=True)[0]
            # new_dict["Benchmark City File"] = bench_code_dd_ad_df["all_target_location_file_names_b"].reset_index(drop=True)[0]

            new_dict["options_target_locations"] = options_target_locations
            new_dict["options_bench_code"] = options_bench_code
            new_dict["options_bench_locations"] = options_bench_locations

            options_value_target_location_small_dd = new_dict["options_value_target_location_small_dd"]

            bench_short_name = \
                input_fields[input_fields["code_or_ticker"] == bench_code_dd]["short_name"].reset_index(drop=True)[
                    0]

            option_value_bench_code_dd = bench_code_dd

            ye = yeil.dic(bench_short_name, options_value_target_location_small_dd, option_value_bench_code_dd,
                          option_value_bench_location_dd, options_target_locations, options_bench_code,
                          options_bench_locations,
                          target_code, all_target_location_small_names, target_short_name, bench_location_file_name,
                          target_location_file_name)

            tab = ye["table"]
            adds = ye["adds"]

            layout = html.Div([html.Br([]),

                               html.H6('Convenience Extract',
                                       className="gs-header gs-table-header padded", style={"margin-top": "0.6cm"}),

                               html.P("The right-hand side of the table is a selection of the restaurants closest in "
                                      "the vicinity of the target location. See the footer on this page to decipher the "
                                      "exact location of the short codes used in the table. Of more than 100 convenience indicators "
                                      "these were chosen as they were strongly associated with firm value and survivability. ",
                                      style={"margin-top": "0.2cm", "margin-bottom": "0.2cm"}),

                               html.Table(tab, id="mgmt_perf", className="reversed"),
                               html.H6('Overall Convenience',
                                       className="gs-header gs-table-header padded", style={"margin-top": "0.6cm"}),

                               # html.H5("Overall Convenience", style={'color': 'grey', 'margin': '0px 0px 0px 0px',
                               #                                      'padding': '0px 0px 0px 0px'}),

                               html.Hr(
                                   style={'color': 'grey', 'margin': '0px 0px 0px 0px', 'padding': '0px 0px 0px 0px'}),

                               dcc.Graph(figure=ye["fig_national"], id="4f",
                                         style={'border': '0', 'width': "100%"},
                                         config={'displayModeBar': False}
                                         ),

                               dcc.Graph(figure=ye["fig_local"], id="4g",
                                         style={'border': '0', 'width': "100%"},
                                         config={'displayModeBar': False}
                                         ),
                               html.Hr(
                                   style={'color': 'grey', 'margin': '6px 0px 0px 0px', 'padding': '5px 0px 5px 0px'}),

                               html.P(adds),
                               html.Hr(
                                   style={'color': 'grey', 'margin': '0px 0px 0px 0px', 'padding': '0px 0px 0px 0px'}),

                               ], style={'margin-top': '0.5cm'})


        except:

            bench_location_file_name = new_dict["bench_location_file_name"]
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

            bench_short_name = \
                input_fields[input_fields["code_or_ticker"] == bench_code_dd]["short_name"].reset_index(drop=True)[0]

            ye = yeil.dic(bench_short_name, options_value_target_location_small_dd, option_value_bench_code_dd,
                          option_value_bench_location_dd, options_target_locations, options_bench_code,
                          options_bench_locations,
                          target_code, all_target_location_small_names, target_short_name, bench_location_file_name,
                          target_location_file_name)

            tab = ye["table"]
            adds = ye["adds"]

            layout = html.Div([html.Br([]),

                               html.Table(tab, id="mgmt_perf", className="reversed"),

                               html.Hr([]),

                               dcc.Graph(figure=ye["fig_national"], id="4f",
                                         style={'margin-top': '-1.85cm', 'border': '0', 'width': "100%",
                                                'height': "280"},
                                         config={'displayModeBar': False}
                                         ),

                               dcc.Graph(figure=ye["fig_local"], id="4g",
                                         style={'margin-top': '-1.4cm', 'border': '0', 'width': "100%",
                                                'height': "280"},
                                         config={'displayModeBar': False}
                                         ),

                               html.P(adds)

                               ], style={'margin-top': '0.5cm'})


    elif value == "Map":

        comp_data = pd.DataFrame()
        all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
        all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
        comp_data["all_target_location_small_names"] = all_target_location_small_names
        comp_data["all_target_location_full_addresses"] = all_target_location_full_addresses
        target_location_add_info = comp_data[comp_data["all_target_location_small_names"] == target_location_info][
            "all_target_location_full_addresses"].reset_index(drop=True)[0]

        bench_data = pd.DataFrame()
        all_target_location_small_names = ext_info_dict[benchmark_code_info]["All Target Location Small Names"]
        all_target_location_full_addresses = ext_info_dict[benchmark_code_info]["All Target Location Full Addresses"]
        bench_data["all_target_location_small_names"] = all_target_location_small_names
        bench_data["all_target_location_full_addresses"] = all_target_location_full_addresses
        bench_location_add_info = bench_data[bench_data["all_target_location_small_names"] == bench_location_info][
            "all_target_location_full_addresses"].reset_index(drop=True)[0]

        m = ml.dic(target_code, target_location_add_info, benchmark_code_info, bench_location_add_info)

        layout = m["map_layout"]

    elif value == "State":

        print("Success")
        target_short_name = \
            input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

        bench_code_dd = benchmark_code_info
        target_location_small_dd = target_location_info

        bench_code_dd_ad_df = pd.DataFrame()

        all_benchmark_codes = list(ext_info_dict[target_code]["All Benchmark Codes"])
        all_benchmark_codes.append("All")
        all_benchmark_small_names = list(ext_info_dict[target_code]["All Benchmark Small Names"])
        all_benchmark_small_names.append("All")

        options_bench_code = [{'label': r, 'value': i} for r, i in
                              zip(np.array(all_benchmark_small_names), np.array(all_benchmark_small_names))]

        options_value_target_location_small_dd = new_dict["options_value_target_location_small_dd"]

        bench_short_name = \
            input_fields[input_fields["code_or_ticker"] == bench_code_dd]["short_name"].reset_index(drop=True)[
                0]

        option_value_bench_code_dd = bench_code_dd

        comp_data = pd.DataFrame()
        all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
        all_target_location_full_addresses = ext_info_dict[target_code]["All Target Location Full Addresses"]
        comp_data["all_target_location_small_names"] = all_target_location_small_names
        comp_data["all_target_location_full_addresses"] = all_target_location_full_addresses
        target_location_add_info = comp_data[comp_data["all_target_location_small_names"] == target_location_info][
            "all_target_location_full_addresses"].reset_index(drop=True)[0]

        bench_data = pd.DataFrame()
        all_target_location_small_names = ext_info_dict[benchmark_code_info]["All Target Location Small Names"]
        all_target_location_full_addresses = ext_info_dict[benchmark_code_info]["All Target Location Full Addresses"]
        bench_data["all_target_location_small_names"] = all_target_location_small_names
        bench_data["all_target_location_full_addresses"] = all_target_location_full_addresses
        bench_location_add_info = bench_data[bench_data["all_target_location_small_names"] == bench_location_info][
            "all_target_location_full_addresses"].reset_index(drop=True)[0]

        r = rl.dic(options_bench_code, target_code, benchmark_code_info)  #

        layout = r["region_layout"]

    if value == "Sent Score":
        dr = scl.sent_cust(target_code)

        layout = html.Div([html.Br([]),

                           dcc.Graph(figure=dr["quarter"], id="43s",
                                     style={'margin-top': '-1.45cm', 'border': '0', 'width': "100%", 'height': "160%"},
                                     config={'displayModeBar': False}
                                     )
                           ], style={'margin-top': '0.5cm'})

    if value == "Sentiment":

        dr = scl.sent_cust(target_code)

        layout = html.Div([html.Br([]),

                           dcc.Graph(figure=dr["full"], id="44f",
                                     style={'margin-top': '-1.45cm', 'border': '0', 'width': "100%", 'height': "80%"},
                                     config={'displayModeBar': False}
                                     ),
                           dcc.Graph(figure=dr["small"], id="44df",
                                     style={'margin-top': '-1.45cm', 'border': '0', 'width': "100%", 'height': "80%"},
                                     config={'displayModeBar': False}
                                     )
                           ], style={'margin-top': '0.5cm'})

    elif value == "Food":

        target_short_name = \
            input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]

        bench_code_dd = benchmark_code_info
        target_location_small_dd = target_location_info

        layout = tlcw.di(target_code, bench_code_dd, target_location_info, option_value_bench_location_dd,
                         "Most Popular")

    return layout


"""
@app.callback(Output('map_hidden', 'children'),
              [dash.dependencies.Input('bench_location_info', 'value'),
              dash.dependencies.Input('benchmark_code_info', 'value'),
              dash.dependencies.Input('target_location_info', 'value'),])
def update_datatable(bench_location_info,benchmark_code_info,target_location_info):
    dics = {}
    dics["bench_location_info"] = bench_location_info
    dics["benchmark_code_info"] = benchmark_code_info
    dics["target_location_info"]  = target_location_info

    return json.dumps(dics)

"""


@app.callback(
    dash.dependencies.Output('map_fig', 'figure'),
    [Input('map_table', 'rows'),
     Input('map_table', 'selected_row_indices')]
)
def dadr(rows, select_row_indices):
    import pandas as pd
    import _pickle as pickle
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")

    df = pd.DataFrame(rows)

    # df = pickle.load(open(path_in_ngrams + "map_dict.p", "rb"))

    df['text'] = df['target_small_name'] + '<br>Location ' + (df.index).astype(str) + \
                 '<br>Number of Reviewers ' + (df['Number of Reviewers']).astype(str) + \
                 '<br>Average Rating ' + (df['Female']).astype(str)

    df["Rate"] = df["Female"] ** 5

    limits = [(0, 2), (3, 10), (11, 20), (21, 50), (50, 3000)]

    colors = ["rgb(0,116,217)", "rgb(255,65,54)", "rgb(133,20,75)", "rgb(255,133,27)", "lightgrey", "purple", "green"]
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
                line={'width': '0.5', 'color': 'rgb(40,40,40)'},
                sizemode='area'
            ),
            name='{}'.format(i))
        cities.append(city)

    layout = dict(
        title='Competitive Map<br>(Size Indicates Rating)',
        showlegend=True,
        annotations=[dict(
            showarrow=True,
            text="Use the Colors Below <br> to Toggle the Selection",
            xanchor="right",
            yanchor="top",
            xshift=340,
            font=dict(
                color="black",
                size=12
            ),
            arrowcolor="black",
            arrowsize=0,
            arrowwidth=1,
            arrowhead=1,
            yshift=130,
            opacity=0.7,
            ax=20,
            ay=-80,
        ), dict(
            showarrow=True,
            text="Click on the Map <br> Tab to Reset",
            xanchor="right",
            yanchor="top",
            xshift=-110,
            yshift=170,
            opacity=0.7,
            ax=-105,
            ay=32,
            font=dict(
                color="black",
                size=12
            ),
            arrowcolor="black",
            arrowsize=0,
            arrowwidth=1,
            arrowhead=1,
        ),
            dict(
                showarrow=True,
                text="Double Click Map To <br> Reset The Size",
                xanchor="right",
                yanchor="top",
                xshift=-170,
                yshift=-40,
                opacity=0.7,
                ax=-20,
                ay=20,
                font=dict(
                    color="black",
                    size=12
                ),
                arrowcolor="black",
                arrowsize=0,
                arrowwidth=1,
                arrowhead=1,
            ),
            dict(
                text="Use the Table to <br>Further Toggle the Selection",
                textangle=0,
                font=dict(
                    color="black",
                    size=12
                ),
                arrowcolor="black",
                arrowsize=0,
                arrowwidth=1,
                arrowhead=1,
                xshift=275,
                yshift=-125,
                opacity=0.7,
                ax=20,
                ay=-60,
            )],
        #
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

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'annotations': [], 'updatemenus': []}],
                    label='Remove Annotations',
                    method='relayout'
                ),
            ]),

            direction='left',
            pad={'r': -100, 't': -90},
            showactive=True,
            type='buttons',
            x=-20,
            xanchor='left',
            # y=button_layer_2_height,
            yanchor='top'
        )])

    layout['updatemenus'] = updatemenus

    fig = dict(data=cities, layout=layout)

    return fig


@app.callback(Output('data_table_hide', 'children'), [Input('tabs-areas', 'value')], )
def update_datatable(value):
    if value == "Description":
        layout = html.Div([
            html.H5(
                ("Highlighting customer experience between " +
                 " location" + ", and the closest benchmark location " + " location at the local and national level. ").title(),
                style={'font-size': '14px', 'margin-top': '-1.1cm', 'display': 'none'}),

        ], id="description_writ")
        return layout


@app.callback(Output('two_frames', 'children'), [Input('first_radio', 'value'),
                                                 dash.dependencies.Input('intermediate_value', 'children')],
              [dash.dependencies.State('bench_location_info', 'value'),
               dash.dependencies.State('benchmark_code_info', 'value'),
               dash.dependencies.State('target_location_info', 'value'), ])
def update_datatable(radio, hidden_dict, bench_location_info, benchmark_code_info, target_location_info):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")
    cutomer_area_dict = pickle.load(open(path_in_ngrams + "cutomer_area_dict.p", "rb"))

    if radio == "Most Ordered":
        fally = "Most Popular"

    if radio == "Best Rated":
        fally = "Most Loved"

        print("tallla")

    d_target = target_location_info

    d_bench = bench_location_info

    target = target_code

    bench = benchmark_code_info

    return tlcs.di(target, bench, d_target, d_bench, fally)


@app.callback(Output('empc_plot', 'figure'), [Input('employee_dd', 'value')],
              )
def update_datatable(value):
    if value == "Employee Level":
        figure = eaf.fig_level

    if value == "Monthly Activity":
        figure = eaf.fig_month

    return figure


@app.callback(Output('datatable', 'rows'),
              [Input('tabs-areas', 'value'), dash.dependencies.Input('intermediate_value', 'children')],
              [dash.dependencies.State('bench_location_info', 'value'),
               dash.dependencies.State('benchmark_code_info', 'value'),
               dash.dependencies.State('target_location_info', 'value'), ])
def update_datatable(second_tab, hidden_dict, bench_location_info, benchmark_code_info, target_location_info):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")
    cutomer_area_dict = pickle.load(open(path_in_ngrams + "cutomer_area_dict.p", "rb"))

    if second_tab == "Area":
        df = cad.darn(target_location_info, benchmark_code_info, bench_location_info)
        df = df.reset_index()
        df = df.rename(columns={'index': 'Description'})

    if second_tab == "Company":
        df = cutomer_area_dict[target_code]
        df = df.reset_index()
        df = df.rename(columns={'Addresses': 'Address'})

    if second_tab == "Bench":
        df = cutomer_area_dict[benchmark_code_info]
        df = df.reset_index()
        df = df.rename(columns={'Addresses': 'Address'})

    if second_tab == "Description":
        return None

    return df.to_dict('records')


@app.callback(Output('tab-output-interview-bottom', 'children'),
              [Input('intermediate_value', 'children'),
               Input('tabs-interview-bottom', 'value')])
def display_content(hidden_dict, value):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    d = el.dic(target_code)
    layout = d["interview_layout_accepted"]

    if value == "Accepted":
        layout = d["interview_layout_accepted"]
    elif value == "Positive":
        layout = d["interview_layout_positive"]
    elif value == "Negative":
        layout = d["interview_layout_negative"]
    elif value == "Difficult":
        layout = d["interview_layout_difficult"]
    elif value == "Easy":
        layout = d["interview_layout_easy"]

    return layout


@app.callback(Output('tab-output-language', 'children'),
              [Input('drops-language', 'value')],
              [dash.dependencies.State('intermediate_value', 'children')])
def display_content(value, hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    d = el.dic(target_code)
    l = ll.dic(target_code)
    ##c = cl.dic(target_code,hidden_dict["target_location_small_dd"])

    layout = l["four_figs_layout"]

    if value == "Noun":
        layout = l["four_figs_layout"]
    elif value == "Phrase":
        layout = l["phrase_layout"]
    elif value == "Sentiment":
        layout = d["interview_layout_negative"]
    elif value == "Map":
        layout = d["interview_layout_easy"]

    return layout


@app.callback(Output('tab-output-compensation', 'children'),
              [Input('drops-compensation', 'value')],
              [dash.dependencies.State('intermediate_value', 'children'), ])
def display_content(value, hidden_dict):
    hidden_dict = json.loads(hidden_dict)
    target_code = hidden_dict["target_code"]
    l = ll.dic(target_code)
    c = cl.dic(target_code, hidden_dict["target_location_small_dd"])

    layout = l["four_figs_layout"]

    if value == "Benefits":
        layout = c["benefits_layout"]
    elif value == "Salaries":
        layout = c["benefits_layout"]
    elif value == "Third":
        layout = c["benefits_layout"]

    return layout


# Our main function
if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server()