import dash_html_components as html
import os
import pandas as pd
import _pickle as pickle
import plotly.graph_objs as go
from plotly import tools
import dash_core_components as dcc


my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")


def employ_an(coy, bench):

    input_fields = pd.read_csv(path)

    short  = input_fields["short_name"]
    codes = input_fields["code_or_ticker"]


    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_out = my_path + "/data/linkedin/"

    dop_dict = pickle.load(open(path_out +"employee.p", "rb"))

    dop_dict_new = pickle.load(open(path_out +"new_employee.p", "rb"))

    figures = dop_dict_new["figures"]

    link = input_fields["linkedin"]

    my_path = os.path.abspath(os.path.dirname('__file__'))


    def dot(car):
        input_fields = pd.read_csv("input_fields.csv").reset_index(drop=True)
        codes = list(input_fields["code_or_ticker"].values)

        nol = -1
        for coy in codes:
            nol = nol +1

            my_path = os.path.abspath(os.path.dirname('__file__'))
            path = os.path.join(my_path, "data/linkedin/")
            print(path)
            links = pd.read_json(path + coy + "_final_observation.json")

            degrees = links["companies"][0]["employee_insights"][car]

            categ = []
            cnt = []
            perc = []
            for r in range(len(degrees)):
                categ.append(degrees[r]["category"])
                perc.append(degrees[r]["percentage"])

            degrees_df = pd.DataFrame()
            degrees_df["category"] = categ
            degrees_df["percentage"] = perc

            degrees_df = degrees_df.replace("Master of Business Administration","MBA")
            degrees_df = degrees_df.set_index("category")

            degrees_df.columns = [coy]

            degrees_df = degrees_df.T
            if nol ==0:
                deg_full = degrees_df
            else:
                deg_full = pd.concat((deg_full, degrees_df),axis=0)
        return deg_full


    desc = ["The number of employees on Linkedin",
            "The likelihood for employees to be managers or higher-level employees",
            "The number of high ranking titles",
            "The number of low ranking titles",
            "This measures is a ratio of high and low ranking titles, a higher measure is indicative "
            "of a company being more specialised at higher than lower levels. Lower level can mean "
            "a more streamlined management approach."]

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


    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    def make_dash_table_space(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]],style={"padding-left":"6px", "vertical-align": "top","text-align": "left"}))
            table.append(html.Tr(html_row))
        return table


    loca = make_dash_table(dop_dict["frame_loca"].iloc[:,0:9])
    loca.insert(
        0, html.Tr([
            html.Td([]),
            html.Td([link[0]], colSpan=2, style={'text-align': "left"}),
            html.Td([link[1]], colSpan=2, style={'text-align': "left"}),
            html.Td([link[2]], colSpan=2, style={'text-align': "left"}),
            html.Td([link[3]], colSpan=2, style={'text-align': "left"}),

        ], style={'background': 'white', 'font-weight': '600'}
        )
    )

    title = make_dash_table(dop_dict["frame_loca"].iloc[:,0:9])
    title.insert(
        0, html.Tr([
            html.Td([]),
            html.Td([link[0]], colSpan=2, style={'text-align': "left"}),
            html.Td([link[1]], colSpan=2, style={'text-align': "left"}),
            html.Td([link[2]], colSpan=2, style={'text-align': "left"}),
            html.Td([link[3]], colSpan=2, style={'text-align': "left"}),


        ], style={'background': 'white', 'font-weight': '600'}
        )
    )

    input_fields = pd.read_csv("input_fields.csv").reset_index(drop=True)
    codes = list(input_fields["code_or_ticker"].values)

    nil = -1
    for coy in codes:
        print(coy)
        nil = nil +1

        links = pd.read_json(path_out + coy + "_final_observation.json")

        jobs = pd.DataFrame.from_dict(links["companies"][0]['jobs'])

        locas = jobs.groupby("formattedLocation").size().to_frame()
        locas.columns = [coy]
        if nil ==0:
            frame_loc = locas.round()
        else:
            frame_loc = pd.merge(frame_loc,locas, right_index=True, left_index=True,how="outer" )



    frame_loc["Bench"] = frame_loc.mean(axis=1)

    gat = pd.concat((frame_loc[~frame_loc[coy].isnull()].sort_values(coy,ascending=False)[[coy,"Bench"]].divide(10).round(1).reset_index().dropna().head(5).dropna().reset_index(drop=True),
              frame_loc[~frame_loc[bench].isnull()].sort_values(bench,ascending=False)[[bench, "Bench"]].divide(10).round(1).reset_index().dropna().head(5).dropna().reset_index(drop=True)),axis=1)

    gat = pd.concat((gat,
              frame_loc[~frame_loc["Bench"].isnull()].sort_values("Bench",ascending=False)[["Bench"]].divide(10).round(1).reset_index().dropna().head(5).dropna().reset_index(drop=True)),axis=1)

    gat.columns = [coy + " Locations", coy + " %", " Ind %",bench + " Locations", bench + " %", " Ind %", "Ind Locations", " Ind %"]

    def inde(gr, w):
        gr = gr.reset_index()
        gr = gr.T
        gr = gr.reset_index()
        key_metrics = gr.replace({"index": w})
        return key_metrics

    gat = gat.T.reset_index().T

    location = dot("emp_location").T
    location["Bench"] = location.mean(axis=1)



    location = location[~location[coy].isnull()]

    location = location[[coy, "Bench"]].sort_values(coy, ascending=False)

    location.columns = [coy + " %", "Ind %"]
    location

    location_b = dot("emp_location").T
    location_b["Bench"] = location_b.mean(axis=1)

    location_b = location_b[~location_b[bench].isnull()]

    location_b = location_b[[bench, "Bench"]].sort_values(bench, ascending=False)


    location_b.columns = [bench + " %", "Ind %"]

    location_b

    location_i = dot("emp_location").T
    location_i["Bench"] = location_i.mean(axis=1)

    location_i = location_i[~location_i["Bench"].isnull()]

    location_i = location_i[["Bench"]].sort_values("Bench", ascending=False)

    location_i.columns = ["Ind %"]

    inds = location_i.head().reset_index()
    inds.columns = ["Ind Locations", "Ind %"]
    location = pd.concat((location.reset_index(), location_b.reset_index()),axis=1)
    location = pd.concat((location,inds ),axis=1)

    location.columns = [coy +" Locations",coy+' %', 'Ind %', bench +" Locations", bench+' %', 'Ind %', 'Ind Locations',
           'Ind %' ]

    location = location.T.reset_index().T

    jobs_frame = make_dash_table(gat)

    emp_frame = make_dash_table(location)


    mes  = ["Employee Level", "Monthly Activity"]
    layout = html.Div([
        html.Div([

            html.H6('Metrics',
                    className="gs-header gs-text-header padded"),

            html.Table(make_dash_table_space(figures), id="df_FS",style={"margin-top":"5","margin-bottom":"0","display": "block", "overflow": "scroll"}),
            html.P("*Only Employees With Public Profiles",style={"margin-top":"0"}),

            html.Div([
                dcc.Dropdown(
                    id='employee_dd',
                    options=[{'label': r, 'value': v} for r, v in zip(mes, mes)],
                    value="Employee Level",
                    clearable=False,
                    className="dropper"
                )
            ], style={'background-color': "white", 'padding-right': '0.3cm', 'color': 'rgb(217, 224, 236)',
                      'width': '28%'}),
            dcc.Graph(
                      id='empc_plot', style={'border': '0', 'width': "100%", 'height': "230","margin-top":"0.4cm"},
                      config={'displayModeBar': False}
                      )
            ,


            html.H6('Top Open Job Locations',
                    className="gs-header gs-text-header padded", style={"margin-top": "0.7cm"}),
            html.Table(jobs_frame  , id="df_FfS", style={"margin-top": "0.2cm", "margin-bottom": "0"}),

            html.H6('Top Employment Regions',
                    className="gs-header gs-text-header padded", style={"margin-top": "0.7cm"}),
            html.Table(emp_frame, id="dff_FS", style={"margin-top": "0.2cm", "margin-bottom": "0"}),

        ]),

                ])
    return layout
