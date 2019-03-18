import dash_core_components as dcc
import dash_html_components as html
import pickle
import layout.chart_ratings as cr
import os
import pandas as pd

# NB never define any variable as path, that screws few things up.

my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_cpickle = os.path.join(my_path, "../data/cpickle/")

#input_fields = pd.read_csv(path)

#code = input_fields["code_or_ticker"]#

def dic(code,small):

    p = code

    dict_ben = pickle.load(open(path_in_cpickle + p + "_benefits.p", "rb"))
    d = cr.dic(p,small)
    benefits_layout =   \
        html.Div([
            html.H5("Compensation Sentiment"),
            html.P("The below chart presents the sentiment of the company in blue, and the average movement in orange. For comparison "
                   "purposes the green line includes the sentiment of all the benchmarks (seven firms) over time. Below the chart is direct summaries"
                   " that have been extracted from the reviews with AI tools."),

            html.Div([dcc.Graph(id='benefits_chart', figure=d["fig_ben"], config={'displayModeBar': False},
                                    style={'position': 'relative','width': '100%','height': '330px', 'top': '-45px','bottom': '0px','left': '0px'})]
                     , style={'width': '100%', 'height':'330px', 'overflow': 'hidden'}),

            html.Div([

                html.H5("Positive Summary",style={'padding-top':'30px'}),
                html.Div([dcc.Textarea(id='pos_int_sum', placeholder='Summary', value=dict_ben["positive"], style={'width': '100%', 'height':'115px'}
                                ),], style={'padding-top':'25px','clear':'both'}),

                html.H5("Negative Summary"),
                html.Div([dcc.Textarea(id='pos_int_sum', placeholder='Summary', value=dict_ben["negative"],
                                       style={'width': '100%', 'height': '115px'}
                                       ), ], style={'padding-top': '25px', 'clear': 'both'}),
                     ],style={'position': 'relative', 'top': '-65px','bottom': '0px','left': '0px'})

                ],style={'margin-top':'-1.2cm'})


    compensation_layout = html.Div([

        html.Br([]),
        html.Br([]),

        html.Div([

        html.Br([]),
        html.Br([])

        ],),

            html.Div([
                    html.Div(benefits_layout, id='tab-output-compensation')
                        ], style={
                            'width': '100%',
                            'fontFamily': 'Sans-Serif',
                            'margin-left': 'auto',
                            'margin-right': 'auto'
                        }),])

    d = {}
    d["benefits_layout"] = benefits_layout
    d["compensation_layout"] = compensation_layout

    return d


