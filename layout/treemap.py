import numpy as np
import plotly.graph_objs as go

import squarify


def treemap(df, req):
    bs = df
    if req == "balance_sheet":
        liab = [
            "Total current liabilities",
            "Total non-current liabilities",
        ]

        ass = [
            "Total non-current assets",
            "Total current assets",

        ]

        equ = [
            "Total stockholders' equity",
        ]

        tras = bs.T[bs.T.index.isin(["Total non-current assets",
                                     "Total current assets",
                                     "Total current liabilities",
                                     "Total non-current liabilities",
                                     "Total stockholders' equity", ])]

        tras["cat"] = np.where(tras.index.isin(ass), "asset", (
            np.where(tras.index.isin(liab), "liability", (np.where(tras.index.isin(equ), "equity", np.nan)))))

        tras

        tras = tras[tras["cat"].isin(["liability", "equity", "asset"])]

        tras = tras.sort_values("cat", ascending=True)

        lit = list(tras.index.values)

        dam = [str(v) for v in ['ca',
                                'nca',
                                'ce',
                                'cl',
                                'ncl',

                                ]]
    if req == "income_statement":
        inc = [
            "Revenue", "Operating income"
        ]

        exp = [
            "Cost of revenue", "Total operating expenses", "Sales, General and administrative",

        ]

        tras = bs.T[bs.T.index.isin(["Total non-current assets",
                                     "Total current assets",
                                     "Total current liabilities",
                                     "Total non-current liabilities",
                                     "Total stockholders' equity", ])]

        tras["cat"] = np.where(tras.index.isin(inc), "income", (
            np.where(tras.index.isin(exp), "expense", np.nan)))

        tras

        tras = tras[tras["cat"].isin(["income", "expense"])]

        tras = tras.sort_values("cat", ascending=True)

        lit = list(tras.index.values)

        dam = [str(v) for v in ['rev',
                                'oi',
                                'cor',
                                'tor',
                                'sga',

                                ]]
    if req == "cash_flow":
        cash = [
            "Net cash provided by (used for) financing activities",
            "Net cash used for investing activities",
            "Net cash provided by operating activities",
            "Free cash flow"
        ]

        tras = bs.T[bs.T.index.isin(["Net cash provided by (used for) financing activities",
                                     "Net cash used for investing activities",
                                     "Net cash provided by operating activities",
                                     "Free cash flow"])]

        tras["cat"] = np.where(tras.index.isin(cash), "cash", np.nan)

        tras = tras[tras["cat"].isin(["cash"])]

        tras = tras.sort_values("cat", ascending=True)

        lit = list(tras.index.values)

        dam = [str(v) for v in ['CFA',
                                'CIA',
                                'COA',
                                'FCF',

                                ]]

    x = 0.
    y = 0.
    width = 100.
    height = 100.

    # values = [500, 433, 78, 25, 25, 7]
    print(tras)
    values = list(tras.iloc[:, -2].values)

    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = ['rgb(166,206,227)', '#CAFF70', '#CDB7B5',
                    '#EED5B7', 'pink', '#EBEBEB']
    shapes = []
    annotations = []
    counter = 0

    for r in rects:
        shapes.append(
            dict(
                type='rect',
                x0=r['x'],
                y0=r['y'],
                x1=r['x'] + r['dx'],
                y1=r['y'] + r['dy'],
                line=dict(width=2),
                fillcolor=color_brewer[counter],
                opacity="0.3",
                text=""
            )
        )
        annotations.append(
            dict(
                x=r['x'] + (r['dx'] / 2),
                y=r['y'] + (r['dy'] / 2),
                text=dam[counter],
                textangle=15,
                showarrow=False
            )
        )
        counter = counter + 1
        if counter >= len(color_brewer):
            counter = 0

    # For hover text
    trace0 = go.Scatter(
        x=[r['x'] + (r['dx'] / 2) for r in rects],
        y=[r['y'] + (r['dy'] / 2) for r in rects],
        text=[str(v) for v in lit],
        mode='text',
        textfont=dict(
            family='sans serif',
            size=1,
            color='#ff7f0e'
        )
    )

    layout = dict(
        height=350,
        width=350,
        xaxis=dict(showgrid=False, zeroline=False, showline=False, autotick=False, ticks='', showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showline=False, autotick=False, ticks='', showticklabels=False),
        shapes=shapes,
        annotations=annotations,
        hovermode='closest',

    )

    # With hovertext
    figure = dict(data=[trace0], layout=layout)

    # Without hovertext
    # figure = dict(data=[Scatter()], layout=layout)

    return figure


