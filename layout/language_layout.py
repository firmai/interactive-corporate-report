
import dash_core_components as dcc
import dash_html_components as html
import layout.frequency_word_chart as fwc
import processing.input as inp
import layout.glassdoor_chart as gc


def dic(code):

    #### Language Layout, Four Figs have to be updated.

    four_figs_layout = html.Div([  # subpage 2

                # Row 1 (Header)


                dcc.Graph(figure=fwc.four_figs(code), id='words_one', config={'displayModeBar': False},
                          style={'padding-left': '0cm','margin-right': '100px','border': '0', 'width': "100%", 'height': "550"}),

                html.Div(html.P(inp.exec, style={"padding-top": "1mm"}))


            ],)

            # Row 2

    phrase_layout = html.Div([  # subpage 2

                    # Row 1 (Header)

                            gc.layout(code)

            ],)



    language_layout = html.Div([

                 html.Br([]),
        html.Br([]),

                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='drops-language',
                            options=[{'label': "Noun", 'value': "Noun"},
                                     {'label': "Phrase", 'value': "Phrase"},
                                     {'label': "Sentiment", 'value': "Sentiment"},
                                     {'label': "Jobs Map", 'value': "Map"},
                                     ],
                            value="Noun",
                            clearable=False,
                            className="dropper",
                            placeholder="Type Location",

                        )
                    ], style={'background-color': '#a9a9a9', 'color': 'rgb(217, 224, 236)', 'float': 'left',
                              'padding-right': '0cm',
                              'width': '100%'}),
                    html.Br([]),
                    html.Br([]),
                    html.Br([]),


                    html.Div(four_figs_layout, id='tab-output-language')
                        ], style={
                            'width': '100%',
                            'fontFamily': 'Sans-Serif',
                            'margin-left': 'auto',
                            'margin-right': 'auto'
                        }),])


    dic = {}
    dic['four_figs_layout'] = four_figs_layout
    dic['phrase_layout'] = phrase_layout
    dic['language_layout'] = language_layout
    return dic




