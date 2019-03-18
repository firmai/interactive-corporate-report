from plotly import tools
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import os


my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_pickle = os.path.join(my_path, "../data/pos/")


def four_figs(code):

    first = "good"
    second = "bad"

    code = code

    g_b = pd.read_csv(path_in_pickle + "big_ass_q1_"+ code + "_" + first + "_" + second + ".csv")

    b_g = pd.read_csv(path_in_pickle +"big_ass_q1_"+ code + "_" +second + "_" + first + ".csv")

    g_b_p = pd.read_csv(path_in_pickle +"big_ass_q1_"+ code + "_" +first + "_" + second + "_pro.csv")

    b_g_p = pd.read_csv(path_in_pickle + "big_ass_q1_"+code + "_" +second + "_" + first + "_pro.csv")

    line_dict_pos = dict(
        color=('rgb(22, 96, 167)'),
        width=2,
        dash='dash')

    line_dict_neg = dict(
        color=('rgb(205, 12, 24)'),
        width=2,
        dash='dash')

    trace1 = go.Scatter(x=list(g_b["name"].values), y=list(g_b["good"].values), showlegend=False, line=line_dict_pos)
    trace2 = go.Scatter(x=list(g_b["name"].values), y=list(g_b["bad"].values), showlegend=False, line=line_dict_neg)

    trace3 = go.Scatter(x=list(b_g["name"].values), y=list(b_g["good"].values), showlegend=False, line=line_dict_neg)
    trace4 = go.Scatter(x=list(b_g["name"].values), y=list(b_g["bad"].values), showlegend=False, line=line_dict_pos)

    trace5 = go.Scatter(x=list(g_b_p["entity"].values), y=list(g_b_p["best"].values), showlegend=False, line=line_dict_pos)
    trace6 = go.Scatter(x=list(g_b_p["entity"].values), y=list(g_b_p["worst"].values), showlegend=False, line=line_dict_neg)

    trace7 = go.Scatter(x=list(b_g_p["entity"].values), y=list(b_g_p["best"].values), line=line_dict_pos, name="Positive")
    trace8 = go.Scatter(x=list(b_g_p["entity"].values), y=list(b_g_p["worst"].values), line=line_dict_neg, name="Negative")

    fig = tools.make_subplots(rows=2, cols=2, subplot_titles=('Positive Nouns', 'Negative Nouns',

                                                              'Poitive Pronouns', 'Negative Pronouns'))
    # data = [trace1, trace2]
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)

    fig.append_trace(trace3, 1, 2)
    fig.append_trace(trace4, 1, 2)

    fig.append_trace(trace5, 2, 1)
    fig.append_trace(trace6, 2, 1)

    fig.append_trace(trace7, 2, 2)
    fig.append_trace(trace8, 2, 2)

    fig['layout']['xaxis1'].update(showgrid=False)
    fig['layout']['xaxis2'].update(showgrid=False)
    fig['layout']['xaxis3'].update(showgrid=False)
    fig['layout']['xaxis4'].update(showgrid=False)

    fig['layout']['yaxis1'].update(showticklabels=False, showgrid=False)
    fig['layout']['yaxis2'].update(showticklabels=False, showgrid=False)
    fig['layout']['yaxis3'].update(showticklabels=False, showgrid=False)
    fig['layout']['yaxis4'].update(showticklabels=False, showgrid=False)

    fig['layout'].update(title='Frequency Analysis')
    return fig