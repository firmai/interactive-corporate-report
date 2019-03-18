
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



def dict(option_value_bench_code_dd, options_target_locations,target_code, target_location_file_name):

    import _pickle as pickle
    import pandas as pd

    print(target_location_file_name)
    print(options_target_locations)

    closest = ld.dict(target_code, option_value_bench_code_dd, target_location_file_name)

    agg = pickle.load(open(path_in_ngrams + "figures_dict_agg.p", "rb"))

    fig_d_n = agg[target_code]

    fig_b_n = agg[option_value_bench_code_dd]

    # Local

    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_" + target_code + ".p", "rb"))

    fig_d = figures_dict[target_code, target_location_file_name]

    figures_dict_b = pickle.load(open(path_in_ngrams + "figures_dict_" + option_value_bench_code_dd + ".p", "rb"))

    fig_b = figures_dict_b[option_value_bench_code_dd, closest["name"]]


    info_table_layout =  html.Div([

            html.Div([

                html.Div([

                    html.H5("Description"),
                    html.Div([

                        html.Div([
                            html.Br([]),
                            html.Br([]),
                            html.H5("Reviewers", id='info_1',style={'margin-top':'8px','font-size':'22px', 'color':'gray'}),
                            html.H5("Network", style={'font-size':'22px', 'color':'gray'}),
                            html.H5("Patron",style={'font-size':'22px', 'color':'gray'}),
                            html.H5("Connoisseur",style={'font-size':'22px', 'color':'gray'})

                        ])

                    ],),
                ], style={'display': 'table-cell', 'width': '150px'}),

                html.Div([


                    html.H5("Local"),
                    html.Div([

                        html.Div([
                            html.H5("Company",style={'color':'gray'}),

                            html.H5("{:,}".format(fig_d["Number of Reviewers"]),id='info_1',style={'font-size':'22px','color':fig_d["Number of Reviewers","color"]}),
                            html.H5("{:,}".format(fig_d["Total Network"]),id='info_1',style={'font-size':'22px', 'color':fig_d["Total Network","color"]}),
                            html.H5(str(round(fig_d["Patrons"], 2)),style={'font-size':'22px', 'color':fig_d["Patrons","color"]}),
                            html.H5(str(round(fig_d["Connoisseur"], 2)),style={'font-size':'22px', 'color':fig_d["Connoisseur","color"]})

                        ],style={'display': 'table-cell','width':'175px'}),

                        html.Div([
                            html.H5("Bench  ",style={'color':'gray'}),
                            html.H5("{:,}".format(fig_b["Number of Reviewers"]),id='info_1',style={'font-size':'22px', 'color':fig_b["Number of Reviewers","color"]}),
                            html.H5("{:,}".format(fig_b["Total Network"]),id='info_1',style={'font-size':'22px', 'color':fig_b["Total Network","color"]}),
                            html.H5(str(round(fig_b["Patrons"], 2)),style={'font-size':'22px', 'color':fig_b["Patrons","color"]}),
                            html.H5(str(round(fig_b["Connoisseur"], 2)),style={'font-size':'22px', 'color':fig_b["Connoisseur","color"]}),

                        ],style={'display': 'table-cell'}),

                    ],style={'display': 'table'}),
                         ],style={'display': 'table-cell','width':'200px'}),

                    html.Div([


                    html.H5(""),
                    html.Div([

                        html.Div([
                            html.H5(""),

                        ],style={'display': 'table-cell','width':'175px'}),

                        html.Div([

                        ],style={'display': 'table-cell'}),

                    ],style={ 'display': 'table'}),
                         ],style={'display': 'table-cell','width':'40px'}),

                html.Div([

                    html.H5("National"),
                    html.Div([

                        html.Div([
                            html.H5("Company",style={'color':'gray'}),
                            html.H5("{:,}".format(int(fig_d_n["Number of Reviewers"])),id='info_1',style={'font-size':'22px','color':fig_d_n["Number of Reviewers","color"]}),
                            html.H5("{:,}".format(int(fig_d_n["Total Network"])),id='info_1',style={'font-size':'22px','color':fig_d_n["Number of Reviewers","color"]}),
                            html.H5(str(round(fig_d_n["Patrons"], 2)),style={'font-size':'22px','color':fig_d_n["Number of Reviewers","color"]}),
                            html.H5(str(round(fig_d_n["Connoisseur"], 2)),style={'font-size':'22px','color':fig_d_n["Number of Reviewers","color"]}),

                        ], style={'display': 'table-cell', 'width': '175px'}),

                        html.Div([
                            html.H5("Bench",style={'color':'gray'}),
                            html.H5("{:,}".format(int(fig_b_n["Number of Reviewers"])),id='info_1',style={'font-size':'22px', 'color':fig_b_n["Number of Reviewers","color"]}),
                            html.H5("{:,}".format(int(fig_b_n["Total Network"])),id='info_1',style={'font-size':'22px', 'color':fig_b_n["Number of Reviewers","color"]}),
                            html.H5(str(round(fig_b_n["Patrons"], 2)),style={'font-size':'22px', 'color':fig_b_n["Number of Reviewers","color"]}),
                            html.H5(str(round(fig_b_n["Connoisseur"], 2)),style={'font-size':'22px', 'color':fig_b_n["Number of Reviewers","color"]}),

                        ], style={'display': 'table-cell'}),

                    ], style={ 'display': 'table'}),
                        ],style={'display': 'table-cell'}),

                    ],style={'display': 'table','margin-top':'-0.5cm'})

                ],style={'margin-top': '0.5cm'}),



    interview_layout_accepted =   html.Div([
                dcc.Graph(id='offer_figs', figure=di.offer_fig, config={'displayModeBar': False},
                          style={'position': 'relative', 'top': '-14px','left': '-110px'})

                     ], style={'width': '100%', 'height': '430px', 'overflow': 'hidden'})


    import pickle
    import pandas as pd


    rents = pickle.load(open(path_in_ngrams + target_code+"_gd_rents.p", "rb"))

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
    d["info_table_layout"] = info_table_layout
    d["interview_layout_accepted"] =interview_layout_accepted
    d["interview_layout_negative"] =interview_layout_negative
    d["interview_layout_positive"] =interview_layout_positive
    d["interview_layout_difficult"] =interview_layout_difficult
    d["interview_layout_easy"] =interview_layout_easy

    return d
