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




#def dict(firm_location, benchmark, bench_location, firm_location_options,benchmark_options,bench_location_options, code_start,a_small_names):

def dict(bench_short_name, options_value_target_location_small_dd, option_value_bench_code_dd,
                 option_value_location_dd, options_target_locations,options_bench_code,options_bench_locations,
                 target_code, all_target_location_small_names, target_short_name, target_location_file_name):
    import pandas as pd


    import _pickle as pickle
    import pandas as pd

    print(target_location_file_name)
    print(options_target_locations)

    RECORDS = [
        {'Input': '', 'Output': ''}
        for i in range(100)
    ]


    if second_tab == "Area":
        df = RECORDS

    if second_tab == "Company":
        df = RECORDS

    if second_tab == "Bench":
        df = RECORDS


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



    area_layout = html.Div([
        html.Div([

            dcc.Tabs(
                tabs=[{'label': "Area", 'value': "Area"},
                      {'label': "Company", 'value': "Company"},
                      {'label': "Bench", 'value': "Bench"},
                      ],
                value="Area",
                id='tabs-areas'
            ),
        ], style={
            'width': '100%',
            'height': '10%',
            'fontFamily': 'Sans-Serif',
            'margin-left': 'auto',
            'margin-top': '-0.5cm',
            'margin-right': 'auto'
        }),

        dt.DataTable(
            rows=RECORDS,
            row_selectable=True,
            filterable=True,
            sortable=True,
            # optional - sets the order of columns
            columns=['Input', 'Output'],
            id='datatable'
        ),

    ])

    info_layout = html.Div([


        html.Div([

            html.Div([
                html.Br([]),
                html.Br([]),
                html.Hr(style={'padding-top': '0.15cm', 'padding-bottom': '0.0cm', 'margin-top': '-0.2cm'}),


            ]),

            html.Div([


                html.Div([

                    html.H5("Description"),
                    html.Div([

                        html.Div([
                            html.Br([]),
                            html.Br([]),
                            html.H5("Reviewers", id='info_1',
                                    style={'margin-top': '8px', 'font-size': '22px', 'color': 'gray'}),
                            html.H5("Network", style={'font-size': '22px', 'color': 'gray'}),
                            html.H5("Patron", style={'font-size': '22px', 'color': 'gray'}),
                            html.H5("Connoisseur", style={'font-size': '22px', 'color': 'gray'})

                        ])

                    ], ),
                ], style={'display': 'table-cell', 'width': '150px'}),

                html.Div([

                    html.H5("Local"),
                    html.Div([

                        html.Div([
                            html.H5("Company", style={'color': 'gray'}),

                            html.H5("{:,}".format(fig_d["Number of Reviewers"]), id='info_1',
                                    style={'font-size': '22px', 'color': fig_d["Number of Reviewers", "color"]}),
                            html.H5("{:,}".format(fig_d["Total Network"]), id='info_1',
                                    style={'font-size': '22px', 'color': fig_d["Total Network", "color"]}),
                            html.H5(str(round(fig_d["Patrons"], 2)),
                                    style={'font-size': '22px', 'color': fig_d["Patrons", "color"]}),
                            html.H5(str(round(fig_d["Connoisseur"], 2)),
                                    style={'font-size': '22px', 'color': fig_d["Connoisseur", "color"]})

                        ], style={'display': 'table-cell', 'width': '175px'}),

                        html.Div([
                            html.H5("Bench  ", style={'color': 'gray'}),
                            html.H5("{:,}".format(fig_b["Number of Reviewers"]), id='info_1',
                                    style={'font-size': '22px', 'color': fig_b["Number of Reviewers", "color"]}),
                            html.H5("{:,}".format(fig_b["Total Network"]), id='info_1',
                                    style={'font-size': '22px', 'color': fig_b["Total Network", "color"]}),
                            html.H5(str(round(fig_b["Patrons"], 2)),
                                    style={'font-size': '22px', 'color': fig_b["Patrons", "color"]}),
                            html.H5(str(round(fig_b["Connoisseur"], 2)),
                                    style={'font-size': '22px', 'color': fig_b["Connoisseur", "color"]}),

                        ], style={'display': 'table-cell'}),

                    ], style={'display': 'table'}),
                ], style={'display': 'table-cell', 'width': '200px'}),

                html.Div([

                    html.H5(""),
                    html.Div([

                        html.Div([
                            html.H5(""),

                        ], style={'display': 'table-cell', 'width': '175px'}),

                        html.Div([

                        ], style={'display': 'table-cell'}),

                    ], style={'display': 'table'}),
                ], style={'display': 'table-cell', 'width': '40px'}),

                html.Div([

                    html.H5("National"),
                    html.Div([

                        html.Div([
                            html.H5("Company", style={'color': 'gray'}),
                            html.H5("{:,}".format(int(fig_d_n["Number of Reviewers"])), id='info_1',
                                    style={'font-size': '22px', 'color': fig_d_n["Number of Reviewers", "color"]}),
                            html.H5("{:,}".format(int(fig_d_n["Total Network"])), id='info_1',
                                    style={'font-size': '22px', 'color': fig_d_n["Number of Reviewers", "color"]}),
                            html.H5(str(round(fig_d_n["Patrons"], 2)),
                                    style={'font-size': '22px', 'color': fig_d_n["Number of Reviewers", "color"]}),
                            html.H5(str(round(fig_d_n["Connoisseur"], 2)),
                                    style={'font-size': '22px', 'color': fig_d_n["Number of Reviewers", "color"]}),

                        ], style={'display': 'table-cell', 'width': '175px'}),

                        html.Div([
                            html.H5("Bench", style={'color': 'gray'}),
                            html.H5("{:,}".format(int(fig_b_n["Number of Reviewers"])), id='info_1',
                                    style={'font-size': '22px', 'color': fig_b_n["Number of Reviewers", "color"]}),
                            html.H5("{:,}".format(int(fig_b_n["Total Network"])), id='info_1',
                                    style={'font-size': '22px', 'color': fig_b_n["Number of Reviewers", "color"]}),
                            html.H5(str(round(fig_b_n["Patrons"], 2)),
                                    style={'font-size': '22px', 'color': fig_b_n["Number of Reviewers", "color"]}),
                            html.H5(str(round(fig_b_n["Connoisseur"], 2)),
                                    style={'font-size': '22px', 'color': fig_b_n["Number of Reviewers", "color"]}),

                        ], style={'display': 'table-cell'}),

                    ], style={'display': 'table'}),
                ], style={'display': 'table-cell'}),

            ], style={'display': 'table', 'margin-top': '-1cm'})

        ], style={'margin-top': '0.5cm'}),

        html.Div([

            html.Div([
                html.Hr(style={'padding-top': '0.26cm', 'padding-bottom': '0.0cm', 'margin-top': '-0.0cm'}),
                html.H5("Customer experience between " + target_short_name +" - " +options_value_target_location_small_dd +
                        " location" + ", and " + bench_short_name + " - " + option_value_location_dd +" location at the local and national level. ",
                        style={'font-size': '14px','margin-top': '-1.1cm'}),
                html.Hr(style={'padding-top': '0.15cm', 'padding-bottom': '0.26cm', 'margin-top': '-0.0cm'})
            ], ),

        ]),



    ])



    interview_layout_accepted = html.Div([
        dcc.Graph(id='offer_figs', figure=di.offer_fig, config={'displayModeBar': False},
                  style={'position': 'relative', 'top': '-14px', 'left': '-110px'})

    ], style={'width': '100%', 'height': '430px', 'overflow': 'hidden'})

    import pickle
    import pandas as pd

    rents = pickle.load(open(path_in_ngrams + target_code + "_gd_rents.p", "rb"))

    neg_que = rents["Negative", "questions"]

    neg_com = rents["Negative", "comments"]

    mkdwn = ""
    fr = 0
    for i in neg_que:
        fr = fr + 1
        if fr <= 5:
            cos = "###### " + str(fr) + ". " + i + "\n"
            mkdwn = mkdwn + cos

    interview_layout_negative = \
        html.Div([

            html.H5("Summary"),
            html.Div([dcc.Textarea(id='neg_int_sum', placeholder='Summary', value=neg_com,
                                   style={'width': '98%', 'height': '140px'}
                                   )], style={'padding-top': '25px', 'clear': 'both'}),
            html.H5("Top Questions", style={'padding-bottom': '25px'}),
            dcc.Markdown(mkdwn

                         )

        ], style={'position': 'relative', 'left': '20px'})

    ## Positive

    pos_que = rents["Positive", "questions"]

    pos_com = rents["Positive", "comments"]

    mkdwn = ""
    fr = 0
    for i in pos_que:
        fr = fr + 1
    if fr <= 5:
            cos = "###### " + str(fr) + ". " + i + "\n"
            mkdwn = mkdwn + cos

    interview_layout_positive = \
        html.Div([

            html.H5("Summary"),
            html.Div([dcc.Textarea(id='pos_int_sum', placeholder='Summary', value=pos_com,
                                   style={'width': '98%', 'height': '140px'}
                                   )], style={'padding-top': '25px', 'clear': 'both'}),
            html.H5("Top Questions", style={'padding-bottom': '25px'}),
            dcc.Markdown(mkdwn

                         )

        ], style={'position': 'relative', 'left': '20px'})

    # Difficult

    dif_que = rents["Difficult", "questions"]

    dif_com = rents["Difficult", "comments"]

    mkdwn = ""
    fr = 0
    for i in dif_que:
        fr = fr + 1
    if fr <= 5:
        cos = "###### " + str(fr) + ". " + i + "\n"
    mkdwn = mkdwn + cos

    interview_layout_difficult = \
        html.Div([

            html.H5("Summary"),
            html.Div([dcc.Textarea(id='dif_int_sum', placeholder='Summary', value=dif_com,
                                   style={'width': '98%', 'height': '140px'}
                                   )], style={'padding-top': '25px', 'clear': 'both'}),
            html.H5("Top Questions", style={'padding-bottom': '25px'}),
            dcc.Markdown(mkdwn

                         )

        ], style={'position': 'relative', 'left': '20px'})

    # Easy

    eas_que = rents["Easy", "questions"]

    eas_com = rents["Easy", "comments"]

    mkdwn = ""
    fr = 0
    for i in eas_que:
        fr = fr + 1
    if fr <= 5:
        cos = "###### " + str(fr) + ". " + i + "\n"
    mkdwn = mkdwn + cos

    interview_layout_easy = \
        html.Div([

            html.H5("Summary"),
            html.Div([dcc.Textarea(id='eas_int_sum', placeholder='Summary', value=eas_com,
                                   style={'width': '98%', 'height': '140px'}
                                   )], style={'padding-top': '25px', 'clear': 'both'}),
            html.H5("Top Questions", style={'padding-bottom': '25px'}),
            dcc.Markdown(mkdwn

                         )

        ], style={'position': 'relative', 'left': '20px'})

    d = {}
    d["info_layout"] = info_layout
    d["interview_layout_accepted"] = interview_layout_accepted
    d["interview_layout_negative"] = interview_layout_negative
    d["interview_layout_positive"] = interview_layout_positive
    d["interview_layout_difficult"] = interview_layout_difficult
    d["interview_layout_easy"] = interview_layout_easy

    return d





