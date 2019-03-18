import _pickle as pickle

import requests
import pickle

# Replace [app_id] with the App ID and [app_secret] with the App Secret
app_id = 'i_8dCQfUhgdirD-y3W6MuA'
app_secret = 'eFsJS7GtnABrrm3yV1vW7U2yt9AthO1XZ2fOCwZ9euZnk9qIyShRl1JdSUO7Y1rm'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
token = requests.post('https://api.yelp.com/oauth2/token', data=data)
access_token = token.json()['access_token']
headers = {'Authorization': 'bearer %s' % access_token}

from os import listdir
from os.path import isfile, join
import os
import pandas as pd
import numpy as np

my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

# tick  = [x for x in input_fields[input_fields["ticker"]!="PE"].ticker]

code = input_fields[input_fields["code_or_ticker"] != "x"]["code_or_ticker"]

for coy in code:

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path = os.path.join(my_path, "../data/yelp/" + coy + "/")

    path_out = os.path.join(my_path, "../data/ratings/")

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    names_final = []
    for li in onlyfiles:
        if len(li) > 9:
            li = li[:-4]
            names_final.append(li)

    rat = ""
    for li in onlyfiles:
        rat = rat + li + "-"

    from collections import Counter
    import re

    coun = Counter(rat.split("-"))

    ad = pd.DataFrame()

    ad["word"] = list(coun.keys())
    ad["number"] = list(coun.values())

    ad = ad.sort_values("number", ascending=False)

    ad = ad[~(np.abs(ad.number - ad.number.mean()) <= (3.2 * ad.number.std()))]

    ad.reset_index(inplace=True, drop=True)
    ad["word_1"] = "-" + ad["word"] + "-"
    ad["word_2"] = ad["word"] + "-"
    ad["word_3"] = "-" + ad["word"]

    ad["final"] = ad["word_1"]

    words = list(ad["final"].append(ad["word_2"]).append(ad["word_3"]).values)

    full_names = []
    small_names = []
    for i in range(len(onlyfiles)):
        my_string = onlyfiles[i]
        full_names.append(my_string)
        li = my_string
        if len(li) > 9:
            li = re.sub(r'|'.join(map(re.escape, list(words))), '', li)
            small_names.append(li[:-4])

    names_frame = pd.DataFrame()
    names_frame["full"] = names_final
    names_frame["small"] = small_names

    ########

    figures_dict = {}
    biz_ids = []

    code = input_fields[input_fields["code_or_ticker"] != "x"]["code_or_ticker"]
    path_in_ngrams = os.path.join(my_path, "../data/cpickle/")

    for full, small in zip(names_frame["full"], names_frame["small"]):

        # You would normall do this
        # Call Yelp API to pull business data for Kiku Sushi
        #biz_id = full
        #biz_ids.append(biz_id)
        #url = 'https://api.yelp.com/v3/businesses/%s' % biz_id
        #response = requests.get(url=url, headers=headers)
        #response_data = response.json()

        # You would not normally do this:
        ribd = pickle.load(open(path_in_ngrams + "figures_dict_" + coy + ".p", "rb"))

        try:
            response_data = ribd[coy, full]["Response Data"]
        except:
            continue
        ###
        # Extract the business ID, name, price, rating and address

        rating = response_data['rating']
        print(rating)
        review_count = response_data['review_count']

        location = response_data['location']
        city = location["city"]
        state = location["state"]
        local = str(city) + ", " + str(state)

        rating = float(rating)
        review_count = int(review_count)

        from nltk import NaiveBayesClassifier, classify
        import processing.name_loader as name_loader
        import random


        class genderPredictor():

            def getFeatures(self):
                maleNames, femaleNames = self._loadNames()

                featureset = list()

                for nameTuple in maleNames:
                    features = self._nameFeatures(nameTuple[0])
                    male_prob, female_prob = self._getProbDistr(nameTuple)
                    features['male_prob'] = male_prob
                    features['female_prob'] = female_prob
                    featureset.append((features, 'M'))

                for nameTuple in femaleNames:
                    features = self._nameFeatures(nameTuple[0])
                    male_prob, female_prob = self._getProbDistr(nameTuple)
                    features['male_prob'] = male_prob
                    features['female_prob'] = female_prob
                    featureset.append((features, 'F'))

                return featureset

            def trainAndTest(self, trainingPercent=0.80):
                featureset = self.getFeatures()
                random.shuffle(featureset)

                name_count = len(featureset)

                cut_point = int(name_count * trainingPercent)

                train_set = featureset[:cut_point]
                test_set = featureset[cut_point:]

                self.train(train_set)

                return self.test(test_set)

            def classify(self, name):
                feats = self._nameFeatures(name)
                return self.classifier.classify(feats)

            def train(self, train_set):
                self.classifier = NaiveBayesClassifier.train(train_set)
                return self.classifier

            def test(self, test_set):
                return classify.accuracy(self.classifier, test_set)

            def _getProbDistr(self, nameTuple):
                male_prob = (nameTuple[1] * 1.0) / (nameTuple[1] + nameTuple[2])
                if male_prob == 1.0:
                    male_prob = 0.99
                elif male_prob == 0.0:
                    male_prob = 0.01
                else:
                    pass
                female_prob = 1.0 - male_prob
                return (male_prob, female_prob)

            def getMostInformativeFeatures(self, n=5):
                return self.classifier.most_informative_features(n)

            def _loadNames(self):
                return name_loader.getNameList()

            def _nameFeatures(self, name):
                name = name.upper()
                if len(name) > 2:
                    return {
                        'last_letter': name[-1],
                        'last_two': name[-2:],
                        'last_three': name[-3:],
                        'last_is_vowel': (name[-1] in 'AEIOUY')
                    }
                else:
                    return {
                        'last_letter': name[0],
                        'last_two': name[0],
                        'last_three': name[0],
                        'last_is_vowel': (name[-1] in 'AEIOUY')
                    }


        if __name__ == "__main__":
            gp = genderPredictor()
            accuracy = gp.trainAndTest()
            feats = gp.getMostInformativeFeatures(10)
            name = ''

        # Gender and Unique DF
        rest = pd.read_csv(path+full+ ".csv")

        if review_count > 5:

            rest["Username"] = rest["Username"].fillna("Postu T.")

            rest["Username"] = rest["Username"].apply(lambda x: "Postu T." if len(x) < 4 else x)

            rest["first_name"] = rest["Username"].apply(lambda x: x.split(" ")[0] if " " in x else x)

            try:
                rest["gender"] = rest["first_name"].apply(lambda x: gp.classify(x))
            except:
                rest["gender"] = "M"

            unique_num = len(rest["Username"].value_counts())

            friend_num = rest["friend_count"].sum()

            network_num = friend_num / unique_num
            # The network num should probably be benched.

            rest_unique = rest.drop_duplicates("Username").reset_index(drop=True)

            #  RATIOS

            men_num = len(rest_unique[rest_unique["gender"] == "M"])
            if men_num == 0:
                men_num = 1
            female_num = len(rest_unique[rest_unique["gender"] == "F"])
            if female_num == 0:
                female_num = 1

            male_df = rest_unique[rest_unique["gender"] == "M"]
            female_df = rest_unique[rest_unique["gender"] == "F"]

            male_female_ratio = men_num / female_num

            local_df = rest_unique[rest_unique["location"] == local]
            foreign_df = rest_unique[rest_unique["location"] != local]
            if len(local_df) < 5:
                loc_pseudo = rest["location"].value_counts().index[0]

                local_df = rest_unique[rest_unique["location"] == loc_pseudo]
                foreign_df = rest_unique[rest_unique["location"] != loc_pseudo]

            local_num = len(local_df)
            if local_num == 0:
                local_num = 1
            foreign_num = len(foreign_df)
            if foreign_num == 0:
                foreign_num = 1

            for_loc_ratio = foreign_num / local_num

            #  RATINGS

            male_rate = male_df["rating"].mean()
            female_rate = female_df["rating"].mean()

            local_rate = local_df["rating"].mean()
            foreign_rate = foreign_df["rating"].mean()

            # Network
            rest_low_friends = rest_unique[rest_unique["friend_count"] < rest_unique["friend_count"].median()]

            rest_high_friends = rest_unique[rest_unique["friend_count"] > rest_unique["friend_count"].median()]

            high_net_rate = rest_high_friends["rating"].mean()
            low_net_rate = rest_low_friends["rating"].mean()

            # Connisour
            rest_low_reviews = rest_unique[rest_unique["review_count"] < rest_unique["review_count"].median()]

            rest_high_reviews = rest_unique[rest_unique["review_count"] > rest_unique["review_count"].median()]

            high_mean_rate_rev = rest_high_reviews["rating"].mean()

            # Food Aestheticist

            rest_low_pho = rest_unique[rest_unique["photo_count"] < rest_unique["photo_count"].median()]

            rest_high_pho = rest_unique[rest_unique["photo_count"] > rest_unique["photo_count"].median()]

            high_mean_rate_pho = rest_high_pho["rating"].mean()

            # Patrons and First Timers Rating
            pats = rest["Username"].value_counts()

            rc = pats[pats > 1].index

            patrons = rest[rest["Username"].isin(list(rc.values))]

            patrons_rating = patrons['rating'].mean()

            first_timers = rest[~rest["Username"].isin(list(rc.values))]

            first_timers_rating = first_timers["rating"].mean()

            if not patrons_rating:

                patrons_rating = high_mean_rate_rev - 0.02

            first_timers_rating

            ## OTHER

            # Visual
            sum_count = rest["review_count"].sum()

            if sum_count == 0:
                sum_count = 1
            visual_index = rest["photo_count"].sum() / sum_count

            # Female
            network_num_mal = male_df["friend_count"].sum() / men_num
            network_num_fem = female_df["friend_count"].sum() / female_num

            if network_num_mal == 0:
                network_num_mal = 1
            fem_net_imp = network_num_fem / network_num_mal

            # Foreign
            local_reach = local_df["friend_count"].sum()
            foreign_reach = foreign_df["friend_count"].sum()

            if local_reach == 0:
                local_reach = 1

            for_loc_reach = foreign_reach / local_reach

            figures_dict[coy, full] = {
                "id": small,
                "Male to Female": male_female_ratio,
                "Foreign to Local": for_loc_ratio,
                "Male": male_rate,
                "Female": female_rate,
                "Local": local_rate,
                "Foreign": foreign_rate,
                "High Network": high_net_rate,
                "Low Network": low_net_rate,
                "Connoisseur": high_mean_rate_rev,
                "Food Aestheticist": high_mean_rate_pho,
                "Patrons": patrons_rating,
                "First Visit": first_timers_rating,
                "Visual Importance": visual_index,
                "Female Importance": fem_net_imp,
                "Foreign Importance": for_loc_reach,
                "Average Customer Network": network_num,
                "Total Network": friend_num,
                "Number of Reviewers": unique_num,
                "Response Data": response_data}

        else:
            continue

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_one = os.path.join(my_path, "../data/cpickle/")

    pickle.dump(figures_dict, open(path_one + "figures_dict_" + coy + ".p", "wb"))