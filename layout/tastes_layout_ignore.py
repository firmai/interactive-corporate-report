import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd
import _pickle as pickle


my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/data/doordash/"
mat = pickle.load(open(path_out +"dict_doordash.p", "rb"))
fally = "Most Loved"

vat = mat[fally]


target = "BJRI"

bench = "CAKE"

t_folder = mat["local " + fally][target]

b_folder = mat["local " + fally][bench]

my_path = os.path.abspath(os.path.dirname('__file__'))

path_in_ngrams = os.path.join(my_path, "data/cpickle/")

path_in_file = os.path.join(my_path, "input_fields.csv")


input_fields = pd.read_csv(path_in_file)


loca_frame = mat["location"]


def dic(coy,d_target, loca_frame):
    print(d_target)
    adds = pd.read_csv("big_small_add.csv")

    adds = adds[adds["Target"] == coy].reset_index(drop=True)

    long_name = adds[adds["All Target Location Small Names"]==d_target]["All Target Location File Names"].reset_index(drop=True)[0]

    rads = adds[adds["All Target Location Small Names"].isin(loca_frame[coy])]["All Target Location File Names"]
    shorties = adds[adds["All Target Location Small Names"].isin(loca_frame[coy])]["All Target Location Small Names"]
    addies = adds[adds["All Target Location Small Names"].isin(loca_frame[coy])]["All Target Location Full Addresses"]

    city = long_name

    figures_dict_c = pickle.load(open(path_in_ngrams + "figures_dict_" + coy + ".p", "rb"))

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
    for key, values in figures_dict_c.items():
        location = key[1]
        name_list.append(location)
        lat = values["Response Data"]["coordinates"]["latitude"]
        lon = values["Response Data"]["coordinates"]["longitude"]
        lat_list.append(lat)
        lon_list.append(lon)

    ff = pd.DataFrame()
    ff["lat"] = lat_list
    ff["lon"] = lon_list
    ff["name_list"] = name_list

    lf = ff[ff["name_list"].isin(list(rads))]
    lf["adds"] = addies
    lf["short"] = shorties

    das = [{"lat": lat, "lon": lon, "name": name,"short": short, "add":add} for lat, lon, name, short, add in zip(list(lf["lat"]), list(lf["lon"]), list(lf["name_list"]), list(lf["short"]), list(lf["adds"]))]

    coy_target = figures_dict_c[coy, city]

    v = {'lat': coy_target["Response Data"]["coordinates"]["latitude"],
         'lon': coy_target["Response Data"]["coordinates"]["longitude"]}
    print(closest(das, v))
    close = closest(das, v)
    return close

d_target = "Henrico"

d_bench = "Chesterfield"

ta = dic(target,d_target,loca_frame)

target_location = ta["short"]

be = dic(bench,d_bench,loca_frame)

bench_location = be["short"]


# Target
tronc = t_folder[t_folder["small"]==target_location].reset_index(drop=True)

tlonc = tronc[["products","prices"]]

tlonc = tlonc.append(pd.Series([str(tronc.mean()["rating"])+"/5","$"+str(round(tronc.mean()["prices"],2))], index=tlonc.columns),ignore_index=True)

tlonc.index = tlonc.index + 1

tlonc.reset_index(inplace=True)
tlonc.columns = ["Ranking","Product","Prices"]
tlonc.loc[5,"Ranking"] = "Rating"

tlonc.loc[-1] = tlonc.columns  # adding a row
tlonc.index = tlonc.index + 1  # shifting index
tlonc = tlonc.sort_index()

# Bench
bronc = b_folder[b_folder["small"]==bench_location].reset_index(drop=True)

lonc = bronc[["products","prices"]]

lonc = lonc.append(pd.Series([str(bronc.mean()["rating"])+"/5","$"+str(round(bronc.mean()["prices"],2))], index=lonc.columns),ignore_index=True)

lonc.index = lonc.index + 1

lonc.reset_index(inplace=True)
lonc.columns = ["Ranking","Product","Prices"]
lonc.loc[5,"Ranking"] = "Rating"

lonc.loc[-1] = lonc.columns  # adding a row
lonc.index = lonc.index + 1  # shifting index

lonc = lonc.sort_index().iloc[:,1:]

loc_fin = pd.concat((tlonc,lonc),axis=1)



vat_tar = [col for col in vat.columns if target in col]
first_g = vat[vat_tar]

vat_ben = [col for col in vat.columns if bench in col]
second_g = vat[vat_ben]
fins = pd.concat((first_g,second_g), axis=1)
fins.columns = [col.split("_")[0].title() for col in fins.columns]


fins.index = fins.index + 1  # shifting index
fins = fins.reset_index()
fins = fins.rename(columns={"index": "Ranking"})
fins.loc[-1] = fins.columns  # adding a row
fins = fins.sort_index()

fins["Ranking"][1:] = fins["Ranking"][1:].astype(int) + 1

fins.loc[10,"Ranking"] = "Rating"

def make_dash_table(df):
    ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
    table = []
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


modifed_perf_table = make_dash_table(fins)

modifed_perf_table.insert(
    0, html.Tr([
        html.Td([]),
        html.Td([target], colSpan=3, style={'text-align': "center"}),
        html.Td([bench], colSpan=3, style={'text-align': "center"})
    ], style={'background': 'white', 'font-weight': '600'}
    )
)


loc_perf_table = make_dash_table(loc_fin)

loc_perf_table.insert(
    0, html.Tr([
        html.Td([]),
        html.Td([d_target], colSpan=2, style={'text-align': "center"}),
        html.Td([d_bench], colSpan=2, style={'text-align': "center"})
    ], style={'background': 'white', 'font-weight': '600'}
    )
)


layout = html.Div([
    html.Br([]),
    html.Br([]),
    html.Br([]),

html.Div([
    html.Div([
    dcc.RadioItems(id="first_radio",
        options=[
            {'label': 'Most Ordered', 'value': 'Most Ordered'},
            {'label': 'Best Rated', 'value': 'Best Rated'},
        ],
        value='Most Ordered',


    ),
    ],style={"float":"left","padding-right":"2.1cm"}),
html.Div([
    html.H5("Top Products Nationally and Locally"),

    ]),
]),

        html.Div([

        html.Table(modifed_perf_table,id="df", className="reversed")

                ]),

    html.Div([

        html.Table(loc_perf_table, id="df3", className="reversed")

    ]),

    html.Div([

        html.Table(make_dash_table(mat["category"]), id="df2", className="reversed")

    ]),



],id="full_layout")

"""
layout = html.Div([
dt.DataTable(
    #rows=[{}],
    rows = dict_doordash["most_popular"].to_dict('records'),
    row_selectable=True,
    filterable=True,
    sortable=True,
    # optional - sets the order of columns
    selected_row_indices=[0],
    id='datatable'),])

"""
