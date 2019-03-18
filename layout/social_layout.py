import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd
import _pickle as pickle



def bra(coy):

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../input_fields.csv")


    input_fields = pd.read_csv(path)

    short  = input_fields["short_name"]
    codes = input_fields["code_or_ticker"]

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_out = my_path + "/data/similarweb/"
    fi_dict = pickle.load(open(path_out +"website.p", "rb"))

    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly import tools
    import plotly.plotly as py
    import plotly.graph_objs as go
    from plotly import tools


    perc_p_s = fi_dict["social"][coy + "_perc"]
    webs_p_s = fi_dict["social"][coy + "_webs"]

    perc_s = fi_dict["top"][coy + "_perc"]
    webs_s = fi_dict["top"][coy + "_webs"]

    trace3 = go.Bar(
        x=perc_p_s,
        y=webs_p_s,
        text="%",
        name="Social",
        orientation='h',
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=3),

        ))

    trace4 = go.Bar(
        x=perc_s,
        y=webs_s,
        text="%",
        name="Other",
        orientation='h',
        marker=dict(color='rgba(208, 105, 80, 0.6)',
                    line=dict(color='rgba(208, 105, 80, 1.0)',
                              width=3)

                    ))

    perc = fi_dict["top_org"][coy + "_perc"]
    webs = fi_dict["top_org"][coy + "_webs"]
    perc_p = fi_dict["top_paid"][coy + "_perc"]
    webs_p = fi_dict["top_paid"][coy + "_webs"]

    trace1 = go.Bar(
        x=perc,
        y=webs,
        text="%",
        name="Organic",
        orientation='h',
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=3),

        ))

    trace2 = go.Bar(
        x=perc_p,
        y=webs_p,
        text="%",
        name="Paid",
        orientation='h',
        marker=dict(color='rgba(208, 105, 80, 0.6)',
                    line=dict(color='rgba(208, 105, 80, 1.0)',
                              width=3)

                    ))

    fig = tools.make_subplots(rows=2, cols=2)

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 1, 2)
    fig.append_trace(trace4, 2, 2)

    fig["layout"].update(
    height=300,
        margin=go.Margin(
            l=110,
            t=20,
            b=30,
        ),
        xaxis1=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
    ),
        yaxis1=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickangle=20
        ),

        xaxis2=dict(
            showgrid=False,
            zeroline=False,
            showline=False,

        ),
        yaxis2=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickangle=20
        ),
        xaxis3=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
        ),
        yaxis3=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickangle=20
        ),

        xaxis4=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
        ),
        yaxis4=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickangle=20
        ), )


    def make_dash_table(df):
        ''' Return a dash definitio of an HTML table for a Pandas dataframe '''
        table = []
        for index, row in df.iterrows():
            html_row = []
            for i in range(len(row)):
                html_row.append(html.Td([row[i]]))
            table.append(html.Tr(html_row))
        return table

    layout = html.Div([
        html.Br([]),

        html.Div([
            dcc.Dropdown(
                id='selector_dd',
                options=[{'label': r, 'value': v} for r, v in zip(short, codes)],
                value=coy,
                clearable=False,
                className="dropper"
            )
        ], style={'background-color': "white", 'padding-right': '0.3cm', 'color': 'rgb(217, 224, 236)',
                  'width': '28%'}),

        html.H6(["Visit Stats"],
                className="gs-header gs-text-header padded",style={'margin-top': "3mm",'margin-bottom': "3mm"}),

    html.Div([

    html.Iframe(style={'width': "100%", 'height': '420', 'right': '0','position':'relative','border': '0','margin-left':'-0.2cm'}, src="https://public.tableau.com/views/website_cross/Sheet4?:embed=y&:display_count=no&:toolbar=no?:embed=y&:showVizHome=no&:hoswidtt_url=https%3A%2F%2Fpublic.tableau.com%2F&:tabs=no&:toolbar=no&:animate_transition=yes&:display_static_image=no&:display_spinner=no&:display_overlay=no&:display_count=no#3",
     width="645", height="420",seamless="seamless")


                ],style={"width": "100%", "height": "190", "overflow": "hidden"}),

        html.Br([]),

        html.H6(["Inbound Links"],
                className="gs-header gs-text-header padded", style={'margin-top': "3mm", 'margin-bottom': "3mm"}),
    dcc.Graph(id='fig_social', figure=fig, config={'displayModeBar': False}),

        html.H6(["Website Stats"],
                className="gs-header gs-text-header padded", style={'margin-top': "3mm", 'margin-bottom': "3mm"}),
        html.Div([

            html.Table(make_dash_table(fi_dict["key_metrics"]), id="df_rat")

        ]),





                ])

    return layout, fig