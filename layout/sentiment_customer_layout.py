import pandas as pd
import os
import numpy as np
import _pickle as pickle

import plotly
plotly.tools.set_credentials_file(username='xxxxx', api_key='xxxxxx')

##target = "BJRI"

def sent_cust(target):

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

    path_in_pos = os.path.join(my_path, "../data/pos/")

    import colorlover as cl
    from IPython.display import HTML

    colors_all = cl.scales['11']["qual"]["Set3"]

    colors_all.extend(cl.scales['11']["qual"]["Paired"])

    colors_all.extend(cl.scales['11']["qual"]["Set3"])

    import plotly.plotly as py
    import plotly.graph_objs as go

    data = []


    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_sent = os.path.join(my_path, "data/yelp_sentiment/")

    dat = pickle.load(open(path_in_sent + "yelp_sent.p", "rb"))
    dt = {}
    mata = []
    for aes, dars in dat.items():
        i = -1
        data = []
        dars = (dars / len(dars.columns))/4*100
        for col in dars.columns:
            i = i + 1

            trace = go.Bar(
                y=list(dars.index), x=list(dars[col]),
                name=str(col),
                orientation='h',
                legendgroup=str(aes),
                marker=dict(color=colors_all[i],
                            line=dict(color=colors_all[i],
                                      width=1)))
            data.append(trace)
            mata.append(trace)

        layout = go.Layout(
            barmode='stack',
            bargap=0.2,
            title="Service, Food, Preparation and Location Sentiment <br>"
                  "(Please Use Legend To Toggle)",
            #width=500,
            height=500,
            xaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,

            ),
            yaxis=dict(
                showgrid=False,
                zeroline=False,
                showline=False,
            ),
        )

        fig = go.Figure(data=data, layout=layout)
        # py.iplot(fig, filename='marker-h-bar')
        dt[aes] = fig

    fig = go.Figure(data=mata, layout=layout)
    dt["full"] = fig


    ### For Quarter:

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_sent = os.path.join(my_path, "data/yelp_sentiment/")

    dat = pickle.load(open(path_in_sent + "yelp_sent.p", "rb"))
    ke = []

    i = -1

    for aes, dars in dat.items():
        i = i + 1
        ke.append(aes)
        if i == 0:
            va = pd.DataFrame(index=dars.index)
        va = pd.concat((va, dars), axis=1)

    ra = va[va.index.str.contains("-TQ")]

    df_rank = pd.DataFrame()
    for col in ra.columns:
        df_rank[col] = ra[col].rank(ascending=0)

    df_rank = df_rank.astype(int)

    bjri_tq = va[va.index == (target + "-TQ ")]
    # .iloc[0,:]
    # .sort_values()

    bjri_tq = bjri_tq.T

    bjri_tq_rank = df_rank[df_rank.index == (target + "-TQ ")]

    bjri_tq["rank"] = bjri_tq_rank.T

    bjri_tq = bjri_tq.sort_values((target + "-TQ "), ascending=True)


    trace0 = go.Bar(
        x=bjri_tq[(target + "-TQ ")].values,
        y=bjri_tq.index,
        orientation='h',
        text=["Overall Position: " + str(s) for s in list(bjri_tq["rank"].values)],
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )

    data = [trace0]
    layout = go.Layout(

    annotations=[dict(

                    showarrow=False,
                    text =str(int(bjri_tq[(target + "-TQ ")].mean()*100)) +'/100',
                    #xanchor="right",
                    x=1,
                    y=3,
                    xref='x',
                    yref='y',
                    opacity=0.1,
                    font=dict(
                        color="black",
                        size=30
                    ),)],

        height=800,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,



        ),

        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            # tickangle=45,
            tickfont=dict(
                size=10),

        ),
        margin=go.Margin(
            l=90,
            r=0,
            b=0,
            t=70,
            pad=0
        ),
        title=bjri_tq.columns[0] + ' Sentiment Report',
    )

    fig = go.Figure(data=data, layout=layout)


    dt["quarter"] = fig



    ba = va[va.index.str.contains("-TQ")].T.sum()

    ba.index = [s[:-4] for s in list(ba.index)]

    ba = ba/len(va.columns)*100

    trace1 = go.Bar(
        x=ba.index,
        y=ba.values,
        marker=dict(
            color='Lightgrey',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=1
    )

    layout = go.Layout(
        height=150,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,),

    margin=go.Margin(
        l=0,
        r=0,
        b=23,
        t=20,
        pad=0
    ),
    )
    data = [trace1]
    fig_national = go.Figure(data=data, layout=layout)


    dt["small"] = fig_national

    return dt