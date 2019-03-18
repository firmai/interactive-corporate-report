import pickle
import pandas as pd
import os



my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")

input_fields = pd.read_csv(path)

path_in = os.path.join(my_path, "../data/glassdoor/")

path_out = os.path.join(my_path, "../data/cpickle/")


for p in input_fields["code_or_ticker"]:

    benefits = pd.read_csv(path_in + p + "_benefits.csv")

    pos_ben = [ga[3:-3] for ga in benefits[benefits["Rating"]>3].reset_index(drop=True)["Description"].values]

    neg_ben = [ga[3:-3] for ga in benefits[benefits["Rating"]<3].reset_index(drop=True)["Description"].values]

    ra = " "
    for sa in neg_ben:
        ra = ra + sa

    ra = ra.replace("'", '"')
    ra = ra.replace('"', "'")


    from sumy.summarizers.lex_rank import LexRankSummarizer
    from sumy.summarizers.text_rank import TextRankSummarizer

    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.utils import get_stop_words

    lexi = LexRankSummarizer(Stemmer("english"))
    texi = TextRankSummarizer(Stemmer("english"))

    parser = PlaintextParser.from_string(ra, Tokenizer("english"))

    texi = TextRankSummarizer(Stemmer("english"))

    rentence = "dddd"
    for sentence in texi(parser.document, 20):  # This does indeed summarise the document


        if (str(rentence).split()[len(str(rentence).split()) - 1][-1] == ".") and (len(rentence) > 2):
            rentence = rentence + " " + str(sentence)
        elif len(rentence) < 3:
            rentence = rentence + " " + str(sentence)
        else:
            rentence = rentence + ". " + str(sentence)

    negative = rentence[6:]

    ra = " "
    for sa in pos_ben:
        ra = ra + sa

    ra = ra.replace("'", '"')
    ra = ra.replace('"', "'")


    from sumy.summarizers.lex_rank import LexRankSummarizer
    from sumy.summarizers.text_rank import TextRankSummarizer

    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.nlp.stemmers import Stemmer
    from sumy.utils import get_stop_words

    lexi = LexRankSummarizer(Stemmer("english"))
    texi = TextRankSummarizer(Stemmer("english"))

    parser = PlaintextParser.from_string(ra, Tokenizer("english"))

    texi = TextRankSummarizer(Stemmer("english"))

    rentence = "dddd"
    for sentence in texi(parser.document, 20):  # This does indeed summarise the document


        if (str(rentence).split()[len(str(rentence).split()) - 1][-1] == ".") and (len(rentence) > 2):
            rentence = rentence + " " + str(sentence)
        elif len(rentence) < 3:
            rentence = rentence + " " + str(sentence)
        else:
            rentence = rentence + ". " + str(sentence)

    positive = rentence[6:]

    dict_ben = {}
    dict_ben["positive"] = positive
    dict_ben["negative"] = negative

    pickle.dump(dict_ben, open(path_out +p + "_benefits.p", "wb"))