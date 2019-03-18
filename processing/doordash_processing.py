import pandas as pd
import os
import os.path
from functools import reduce

### To say the truth you should add number here - included in matrics
small_dict = {}
input_fields = pd.read_csv("../input_fields.csv")
short = input_fields["short_name"]
codes = input_fields["code_or_ticker"]
overall_dict = {}
for coy in codes:
    print(coy)
    final = []

    my_path = os.path.abspath(os.path.dirname('__file__'))

    dir_lis = my_path + "/../data/doordash/" + coy + "/"

    a = os.listdir(dir_lis)
    b = ["category"]

    final = [word for word in a if not any(bad in word for bad in b)]

    my_path = os.path.abspath(os.path.dirname('__file__'))
    if not os.path.exists(dir_lis + final[0].split(".")[0] + '.xlsx'):
        print("Ra")
        for csvfile in final:
            workbook = Workbook(dir_lis + csvfile[:-4] + '.xlsx')
            worksheet = workbook.add_worksheet()
            with open(dir_lis + csvfile, 'rt', encoding='utf8') as f:
                reader = csv.reader(f)
                for r, row in enumerate(reader):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)
            workbook.close()

    a = os.listdir(dir_lis)
    b = ["category"]

    final = [word for word in a if not any(bad in word for bad in b)]

    final = [i for i in final if ('.xlsx' in i)]

    small_dict = {}
    for fil in final:

        path_in = os.path.join(dir_lis, fil)
        print(path_in)
        doors = pd.read_excel(path_in)
        doors.columns = ["Name", "Price", "Description", "Ingredients"]
        # doors = pd.read_csv(path_in, error_bad_lines=False)

        # pd.set_option('display.max_columns', None)
        # pd.set_option('display.max_rows', None)
        # disc = doors["Name"].str.find("Disclaimer")
        # disc = doors["Name"].str.find("Disclaimer")
        # disc = disc[disc.values==0].index[0]
        # ext_info = doors.iloc[disc+1,:]

        disc = doors["Price"].str.find(doors.loc[0, "Price"])

        disc = disc[disc.values == 0].index
        if len(disc) > 1:
            doors = doors.iloc[:disc[1], :]

        ext_info = doors.iloc[0, :]

        addy = ext_info["Description"]
        try:
            rating = ext_info["Name"].split("/")[0]
        except AttributeError:
            rating = None

        try:
            number = ext_info["Price"].split(" ")[0]
        except AttributeError:
            number = None

        adds = pd.read_csv("../big_small_add.csv")

        adds = adds[adds["Target"] == coy].reset_index(drop=True)

        from difflib import SequenceMatcher

        matching_ratio = []
        for com in adds["All Target Location Full Addresses"].values:
            matching_ratio.append(SequenceMatcher(None, addy.lower(), com.lower()).ratio())

        ft = pd.DataFrame(columns=["Ratio", "Adds"])

        ft["Ratio"] = matching_ratio

        ft["Adds"] = adds["All Target Location Full Addresses"].values

        ft = ft.sort_values("Ratio", ascending=False).reset_index(drop=True)["Adds"][0]

        small_name = \
        adds[adds["All Target Location Full Addresses"] == ft]["All Target Location Small Names"].reset_index(
            drop=True)[0]

        ### Okay Now You have the name # If error then something else

        # Most Loved 5
        # Most Popular 10
        voors = doors[doors.index > 0].reset_index(drop=True)

        voors["Price"] = [v[1:] for v in voors["Price"]]
        voors["Price"] = voors["Price"].astype(float)

        rad = voors.dtypes == "object"

        rad = rad[rad == True].index

        repls = ('¬†', ''), ('.', ''), ('‚Äô', ''), ('‚Ä†', ''), ('√±', 'n'), ('√©', 'i'), ('Ôøº', ''), ('Ñ¢', ''), (
        '¬Æ', ''),

        for col in list(rad):
            voors[col] = [reduce(lambda a, kv: a.replace(*kv), repls, s) for s in voors[col]]

        food_dict = {}
        for f in voors["Description"].unique():
            pops = voors[voors["Description"] == f].reset_index(drop=True)

            ingr = []
            for r in pops["Ingredients"]:
                for v in r.split("|"):
                    ingr.append(v.strip())

            prod = []
            for r in pops["Name"]:
                prod.append(r.strip())

            prices = []
            for r in pops["Price"]:
                prices.append(r)

            ingr = list(filter(None, ingr))
            food_dict[f] = {}
            food_dict[f]["ingredients"] = ingr
            food_dict[f]["products"] = prod
            food_dict[f]["prices"] = prices
            food_dict["rating"] = rating
            food_dict["number"] = number

        small_dict[small_name] = food_dict
    overall_dict[coy] = small_dict

dict_doordash = {}

nerf = pd.DataFrame(columns=["category", "products", "prices", "target"])

bord = overall_dict
for coy in codes:
    for g in bord[coy].keys():
        del bord[coy][g]["rating"]
        del bord[coy][g]["number"]
        for k, v in overall_dict[coy][g].items():
            wilf = pd.DataFrame()
            prods = overall_dict[coy][g][k]["products"]
            prices = overall_dict[coy][g][k]["prices"]
            wilf["products"] = prods
            wilf["prices"] = prices
            wilf["category"] = str(k)
            wilf["target"] = coy

            nerf = pd.concat((nerf, wilf), axis=0)

verf = nerf.copy()

verf['category'] = verf['category'].replace(
    ['Ribs and Steaks', 'Ribs', 'Fresh Steaks', 'Steaks & Ribs', 'Texas-Size Baby Back Ribs', 'Hand-Trimmed Steaks',
     'From the Grill', 'Steak & Ribs', 'Steaks & Chops'], "Ribs, Steak and Chops")

verf['category'] = verf['category'].replace(
    ['Guiltless Grill®', 'Fish & Seafood', 'Chicken', 'Chicken, Seafood & Pasta', 'Other Fun on a Bun',
     'Fish & Seafood', "BJ's Premium Wings"], "Fish, Chicken and Other")

verf['category'] = verf['category'].replace(
    ['Apps to Share', 'Build Your Appetizer Sampler', 'Entrées', 'Appetizers', 'Appetizer Salads',
     'SkinnyLicious®: Small Plates & Appetizers', 'Appetizers', "BJ's Enlightened Entrées", 'Sizzling & Main Entrees',
     'Specialty Entrees'], "Appetizers")

verf['category'] = verf['category'].replace(
    ['Big Mouth® Burgers', 'Handcrafted Burgers', 'Fresh Mex', 'Full-On Fajitas', 'Burgers',
     'Fire-Grilled Gourmet Burgers', "Red's Tavern Burgers", "Red Robin's Finest Gourmet Burgers", 'Burger', 'Sandwich',
     'Glamburgers® & Sandwiches', "BJ's Loaded Burgers", "BJ's Brewhouse Burgers", 'Crispy Chicken Sandwiches',
     'Sandwiches and Tacos'], "Burgers and Sandwiches")

verf['category'] = verf['category'].replace(
    ['Fresh Salads', 'Sandwiches & Soups', 'Soups', 'Fresh Salads', 'Soups', 'Salads', 'Soup', 'Salad',
     "BJ's Garden Fresh Entrée Salads", 'Starter Salads', 'Housemade Soups', 'SkinnyLicious®: Salads'],
    "Salads and Soup")

verf['category'] = verf['category'].replace(
    ['Hey, Sweet Stuff', 'Ice Cream Delights', 'Sweet Things', 'Desserts', 'Dessert',
     'Cheesecakes & Specialty Desserts', 'Ice Cream Delights', 'World-Famous Pizookies®', 'More Great Desserts'],
    "Desserts")

verf['category'] = verf['category'].replace(
    ['Wraps & Sandwiches', 'Cajun Pasta', 'Chicken & Pastas', 'Pasta, Seafood More', 'Original Hand-Tossed Pizzas',
     'Crispy Thin Crust Pizzas', 'Gluten-Free Pizzas', 'Pastas', 'Pastas', 'Pastas + Specialties', 'Pizzas',
     'Pasta Favorites', 'Build Your Own Pizza', "BJ's Deep Dish Pizza", "BJ's Tavern-Cut Pizza"], "Pizza and Pastas")

cats = ["Ribs, Steak and Chops",
        "Fish, Chicken and Other",
        "Appetizers",
        "Burgers and Sandwiches",
        "Salads and Soup",
        "Desserts",
        "Pizza and Pastas"]

tgif = nerf[nerf["target"] == "RRGB"]

kerf = verf[verf["category"].isin(cats)].reset_index(drop=True)

len(kerf)

mens = kerf.groupby(["category", "target"]).mean();
mens

sens = mens.reset_index()
goku = pd.DataFrame(columns=codes)
for cat in sens["category"].unique():
    rat = sens[sens["category"] == cat].set_index("target")
    rat = rat.T
    rat.index = ["category", cat]
    rat = rat.iloc[1:, :]
    goku = pd.concat((goku, rat), axis=0)

mean = goku.mean()
far = goku.T
far["mean"] = mean
goku = far.T
goku = goku.astype(float).round(2)

my_path = os.path.abspath(os.path.dirname('__file__'))

path_out = my_path + "/../data/doordash/"

goku = goku.reset_index()
goku = goku.rename(columns={"index": "Category"})
goku.loc[-1] = goku.columns  # adding a row
goku.index = goku.index + 1  # shifting index
goku = goku.sort_index()

dict_doordash["category"] = goku

goku.to_csv(path_out + "bench_cats.csv")

goku

loca_frame = {}

loca_frame["BJRI"] = list(overall_dict["BJRI"].keys())

loca_frame["CAKE"] = list(overall_dict["CAKE"].keys())

loca_frame["TGIF"] = list(overall_dict["TGIF"].keys())

loca_frame["CPKI"] = list(overall_dict["CPKI"].keys())

loca_frame["RRGB"] = list(overall_dict["RRGB"].keys())

loca_frame["APPB"] = list(overall_dict["APPB"].keys())

loca_frame["CHIL"] = list(overall_dict["CHIL"].keys())

dict_doordash["location"] = loca_frame

import _pickle as pickle

for item, backup in zip(["Most Popular", "Most Loved"], ["Most Loved", "Most Popular"]):
    dict_doordash["local " + item] = {}

    fat = pd.DataFrame()
    rat = []
    raty = []

    for coy in codes:

        bad = overall_dict[coy]

        conc = pd.DataFrame(columns=["products", "prices", "rating", "number", "small"])
        for k, v in bad.items():
            kel = pd.DataFrame()
            try:
                products = v[item]["products"]
                prices = v[item]["prices"]
            except:
                try:
                    products = v[backup]["products"]
                    prices = v[backup]["prices"]
                except:
                    continue

            kel["products"] = products
            kel["prices"] = prices
            kel["rating"] = v["rating"]
            kel["number"] = v["number"]
            kel["small"] = k

            conc = pd.concat((conc, kel), axis=0)
            # This one should be saved for hte individual locations

        conc["rating"] = conc["rating"]
        conc["number"] = conc["number"].replace({"Newly": None})
        conc["rating"] = conc["rating"].astype(float)
        conc["number"] = conc["number"].astype(float)

        ronc = conc[conc.index < 5]

        ronc = ronc.fillna(ronc.mean())
        ronc["number"] = ronc["number"].astype(int)

        dict_doordash["local " + item][coy] = ronc

        rag = conc.drop_duplicates("small").groupby("small").mean()

        rag = rag[~rag["rating"].isnull()]

        rag["percentage"] = ((rag["number"] / rag["number"].sum())).round(2)

        fr = pd.DataFrame()
        fr["products"] = conc["products"].value_counts().index
        fr["count"] = conc["products"].value_counts().values
        fr["percentage"] = (fr["count"].div(fr["count"].sum(), axis=0).multiply(100)).round(2)
        pir = []
        for c in fr["products"]:
            pra = conc[conc["products"] == c].drop_duplicates("products").reset_index(drop=True)["prices"][0]
            pir.append(pra)

        fr["prices"] = pir
        drs = fr[["products", "percentage", "prices"]]
        drs.columns = [s + "_" + coy for s in drs.columns]
        rat.append((rag["percentage"] * rag["rating"]).sum())  # I am weighting by amount of reviews.
        fat["Ranking"] = fat.index + 1
        fat = pd.concat((fat, drs), axis=1)

    gat = fat[fat.index < 10]

    per_col = [col for col in gat.columns if 'percentage' in col]
    pe_col = [col for col in gat.columns if 'prices' in col]

    new_row = ["Rating/Avg"]

    for r, pe, pr in zip(rat, gat[per_col].sum().values, gat[pe_col].mean().values):
        new_row.append(str(round(r, 2)) + "/5")
        new_row.append(str(round(pe, 2)) + "%")
        new_row.append("$" + str(round(pr, 2)))

    vat = gat.append(pd.Series(new_row, index=gat.columns), ignore_index=True)

    dict_doordash[item] = vat

my_path = os.path.abspath(os.path.dirname('__file__'))
path_out = my_path + "/../data/doordash/"
pickle.dump(dict_doordash, open(path_out + "dict_doordash.p", "wb"))