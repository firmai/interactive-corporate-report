import pandas as pd
import json
import os

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

code = input_fields["code_or_ticker"]
dict_metrics = {}

for coy in code:
    try:

        mor_dict = json.load(open("../data/morningstar/" + coy + "_sample.json"))

    except FileNotFoundError:
        continue

    data = mor_dict[0][list(mor_dict[0].keys())[0]]

    BoardDirectors_Parsed = {}
    BoD = data["BoardDirectors"].split("\n")
    i = -3
    r = 0
    for x in range(len(BoD)):
        i = i + 3
        r = i + 3
        print(i, r)
        part = BoD[i:r]
        try:
            BoardDirectors_Parsed["Name", i] = part[0].split(",")[0]
            BoardDirectors_Parsed["Age", i] = part[0].split(",")[1]
            BoardDirectors_Parsed["Title", i] = part[1].split("Since")[0]
            BoardDirectors_Parsed["Since", i] = part[1].split("Since")[1][2:]
            BoardDirectors_Parsed["Description", i] = part[2].split("Since")[0]
        except:
            break

    data["BoardDirectors_Parsed"] = BoardDirectors_Parsed

    dict_metrics[coy] = {}

    dict_metrics[coy]["ForwardCalculation"] = data['ForwardCalculation']

    fwc = data['ForwardCalculation']

    dict_metrics[coy]["Forward Price/Earnings"] = fwc.split("Forward Price/Earnings ")[1].split(" ")[0]

    dict_metrics[coy]["PEG Ratio"] = fwc.split("PEG Ratio ")[1].split(" ")[0]

    dict_metrics[coy]["PEG Payback (Yrs)"] = fwc.split("PEG Payback (Yrs) ")[1].split(" ")[0]

    dict_metrics[coy]["DayAvgVol"] = data['DayAvgVol']
    dict_metrics[coy]["Employees"] = data['Employees']

    dict_metrics[coy]["FiscalYearEnds"] = data['FiscalYearEnds']

    dict_metrics[coy]["LegalAdvisor"] = data['LegalAdvisor'].replace("&amp;", "&")

    dict_metrics[coy]["Auditor"] = data['Auditor'].replace("&amp;", "&")

    dict_metrics[coy]["MarketCap"] = data['MarketCap']

    dict_metrics[coy]["NetIncome"] = data['NetIncome']

    dict_metrics[coy]["Sales"] = data['Sales']

    dict_metrics[coy]["Sector"] = data['Sector']

    dict_metrics[coy]["StockSale"] = data['StockSale'].replace("\xa0 ", "")

    import dash_html_components as html
    import pandas as pd
    import datetime

    inde = []
    valu = []
    usd_old = []
    grow_old = []
    usd_new = []
    grow_new = []
    for rin in data["AnnualEarningEst"]:
        inde.append(list(rin.keys())[0])
        valu.append(list(rin.values())[0])

    rat = pd.DataFrame(index=inde, columns=["USD_", "Growth %_", "", "USD", "Growth %"])

    i = -1
    for rin in data["AnnualEarningEst"]:
        i = i + 1
        rat.iloc[i, :] = list(rin.values())[0]

    rat = rat.reset_index()

    rat = rat.rename(columns={"index": ""})
    rat.loc[-1] = [s.strip("_") for s in rat.columns]  # adding a row
    rat.index = rat.index + 1  # shifting index
    rat = rat.sort_index()

    splits = data['FiscalYearEnds'].split("-")

    this_y = datetime.date(int(splits[0]), int(splits[1]), int(splits[2]))

    next_y = this_y + datetime.timedelta(360)

    this_y = str(this_y.year) + "/" + str(this_y.month)
    next_y = str(next_y.year) + "/" + str(next_y.month)

    dict_metrics[coy]["Earnings"] = {}
    dict_metrics[coy]["Earnings"]["Table"] = rat
    dict_metrics[coy]["Earnings"]["ThisYear"] = this_y
    dict_metrics[coy]["Earnings"]["NextYear"] = next_y

    strips = [' ',
              ' Stock Ind Avg ',
              ' ',
              ' Relative to Industry Price/Earnings TTM ',
              ' Price/Book ',
              ' Price/Sales TTM ',
              ' Rev Growth (3 Yr Avg) ',
              ' Net Income Growth (3 Yr Avg) ',
              ' Operating Margin % TTM ',
              ' Net Margin % TTM ',
              ' ROA TTM ',
              ' ROE TTM ',
              ' Debt/Equity ',
              ' – Avg + – Avg + ']

    ai = data["Keystats"].split("\xa0")
    ind = []
    val = []
    for a, s in zip(ai, strips):
        ind.append(s[1:-1])
        val.append(a.replace(s[:-1], ""))

    first = [s[1:-1].split(" ")[0] for s in val[3:-1]]

    second = [s[1:-1].split(" ")[1] for s in val[3:-1]]

    import numpy as np

    darg = pd.DataFrame(index=ind[3:-1])

    darg["Stock"] = first
    darg["Ind Avg"] = second

    darg = darg.reset_index()
    darg = darg.rename(columns={"index": ""})
    darg.loc[-1] = [s.strip("_") for s in darg.columns]  # adding a row
    darg.index = darg.index + 1  # shifting index
    darg = darg.sort_index()

    farg = darg
    dict_metrics[coy]["KeyMetrics"] = {}
    dict_metrics[coy]["KeyMetrics"]["Table"] = darg

    import re

    strips = ['Price/Earnings ',
              ' Price/Book',
              ' Price/Sales',
              ' Price/Cash Flow',
              ' Dividend Yield %',
              ' Price/Fair Value',
              'Premium']

    ind = ['Price/Earnings',
           'Price/Book',
           'Price/Sales',
           'Price/Cash Flow',
           'Dividend Yield %']

    data["CurrentCalculation"]

    litt = re.sub(r'|'.join(map(re.escape, strips)), '', data["CurrentCalculation"]).split(" ")

    pe = litt[0:4]

    pb = litt[4:8]

    ps = litt[8:12]

    pc = litt[12:16]

    dy = litt[16:20]

    ft = pd.DataFrame(index=ind, columns=["Company", "Industry Avg", "S&P500", "Company 5Y Avg"])

    for i, r in zip(ft.index, [pe, pb, ps, pc, dy]):
        ft.loc[i, :] = r

    ft = ft.reset_index();
    ft

    dict_metrics[coy]["Valuation"] = {}
    dict_metrics[coy]["Valuation"]["Table"] = ft

    splits = data['FiscalYearEnds'].split("-")

    this_y = datetime.date(int(splits[0]), int(splits[1]), int(splits[2]))

    next_y = this_y + datetime.timedelta(360)

    previous_y = this_y - datetime.timedelta(364)
    previous_y_1 = previous_y - datetime.timedelta(364)
    previous_y_2 = previous_y_1 - datetime.timedelta(364)

    prev_year = str(previous_y.year)
    prev_year_1 = str(previous_y_1.year)

    previous_y = str(previous_y.year) + "/" + str(previous_y.month)
    previous_y_1 = str(previous_y_1.year) + "/" + str(previous_y_1.month)
    previous_y_2 = str(previous_y_2.year) + "/" + str(previous_y_2.month)

    inde = []
    valu = []

    for rin in data["Cfinancials"]:
        inde.append(list(rin.keys())[0])
        valu.append(list(rin.values())[0])

    fat = pd.DataFrame(index=inde, columns=[previous_y, previous_y_1, previous_y_2, "", prev_year, prev_year_1])

    i = -1
    for rin in data["Cfinancials"]:
        i = i + 1
        fat.iloc[i, :] = [re.sub("[^0-9]", "", str(g)) for g in list(rin.values())[0]]

    fat.reset_index(inplace=True)

    fat = fat.rename(columns={"index": ""})
    fat.loc[-1] = [s.strip("_") for s in fat.columns]  # adding a row
    fat.index = fat.index + 1  # shifting index
    fat = fat.sort_index()

    dict_metrics[coy]["BalanceTable"] = fat

    inde = []
    valu = []

    for rin in data["Competitors"]:
        inde.append(list(rin.keys())[0])
        valu.append(list(rin.values())[0])

    gat = pd.DataFrame(index=inde, columns=["Market Cap Mill", "Net Income", "P/S", "P/B", "P/E", "Dividend Yield%",
                                            "5-Yr Rev CAGR%", "Med Oper. Margin%", "Interest Coverage", "D/E"])

    i = -1
    for rin in data["Competitors"]:
        i = i + 1
        gat.iloc[i, :] = list(rin.values())[0]

    gat = gat.reset_index()

    gat = gat.rename(columns={"index": ""})
    gat = gat.rename(columns={"P/S": "Price to Sales   "})
    gat = gat.rename(columns={"P/B": "Price to Book    "})
    gat = gat.rename(columns={"P/E": "Price to Earnings    "})
    gat.loc[-1] = [s.strip("_") for s in gat.columns]  # adding a row
    gat.index = gat.index + 1  # shifting index
    gat = gat.sort_index()

    dict_metrics[coy]["CompetitionTable"] = gat

    dial = data["AnalystRating"]
    yg_5 = dial.split("Five-Year Growth Forecast Industry Avg ")[1].split("%")[0] + "%"

    avg = dial.split("500 Avg ")[1].split(" ")[0]

    dict_metrics[coy]["Five-Year Growth"] = yg_5
    dict_metrics[coy]["500 Avg"] = avg

    BoardDirectors_New = {}
    names = []
    for key, values in BoardDirectors_Parsed.items():
        name = BoardDirectors_Parsed["Name", key[1]]
        names.append(name)
        BoardDirectors_New[name] = {}
        BoardDirectors_New[name]["Age"] = BoardDirectors_Parsed["Age", key[1]]
        BoardDirectors_New[name]["Description"] = BoardDirectors_Parsed["Description", key[1]]
        BoardDirectors_New[name]["Since"] = BoardDirectors_Parsed["Since", key[1]]
        BoardDirectors_New[name]["Title"] = BoardDirectors_Parsed["Title", key[1]]

    import datetime

    count = 0
    total = 0
    age = 0
    served = 0
    for r, s, name, in zip(BoardDirectors_New.keys(), BoardDirectors_New.values(), names):
        title = BoardDirectors_New[name]["Title"]
        total = total + 1
        if "independent" in title.lower():
            count = count + 1

        wage = int(BoardDirectors_New[name]["Age"])
        age = age + wage

        su = datetime.datetime.now().year - int(BoardDirectors_New[name]["Since"])
        served = served + su

    avg_age = int(age / total)
    dict_metrics[coy]["avg_age"] = avg_age

    avg_served = served / total
    dict_metrics[coy]["avg_served"] = avg_served

    total_board = total
    dict_metrics[coy]["total_board"] = total_board

    dict_metrics[coy]["acc_served"] = served

    itod = round(count / total, 2)
    dict_metrics[coy]["itod"] = itod

from scipy import stats

new_metrics = dict_metrics

for coy in dict_metrics.keys():

    lisf = []
    ga = {}
    for co in dict_metrics.keys():
        ga[co] = list(new_metrics[co]["CompetitionTable"].iloc[1, :])

    fg = pd.DataFrame(index=darg.iloc[1:, 0])

    for co in dict_metrics.keys():
        fg[co] = list(new_metrics[co]["KeyMetrics"]["Table"].iloc[1:, 1:]["Stock"])

    fg = fg.replace("—", 0)
    fg = fg.astype(float)

    dar = pd.DataFrame(index=fg.index, columns=fg.columns)
    for i in range(len(fg)):
        dar.iloc[i, :] = list(stats.zscore(fg.iloc[i, :]))

    # If mean standard deviation bigger than 0.8 just remove.
    vat = dar.mean()

    banned = list(vat[abs(vat) > 0.8].keys())

    sg = fg.drop(banned, axis=1)
    sg = sg.astype(float)
    figt = sg.T
    mean = list(figt.mean().values)
    fggt = figt.T
    fggt["mean"] = mean

    sg = fg.astype(float)
    figt = sg.T
    mean = list(figt.mean().values)
    sggt = figt.T
    sggt["mean"] = mean

    rg = new_metrics[co]["KeyMetrics"]["Table"].iloc[1:, 1:]["Ind Avg"]
    rg = rg.replace("—", 0)
    rg = rg.astype(float)

    rg = rg.reset_index(drop=True)

    meane = fggt["mean"].reset_index(drop=True)

for coy in dict_metrics.keys():
    comps = sggt[coy].reset_index(drop=True)

    # This should be added to industry to recallibrate.

    final_ind = (rg + meane) / 2

    corrector = (comps - final_ind) * .50

    final_ind = final_ind + corrector

    final_ind = round(final_ind, 1)

    lit = ["Ind Avg"]
    diff = np.array(comps) - np.array(list(final_ind))
    lit.extend(list(final_ind))
    print(lit)

    darg = pd.DataFrame(index=farg.set_index("").index)

    df = list(["Stock"])

    df.extend(comps)

    darg["Stock"] = df
    darg["Ind Avg"] = lit

    dict_metrics[coy]["KeyMetrics"]["diff"] = diff

    dict_metrics[coy]["KeyMetrics"]["Table"] = darg.reset_index().copy()

    ht = pd.DataFrame.from_dict(ga, orient="index")

    ht.columns = gat.columns

    ha = pd.concat((gat, ht), axis=0)

    ha = ha[ha[""] != "Industry Average"].reset_index(drop=True)

    ha = ha.drop_duplicates("", keep="last").reset_index(drop=True)

    dict_metrics[coy]["CompetitionTable"] = ha

import _pickle as pickle
import os

my_path = os.path.abspath(os.path.dirname('__file__'))
path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

pickle.dump(dict_metrics, open(path_in_ngrams + "shareholder.p", "wb"))