import numpy as np
import pandas as pd

import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import os

def dic(c,small_location):

    my_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(my_path, "../input_fields.csv")
    path_in = os.path.join(my_path, "../data/ratings/")

    input_fields = pd.read_csv(path)

    code = input_fields["code_or_ticker"]

    glassdoor = pd.read_csv(path_in + c + "_gdoor_employee_rate.csv")
    glassdoor_m= pd.read_csv(path_in +c + "_gdoor_mgmt_rate.csv")
    df_tick= pd.read_csv(path_in +c + "_stock_rate.csv")
    yelp= pd.read_csv(path_in + "all_yelps_rates_" + c +".csv")

    c_corr = input_fields[input_fields["code_or_ticker"]==code]["ticker"].reset_index(drop=True)[0]

    #
    trace_emp = go.Scatter(
        x=glassdoor["Review Date"],
        y=glassdoor["Final_Rating"],
        name = "Employees Sentiment",
        line = dict(color = '#17BECF'),

        opacity = 0.8)



    trace_wlb = go.Scatter(
        x=glassdoor["Review Date"],
        y=glassdoor["Final_Work Life Balance"],
        name = "Work Life Balance",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    trace_cva = go.Scatter(
        x=glassdoor["Review Date"],
        y=glassdoor["Final_Culture Values"],
        name = "Culture Values",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    trace_cop = go.Scatter(
        x=glassdoor["Review Date"],
        y=glassdoor["Final_Career Opportunities"],
        name = "Career Opportunities",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    trace_cbe = go.Scatter(
        x=glassdoor["Review Date"],
        y=glassdoor["Final_Comp Benefits"],
        name = "Comp Benefits",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    trace_sma = go.Scatter(
        x=glassdoor["Review Date"],
        y=glassdoor["Final_Senior Management"],
        name = "Management Competence",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)



    trace_mse = go.Scatter(
        x=glassdoor_m["date"],
        y=glassdoor_m["trace_mse"],
        name = "Management Sentiment",
        line = dict(color = 'green'),
        opacity = 0.8)

    ###

    trace_mwlb = go.Scatter(
        x=glassdoor_m["date"],
        y= glassdoor_m["trace_mwlb"],
        name = "Work Life Balance",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    trace_mcva = go.Scatter(
        x=glassdoor_m["date"],
        y=glassdoor_m["trace_mcva"],
        name = "Culture Values",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    trace_mcop = go.Scatter(
        x=glassdoor_m["date"],
        y=glassdoor_m["trace_mcop"],
        name = "Career Opportunities",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    trace_mcbe = go.Scatter(
        x=glassdoor_m["date"],
        y=glassdoor_m["trace_mcbe"],
        name = "Comp Benefits",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    trace_msma = go.Scatter(
        x=glassdoor_m["date"],
        y=glassdoor_m["trace_msma"],
        name = "Upper Management Competence",
        line = dict(color = '#17BECF'),
        legendgroup='Employees',
        opacity = 0.2)

    ###


    trace_sto = go.Scatter(
        x=df_tick["date"],
        y=df_tick["close"],
        name = "Stock Price",
        line = dict(color = '#7F7F7F'),
        opacity = 1)

    trace_cus = go.Scatter(
        x=yelp["date"],
        y=yelp["all"],
        name = "Customer Sentiment",
        line = dict(color = "orange"),
        opacity = 0.8)

    my_path = os.path.abspath(os.path.dirname(__file__))
    path_in_search = os.path.join(my_path[:-7] + "/data/search/")


    # Google Search #

    #search_df = pd.read_csv("/Users/dereksnow/crc-status-dash/data/search/correlate-"+c+".csv")
    print(path_in_search)



    search_df = pd.read_csv(path_in_search + "correlate-" + c_corr +".csv")
    rat = pd.read_csv(path_in_search + "rat_search.csv")
    search = []

    import colorlover as cl

    daf = ["red","green","blue","violet","purple","grey" ]

    search_dandas = pd.read_csv(path_in_search + "searches_BRJI_dandas.csv")   #  This has to be changed for new categories.

    trace_search_all = go.Scatter(
        x=search_dandas["date"],
        y=search_dandas.sum(axis=1)/(len(search_dandas.columns)-1),
        name = "Search Sentiment",
        opacity = 0.8)

    rit = -1
    for col in search_dandas.drop(["date"], axis=1).columns:
        rit = rit + 1
        trace = go.Scatter(x=search_dandas["date"], y=search_dandas[col], line = dict(color = daf[rit]),name=col,legendgroup=col,  opacity=0.8)
        search.append(trace)
    #print(rat)#

    color_dict = {}
    sam = -1
    for i in ["Reds","Greens","Blues","PuRd","Purples","Greys" ]:
        sam = sam + 1
        dan = cl.flipper()['seq'][str(rat.groupby("type").count().max()[0]+1)][i]
        color_dict[sam] = dan



    for col in search_df.drop(["Date"],axis=1).columns:
        tio = -1
        for g in rat["type"].unique():
            tio = tio + 1
            ban = daf[tio]
            if col in rat[rat["type"]==g]["0"].values:
                trace = go.Scatter(x = search_df["Date"], y=search_df[col],line = dict(color = ban), name = col,legendgroup=g,opacity = 0.05)
                search.append(trace)

    #dat = pd.read_csv("all_yelps_rates.csv")

    yelp["new"] = yelp["all"]**(1*(np.sqrt(np.abs(np.log(np.abs(yelp["all"].iloc[-1] - yelp["all"].iloc[1]))))**3.5))/10000

    yelp["new"] = (yelp["all"].iloc[-1]/yelp["new"].iloc[-1])*yelp["new"]

    multiplier = (glassdoor_m["trace_mse"].tail(1)).values[0]/yelp["new"].tail(1).values[0]

    yelp["new"] = yelp["new"] * multiplier

    dat = yelp

    yep = []

    trace_all_yelp = go.Scatter(x = dat["date"], y=dat["new"],line = dict(color = 'orange'), name = "Customer Sentiment Avg.",legendgroup="yelps", opacity = 0.8)
    yep.append(trace_all_yelp)
    for col in dat.drop(["date","all"],axis=1).columns:
        if col.lower()==small_location.lower():
            trace = go.Scatter(x = dat["date"], y=dat[col],line = dict(color = 'orange'), name = col,legendgroup="yelps", opacity = 0.50)
            yep.append(trace)


    #df_rick = df_tick[df_tick["date"]<search_dandas["date"].max()]
    df_rick = df_tick
    trace_stock = go.Scatter(
        x=df_rick["date"],
        y=df_rick["close"],
        name = "Stock",
        line = dict(color = '#7F7F7F'),
        opacity = 1)

    search.append(trace_stock)
    yep.append(trace_sto)

    # now do the api call####

    data = [trace_sto,trace_emp, trace_mse, trace_all_yelp]

    layout = dict(
        margin=dict(
            t=20,
            b=15,
            #r=0,
            #l=30
        ),
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label='1m',
                         step='month',
                         stepmode='backward'),
                    dict(count=6,
                         label='6m',
                         step='month',
                         stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(),
            type='date'
        ),
        hovermode="closest"
    )

    fig_overall = dict(data=data, layout=layout)
    #py.iplot(fig, filename = "Time Series with Rangeslider")####

    fig_search = dict(data=search, layout=layout)

    emp_data = [trace_sto,trace_emp, trace_wlb, trace_cop, trace_cbe, trace_sma]

    fig_emp = dict(data=emp_data, layout=layout)

    mgm_data = [trace_sto, trace_mse, trace_mwlb, trace_mcop, trace_mcbe, trace_msma]

    fig_mgm = dict(data=mgm_data, layout=layout)

    #
    share_data = [trace_sto]

    fig_sha = dict(data=share_data, layout=layout)


    fig_cus = dict(data=yep, layout=layout)



    # Used elsewhere


    from scipy import signal
    glassdoor["ben_smooth"] = signal.savgol_filter(glassdoor["Final_Comp Benefits"], 199, 3)

    trace_cbe_smoothed = go.Scatter(
        x=glassdoor["Review Date"],
        y=glassdoor["ben_smooth"],
        name = "Smoothed",
        showlegend = False,
        legendgroup='Employees',
        opacity = 0.8)

    trace_cbe_new = go.Scatter(
        x=glassdoor["Review Date"],
        y=glassdoor["Final_Comp Benefits"],
        name = "Benefits",
        legendgroup='Employees',
        showlegend = False,
        opacity = 0.8)




    tal = -1
    for c in code:
        tal = tal + 1
        glassdoor = pd.read_csv(path_in + c + "_gdoor_employee_rate.csv")
        glassdoor[c] = signal.savgol_filter(glassdoor["Final_Comp Benefits"], 199, 3)
        glassdoor["Review Date"] = pd.to_datetime(glassdoor["Review Date"], infer_datetime_format=True)
        if tal == 0:
            full = glassdoor[[c, "Review Date"]].set_index("Review Date")
        else:
            full = pd.merge(full, glassdoor[[c, "Review Date"]].set_index("Review Date"), left_index=True,
                            right_index=True, how="outer")

    full = full.fillna(method="bfill")
    full = full.fillna(method="ffill").reset_index()

    full["Inds"] = full.mean(axis=1)



    trace_cbe_smoothed_all = go.Scatter(
        x=full["Review Date"],
        y=full["Inds"],
        name="Smoothed Bench",
        showlegend=False,
        legendgroup='Employees',
        opacity=0.8)


    fig_ben = dict(data=[trace_cbe_new, trace_cbe_smoothed,trace_cbe_smoothed_all], layout=layout)

    #path_in = os.path.join(my_path, "../data/ratings/")



    d = {}
    d["fig_overall"] = fig_overall
    d["fig_search"] = fig_search
    d["fig_emp"] = fig_emp
    d["fig_mgm"] = fig_mgm
    d["fig_sha"] = fig_sha
    d["fig_cus"] = fig_cus
    d["fig_ben"] = fig_ben


    return d

