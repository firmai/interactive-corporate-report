import _pickle as pickle
import pandas as pd
import dash_html_components as html
import os


def dic(bench_short_name, options_value_target_location_small_dd, option_value_bench_code_dd,
        option_value_location_dd, options_target_locations, options_bench_code, options_bench_locations,
        target_code, all_target_location_small_names, target_short_name, bench_location_file_name,
        target_location_file_name):
    import os
    import pandas as pd
    import _pickle as pickle



    def dic(coy, bench, location):

        input_fields = pd.read_csv("input_fields.csv")

        my_path = os.path.abspath(os.path.dirname('__file__'))

        path_in_ngrams = os.path.join(my_path, "data/cpickle/")

        city = location

        figures_dict_c = pickle.load(open(path_in_ngrams + "figures_dict_" + coy + ".p", "rb"))
        figures_dict_b = pickle.load(open(path_in_ngrams + "figures_dict_" + bench + ".p", "rb"))

        from math import cos, asin, sqrt

        def distance(lat1, lon1, lat2, lon2):
            p = 0.017453292519943295
            a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
            return 12742 * asin(sqrt(a))

        def closest(data, v):
            return min(data, key=lambda p: distance(v['lat'], v['lon'], p['lat'], p['lon']))

        lat_list = []
        lon_list = []
        name_list = []
        for key, values in figures_dict_b.items():
            location = key[1]
            name_list.append(location)
            lat = values["Response Data"]["coordinates"]["latitude"]
            lon = values["Response Data"]["coordinates"]["longitude"]
            lat_list.append(lat)
            lon_list.append(lon)

        das = [{"lat": lat, "lon": lon, "name": name} for lat, lon, name in zip(lat_list, lon_list, name_list)]

        coy_target = figures_dict_c[coy, city]

        v = {'lat': coy_target["Response Data"]["coordinates"]["latitude"],
             'lon': coy_target["Response Data"]["coordinates"]["longitude"]}
        print(closest(das, v))
        close = closest(das, v)
        return close

    import _pickle as pickle
    import pandas as pd
    import dash_html_components as html
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

    my_path = os.path.abspath(os.path.dirname('__file__'))

    path_out = os.path.join(my_path, "data/yelp_extra_info/")
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")

    final_df = pd.read_csv(path_out + "extra_info.csv")

    final_df = final_df.set_index("Unnamed: 0")

    i_dict = pickle.load(open(path_in_ngrams + "i_dict.p", "rb"))

    path = os.path.join(my_path, "input_fields.csv")

    input_fields = pd.read_csv(path)

    code_rest = list(input_fields["code_or_ticker"])

    code_rest.remove(target_code)
    code_rest.remove(option_value_bench_code_dd)

    frame_g = pd.DataFrame.from_dict(i_dict[target_code], orient="index")
    frame_g = pd.DataFrame(index=frame_g.index)

    frame_g = frame_g.join(final_df[final_df.index == (target_location_file_name + ".csv")].T, how="outer")
    frame_g = frame_g.join(final_df[final_df.index == (bench_location_file_name + ".csv")].T, how="outer")

    for r in code_rest:
        closest = dic(target_code, r, target_location_file_name)
        frame_g = frame_g.join(final_df[final_df.index == (closest['name'] + ".csv")].T, how="outer")

    small_cols = []
    file_names = [s[:-4] for s in frame_g.columns]
    for col in frame_g.columns:
        wa = ""
        for r in col.split("-"):
            if r[0].isdigit():
                wa = wa + r[:-4]
            else:
                wa = wa + r[0]
        small_cols.append(wa)

    frame_g.columns = small_cols
    frame_g = frame_g.drop(["Target Name", "Average Hours"], axis=0)

    frame_agg = pd.DataFrame.from_dict(i_dict[target_code], orient="index")
    frame_agg = pd.DataFrame(index=frame_agg.index)

    for r in [target_code, option_value_bench_code_dd]:
        dfg = pd.DataFrame.from_dict(i_dict[r], orient="index")
        dfg.columns = [r]
        frame_agg = frame_agg.join(dfg, how="outer")

    for r in code_rest:
        dfg = pd.DataFrame.from_dict(i_dict[r], orient="index")
        dfg.columns = [r]
        frame_agg = frame_agg.join(dfg, how="outer")

    frame_agg = frame_agg.rename(index={'Average Hours': 'Average Weekly Hours'})

    frame_g = frame_g.rename(index={'Hours Open': 'Average Weekly Hours'})

    new_ff = frame_agg.join(frame_g, how="outer")

    new_ff = new_ff.round(2)

    new_ff = new_ff.reset_index()

    new_ff = new_ff.rename(columns={"index": "Category"})

    new_ff.loc[-1] = new_ff.columns
    new_ff.index = new_ff.index + 1
    new_ff = new_ff.sort_index()

    modifed_perf_table = make_dash_table(new_ff)

    modifed_perf_table.insert(
        0, html.Tr([
            html.Td([]),
            html.Td(['National (%)'], colSpan=8, style={'text-align': "center"}),
            html.Td(['Local'], colSpan=7, style={'text-align': "center"})
        ], style={'background': 'white', 'font-weight': '600'}
        )
    )

    d = {}
    d["table"] = modifed_perf_table


    f_df = pd.read_csv("big_small_add.csv")
    f_df = f_df.reset_index(drop=True)

    f_df = list(f_df[f_df["All Target Location File Names"].isin(file_names)].reset_index(drop=True)["All Target Location Full Addresses"])

    code_sap = list(input_fields["code_or_ticker"])

    rw = ""
    for t, c, w in zip(small_cols,code_sap,f_df):
        rw = rw + t.upper() + '/'+c  + ':      ' + w + "     "

    d["adds"] = rw


    code = input_fields["code_or_ticker"]

    my_path = os.path.abspath(os.path.dirname('__file__'))

    path = os.path.join(my_path, "../data/cpickle/")

    rates_df = pd.DataFrame()
    for coy in code:
        rad = pd.DataFrame()
        path_in = os.path.join(my_path, "data/ratings/")
        yelp = pd.read_csv(path_in + "all_yelps_rates_" + coy + ".csv")
        better = [d.title() for d in yelp.columns]
        yelp.columns = better
        das = yelp.iloc[-1:, :].T[1:]
        wel = das.reset_index()
        wel["Target"] = coy

        rates_df = rates_df.append(wel)

    rates_df.iloc[:, 1] = rates_df.iloc[:, 1].fillna(rates_df.iloc[:, 1].mean() - .2)

    final_df = pd.read_csv(path_out + "extra_info.csv")
    final_df = final_df.set_index("Unnamed: 0")
    final_tact = final_df.copy()

    final_tact = final_tact[final_tact["Hours Open"] > 10]

    for s in ['Free Wi-Fi', 'Takes Reservations',
              'Outdoor Seating', 'Delivery', 'Caters', 'Bike Parking',
              'Accepts Apple Pay', 'Accepts Android Pay']:
        final_tact[s + " - S"] = final_tact[s].apply(lambda x: 1 if x == "Yes" else 0)

    final_tact["Noisy" + " - S"] = final_tact["Noisy"].apply(lambda x: 1 if x == "No" else 0)

    ads = final_tact[['Free Wi-Fi - S',
                      'Takes Reservations - S', 'Outdoor Seating - S', 'Delivery - S',
                      'Caters - S', 'Bike Parking - S', 'Accepts Apple Pay - S',
                      'Accepts Android Pay - S', 'Noisy - S']]

    fap = ads.sum(axis=1) + (final_tact["Hours Open"] * 2) / 100

    fap = fap / (fap.sort_values()[-1]) * 10

    f_df = pd.read_csv("big_small_add.csv")

    dap = pd.merge(f_df, rates_df, left_on=["All Target Location Small Names", "Target"], right_on=["index", "Target"],
                   how="left")

    dap["rating"] = dap.iloc[:, -1]

    dap = dap.set_index(dap["All Target Location File Names"], drop=True)

    fap.index = [r[:-4] for r in fap.index]

    fap = pd.DataFrame(fap)

    dap = dap[["rating", "Target", "All Target Location Small Names", "All Target Location Full Addresses"]].copy()
    fin = fap.join(dap, how="outer")

    fin = fin.fillna(fin.mean() - .15)

    fin["final"] = fin[0] * 0.45 + fin["rating"] * 0.55 * 2

    group_fin = fin.copy()

    f_df = pd.read_csv("big_small_add.csv")
    f_df = f_df.reset_index(drop=True)

    f_df = pd.read_csv("big_small_add.csv")
    f_df = f_df.reset_index(drop=True)

    list_f = f_df[f_df["All Target Location File Names"].isin(file_names)].reset_index(drop=True)

    list_f.reset_index(inplace=True)

    list_f["All Target Location File Names"] = list_f["All Target Location File Names"].astype("category")

    list_f["All Target Location File Names"].cat.set_categories(list(file_names), inplace=True)

    list_fd = list(list_f.sort_values(["All Target Location File Names"])["Target"] +
                   list_f.sort_values(["All Target Location File Names"])["All Target Location Small Names"])

    fin["new_id"] = fin["Target"] + fin["All Target Location Small Names"]

    fin = fin[fin["new_id"].isin(list_fd)]

    fin.reset_index(inplace=True)

    fin["new_id"] = fin["new_id"].astype("category")

    fin["new_id"].cat.set_categories(list_fd, inplace=True)
    fin = fin.sort_values(["new_id"])

    small_cols = []
    file_names = [s[:-4] for s in fin["index"]]
    for ss in list(fin["index"]):
        wa = ""
        for r in ss.split("-"):
            if r[0].isdigit():
                wa = wa + r.strip(".csv")
            else:
                wa = wa + r[0]
        small_cols.append(wa)

    fin["smc"] = small_cols

    import plotly.plotly as py
    import plotly.graph_objs as go

    trace1 = go.Bar(
        x=fin.smc.values,
        y=fin.final,
        name='Local Convenience Rating',

        marker=dict(
            color='grey',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=1
    )

    layout = go.Layout(
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,),

        height=150,
    margin=go.Margin(
        l=0,
        r=0,
        b=23,
        t=10,
        pad=0
    ),
    )
    data = [trace1]
    fig_local = go.Figure(data=data, layout=layout)
    # py.iplot(fig, filename='stacked-bar')

    grouped = group_fin.groupby("Target").mean()

    grouped.reset_index(inplace=True)

    grouped.Target = grouped.Target.astype("category")

    grouped.Target.cat.set_categories(list(frame_agg.columns), inplace=True)

    import plotly.plotly as py
    import plotly.graph_objs as go

    grouped = grouped.sort_values(["Target"])
    trace1 = go.Bar(
        x=grouped.Target.values,
        y=grouped.final,
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
    # py.iplot(fig, filename='stacked-bar')

    d["fig_national"] = fig_national

    d["fig_local"] = fig_local


    return d