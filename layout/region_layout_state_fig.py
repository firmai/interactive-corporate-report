def figs_state(short_name, rating_type ):

    import os
    import pandas as pd
    import _pickle as pickle
    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")

    all_dicts_state = pickle.load(open(path_in_ngrams + "all_dicts_state.p", "rb"))
    print(short_name)

    df = all_dicts_state[short_name].round(3)

    scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'], \
           [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]

    df['text']  = '<br>' +rating_type+'<br>' +  \
                 '<br>Number of Reviewers ' + (df['Number of Reviewers']).astype(str) + \
                 '<br>Average Rating ' + (df['Average Rating']).astype(str) + \
                 '<br>Visual Importance ' + (df['Visual Importance']).astype(str) + \
                 '<br>Connectedness ' + (df['Connectedness']).astype(str) + \
                 '<br>Foreign Importance ' + (df['Foreign Importance']).astype(str)

    data = [dict(
        type='choropleth',
        colorscale=scl,
        showscale=False,
        autocolorscale=True,
        locations=df['code'],
        z=df[rating_type].astype(float),
        locationmode='USA-states',
        text=df['text'],
        marker=dict(
            line=dict(
                color='rgb(255,255,255)',
                width=2
            )),
        colorbar=dict(
            title=rating_type)
    )]

    layout = dict(
        margin=dict(
            t=0,
            b=10,
            r=0,
            l=0
        ),
        annotations=[dict(
            dict(
                showarrow=False,
                text=short_name,
                xanchor="right",
                yanchor="top",
                xshift=-95,
                yshift=-80,
                opacity=0.1,
                ax=-20,
                ay=20,
                font=dict(
                    color="black",
                    size=30
                ),
            ), )],
        width=1130 * (2 / 3.2),
        height=650 * (2 / 3.6),
        showlegend=False,
        geo=dict(
            scope='usa',
            projection=dict(type='albers usa'),
            showland=True,

            landcolor='rgb(217, 217, 217)',
            subunitwidth=1,
            countrywidth=1,
            subunitcolor="rgb(255, 255, 255)",
            countrycolor="rgb(255, 255, 255)"

        ), )

    fig = dict(data=data, layout=layout)

    return fig