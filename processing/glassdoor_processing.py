from __future__ import division

# Library Packages
import regex as re
import itertools as it
import spacy
import numpy as np
import pandas as pd
import language_check

# Settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
seed = 7
np.random.seed(seed)

import warnings

warnings.filterwarnings('ignore')


def front(self, n):
    return self.iloc[:, :n]


def back(self, n):
    return self.iloc[:, -n:]


from sklearn.preprocessing import StandardScaler

np.set_printoptions(threshold=np.nan)

from datetime import datetime
from dateutil.parser import parse
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import re
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
from sklearn.preprocessing import MinMaxScaler

# Entity Extraction From Review
import itertools as it
import spacy
import os

def Standardisation(df):
    listed = list(df)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    return df


# Like normalization, standardization can be useful, and even required in some
# machine learning algorithms when your time series data has input values with differing scales.

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

code  = [x +"_review" for x in input_fields.code_or_ticker]

my_path = os.path.abspath(os.path.dirname(__file__))
path_in = os.path.join(my_path, "../data/glassdoor/")
print(path_in)


for p in ["CHIL_review",
"CPKI_review",]:
    glassdoor = pd.read_csv(path_in + p + ".csv")
    print(glassdoor.head())

    # This is just the glassdoor processing step.

    glassdoor['Review Date'] = glassdoor['Review Date'].apply(lambda x: parse(x))

    # Good
    # Bad
    # Great
    # Severe

    glassdoor["Pros"] = glassdoor["Pros"].apply(lambda x: re.sub('<br\s*?>', '. ', x))
    glassdoor["Cons"] = glassdoor["Cons"].apply(lambda x: re.sub('<br\s*?>', '. ', x))
    glassdoor["Advice to Management"] = glassdoor["Advice to Management"].fillna(value="").apply(
        lambda x: re.sub('<br\s*?>', '. ', x))

    glassdoor["Location"] = glassdoor["Location"].fillna(value="np.nan, np.nan")

    glassdoor["Location"] = glassdoor["Location"].apply(lambda x: x.split(",")[0])


    def sent(type_t, glassdoor):
        glassdoor["positive"] = 0
        glassdoor["compound"] = 0.0
        glassdoor["negative"] = 0
        glassdoor["neutral"] = 0

        analyzer = SIA()
        for sentence, row in zip(glassdoor[type_t], list(range(glassdoor.shape[0]))):
            vs = analyzer.polarity_scores(sentence)
            glassdoor["compound"][row] = float(vs["compound"])
            if vs["compound"] < -0.5:
                glassdoor["negative"][row] = 1
            elif vs["compound"] > 0.5:
                glassdoor["positive"][row] = 1
            else:
                glassdoor["neutral"][row] = 1
                # print("{:-<65} {}".format(sentence, str(vs)))

        if type_t == "Pros":

            good = glassdoor[(glassdoor["Rating"] < 4) & (glassdoor["compound"] > .0)]
            good = good.sort_values("Review Date", ascending=False)
            good["review"] = good["Pros"]

            best = glassdoor[(glassdoor["Rating"] > 3) & (glassdoor["compound"] > .0)]
            best = best.sort_values("Review Date", ascending=False)
            best["review"] = best["Pros"]

            return good, best
        elif type_t == "Cons":
            bad = glassdoor[(glassdoor["Rating"] > 2) & (glassdoor["compound"] < .0)]
            bad = bad.sort_values("Review Date", ascending=False)
            bad["review"] = bad["Cons"]

            severe = glassdoor[(glassdoor["Rating"] < 3) & (glassdoor["compound"] < .0)]
            severe = severe.sort_values("Review Date", ascending=False)
            severe["review"] = severe["Cons"]
            return bad, severe


    def gaz(type_df, time, cut, many):
        nlp = spacy.load('en')

        if cut == "True":
            type_df = type_df[type_df["Review Date"] > time]
        else:
            type_df = type_df[type_df["Review Date"] < time]

        sample_review = ""
        for i in type_df["review"]:
            sample_review = sample_review + " " + str(i)

        # print(sample_review)

        len(sample_review)

        sample_review = sample_review.replace("\\", "")

        #### Summary:

        ### Summaries
        import sumy

        from sumy.summarizers.lex_rank import LexRankSummarizer
        from sumy.summarizers.text_rank import TextRankSummarizer

        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.nlp.stemmers import Stemmer
        from sumy.utils import get_stop_words

        lexi = LexRankSummarizer(Stemmer("english"))
        texi = TextRankSummarizer(Stemmer("english"))

        parser = PlaintextParser.from_string(sample_review, Tokenizer("english"))

        texi = TextRankSummarizer(Stemmer("english"))

        rentence = "dddd"
        for sentence in texi(parser.document, 10):  # This does indeed summarise the document
            if (str(rentence).split()[len(str(rentence).split()) - 1][-1] == ".") and (len(rentence) > 2):
                rentence = rentence + " " + str(sentence)
            elif len(rentence) < 3:
                rentence = rentence + " " + str(sentence)
            else:
                rentence = rentence + ". " + str(sentence)

        stop_words = set(stopwords.words('english'))
        stop_words.update(['.', ',', '"', "'", '?', '!', '! !', ':', ';', '(', ')', '[', ']', '{',
                           '}'])  # remove it if you need punctuation

        list_of_words = [i.lower() for i in wordpunct_tokenize(sample_review) if i.lower() not in stop_words]

        final = ' '.join(list_of_words)

        from nltk.tokenize import RegexpTokenizer

        tokenizer = RegexpTokenizer(r'\w+')
        list_of_words = tokenizer.tokenize(final)
        final = ' '.join(list_of_words)

        parsed_review = nlp(final)

        # print(parsed_review)

        token_text = [token.orth_ for token in parsed_review]
        token_pos = [token.pos_ for token in parsed_review]

        df = pd.DataFrame({'token_text': token_text, 'part_of_speech': token_pos})

        # Unigrams
        import nltk
        from nltk import word_tokenize
        from nltk.util import ngrams
        from collections import Counter

        token = nltk.word_tokenize(str(parsed_review))
        grams = ngrams(token, many)

        dra = Counter(grams)

        t = pd.DataFrame()

        f = pd.DataFrame(list(dra.keys()))

        if many == 2:
            f[0] = f[0] + " " + f[1]

        if many == 3:
            f[0] = f[0] + " " + f[1] + " " + f[2]

        f = f[0]

        t["name"] = f
        t["count"] = list(dra.values())

        df = df.drop_duplicates()
        r = pd.merge(t, df, left_on=["name"], right_on=["token_text"], how="left", right_index=False)
        r = r.drop("token_text", axis=1)
        r.columns = ["name", "count", "pos"]

        scaler = MinMaxScaler()
        r["norm"] = scaler.fit_transform(r["count"].values.reshape(-1, 1))

        if many == 1:
            dfs = r[r["pos"] == "NOUN"].sort_values("count", ascending=False)
        else:
            dfs = r.sort_values("count", ascending=False)

        return dfs, rentence


    bad, severe = sent("Cons", glassdoor)
    good, great = sent("Pros", glassdoor)

    import datetime

    dar = np.datetime64('2017-01-01')

    now = datetime.datetime.now()

    six_month = now - datetime.timedelta(190)
    year = now - datetime.timedelta(365)
    three_year = now - datetime.timedelta(1150)
    five_years = now - datetime.timedelta(1800)
    first_five = good["Review Date"].min() + datetime.timedelta(1800)

    # location = ["allloc","Jacksonville","Laguna Beach"]


    my_path = os.path.abspath(os.path.dirname(__file__))
    path_out = os.path.join(my_path, "../data/ngrams/")
    print(path_out)



    type_df = {"bad": bad, "severe": severe, "good": good, "great": great}

    for k, r in type_df.items():
        for time, time_s in zip([now, first_five], ["alltime", "five_years_ago"]):
            for cut in ["False"]:
                for many in [1, 2, 3]:
                    df, sentence = gaz(r, time, cut, many)
                    df.to_csv(path_out + p + "_" + k + "_" + time_s + "_" + str(many) + ".csv")

                    tool = language_check.LanguageTool('en-US')
                    matches = tool.check(sentence)
                    sentence = language_check.correct(sentence, matches)[6:]
                    text_file = open(path_out +p + "_" + k + "_" + time_s + "_" + str(many) + ".txt", "w")
                    text_file.write(sentence)
                    text_file.close()

    for k, r in type_df.items():
        for time, time_s in zip([six_month, year, three_year, five_years],
                                ["six month", "year", "three_years", "five_years"]):
            for cut in ["True"]:
                for many in [1, 2, 3]:
                    df, sentence = gaz(r, time, cut, many)
                    df.to_csv(path_out +p + "_" + k + "_" + time_s + "_" + str(many) + ".csv")

                    tool = language_check.LanguageTool('en-US')
                    matches = tool.check(sentence)
                    sentence = language_check.correct(sentence, matches)[6:]
                    text_file = open(path_out +p + "_" + k + "_" + time_s + "_" + str(many) + ".txt", "w")
                    text_file.write(sentence)
                    text_file.close()


