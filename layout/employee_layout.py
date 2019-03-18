import layout.donuts_interview as di
import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc
import dash_html_components as html

import os


def dic(c):

    my_path = os.path.abspath(os.path.dirname(__file__))
    path_2 = os.path.join(my_path, "../input_fields.csv")
    path_in_pickle = os.path.join(my_path, "../data/cpickle/")

    #input_fields = pd.read_csv(path)

    #code = input_fields["code_or_ticker"]

    p = c

    #p = "BJRI"

    difficulty_fig, experience_fig, offer_fig = di.donuts_fig(p)

    interview_layout = html.Div([

                html.Div([

                    html.Div([
                        dcc.Graph(id='difficulty_figs', figure=difficulty_fig, config={'displayModeBar': False})

                    ], style={'float': 'left'}),

                    html.Div([
                        dcc.Graph(id='experience_figs', figure=experience_fig, config={'displayModeBar': False})
                    ], style={'float': 'left'})

                ], style={'float': 'left'}),


                html.Div([
                    html.Div(
                    dcc.Tabs(
                        tabs=[{'label':"Accepted Job Offer" , 'value':"Accepted" },
                              {'label':"Positive Interview" , 'value':"Positive" },
                              {'label':"Negative Interview" , 'value':"Negative" },
                              {'label':"Difficult Interview" , 'value':"Difficult" },
                              {'label':"Easy Interview" , 'value':"Easy" },
                        ],
                        value="Accepted",
                        id='tabs-interview-bottom',
                        vertical=True,
                        style={
                            'height': '18vh',
                            'borderRight': 'thin lightgrey solid',
                            'textAlign': 'left' }
                    ),
                style={'width': '20%', 'float': 'left'}
                    ),
                  html.Div(
                    html.Div(id='tab-output-interview-bottom'),
                        style={
                            'width': '80%',
                            'float': 'right'
                        })
                ],
                        style={
                                'fontFamily': 'Sans-Serif',
                                'margin-left': 'auto',
                                'margin-right': 'auto'
                        }
                )

    ])


    interview_layout_accepted =   html.Div([
                    dcc.Graph(id='offer_figs', figure=offer_fig, config={'displayModeBar': False},
                              style={'position': 'relative', 'top': '-14px','left': '-110px'})

                         ], style={'width': '100%', 'height': '430px', 'overflow': 'hidden'})


    import _pickle as pickle
    import pandas as pd

    path_in_pickle = os.path.join(my_path, "../data/interviews/")

    rents = pickle.load(open(path_in_pickle+ p+ "_interview.p", "rb"))

    neg_que = rents["Negative", "questions"]

    neg_com = rents["Negative", "comments"]

    mkdwn = ""
    fr = 0
    for i in neg_que:
        fr = fr +1
        if fr <= 5:
            cos = "###### " +str(fr) +". " + i + "\n"
            mkdwn = mkdwn + cos

    interview_layout_negative =   \
        html.Div([

            html.H5("Summary"),
            html.Div([dcc.Textarea(id='neg_int_sum', placeholder='Summary', value=neg_com, style={'width': '98%', 'height':'140px'}
                            )], style={'padding-top':'25px','clear':'both'}),
            html.H5("Top Questions", style={'padding-bottom':'25px'}),
            dcc.Markdown(mkdwn

            )

                ],style={'position': 'relative','left': '20px'})


    ## Positive

    pos_que = rents["Positive", "questions"]

    pos_com = rents["Positive", "comments"]

    mkdwn = ""
    fr = 0
    for i in pos_que:
        fr = fr +1
        if fr <= 5:
            cos = "###### " +str(fr) +". " + i + "\n"
            mkdwn = mkdwn + cos

    interview_layout_positive =   \
        html.Div([

            html.H5("Summary"),
            html.Div([dcc.Textarea(id='pos_int_sum', placeholder='Summary', value=pos_com, style={'width': '98%', 'height':'140px'}
                            )], style={'padding-top':'25px','clear':'both'}),
            html.H5("Top Questions", style={'padding-bottom':'25px'}),
            dcc.Markdown(mkdwn

            )

                ],style={'position': 'relative','left': '20px'})


    # Difficult

    dif_que = rents["Difficult", "questions"]

    dif_com = rents["Difficult", "comments"]

    mkdwn = ""
    fr = 0
    for i in dif_que:
        fr = fr +1
        if fr <= 5:
            cos = "###### " +str(fr) +". " + i + "\n"
            mkdwn = mkdwn + cos

    interview_layout_difficult =   \
        html.Div([

            html.H5("Summary"),
            html.Div([dcc.Textarea(id='dif_int_sum', placeholder='Summary', value=dif_com, style={'width': '98%', 'height':'140px'}
                            )], style={'padding-top':'25px','clear':'both'}),
            html.H5("Top Questions", style={'padding-bottom':'25px'}),
            dcc.Markdown(mkdwn

            )

                ],style={'position': 'relative','left': '20px'})

    # Easy

    eas_que = rents["Easy", "questions"]

    eas_com = rents["Easy", "comments"]

    mkdwn = ""
    fr = 0
    for i in eas_que:
        fr = fr +1
        if fr <= 5:
            cos = "###### " +str(fr) +". " + i + "\n"
            mkdwn = mkdwn + cos

    interview_layout_easy =   \
        html.Div([

            html.H5("Summary"),
            html.Div([dcc.Textarea(id='eas_int_sum', placeholder='Summary', value=eas_com, style={'width': '98%', 'height':'140px'}
                            )], style={'padding-top':'25px','clear':'both'}),
            html.H5("Top Questions", style={'padding-bottom':'25px'}),
            dcc.Markdown(mkdwn

            )

                ],style={'position': 'relative','left': '20px'})

    d = {}
    d["interview_layout"] = interview_layout
    d["interview_layout_accepted"] = interview_layout_accepted
    d["interview_layout_positive"] = interview_layout_positive
    d["interview_layout_negative"] = interview_layout_negative
    d["interview_layout_difficult"] = interview_layout_difficult
    d["interview_layout_easy"] = interview_layout_easy

    return  d