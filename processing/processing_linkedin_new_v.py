
import os
import pandas as pd
import _pickle as pickle

#### New Analysis here:


my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/../data/linkedin/"

path_out = my_path + "/../data/linkedin/"


def dot(car):
    input_fields = pd.read_csv("../input_fields.csv").reset_index(drop=True)
    codes = list(input_fields["code_or_ticker"].values)

    nol = -1
    for coy in codes:
        nol = nol +1
        #coy = "CAKE"
        my_path = os.path.abspath(os.path.dirname('__file__'))
        path = os.path.join(my_path, "../data/linkedin/")
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




my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/../data/linkedin/"

dop_dict = pickle.load(open(path_out +"employee.p", "rb"))

figures = dop_dict["figures"].round(2)


figures

fig_cor = figures.iloc[1:,:].set_index("Firms")

fig_cor = pd.merge(fig_cor.iloc[:,0].to_frame(), dot("emp_seniority"),left_index=True, right_index=True, how="left")

fig_cor = pd.merge(fig_cor, dot("emp_degree"),left_index=True, right_index=True, how="left")

df = dot("emp_skill")

df = df.loc[df.count(1) > df.shape[1]/2, df.count(0) > df.shape[0]/2]
df = df.fillna(df.mean()).round()


fig_cor = pd.merge(fig_cor, df,left_index=True, right_index=True, how="left")


fig_cor.columns = [r + " (%)" for r in fig_cor.columns]

fig_cor = pd.merge(fig_cor, figures.iloc[1:,:].set_index("Firms").iloc[:,1:],left_index=True, right_index=True, how="left")

fig_cor = fig_cor.rename(columns={"Employee Count* (%)":"Employee Count*"})

fig_cor.T.mean(axis=1)

far = fig_cor.T
far["Bench"] = list(far.mean(axis=1))
far["Bench"].iloc[:-4] = far["Bench"].iloc[:-4].round()
far["Bench"].iloc[-4:] = far["Bench"].iloc[-4:].round(2)
far = far.T

far = far.reset_index().T.reset_index().T
dop_dict={}


dop_dict["figures"] = far

pickle.dump(dop_dict,open(path_out +"new_employee.p", "wb"))