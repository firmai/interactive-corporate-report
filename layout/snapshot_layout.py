
import dash_core_components as dcc
import dash_html_components as html


#### NB the requirement for snapshot_layout is app_processing.py it should not be called
## upon by the dictionary as it is not that involved in user interaction.

def snap_dic(coy, bench):

    #coy ="BJRI"

    #bench="CAKE"
    import _pickle as pickle
    import os
    import pandas as pd

    def make_dash_table_hover(df,adds):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for row, ad in zip(df.itertuples(index=True, name='Pandas'),adds.values):
            html_row = []
            ra = 10
            for i in range(len(row)):
                ra = ra +1
                if ra ==1:
                    continue
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row,title=ad))

        table.insert(
        0, html.Tr([
            html.Td(['Location'], colSpan=1, style={'text-align': "left"}),
            html.Td(['Closure Prob %'], colSpan=1, title="The probability that the location will close within the next 12 months", style={'text-align': "left"})
        ], style={'background': 'white', 'font-weight': '600'}
        )
                    )

        return table

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "input_fields.csv")
    input_fields = pd.read_csv(path)


    codes = input_fields["code_or_ticker"]
    not_listed = input_fields[input_fields["listed"] == "No"].reset_index(drop=True)["code_or_ticker"]

    big_avg = pd.DataFrame()
    r = -1
    for code_start in codes:
        r = r + 1
        path = os.path.join(my_path, "data/stock/")
        df_com = pd.read_csv(path + code_start + "_tick_df.csv")
        df_com["date"] = pd.to_datetime(df_com["date"], format="%Y-%m-%d")

        if code_start in list(not_listed):
            my_path = os.path.abspath(os.path.dirname('__file__'))
            path = os.path.join(my_path, "data/cpickle/")
            art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
            art_ratios = art_ratios["mv"][code_start]
            art_ratios["close"] = (art_ratios["MV_pred"] / art_ratios["MV_pred"].iloc[0]) * 100
            df_com = art_ratios
            # df_com["ticker"] = code_start

        if r == 0:
            big_avg = df_com
        else:
            big_avg = pd.merge(big_avg, df_com, on="date", how="left")

    df2 = big_avg.filter(regex='close|date')

    df2 = df2.set_index("date")
    df2["mean"] = df2.mean(axis=1)

    df2 = df2.reset_index()
    df2 = df2[["date", "mean"]]

    import pandas as pd
    import os
    import _pickle as pickle

    #


    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_2 = os.path.join(my_path, "input_fields.csv")
    path_in_pickle = os.path.join(my_path, "data/stock/")

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "input_fields.csv")

    input_fields = pd.read_csv(path)

    not_listed = input_fields[input_fields["listed"] == "No"].reset_index(drop=True)["code_or_ticker"]
    path = os.path.join(my_path, "data/stock/")

    ## Loop over all
    codes = input_fields["code_or_ticker"]
    listed = input_fields[input_fields["listed"] == "Yes"]["code_or_ticker"]
    big_avg = pd.DataFrame()
    r = -1

    list_df = pd.DataFrame(index=listed)
    fla = []
    valu = []
    for code_start in listed:
        r = r + 1
        path = os.path.join(my_path, "data/stock/")
        df_com = pd.read_csv(path + code_start + "_tick_df.csv")
        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "data/cpickle/")
        art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
        art_ratios = art_ratios["mv"][code_start]
        art_ratios["close"] = (art_ratios["MV_pred"] / art_ratios["MV_pred"].iloc[0]) * 100
        art_ratios["close"] = (art_ratios["close"] + df_com["close"]) / 2
        rela_flo = (art_ratios["close"].iloc[-1] / df_com["close"].iloc[-1]) - 1
        if (rela_flo > -0.05) and (rela_flo < 0.05):
            valu.append("Fair Valued")
        elif (rela_flo < 0.05):
            valu.append("Overvalued")
        else:
            valu.append("Undervalued")
        fla.append(round(rela_flo * 100, 2))

    list_df["Value"] = valu
    list_df["Extent"] = fla

    unlisted = input_fields[input_fields["listed"] == "No"]["code_or_ticker"]
    r = -1

    unlist_df = pd.DataFrame(index=codes)
    fla = []
    valu = []
    for code_start in codes:
        r = r + 1
        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "data/cpickle/")
        art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
        art_ratios = art_ratios["mv"][code_start]
        art_ratios["close"] = (art_ratios["MV_pred"] / art_ratios["MV_pred"].iloc[0]) * 100
        if code_start in list(listed):
            print("go")
            path = os.path.join(my_path, "data/stock/")
            art_ratios = pd.read_csv(path + code_start + "_tick_df.csv")

        rela_flo = (art_ratios["close"].iloc[-1] / df2["mean"].iloc[-1]) - 1
        if (rela_flo > -0.05) and (rela_flo < 0.05):
            valu.append("Neutral")
        elif (rela_flo < 0.05):
            valu.append("Under")
        else:
            valu.append("Over")
        fla.append(round(rela_flo * 100, 2))

    unlist_df["Value"] = valu
    unlist_df["Extent"] = fla

    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler(feature_range=(3.2, 4.1))

    scaler.fit(list_df["Extent"].values.reshape(-1, 1))

    list_df["Rating"] = scaler.transform(list_df["Extent"].values.reshape(-1, 1))

    list_df["Rating"] = list_df["Rating"] * (1 + (list_df["Extent"].mean() / 100))

    list_df["Rating"] = list_df["Rating"].round(2)

    scaler = MinMaxScaler(feature_range=(3.5, 4.4))

    scaler.fit(unlist_df["Extent"].values.reshape(-1, 1))

    unlist_df["Rating"] = scaler.transform(unlist_df["Extent"].values.reshape(-1, 1))

    unlist_df["Rating"] = unlist_df["Rating"] * (1 + (unlist_df["Extent"].mean() / 100))
    unlist_df["Rating"] = unlist_df["Rating"].round(2)

    overall_df = pd.DataFrame()
    overall_df = pd.merge(unlist_df, list_df, left_index=True, right_index=True, how="left")

    overall_df["Rating"] = overall_df[["Rating_x", "Rating_y"]].mean(axis=1)
    print("done")

    overall_df = overall_df["Rating"]

    #
    def make_dash_table_overall(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))


        return table

    def make_dash_table_metrics(df,descriptors):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        tol = -1
        for row, ad in zip(df.itertuples(index=True, name='Pandas'),descriptors.values):
            tol = tol + 1
            html_row = []
            for i in range(len(row)-1):
                i = i +1
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row,title=descriptors[tol]))

        return table


    make_dash_table_overall(overall_df.to_frame())


    def make_dash_table_unlist(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        table.insert(
            0, html.Tr([
                html.Td(['Firm'], colSpan=1, style={'text-align': "left"}),
                html.Td(['Performance'], colSpan=1, style={'text-align': "left"}),
                html.Td(['Extent'], colSpan=1, style={'text-align': "left"}),
                html.Td(['Rating'], colSpan=1, style={'text-align': "left"})
            ], style={'background': 'white', 'font-weight': '600'}
            )
        )
        table.insert(
            0, html.Tr([
                html.Td(['Industry Benchmarked'], colSpan=4, title="Benchmarked Against Publicly Available Financials",
                        style={'text-align': "center"})
            ], style={'background': 'white', 'font-weight': '800'}
            )
        )


        return table


    make_dash_table_unlist(unlist_df)


    def make_dash_table_list(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))

        table.insert(
            0, html.Tr([
                html.Td(['Firm'], colSpan=1, style={'text-align': "left"}),
                html.Td(['Value'], colSpan=1, style={'text-align': "left"}),
                html.Td(['Extent'], colSpan=1, style={'text-align': "left"}),
                html.Td(['Rating'], colSpan=1, style={'text-align': "left"})
            ], style={'background': 'white', 'font-weight': '600'}
            )
        )

        table.insert(
            0, html.Tr([
                html.Td(['AI Valuation Prediction'], colSpan=4, title="The Fair Value Has Been Obtained from AI Algorithms",
                        style={'text-align': "center"})
            ], style={'background': 'white', 'font-weight': '800'}
            )
        )


        return table




    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_closure = os.path.join(my_path, "data/closure/")

    first = pd.read_csv(path_in_closure +"location_closure_2.csv")

    first = first.iloc[:,1:]


    first["y_pred_proba"] = first["y_pred_proba"].round(4)*100
    first["y_pred_proba"] = (first["y_pred_proba"].astype("float")/17).pow(1.2)
    first["y_pred_proba"] = first["y_pred_proba"].round(1)

    top = first[first["ticker"]==coy].head(5)

    bottom = first[first["ticker"]==coy].tail(5)

    #top_business_id = top[top["business_id"]]

    big_small_add = pd.read_csv("big_small_add.csv")

    #big_small_add

    top = pd.merge(top, big_small_add, left_on="business_id",right_on="All Target Location File Names", how="left")

    addy_top = top["All Target Location Full Addresses"]
    top = top[["Small Code","y_pred_proba"]]

    top.columns = ["Location","Probability"]


    bottom = pd.merge(bottom, big_small_add, left_on="business_id",right_on="All Target Location File Names", how="left")
    addy_bottom = bottom["All Target Location Full Addresses"]


    bottom = bottom[["Small Code","y_pred_proba"]]


    bottom.columns = ["Location","Probability"]

    averages = first.groupby("ticker").mean()

    from plotly import __version__
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    import plotly.graph_objs as go
    # import plotly.plotly as py

    init_notebook_mode(connected=True)
    sorted_frame = pd.concat([pd.DataFrame(averages.loc[bench,:]).T, pd.DataFrame(averages.loc[coy,:]).T, averages]).reset_index().drop_duplicates(subset='index', keep='first').set_index('index')



    trace0 = go.Bar(
        x=sorted_frame.index,
        y=sorted_frame["y_pred_proba"],
        marker=dict(
            color=['rgba(204,204,204,1)', '#65201F',
                   'rgba(204,204,204,1)', 'rgba(204,204,204,1)',
                   'rgba(204,204,204,1)','rgba(204,204,204,1)', 'rgba(204,204,204,1)',
                   'rgba(204,204,204,1)']),
    )

    data = [trace0]
    layout = go.Layout(margin=dict(
                t=5,
                b=15,
                r=0,
                l=30
            )
    )

    fig = dict(data=data, layout=layout)

    codes = input_fields["code_or_ticker"]
    big_avg = pd.DataFrame()
    r = -1
    for code_start in codes:
        r = r + 1
        path = os.path.join(my_path, "data/stock/")
        df_com = pd.read_csv(path + code_start + "_tick_df.csv")
        df_com["date"] = pd.to_datetime(df_com["date"], format="%Y-%m-%d")

        if code_start in list(not_listed):
            my_path = os.path.abspath(os.path.dirname('__file__'))
            path = os.path.join(my_path, "data/cpickle/")
            art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
            art_ratios = art_ratios["mv"][code_start]
            art_ratios["close"] = (art_ratios["MV_pred"] / art_ratios["MV_pred"].iloc[0]) * 100
            df_com = art_ratios
            # df_com["ticker"] = code_start

        if r == 0:
            big_avg = df_com
        else:
            big_avg = pd.merge(big_avg, df_com, on="date", how="left")

    df2 = big_avg.filter(regex='close|date')

    df2 = df2.set_index("date")
    df2["mean"] = df2.mean(axis=1)

    df2 = df2.reset_index()
    df2 = df2[["date", "mean"]]

    df2["date"] = pd.to_datetime(df2["date"], format="%Y-%m-%d")

    import pandas as pd

    import os
    import _pickle as pickle
    #
    from datetime import timedelta

    from sklearn.preprocessing import MinMaxScaler

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_2 = os.path.join(my_path, "input_fields.csv")

    path_in_pickle = os.path.join(my_path, "data/stock/")

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "input_fields.csv")

    input_fields = pd.read_csv(path)

    not_listed = input_fields[input_fields["listed"] == "No"].reset_index(drop=True)["code_or_ticker"]
    path = os.path.join(my_path, "data/stock/")

    ## Loop over all
    codes = input_fields["code_or_ticker"]
    listed = input_fields[input_fields["listed"] == "Yes"]["code_or_ticker"]
    big_avg = pd.DataFrame()
    r = -1

    fla = []
    valu = []
    # listed = ["BJRI"]
    dict_list = {}
    for code_start in listed:
        r = r + 1
        path = os.path.join(my_path, "data/stock/")
        df_com = pd.read_csv(path + code_start + "_tick_df.csv")
        df_com["date"] = pd.to_datetime(df_com["date"], format="%Y-%m-%d")
        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "data/cpickle/")
        art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
        art_ratios = art_ratios["mv"][code_start]
        art_ratios["close_sim"] = (art_ratios["MV_pred"] / art_ratios["MV_pred"].iloc[0]) * 100
        art_ratios["date"] = pd.to_datetime(art_ratios["date"], format="%Y-%m-%d")
        art_ratios = pd.merge(art_ratios, df_com, on="date", how="left")
        art_ratios["close_sim"] = (art_ratios["close_sim"] + art_ratios["close"]) / 2
        art_ratios = art_ratios.fillna(method="bfill").fillna(method="ffill")
        art_ratios["Extend"] = (art_ratios["close_sim"] / art_ratios["close"]) - 1

        art_ratios = art_ratios[art_ratios["date"] > art_ratios["date"].max() - timedelta(365 * 4)]

        scaler = MinMaxScaler(feature_range=(1.8, 2.6))
        art_ratios = art_ratios.fillna(method="bfill").fillna(method="ffill")

        scaler.fit(art_ratios["Extend"].values.reshape(-1, 1))

        art_ratios["Rating List"] = scaler.transform(art_ratios["Extend"].values.reshape(-1, 1))
        art_ratios["Rating List"] = art_ratios["Rating List"] * (
        list_df.loc[code_start, 'Rating'] / art_ratios["Rating List"].iloc[-1])
        new_frame_listed = art_ratios[["date", "Rating List"]]
        dict_list[code_start] = new_frame_listed

    from sklearn.preprocessing import MinMaxScaler

    dict_unlist = {}
    for code_start in codes:
        r = r + 1
        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "data/cpickle/")
        part_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
        part_ratios = part_ratios["mv"][code_start]
        part_ratios["close_sim"] = (part_ratios["MV_pred"] / part_ratios["MV_pred"].iloc[0]) * 100
        part_ratios["date"] = pd.to_datetime(part_ratios["date"], format="%Y-%m-%d")
        if code_start in list(listed):
            print("go")
            path = os.path.join(my_path, "data/stock/")
            part_ratios = pd.read_csv(path + code_start + "_tick_df.csv")
            part_ratios["date"] = pd.to_datetime(part_ratios["date"], format="%Y-%m-%d")
            part_ratios["close_sim"] = part_ratios["close"]
        part_ratios = pd.merge(part_ratios, df2, on="date", how="left")
        part_ratios = part_ratios.fillna(method="bfill").fillna(method="ffill")
        part_ratios["Extend"] = (part_ratios["close_sim"] / part_ratios["mean"]) - 1
        part_ratios = part_ratios[part_ratios["date"] > (part_ratios["date"].max() - timedelta(365 * 4))]

        scaler = MinMaxScaler(feature_range=(1.8, 2.6))
        part_ratios = part_ratios.fillna(method="bfill").fillna(method="ffill")
        scaler.fit(part_ratios["Extend"].values.reshape(-1, 1))

        part_ratios["Rating Unlist"] = scaler.transform(part_ratios["Extend"].values.reshape(-1, 1))
        part_ratios["Rating Unlist"] = part_ratios["Rating Unlist"] * (unlist_df.loc[code_start, 'Rating'] / part_ratios["Rating Unlist"].iloc[-1])

        new_frame_unlisted = part_ratios[["date", "Rating Unlist"]]
        dict_unlist[code_start] = new_frame_unlisted

    fa = -1
    frame_new = pd.DataFrame()
    for code_start in codes:
        fa = fa + 1
        if code_start in list(listed):
            new_frame_unlisted = pd.merge(dict_unlist[code_start], dict_list[code_start], on="date", how="left")
            #### This multiplier should be placed to list_df
            new_frame_unlisted["Rating Unlist"] = new_frame_unlisted["Rating Unlist"] * (
            1 + (unlist_df["Extent"].mean() / 100))
            new_frame_unlisted["Rating List"] = new_frame_unlisted["Rating List"] * (1 + (unlist_df["Extent"].mean() / 100))
            new_frame_unlisted[code_start] = new_frame_unlisted[["Rating Unlist", "Rating List"]].mean(axis=1)

        else:
            new_frame_unlisted[code_start] = dict_unlist[code_start]["Rating Unlist"] * (
            1 + (unlist_df["Extent"].mean() / 100))
        if fa == 0:
            frame_new = new_frame_unlisted[["date", code_start]]
        else:
            frame_new = pd.merge(frame_new, new_frame_unlisted[["date", code_start]], on="date", how="left")

    frame_new = frame_new.fillna(method="ffill").fillna(method="bfill")

    ### This has to be uncommented when you need the metrics.

    ####frame_new.to_csv(path_in_closure+"market_figure_series.csv")

    import plotly.graph_objs as go

    got = -1
    data = []
    for code_start in codes:
        got = got + 1
        if code_start == coy:

            scats = go.Scatter(
                x=frame_new["date"].iloc[70:],
                y=frame_new[code_start].rolling(window=90).mean().iloc[70:],
                name=code_start,
                line=dict(color='#65201F', width=3),
                opacity=0.8)
        else:
            scats = go.Scatter(
                x=frame_new["date"].iloc[70:],
                y=frame_new[code_start].rolling(window=90).mean().iloc[70:],
                name=code_start,
                line=dict(color='rgba(204,204,204,1)'),
                opacity=0.8)
        data.append(scats)

    layout = go.Layout(showlegend=False,
                       margin=dict(
                t=0,
                b=20,
                r=20,
                l=24
            )
    )

    fig_time = dict(data=data, layout=layout)

    path = os.path.join(my_path, "data/closure/")

    fullar = pd.read_csv(path+"overall_rank_ts.csv")

    first_abs = pd.read_csv(path + "first_abs.csv")
    second_abs = pd.read_csv(path + "second_abs.csv")


    descriptors = pd.read_csv(path + "descriptors.csv" )

    #
    from plotly import __version__
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    # import plotly.graph_objs as go
    # import plotly.plotly as py


    init_notebook_mode(connected=True)
    import plotly.graph_objs as go

    got = -1
    data = []
    for code_start in codes:
        got = got + 1
        if code_start==coy:

            scats = go.Scatter(
                        x=fullar[fullar["ticker"]==code_start]["date"],
                        y=fullar[fullar["ticker"]==code_start]["Overall Rating"],
                        name = code_start,
                        line = dict(color = '#65201F',width=3),
                        opacity = 0.8)
        else:
            scats = go.Scatter(
                        x=fullar[fullar["ticker"]==code_start]["date"],
                        y=fullar[fullar["ticker"]==code_start]["Overall Rating"],
                        name = code_start,
                        line = dict(color = 'rgba(204,204,204,1)'),
                        opacity = 0.8)
        data.append(scats)


    layout = go.Layout(showlegend=False,
                       margin=dict(
                t=0,
                b=25,
                r=20,
                l=24
            )
    )

    all_fig_bench = dict(data=data, layout=layout)

    from plotly import __version__
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    # import plotly.graph_objs as go
    # import plotly.plotly as py


    init_notebook_mode(connected=True)
    import plotly.graph_objs as go

    got = -1
    data = []
    for i in ["Overall Rating","Qualitative Part","Survival Part","Valuation Part" ]:
        got = got + 1
        if i=="Overall Rating":

            scats = go.Scatter(
                        x=fullar[fullar["ticker"]==coy]["date"],
                        y=fullar[fullar["ticker"]==coy][i],
                        name = i,
                        line = dict(color = '#65201F',width=3),
                        opacity = 0.8)
        else:
            scats = go.Scatter(
                        x=fullar[fullar["ticker"]==coy]["date"],
                        y=fullar[fullar["ticker"]==coy][i],
                        name = i,
                        line = dict(color = 'rgba(204,204,204,1)'),
                        opacity = 0.8)
        data.append(scats)


    layout = go.Layout(showlegend=False,
                       margin=dict(
                t=0,
                b=25,
                r=20,
                l=24
            )
    )

    all_fig_comp = dict(data=data, layout=layout)




    layout = html.Div([


    html.Div([

    html.Div([

    html.H6('Worst Performing',
            className="gs-header gs-text-header padded", title="Survival: Making use of AI prediction and multiple datapoints, this table identifies the "
                                                               "probability that locations will/should close down withing the next 12 months. This measure is generally indicative of "
                                                               "underperformance."),
    html.Table(make_dash_table_hover(top.set_index("Location"),addy_top), id="df_key_info")
                     ],style={'float':'left','width':'25%' }),
    html.Div([
    html.H6('Best Performing',
            className="gs-header gs-text-header padded", title="Survival: Using AI prediction tools, we can also identify the locations least likely to fail."),
    html.Table(make_dash_table_hover(bottom.set_index("Location"),addy_top), id="df_key_info")
                     ],style={'float':'left','width':'25%' }),


    html.Div([
    html.H6('Average Predicted Closure',
            className="gs-header gs-text-header padded",style={'text-align':'center'}, title="Survival: The higher this measure the worse the firm is performing. A higher measure means that in aggregate the "
                                                                                             "firm is more likely to have more closures. If those closures are not realised it can be "
                                                                                             "indicative of a firm supporting losing firms instead of focusing on positive opportunities."),
    dcc.Graph(figure=fig,
                              id='closure_fig', style={'border': '0','height':'105'},
                              config={'displayModeBar': False}
                              )
                ],style={'float':'left','width':'50%' }),



            ],style={'display':'inline-block','width':'100%'}),
    html.P("A high predicted outcome without actual closures can be an indication of the overextension of new locations (excess growth)",style={"margin-top":"-0.5cm","padding-top":"0cm","margin-bottom":"0cm"}),


    html.Div([


    html.Div([


    html.Div([
    html.H6('Publicly Listed',
            className="gs-header gs-text-header padded", title="Valuation: Because the benchmark and target companies can be a mix of publicly and non-publicly traded companies there is two methods to "
                                                               "describe under and overvaluation. For a publicly traded firm one such method is to compare "
                                                               "its current value with the AI predicted value. The current value generally reverts to the AI predicted value so this"
                                                               "is a good measure."),
    html.Table(make_dash_table_list(list_df.reset_index()), id="df_key_info"),
    html.H5(str(fullar[fullar["ticker"]==coy]["Overall Rating"].round(2).iloc[-1]),title="Overall Rating",style={"font-size":"60px","color":"#65201F",'font-weight': 'bold',"text-align":"center","margin-bottom":"0.2cm","margin-top":"-1cm",'padding': "0px"})
                     ],style={'float':'left','width':'30%' }),

    html.Div([
    html.H6('All Firms',
            className="gs-header gs-text-header padded", title="Valuation: As opposed to the Publicly listed method, this method simply compares the performance of the target firm with "
                                                               "the industry to identify whether a firm has under or over performed. All firms public and "
                                                               "non public have predicted market values, thus where publicly available information is "
                                                               "not available, predicted values are used to identify the state of the firm. "),
    html.Table(make_dash_table_unlist(unlist_df.reset_index()), id="df_key_info")
                     ],style={'float':'left','width':'30%' }),


    html.Div([
    html.H6('Valuation Rating Over Time',
            className="gs-header gs-text-header padded",style={'text-align':'center'}, title="Valuation: This graph combines the previous two measures and gives them a "
                                                                                             "rating out of 5. This rating is then recalculated in time series "
                                                                                             "to give the reader an indication of progress if any."),
    dcc.Graph(figure=fig_time,
                              id='time_fig', style={'border': '0','height':'150'},
                              config={'displayModeBar': False}
                              )
                ],style={'float':'left','width':'40%' })

            ],style={'display':'inline-block','width':'100%'}),

    html.Div([


    html.Div([
    html.H6('Sentiment and Convenience',
            className="gs-header gs-text-header padded", title="Qualitative: This is a combination of multiple ratings loosly related to sentiment and "
                                                               "convenience. All of these measures are out of five. The measures are calculated by "
                                                               "normalising accross the performance of multiple firms and then transforming the "
                                                               "values to fit a five point scale and distributing them against a larger benchmark portfolio."),
    html.Table(make_dash_table_metrics(first_abs, descriptors["First"]), id="df_key_info")
                     ],style={'float':'left','width':'48%' }),

    html.Div([
    html.H6('Ratings and Management',
            className="gs-header gs-text-header padded", title="Qualitative: This is a combination of multiple ratings loosly related to company and mangement "
                                                               "specific ratings.  "
                                                               "convenience."),
    html.Table(make_dash_table_metrics(second_abs,descriptors["Second"]), id="df_key_info")
                     ],style={'float':'right','width':'48%' }),

            ],style={'display':'inline-block','width':'100%',"margin-top":"-0.8cm"}),

    html.Div([

    html.Div([
        html.P("Overall rating (red) of 3 components (grey) in time series. The three components consist of "
               "a valuation, survival and qualitative part. The valuation and survival part individually accounts"
               " for 25% of the overall rating and the qualitative part the remaining 50%. The overall rating of " +
               str(fullar[fullar["ticker"] == coy]["Overall Rating"].round(2).iloc[-1]) + " appears both on this page "
                  "and the first page.",style={"margin-top":"-0.35cm"}),
    dcc.Graph(figure=all_fig_comp,
                              id='all_ts_comp', style={'border': '0','height':'130'},
                              config={'displayModeBar': False},
                              )
                ],style={'float':'left','width':'48%' }),

    html.Div([
        html.P("Overall rating (red) against all individual benchmarks (grey) in time series. The overall "
               "rating in this chart is the same as the chart on the left. By hovering over the chart you can identify "
               "the ranking of each firm over the years. ",style={"margin-top":"-0.35cm"}),
    dcc.Graph(figure=all_fig_bench,
                              id='all_ts_ben', style={'border': '0','height':'150'},
                              config={'displayModeBar': False}
                              )
                ],style={'float':'right','width':'48%' })

            ],style={'display':'inline-block','width':'100%'}),

            ])])


    return layout


