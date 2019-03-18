import dash_html_components as html
import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *

import dash
from dash.dependencies import Input, Output
#import dash_core_components2 as dcc2
import dash_core_components as dcc

def drad(coy):



    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]],style={"width":"25.4px"}))
            table.append(html.Tr(html_row,style={"width":"25.4px"}))
        return table

    def make_dash_big(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]],style={"height":"25.4px"}))
            table.append(html.Tr(html_row))
        return table


    import _pickle as pickle
    import os
    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")

    dict_metrics = pickle.load(open(path_in_ngrams+"shareholder.p","rb"))

    print(dict_metrics.keys())

    try:
        di = dict_metrics[coy]
    except:
        di = dict_metrics["BJRI"]

    first = pd.DataFrame([["Fiscal Year Ends",di["FiscalYearEnds"]],
                                 ["Market Cap",di["MarketCap"]],
                                 ["Net Income",di["NetIncome"]],
                                 ["Sales",di["Sales"]],
                                 ["Sector", di["Sector"]],
                                 ["Type", di["StockSale"]],
                                 ])

    second = pd.DataFrame([["Legal Advisor",di["LegalAdvisor"]],
                                 ["Auditor",di["Auditor"]],
                                 ["Average Director Age",di["avg_age"]],
                                 ["Average Time Served",int(di["avg_served"])],
                                 ["Accumulated Board Experience", di["acc_served"]],
                                 ["Independent Director Ratio", di["itod"]],
                                 ["Number of Directors", di["total_board"]]
                                 ])

    third = pd.DataFrame([["Five Year Growth Forecast",di["Five-Year Growth"]],
                                 ["Analyst Rating                     "
                                  "(5 - Buy, 1 - Sell)",di["500 Avg"]],
                                 ["Forward Price/Earnings",di["Forward Price/Earnings"]],
                                 ["PEG Ratio",di["PEG Ratio"]],
                                 ["PEG Pyaback (Yrs)", di["PEG Payback (Yrs)"]]
                                 ])

    earn_tab = di["Earnings"]["Table"]
    earn_tab = earn_tab.iloc[:,[0,3,4,5]]

    earn_tab = make_dash_table(earn_tab)


    earn_tab.insert(
        0, html.Tr([
            html.Td([]),
            html.Td([di["Earnings"]["NextYear"]], colSpan=3, style={'text-align': "right","padding-right":"0.7cm"})
        ], style={'background': 'white', 'font-weight': '600'}
        )
    )


    trace1 = {
        "x": di["KeyMetrics"]["diff"][::-1],
        "y": di["KeyMetrics"]["Table"].iloc[:, 0].values[1:][::-1],
        "marker": {"color": "rgb(101, 32, 31)"},
        "name": "Col1",
        "orientation": "h",
        "type": "bar",
        "uid": "80eb70"
    }
    data = Data([trace1])

    list_annot = []
    len_fr = len(di["KeyMetrics"]["diff"][::-1])
    t = 0
    for i, g in zip(range(len_fr), di["KeyMetrics"]["diff"]):
        t = t + 1
        list_annot.append(
            {
                "x": 39,
                "y": round((len_fr - t),2),
                "align": "left",
                "arrowcolor": "rgb(60, 60, 60)",
                "arrowhead": 0,
                "arrowwidth": 1,
                "ax": 0,
                "ay": -20,
                "font": {
                    "color": "rgb(60, 60, 60)",
                    "family": "Raleway",
                    "size": 10
                },
                "showarrow": False,
                "text": str(round(g,2)),
                "textangle": 0,
                "xref": "x",
                "yref": "y"
            })

    layout = {
        "annotations": list_annot,
        "autosize": False,
        "font": {
            "family": "Raleway",
            "size": 11
        },
        "height": 250,
        "margin": {
            "r": 0,
            "t": 0,
            "b": 0,
            "l": 10,
            "pad": 0
        },
        "title": "",
        "titlefont": {
            "family": "Raleway",
            "size": 11
        },
        "width": 150,
        "xaxis": {
            "autorange": True,
            "mirror": False,
            "nticks": 6,
            "range": [-62.1338054023, 164.542302644],
            "autorange": True,
            "showgrid": False,
            "zeroline": False,
            "showline": False,
            "autotick": True,
            "ticks": '',
            "showticklabels" : False,
            "title": "",
            "type": "linear",
            "zeroline": False
        },
        "yaxis": {
            "autorange": True,
            "range": [-0.5, 11.5],
            "autorange": True,
            "showgrid": False,
            "zeroline": False,
            "showline": False,
            "autotick": True,
            "ticks": '',
            "showticklabels" : False,
            "title": "",
            "type": "category",
            "zeroline": False
        }
    }
    fig = Figure(data=data, layout=layout)


    layout=  html.Div([

        # Data tables on this page:
        # ---
        # df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')
        # df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')
        # df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')
        # df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')

        # Column 1

        html.Div([
            html.H6('Core Information',
                    className="gs-header gs-text-header padded"),
            html.Table(make_dash_table(first), id="df_key_info"),

            html.H6('Governance Characteristics',
                    className="gs-header gs-text-header padded"),
            html.Table(make_dash_table(second), id="df_governance"),

            html.H6('Growth and Valuation',
                    className="gs-header gs-text-header padded"),
            html.Table(make_dash_table(third), id="df_growth_value"),

            html.H6('Earnings (%)',
                    className="gs-header gs-text-header padded"),
            # ["Earnings"]["Table"]

            html.Table(earn_tab, id="earnings_dataframe", style={'marginBottom': 5})

        ], className="four columns"),

        # Column 2#####

        html.Div([
            html.H6('Financial Metrics',
                    className="gs-header gs-table-header padded"),

            html.Div([

            html.Table(make_dash_big(di["KeyMetrics"]["Table"]), id="earnings_dataframe", style={'marginTop': "-0.7cm",'marginBottom': 5,"float":"left","width":"66%"},
                       className='className="reversed"'),

                dcc.Graph(figure=fig,
                          id='ratio_plot', style={'margin-left':'8cm','margin-top':'1cm','border': '0', 'width': "20%", 'height': "250"},
                          config={'displayModeBar': False}
                          ),

                ]),
            html.Br([]),
            html.Br([]),

            html.H6('Balance Sheet',
                    className="gs-header gs-table-header padded"),

                html.Table(make_dash_big(di["BalanceTable"]), id="BS_dataframe",
                           style={'marginBottom': 5, "float": "left", "width": "100%"},
                           className='className="reversed"'),


        ], className="four columns",style={"width":"68%"}),

    ], className="row")

    return layout




def comp(coy):

    import _pickle as pickle
    import os

    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    def make_dash_big(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]],style={"height":"25.4px"}))
            table.append(html.Tr(html_row))
        return table

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")

    dict_metrics = pickle.load(open(path_in_ngrams+"shareholder.p","rb"))

    print(dict_metrics.keys())

    try:
        di = dict_metrics[coy]
    except:
        di = dict_metrics["BJRI"]


    comp = di["CompetitionTable"]
    comp = make_dash_table(comp)

    layout=  html.Div([

        # Data tables on this page:
        # ---
        # df_fund_info = pd.read_csv('https://plot.ly/~jackp/17544/.csv')
        # df_fund_characteristics = pd.read_csv('https://plot.ly/~jackp/17542/.csv')
        # df_fund_facts = pd.read_csv('https://plot.ly/~jackp/17540/.csv')
        # df_bond_allocation = pd.read_csv('https://plot.ly/~jackp/17538/')


        html.Div([
            html.H6('Financial Metrics',
                    className="gs-header gs-table-header padded"),

            html.Table(comp, id="comp_dataframe", style={'marginBottom': 5},
                       className='className="reversed"'),
                ]),

                ])

    return layout