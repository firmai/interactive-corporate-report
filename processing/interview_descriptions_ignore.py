
import pickle
import pandas as pd
import os

p = "BJRI"

my_path = os.path.abspath(os.path.dirname(__file__))
path_2 = os.path.join(my_path, "../input_fields.csv")
path_in_pickle = os.path.join(my_path, "../data/cpickle/")

path_in_pickle

rents = pickle.load(open(path_in_pickle + p +"_gd_rents.p", "rb"))

neg_que = rents["Negative", "questions"]

neg_com = rents["Negative", "comments"]