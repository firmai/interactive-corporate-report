

def figs_county(short_name, rating_type ):

    import os
    import pandas as pd
    import _pickle as pickle
    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")

    all_dicts_county = pickle.load(open(path_in_ngrams + "all_dicts_county.p", "rb"))
    print(short_name)


    all_f_third = all_dicts_county[short_name]

    all_f_third = all_f_third[~all_f_third["geometry"].isnull()].reset_index(drop=True)

    all_f_third = all_f_third.sort_values(rating_type).reset_index(drop=True)
    all_f_third['Levels_1'] = pd.cut(all_f_third[rating_type], 16)

    all_f_third["Levels_1"] = all_f_third["Levels_1"].astype(str)

    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

    layout = dict(
        hovermode='closest',
        annotations=[dict(
            dict(
                showarrow=False,
                text=short_name,
                xanchor="right",
                yanchor="top",
                xshift=-80,
                yshift=-80,
                opacity=0.1,
                ax=-20,
                ay=20,
                font=dict(
                    color="black",
                    size=30
                ),
            ),)],
        xaxis=dict(
            range=[-125, -65],
            showgrid=False,
            zeroline=False,
            fixedrange=False,
            autorange=True,
            ticks='',
            showticklabels=False
        ),
        yaxis=dict(
            range=[25, 49],
            showgrid=False,
            zeroline=False,
            fixedrange=False,
            autorange=True,
            ticks='',
            showticklabels=False
        ),
        margin=dict(
            t=20,
            b=20,
            r=20,
            l=20
        ),
        width=1100 * (2 / 3),
        height=650 * (2 / 3.5),
        dragmode='select',

    )

    import colorlover as cl

    bupu = cl.scales['9']['seq']['BuPu']
    bupu = cl.interp(bupu, 18)[2:18]
    len(bupu)

    levels = []

    levels = list(all_f_third['Levels_1'].unique())

    color_match = dict(zip(levels, bupu))
    # cubic_helix = ["#46799d", "#48819f", "#4a89a0", "#4c92a1", "#509aa1", "#54a2a0", "#59aa9f", "#60b29e", "#69ba9c", "#74c19b", "#81c89b", "#90ce9c", "#a1d4a0", "#b3d9a6", "#c5ddb0", "#d6e2bc"]
    # cubic_helix = dict(zip(levels, cubic_helix))
    # color_match = dict(zip(levels, cubic_helix))


    plot_data4 = []
    for index, row in all_f_third.iterrows():
        if all_f_third['geometry'][index].type == 'Polygon':
            x, y = row.geometry.exterior.xy
            c_x, c_y = row.geometry.centroid.xy
        elif all_f_third['geometry'][index].type == 'MultiPolygon':
            x = [poly.exterior.xy[0] for poly in all_f_third['geometry'][index]]
            y = [poly.exterior.xy[1] for poly in all_f_third['geometry'][index]]
            c_x = [poly.centroid.xy[0] for poly in all_f_third['geometry'][index]]
            c_y = [poly.centroid.xy[1] for poly in all_f_third['geometry'][index]]
        else:
            print('stop')
        county_outline = dict(
            type='scatter',
            showlegend=False,
            legendgroup="shapes",
            line=dict(color='black', width=1),
            x=x,
            y=y,
            fill='toself',
            fillcolor=color_match[row['Levels_1']],
            hoverinfo='none'
        )
        hover_point = dict(
            type='scatter',
            showlegend=False,
            legendgroup="centroids",
            name=row.NAME,
            text= rating_type +': ' + str(round(row[rating_type], 2)),
            marker=dict(size=2, color='Grey'),
            x=c_x,
            y=c_y,
            fill='toself',
        )
        plot_data4.append(county_outline)
        plot_data4.append(hover_point)

    fig = dict(data=plot_data4, layout=layout)

    return fig