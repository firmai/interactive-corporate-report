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


def Standardisation(df):
    listed = list(df)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df)
    df = pd.DataFrame(scaled)
    df.columns = listed
    return df


# Like normalization, standardization can be useful, and even required in some
# machine learning algorithms when your time series data has input values with differing scales.


import pandas as pd
import plotly.plotly as py
from plotly.graph_objs import *
# py.sign_in('snowde', 'm12EGGpG9bqMssuzLnjY')

from scipy import signal

from datetime import datetime, timedelta

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

init_notebook_mode(connected=True)

from datetime import datetime
from dateutil.parser import parse

#companies = ["BJRI_gd_"]

import os

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

code  = [x +"_interview" for x in input_fields.code_or_ticker]

my_path = os.path.abspath(os.path.dirname(__file__))
path_in = os.path.join(my_path, "../data/glassdoor/")
print(path_in)


for p in code:

    inter = pd.read_csv(path_in + p + ".csv")

    # Cleaning up some bad parsing.

    inter["Offer"] = inter["Offer"].apply(lambda x: x[2:-2])
    inter["Application"] = inter["Application"].apply(lambda x: x[2:-2])
    inter["Experience"] = inter["Experience"].apply(lambda x: x[2:-2])
    inter["Interview"] = inter["Interview"].apply(lambda x: x[2:-2])
    inter["Interview Type"] = inter["Interview Type"].apply(lambda x: x[2:-2])
    inter["Question"] = inter["Question"].apply(lambda x: x[2:-2])

    inter['Interview Date'] = inter['Interview Date'].apply(lambda x: parse(x))

    inter = inter.sort_values("Interview Date")

    pos = inter[inter["Experience"] == "Positive Experience"].reset_index(drop=True)
    neg = inter[inter["Experience"] == "Negative Experience"].reset_index(drop=True)

    easy = inter[inter["Interview Type"] == "Easy Interview"].reset_index(drop=True)
    diff = inter[inter["Interview Type"] == "Difficult Interview"].reset_index(drop=True)

    type_df = {"Positive": pos, "Negative": neg, "Easy": easy, "Difficult": diff}

    parse_df = {}

    for key, value in type_df.items():
        sand_df = value
        print(sand_df.shape)

        questions = ""
        comments = ""

        for i in sand_df["Question"]:
            questions = questions + " " + str(i)

        for i in sand_df["Interview"]:
            comments = comments + " " + str(i)

        questions = questions.replace(",Answer Question", '')
        questions = questions.replace(u'\xa0', u'')
        questions = questions.replace("  ,1 Answer ", '')
        questions = questions.replace("1 Answer,", '')
        questions = questions.replace("2 Answers", '')
        questions = questions.replace("3 Answers", '')

        questions = questions.replace("  ,", '')
        questions = questions.replace(u'   ', u'')
        # Interesting,the old switchero seems to work.
        questions = questions.replace("'", '"')
        questions = questions.replace('"', "'")

        comments = comments.replace("'", '"')
        comments = comments.replace('"', "'")

        parse_df[key, "questions"] = questions
        parse_df[key, "comments"] = comments


    def gaz(doc_str, many):

        nlp = spacy.load('en')

        # doc_str = doc_str.replace("\\", "")

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

        parser = PlaintextParser.from_string(doc_str, Tokenizer("english"))

        texi = TextRankSummarizer(Stemmer("english"))

        rentence = "dddd"
        for sentence in texi(parser.document, 20):  # This does indeed summarise the document


            if (str(rentence).split()[len(str(rentence).split()) - 1][-1] == ".") and (len(rentence) > 2):
                rentence = rentence + " " + str(sentence)
            elif len(rentence) < 3:
                rentence = rentence + " " + str(sentence)
            else:
                rentence = rentence + ". " + str(sentence)

        stop_words = set(stopwords.words('english'))
        stop_words.update(['.', ',', '"', "'", '?', '!', '! !', ':', ';', '(', ')', '[', ']', '{',
                           '}'])  # remove it if you need punctuation

        list_of_words = [i.lower() for i in wordpunct_tokenize(doc_str) if i.lower() not in stop_words]

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


    carse = {}
    rents = {}
    for r in type_df.keys():
        for s in ["questions"]:
            doc_str = parse_df[r, s]
            sat, rentence = gaz(doc_str, 3)


            # tool = language_check.LanguageTool('en-US')
            # matches = tool.check(rentence)
            # rentence = language_check.correct(rentence, matches)

            def tsplit(s, sep):
                stack = [s]
                for char in sep:
                    pieces = []
                    for substr in stack:
                        pieces.extend(substr.split(char))
                    stack = pieces
                return stack


            gas = []
            for i in ["Why", "What", "Do", "How", "When", "If", "Can"]:

                das = tsplit(rentence.replace(",", "."), [i])
                for d in das:
                    d = i + d
                    gas.append(d)

            kaf = []
            for da in gas:
                sar = da.split(".")
                for d in sar:
                    kaf.append(d)

            top = []
            i = -1
            for va in kaf:
                i = i + 1
                if len(va) > 10:
                    if va[-1] == "?":
                        if len(va) < 69:
                            if va.startswith(("Why", "What", "Do", "How", "When", "If", "Can")):
                                top.append(va)

            top = set(top)

            carse[r, s] = sat
            rents[r, s] = top


    def sent(type_t):
        # "Positive", "Easy"

        ter = pd.DataFrame()

        ter["int"] = type_df[type_t]["Interview"]
        ter["Interview Date"] = type_df[type_t]["Interview Date"]

        ter["positive"] = 0
        ter["negative"] = 0
        ter["easy"] = 0
        ter["neutral"] = 0
        ter["difficult"] = 0
        ter["compound"] = 0.0

        ter = ter.iloc[:-5, :]
        analyzer = SIA()

        for sentence, row in zip(ter["int"], list(range(ter["int"].shape[0]))):
            vs = analyzer.polarity_scores(sentence)
            ter["compound"][row] = float(vs["compound"])
            if vs["compound"] < -0.5:
                ter["negative"][row] = 1
            elif vs["compound"] > 0.5:
                ter["positive"][row] = 1
            else:
                ter["neutral"][row] = 1
                # print("{:-<65} {}".format(sentence, str(vs)))

        good = ter[ter["positive"] == 1]
        good = good.sort_values("Interview Date", ascending=False)

        return good


    def sent_n(type_t):
        # "Negative"

        ter = pd.DataFrame()

        ter["int"] = type_df[type_t]["Interview"]
        ter["Interview Date"] = type_df[type_t]["Interview Date"]

        ter["positive"] = 0
        ter["negative"] = 0
        ter["easy"] = 0
        ter["neutral"] = 0
        ter["difficult"] = 0
        ter["compound"] = 0.0

        ter = ter.iloc[:-5, :]
        analyzer = SIA()

        for sentence, row in zip(ter["int"], list(range(ter["int"].shape[0]))):
            vs = analyzer.polarity_scores(sentence)
            ter["compound"][row] = float(vs["compound"])
            if vs["compound"] < 0.2:
                ter["negative"][row] = 1
            elif vs["compound"] > 0.5:
                ter["positive"][row] = 1
            else:
                ter["neutral"][row] = 1
                # print("{:-<65} {}".format(sentence, str(vs)))

        bad = ter[ter["negative"] == 1]
        bad = bad.sort_values("Interview Date", ascending=False)

        return bad


    pos = sent("Positive")
    neg = sent_n("Negative")

    easy = sent("Easy")
    diff = diff

    type_df_new = {"Positive": pos, "Negative": neg, "Easy": easy, "Difficult": diff}

    for key, value in type_df_new.items():
        sand_df = value
        print(sand_df.shape)

        questions = ""
        comments = ""

        if key == "Difficult":
            for i in sand_df["Interview"]:
                comments = comments + " " + str(i)
        else:
            for i in sand_df["int"]:
                comments = comments + " " + str(i)

        comments = comments.replace("'", '"')
        comments = comments.replace('"', "'")

        parse_df[key, "comments"] = comments

    for r in type_df.keys():
        for s in ["comments"]:
            doc_str = parse_df[r, s]
            sat, rentence = gaz(doc_str, 3)

            tool = language_check.LanguageTool('en-US')
            matches = tool.check(rentence)
            rentence = language_check.correct(rentence, matches)[6:]

            carse[r, s] = sat
            rents[r, s] = rentence

    import _pickle as pickle

    my_path = os.path.abspath(os.path.dirname(__file__))
    path_out = os.path.join(my_path, "../data/interviews/")
    print(path_out)

    pickle.dump(rents, open(path_out + p + ".p", "wb"))