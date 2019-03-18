import _pickle as pickle
import os
import pandas as pd
import layout.polar_figure as pf
import json

###
from processing.stock_narration import describe
import processing.frames as fm
from layout.figures import figs
from datetime import datetime, timedelta
# Loading Paths and Input Fields
my_path = os.path.abspath(os.path.dirname('__file__'))
path = os.path.join(my_path, "../data/cpickle/")
ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))
my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../input_fields.csv")
input_fields = pd.read_csv(path)


first_option_target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

first_option_target_long_name = input_fields[input_fields["code_or_ticker"] == first_option_target_code]["yelp_name"].reset_index(drop=True)[0]

first_option_bench_code = input_fields[input_fields["starting"] == 2]["code_or_ticker"].reset_index(drop=True)[0]

first_option_bench_long_name = input_fields[input_fields["code_or_ticker"] == first_option_bench_code]["yelp_name"].reset_index(drop=True)[0]


all_benchmark_codes = ext_info_dict[first_option_target_code]["All Benchmark Codes"]

all_target_location_small_names = ext_info_dict[first_option_target_code]["All Target Location Small Names"]

first_option_target_location_small_name = all_target_location_small_names[0].title()

temp_df = pd.DataFrame()
temp_df["All Target Location Full Addresses"] = ext_info_dict[first_option_target_code]["All Target Location Full Addresses"]
temp_df["All Target Location Small Names"] = ext_info_dict[first_option_target_code]["All Target Location Small Names"]
target_location_address = temp_df[temp_df["All Target Location Small Names"] == first_option_target_location_small_name]["All Target Location Full Addresses"].reset_index(drop=True)[0]


diffy = {'target_location_address': target_location_address,
         'first_option_bench_long_name': first_option_bench_long_name,
         "first_option_target_long_name": first_option_target_long_name,
         'first_option_target_location_small_name': first_option_target_location_small_name,
         'first_option_bench_code': first_option_bench_code,
         'first_option_target_code': first_option_target_code}

all_target_location_addresses = ext_info_dict[diffy["first_option_target_code"]]["All Target Location Full Addresses"]

all_target_location_small_names = ext_info_dict[diffy["first_option_target_code"]]["All Target Location Small Names"]

target_location_small_drop_down_options = [{'label': r, 'value': i} for r, i in zip(all_target_location_addresses , all_target_location_small_names)]

all_benchmark_codes = ext_info_dict[diffy["first_option_target_code"]]["All Benchmark Codes"]
all_benchmark_small_names = ext_info_dict[diffy["first_option_target_code"]]["All Benchmark Small Names"]

bench_code_drop_down_options = [{'label': r, 'value': i} for r, i in zip(all_benchmark_small_names, all_benchmark_codes)]

s_metrics_df_output = ext_info_dict[diffy["first_option_target_code"]]["Stakeholder Metrics"]
s_metrics_df_1_output = ext_info_dict[diffy["first_option_target_code"]]["Stakeholder Metrics"]
c_metrics_df_output = ext_info_dict[diffy["first_option_target_code"]]["Company Metrics"]
dict_info_output = ext_info_dict[diffy["first_option_target_code"]]["Stakeholder Description"]

c_metrics_df_output_1 = ext_info_dict[diffy["first_option_target_code"]]["Company Metrics"]

stock_plot_desc_output, _ = describe(diffy["first_option_target_code"], diffy["first_option_bench_code"])

title_output = str(diffy["first_option_target_long_name"]) + " 4-D Report"
location_output = str(diffy["target_location_address"]) + " Location"
profile_output = str(diffy["first_option_target_location_small_name"]) + " Profile"


df_perf_summary_output = fm.fin_met(diffy["first_option_bench_code"], diffy["first_option_target_code"])



first_dict = {}
#first_dict[""]

first_dict["target_location_small_drop_down_options"] = target_location_small_drop_down_options
first_dict["bench_code_drop_down_options"] = bench_code_drop_down_options
first_dict["first_option_target_location_small_name"] = first_option_target_location_small_name
first_dict["first_option_target_code"] = first_option_target_code
first_dict["first_option_bench_code"] = first_option_bench_code
first_dict["s_metrics_df_output"] = s_metrics_df_output
first_dict["dict_info_output"] = dict_info_output


first_dict["c_metrics_df_output"] = c_metrics_df_output
first_dict["stock_plot_desc_output"] = stock_plot_desc_output
first_dict["title_output"] = title_output
first_dict["location_output"] = location_output
first_dict["profile_output"] = profile_output
first_dict["df_perf_summary_output"] = df_perf_summary_output


my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "../data/cpickle/")

pickle.dump(first_dict, open(path + "first_page.p", "wb"))

