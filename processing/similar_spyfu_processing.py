import os
import pandas as pd

input_fields = pd.read_csv("../input_fields.csv")
websites = input_fields["website"]
codes = input_fields["code_or_ticker"]
my_path = os.path.abspath(os.path.dirname('__file__'))

path_out = my_path + "/../data/similarweb/"

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import re

fi_dict = {}
gr = pd.DataFrame()
pf = pd.DataFrame()
top = pd.DataFrame()
top_org = pd.DataFrame()
top_paid = pd.DataFrame()
top = pd.DataFrame()
similar = pd.DataFrame()
social = pd.DataFrame()

path_spy = my_path + "/../data/spyfu/"

i = -1
for coy in codes:
    i = i + 1
    rad = pd.read_csv(path_out + coy + "_similarweb.csv")
    spyf = pd.read_csv(path_spy + coy + "_spyfu.csv")
    spyf = spyf[["Est Monthly Seo Click", "Est Monthly PPC Click", "Est Monthly AdWords Budget"]]
    spyf.columns = ["Seo Click", "PPC Click", "Adwords Budget"]

    nlof = rad[["Category Rank", "Total Visits", "Avg Visit Duration", "Pages Per Visit", "Bounce Rate"]].iloc[0, :]
    nlof["Seo Click"] = spyf["Seo Click"].values[0]
    nlof["PPC Click"] = spyf["Seo Click"].values[0]
    nlof["Adwords Budget"] = spyf["Seo Click"].values[0]

    sources = rad["Traffic Sources"]

    cat = sources[0][2:].split(", (")
    rt = []
    rt = [f.split(",")[0][1:-1] for f in cat]
    bt = [f.split(", ")[1][1:-2] for f in cat]

    pf[coy] = bt
    pf.index = rt

    sources = rad["Top Referring Sites"]

    cat = sources[0][2:].split(", (")
    rt = []
    rt = [f.split(",")[0][1:-1] for f in cat]
    bt = [f.split(", ")[1][1:-2] for f in cat]

    top[coy + "_perc"] = bt
    top[coy + "_webs"] = rt

    sources = rad["Top 5 Organic Keywords"]

    cat = sources[0][2:].split(", (")
    rt = []
    rt = [f.split(",")[0][1:-1] for f in cat]
    bt = [f.split(", ")[1][1:-2] for f in cat]

    top_org[coy + "_perc"] = bt
    top_org[coy + "_webs"] = rt

    sources = rad["Top 5 Paid Keywords"]

    cat = sources[0][2:].split(", (")
    try:
        bt = [f.split(", ")[1][1:-2] for f in cat]
        rt = [f.split(",")[0][1:-1] for f in cat]
        top_paid[coy + "_perc"] = bt
        top_paid[coy + "_webs"] = rt
    except:
        top_paid[coy + "_perc"] = bt
        top_paid[coy + "_webs"] = rt

    similar[coy + "_webs"] = sources = rad["Similarity Sites"]

    sources = rad["Social Items"]

    cat = sources[0][2:].split(", (")
    rt = []
    rt = [f.split(",")[0][1:-1] for f in cat]
    bt = [f.split(", ")[1][1:-2] for f in cat]

    social[coy + "_perc"] = bt
    social[coy + "_webs"] = rt

    gr[coy] = list(nlof.values)
    org_perc = rad["Organic Keywords Percent"][0]
    paid_perc = rad["Paid Keywords Percent"][0]

gr.index = nlof.index
gr = gr.reset_index()
gr = gr.T
gr = gr.reset_index()
key_metrics = gr.replace({"index": "Firm"})

h = pf
pf = pf.reset_index()
pf = pf.T
pf = pf.reset_index()
referrals = pf.replace({"index": ""})

import _pickle as pickle

key_metrics.columns = key_metrics.iloc[0, :]
fi_dict["key_metrics"] = key_metrics
fi_dict["referrals"] = referrals
fi_dict["top"] = top
fi_dict["org_perc"] = org_perc
fi_dict["paid_perc"] = paid_perc
fi_dict["top_org"] = top_org
fi_dict["top_paid"] = top_paid
fi_dict["social"] = social
fi_dict["similar"] = similar

my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/../data/similarweb/"

pickle.dump(fi_dict, open(path_out + "website.p", "wb"))