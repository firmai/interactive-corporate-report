import os
import pandas as pd
import _pickle as pickle
import json

my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/../data/linkedin/"

path_out = my_path + "/../data/linkedin/"
links = json.loads(open(path_out + "final_observation.json").read())

da = links["companies"].copy()
for i in range(len(da)):
    print(i)
    links[links["companies"][i]["company"]] = da[i]
    del links["companies"][i]["company"]
companies = list(links.keys())[1:]

input_fields = pd.read_csv("../input_fields.csv")
# websites = input_fields["website"]
codes = input_fields["code_or_ticker"]
linkedin = input_fields["linkedin"]

dop_dict = {}
dop_dict["insights"] = {}
dop_dict["employee_count"] = {}
dop_dict["jobs"] = {}
dop_dict["figures"] = {}
frame_loca = pd.DataFrame(index=[0, 1, 2, 3, 4, 5])
frame_title = pd.DataFrame(index=[0, 1, 2, 3, 4, 5])
figures = pd.DataFrame(
    index=["Employee Count*", "Manager Propensity", "High Rank Titles (H)", "Low Rank Titles (L)", "Specificity (H/L)"])

from dateutil.parser import parse

for link, coy in zip(linkedin, codes):
    ins = links[link]["insights"]['hireInsight']
    ins = pd.DataFrame.from_dict(ins)
    ins["date"] = ins["year"].map(str) + "-" + ins["month"].map(str) + "-" + ins["day"].map(str)
    ins["date"] = ins["date"].apply(lambda x: parse(x))
    ins["employee_count"] = pd.DataFrame.from_dict(links[link]["insights"]['headCountInsight'])["employeeCount"]
    ins.sort_values("date", inplace=True)
    ins["employee_add"] = ins["employee_count"] - ins["employee_count"].shift(1)
    ins["employee_left"] = ins["allEmployeeHireCount"] - ins["employee_add"]
    dop_dict["insights"][coy] = ins.fillna(method="bfill")

    dop_dict["employee_count"][coy] = links[link]["company_info"]['staffCount']

    jobs = links[link]["jobs"]
    jobs = pd.DataFrame.from_dict(jobs)
    dop_dict["jobs"][coy] = jobs


    gas = pd.DataFrame()
    gas["Number_" + coy] = jobs["formattedLocation"].value_counts().iloc[:5].values
    gas.index = jobs["formattedLocation"].value_counts().iloc[:5].index
    gas = gas.reset_index()
    gas.rename(columns={"index": "Location_" + coy}, inplace=True)
    frame_loca = pd.concat((frame_loca, gas), axis=1)

    jas = pd.DataFrame()
    jas["Number_" + coy] = jobs["title"].value_counts().iloc[:5].values
    jas.index = jobs["title"].value_counts().iloc[:5].index
    jas = jas.reset_index()
    jas.rename(columns={"index": "Title_" + coy}, inplace=True)
    frame_title = pd.concat((frame_title, jas), axis=1)

    dili = links[link]["employees"]

    far = pd.DataFrame.from_dict(dili)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    occu_lis = "Manager|Server|Assistant|Director|Hostess|Bartender|Host"

    far = far[far["occupation"].str.contains(occu_lis)]

    far["occupation"] = far["occupation"].map(lambda x: x.replace("at BJ's Restaurants, Inc.", "").strip())
    far["occupation"] = far["occupation"].map(lambda x: x.replace(" at BJs Restaurants", "").strip())
    far["occupation"] = far["occupation"].map(lambda x: x.replace(" at BJs Restaurants, Inc.", "").strip())
    far["occupation"] = far["occupation"].map(lambda x: x.replace(" at BJ's Restaurant & Brewhouse", "").strip())
    far["occupation"] = far["occupation"].map(lambda x: x.replace(" at BJ's Restaurant", "").strip())
    far = far[["location", "occupation"]]

    import numpy as np

    far['Manager'] = np.where(far['occupation'].str.contains("Manager|Director", case=False, na=False), 1, 0)

    manager_prep = far["Manager"].sum() / len(far)

    manager_prep

    manager_df = far[far["Manager"] == 1].reset_index(drop=True)

    manager_df["occupation"].value_counts().mean()

    mng = pd.DataFrame()
    mng["occupation"] = manager_df["occupation"].value_counts().index
    mng["number"] = manager_df["occupation"].value_counts().values
    types_managers = len(mng[mng["number"] > manager_df["occupation"].value_counts().mean() + 1])

    non_manager = far[far["Manager"] == 0].reset_index(drop=True)

    non_manager["occupation"].value_counts().mean()

    non = pd.DataFrame()
    non["occupation"] = non_manager["occupation"].value_counts().index
    non["number"] = non_manager["occupation"].value_counts().values
    types_worker = len(non[non["number"] > non["occupation"].value_counts().mean() + 1])

    specif = types_managers / types_worker

    figures[coy] = [round(links[link]["company_info"]['staffCount'], 2), round(manager_prep, 2),
                    round(types_managers, 2), round(types_worker, 2), round(specif, 2)]


def inde(gr, w):
    gr = gr.reset_index()
    gr = gr.T
    gr = gr.reset_index()
    key_metrics = gr.replace({"index": w})
    return key_metrics


figures = inde(figures, "Firms")
figures.columns = figures.iloc[0, :]

frame_title.columns = [f.split("_")[0] for f in frame_title.columns]

frame_title = frame_title.iloc[:-1, :]

bla = frame_loca.copy()

frame_loca.columns = [f.split("_")[0] for f in frame_loca.columns]

frame_loca = frame_loca.iloc[:-1, :]

frame_title = frame_title.T
frame_title = frame_title.reset_index()
frame_title = frame_title.T
frame_title.columns = frame_title.iloc[0, :]

frame_loca = frame_loca.T
frame_loca = frame_loca.reset_index()
frame_loca = frame_loca.T
frame_loca.columns = frame_loca.iloc[0, :]

dop_dict["frame_title"] = frame_title
dop_dict["frame_loca"] = frame_loca




#### New Analysis here:




dop_dict["figures"] = figures

pickle.dump(dop_dict,open(path_out +"employee.p", "wb"))