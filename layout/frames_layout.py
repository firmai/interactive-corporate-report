import pandas as pd
import _pickle as pickle
import datetime
from six.moves import cPickle as pickle  # for performance
import os

# After you are done editing here run app_processing and first_page_execution

##  If you edit this one also edit frames in processing
#### NB Frames is inextricably linked with app_processin.py, you have to run it for any of this to take effect.
# Also linked to first_page_execution
# Try and Except because it is linked to two files as inputs

my_path = os.path.abspath(os.path.dirname('__file__'))
try:
    path = os.path.join("input_fields.csv")
except:
    path = os.path.join(my_path, "../input_fields.csv")


input_fields = pd.read_csv(path)

not_listed = input_fields[input_fields["listed"] == "No"].reset_index(drop=True)["code_or_ticker"]

s = ["'" + str(int(str(datetime.datetime.now().year)[-2:]) - 4 + i) for i in range(5)]

parent = [x for x in input_fields[input_fields["parent"] == "Yes"]["code_or_ticker"]]


s_metrics_df = pd.DataFrame([["Type", "E", "C", "S", "M", "A", "BA"],
                             ["Sentiment", 3, 1, 1, 1, 1, 1],])

c_metrics_df = pd.DataFrame([["Year", s[0], s[1], s[2], s[3], s[4]],
                             ["Solvency", 1, 1, 1, 1, 1],
                             ["Efficiency", 2, 1, 1, 1, 1],
                             ["Profitability", 3, 1, 1, 1, 1],
                             ["Liquidity", 4, 1, 1, 1, 1]])


# Function To Import Dictionary and Open IT.



# And the specification of this table
 # Much rather use this one#


def fin_met(coy, bench):

    import os

    my_path = os.path.abspath(os.path.dirname('__file__'))

    try:
        path = os.path.join(my_path, "data/financial/")

        def load_dict(filename_):
            with open(filename_, 'rb') as f:
                ret_di = pickle.load(f)
            return ret_di

        dict_frames = load_dict(path + 'data.pkl')

    except:
        path = os.path.join(my_path, "../data/financial/")

        def load_dict(filename_):
            with open(filename_, 'rb') as f:
                ret_di = pickle.load(f)
            return ret_di

        dict_frames = load_dict(path + 'data.pkl')


    if coy in list(not_listed):

        my_path = os.path.abspath(os.path.dirname('__file__'))
        try:
            path = os.path.join(my_path, "data/cpickle/")
            art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
        except:
            path = os.path.join(my_path, "../data/cpickle/")
            art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))

        art_ratios = art_ratios["ratios"][coy]

        df_input = art_ratios.round(2)

        df_input["EPS growth_pred"].iloc[:-2].mean() / df_input["Revenue growth_pred"].iloc[:-2].mean()

        df_input["EPS growth_pred"].iloc[:-2].mean() / df_input["ROA_pred"].iloc[:-2].mean()

        rev_rat = df_input["EPS growth_pred"].iloc[:-2].mean() / df_input["Revenue growth_pred"].iloc[:-2].mean()
        roa_rat = df_input["EPS growth_pred"].iloc[:-2].mean() / df_input["ROA_pred"].iloc[:-2].mean()

        df_input.loc[2017:2018, "EPS growth_pred"] = df_input.loc[2017:2018, "Revenue growth_pred"] * rev_rat * (
        1 / 2) + df_input.loc[2017:2018, "ROA_pred"] * roa_rat * (1 / 2)

        df_input.loc[2017:2018, "EPS growth_pred"] = df_input.loc[2017:2018, "EPS growth_pred"].round(2)

        ratios_df = pd.DataFrame([["", 'Yr 1', 'Yr 2', 'Yr 3', 'Yr5'],
                                  ['Revenue growth', df_input["Revenue growth_pred"].iloc[-1],
                                   df_input["Revenue growth_pred"].iloc[-2:].mean(),
                                   df_input["Revenue growth_pred"].iloc[-3:].mean(),
                                   df_input["Revenue growth_pred"].iloc[-5]],
                                  ['EPS growth', df_input["EPS growth_pred"].iloc[-1],
                                   df_input["EPS growth_pred"].iloc[-2:].mean(),
                                   df_input["EPS growth_pred"].iloc[-3:].mean(),
                                   df_input["EPS growth_pred"].iloc[-5:].mean()],
                                  ['ROA', df_input["ROA_pred"].iloc[-1], df_input["ROA_pred"].iloc[-2:].mean(),
                                   df_input["ROA_pred"].iloc[-3:].mean(), df_input["ROA_pred"].iloc[-5:].mean()],
                                  ['Net Margin', df_input["Net Margin_pred"].iloc[-1],
                                   df_input["Net Margin_pred"].iloc[-2:].mean(),
                                   df_input["Net Margin_pred"].iloc[-3:].mean(),
                                   df_input["Net Margin_pred"].iloc[-5:].mean()],
                                  ['FCF/Sales', df_input["FCF/Sales_pred"].iloc[-1],
                                   df_input["FCF/Sales_pred"].iloc[-2:].mean(),
                                   df_input["FCF/Sales_pred"].iloc[-3:].mean(),
                                   df_input["FCF/Sales_pred"].iloc[-5:].mean()]])
        ratios_df.iloc[1:, 1:] = ratios_df.iloc[1:, 1:].applymap(lambda x: round(x, 2))

        if coy in parent:

            df_input = dict_frames[coy, "calculations", "Original"].round(2)
            df_input = df_input.fillna(df_input.mean()).round(2)
            df_input = df_input.iloc[:-1, :]

            vatios_df = pd.DataFrame([["", 'Yr 1', 'Yr 2', 'Yr 3', 'Yr5'],
                                      ['Revenue growth', df_input["Year over Year"].iloc[-1],
                                       df_input["Year over Year"].iloc[-2:].mean(),
                                       df_input["Year over Year"].iloc[-3:].mean(),
                                       df_input["Year over Year"].iloc[-5:].mean()],
                                      ['EPS growth', df_input["Year over Year.3"].iloc[-1],
                                       df_input["Year over Year.3"].iloc[-2:].mean(),
                                       df_input["Year over Year.3"].iloc[-3:].mean(),
                                       df_input["Year over Year.3"].iloc[-5:].mean()],
                                      ['ROA', df_input["Return on Assets %"].iloc[-1],
                                       df_input["Return on Assets %"].iloc[-2:].mean(),
                                       df_input["Return on Assets %"].iloc[-3:].mean(),
                                       df_input["Return on Assets %"].iloc[-5:].mean()],
                                      ['Net Margin', df_input["Net Margin %"].iloc[-1],
                                       df_input["Net Margin %"].iloc[-2:].mean(),
                                       df_input["Net Margin %"].iloc[-3:].mean(),
                                       df_input["Net Margin %"].iloc[-5:].mean()],
                                      ['FCF/Sales', df_input["Free Cash Flow/Sales %"].iloc[-1],
                                       df_input["Free Cash Flow/Sales %"].iloc[-2:].mean(),
                                       df_input["Free Cash Flow/Sales %"].iloc[-3:].mean(),
                                       df_input["Free Cash Flow/Sales %"].iloc[-5:].mean()]])

            ratios_df.iloc[1:, 1:] = (vatios_df.iloc[1:, 1:] * .80).round(2) + (ratios_df.iloc[1:, 1:] * .20).round(2)

            ratios_df.iloc[1:, 1:] = ratios_df.iloc[1:, 1:].applymap(lambda x: round(x, 2))


    else:
        df_input = dict_frames[coy, "calculations", "Original"].round(2)
        df_input = df_input.fillna(df_input.mean()).round(2)
        df_input = df_input.iloc[:-1, :]

        ratios_df = pd.DataFrame([["", 'Yr 1', 'Yr 2', 'Yr 3', 'Yr5'],
                                  ['Revenue growth', df_input["Year over Year"].iloc[-1],
                                   df_input["Year over Year"].iloc[-2:].mean(),
                                   df_input["Year over Year"].iloc[-3:].mean(),
                                   df_input["Year over Year"].iloc[-5:].mean()],
                                  ['EPS growth', df_input["Year over Year.3"].iloc[-1],
                                   df_input["Year over Year.3"].iloc[-2:].mean(),
                                   df_input["Year over Year.3"].iloc[-3:].mean(),
                                   df_input["Year over Year.3"].iloc[-5:].mean()],
                                  ['ROA', df_input["Return on Assets %"].iloc[-1],
                                   df_input["Return on Assets %"].iloc[-2:].mean(),
                                   df_input["Return on Assets %"].iloc[-3:].mean(),
                                   df_input["Return on Assets %"].iloc[-5:].mean()],
                                  ['Net Margin', df_input["Net Margin %"].iloc[-1],
                                   df_input["Net Margin %"].iloc[-2:].mean(), df_input["Net Margin %"].iloc[-3:].mean(),
                                   df_input["Net Margin %"].iloc[-5:].mean()],
                                  ['FCF/Sales', df_input["Free Cash Flow/Sales %"].iloc[-1],
                                   df_input["Free Cash Flow/Sales %"].iloc[-2:].mean(),
                                   df_input["Free Cash Flow/Sales %"].iloc[-3:].mean(),
                                   df_input["Free Cash Flow/Sales %"].iloc[-5:].mean()]])

    if bench in list(not_listed):

        my_path = os.path.abspath(os.path.dirname('__file__'))
        try:
            path = os.path.join(my_path, "data/cpickle/")
            art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))
        except:
            path = os.path.join(my_path, "../data/cpickle/")
            art_ratios = pickle.load(open(path + "art_ratios.p", "rb"))

        art_ratios = art_ratios["ratios"][bench]

        df_input = art_ratios.round(2)

        df_input["EPS growth_pred"].iloc[:-2].mean() / df_input["Revenue growth_pred"].iloc[:-2].mean()

        df_input["EPS growth_pred"].iloc[:-2].mean() / df_input["ROA_pred"].iloc[:-2].mean()

        rev_rat = df_input["EPS growth_pred"].iloc[:-2].mean() / df_input["Revenue growth_pred"].iloc[:-2].mean()
        roa_rat = df_input["EPS growth_pred"].iloc[:-2].mean() / df_input["ROA_pred"].iloc[:-2].mean()

        df_input.loc[2017:2018, "EPS growth_pred"] = df_input.loc[2017:2018, "Revenue growth_pred"] * rev_rat * (
            1 / 2) + df_input.loc[2017:2018, "ROA_pred"] * roa_rat * (1 / 2)

        df_input.loc[2017:2018, "EPS growth_pred"] = df_input.loc[2017:2018, "EPS growth_pred"].round(2)

        ratios_df_ben = pd.DataFrame([["", 'Yr 1', 'Yr 2', 'Yr 3', 'Yr5'],
                                  ['Revenue growth', df_input["Revenue growth_pred"].iloc[-1],
                                   df_input["Revenue growth_pred"].iloc[-2:].mean(),
                                   df_input["Revenue growth_pred"].iloc[-3:].mean(),
                                   df_input["Revenue growth_pred"].iloc[-5]],
                                  ['EPS growth', df_input["EPS growth_pred"].iloc[-1],
                                   df_input["EPS growth_pred"].iloc[-2:].mean(),
                                   df_input["EPS growth_pred"].iloc[-3:].mean(),
                                   df_input["EPS growth_pred"].iloc[-5:].mean()],
                                  ['ROA', df_input["ROA_pred"].iloc[-1], df_input["ROA_pred"].iloc[-2:].mean(),
                                   df_input["ROA_pred"].iloc[-3:].mean(), df_input["ROA_pred"].iloc[-5:].mean()],
                                  ['Net Margin', df_input["Net Margin_pred"].iloc[-1],
                                   df_input["Net Margin_pred"].iloc[-2:].mean(),
                                   df_input["Net Margin_pred"].iloc[-3:].mean(),
                                   df_input["Net Margin_pred"].iloc[-5:].mean()],
                                  ['FCF/Sales', df_input["FCF/Sales_pred"].iloc[-1],
                                   df_input["FCF/Sales_pred"].iloc[-2:].mean(),
                                   df_input["FCF/Sales_pred"].iloc[-3:].mean(),
                                   df_input["FCF/Sales_pred"].iloc[-5:].mean()]])
        ratios_df_ben.iloc[1:, 1:] = ratios_df_ben.iloc[1:, 1:].applymap(lambda x: round(x, 2))

        if bench in parent:

            df_input = dict_frames[bench, "calculations", "Original"].round(2)
            df_input = df_input.fillna(df_input.mean()).round(2)
            df_input = df_input.iloc[:-1, :]

            vatios_df = pd.DataFrame([["", 'Yr 1', 'Yr 2', 'Yr 3', 'Yr5'],
                                      ['Revenue growth', df_input["Year over Year"].iloc[-1],
                                       df_input["Year over Year"].iloc[-2:].mean(),
                                       df_input["Year over Year"].iloc[-3:].mean(),
                                       df_input["Year over Year"].iloc[-5:].mean()],
                                      ['EPS growth', df_input["Year over Year.3"].iloc[-1],
                                       df_input["Year over Year.3"].iloc[-2:].mean(),
                                       df_input["Year over Year.3"].iloc[-3:].mean(),
                                       df_input["Year over Year.3"].iloc[-5:].mean()],
                                      ['ROA', df_input["Return on Assets %"].iloc[-1],
                                       df_input["Return on Assets %"].iloc[-2:].mean(),
                                       df_input["Return on Assets %"].iloc[-3:].mean(),
                                       df_input["Return on Assets %"].iloc[-5:].mean()],
                                      ['Net Margin', df_input["Net Margin %"].iloc[-1],
                                       df_input["Net Margin %"].iloc[-2:].mean(),
                                       df_input["Net Margin %"].iloc[-3:].mean(),
                                       df_input["Net Margin %"].iloc[-5:].mean()],
                                      ['FCF/Sales', df_input["Free Cash Flow/Sales %"].iloc[-1],
                                       df_input["Free Cash Flow/Sales %"].iloc[-2:].mean(),
                                       df_input["Free Cash Flow/Sales %"].iloc[-3:].mean(),
                                       df_input["Free Cash Flow/Sales %"].iloc[-5:].mean()]])

            ratios_df_ben.iloc[1:, 1:] = (vatios_df.iloc[1:, 1:] * .80).round(2) + (ratios_df_ben.iloc[1:, 1:] * .20).round(2)

            ratios_df_ben.iloc[1:, 1:] = ratios_df_ben.iloc[1:, 1:].applymap(lambda x: round(x, 2))

    else:
        df_input = dict_frames[bench, "calculations", "Original"].round(2)
        df_input = df_input.fillna(df_input.mean()).round(2)
        df_input = df_input.iloc[:-1, :]

        ratios_df_ben = pd.DataFrame([["", 'Yr 1', 'Yr 2', 'Yr 3', 'Yr5'],
                                      ['Revenue growth', df_input["Year over Year"].iloc[-1],
                                       df_input["Year over Year"].iloc[-2:].mean(),
                                       df_input["Year over Year"].iloc[-3:].mean(),
                                       df_input["Year over Year"].iloc[-5:].mean()],
                                      ['EPS growth', df_input["Year over Year.3"].iloc[-1],
                                       df_input["Year over Year.3"].iloc[-2:].mean(),
                                       df_input["Year over Year.3"].iloc[-3:].mean(),
                                       df_input["Year over Year.3"].iloc[-5:].mean()],
                                      ['ROA', df_input["Return on Assets %"].iloc[-1],
                                       df_input["Return on Assets %"].iloc[-2:].mean(),
                                       df_input["Return on Assets %"].iloc[-3:].mean(),
                                       df_input["Return on Assets %"].iloc[-5:].mean()],
                                      ['Net Margin', df_input["Net Margin %"].iloc[-1],
                                       df_input["Net Margin %"].iloc[-2:].mean(),
                                       df_input["Net Margin %"].iloc[-3:].mean(),
                                       df_input["Net Margin %"].iloc[-5:].mean()],
                                      ['FCF/Sales', df_input["Free Cash Flow/Sales %"].iloc[-1],
                                       df_input["Free Cash Flow/Sales %"].iloc[-2:].mean(),
                                       df_input["Free Cash Flow/Sales %"].iloc[-3:].mean(),
                                       df_input["Free Cash Flow/Sales %"].iloc[-5:].mean()]])

    ratios_df.columns = ["one", "two", "three", "four", "five"]
    ratios_df_ben.columns = ["six", "seven", "eight", "nine", "ten"]

    ratios_df_final = pd.concat((ratios_df, ratios_df_ben.iloc[:, 1:]), axis=1)
    ratios_df_final.iloc[1:, 1:] = ratios_df_final.iloc[1:, 1:].astype(float).round(2)

    return ratios_df_final


c_metrics_df_2 = c_metrics_df.set_index(0, drop=True)

new_open_string = "{BJ's}  {}."