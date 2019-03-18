
def darn(target_location_info, benchmark_code_info, bench_location_info):

    import os
    import pandas as pd
    import _pickle as pickle

    my_path = os.path.abspath(os.path.dirname('__file__'))
    path_in_file = os.path.join(my_path, "input_fields.csv")
    path = os.path.join(my_path, "data/cpickle/")
    ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))
    path_in_ngrams = os.path.join(my_path, "data/cpickle/")

    input_fields = pd.read_csv(path_in_file)
    input_fields = pd.read_csv(path_in_file)

    target_code = input_fields[input_fields["starting"] == 1]["code_or_ticker"].reset_index(drop=True)[0]

    bench_code = benchmark_code_info

    target_short_name = \
    input_fields[input_fields["code_or_ticker"] == target_code]["short_name"].reset_index(drop=True)[0]
    bench_short_name = input_fields[input_fields["code_or_ticker"] == bench_code]["short_name"].reset_index(drop=True)[
        0]

    path = os.path.join(my_path, "data/cpickle/")
    ext_info_dict = pickle.load(open(path + "ext_info_dict.p", "rb"))
    # all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    # first_option_target_location_small_name = all_target_location_small_names[0].title()
    all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]

    first_option_target_location_file_name = all_target_location_file_names[0]

    # all_target_location_full_addresses =ext_info_dict[target_code]["All Target Location Full Addresses"]
    all_target_location_small_names = ext_info_dict[target_code]["All Target Location Small Names"]
    all_target_location_file_names = ext_info_dict[target_code]["All Target Location File Names"]

    nas = pd.DataFrame()
    nas["Small Names"] = all_target_location_small_names
    nas["File Name"] = all_target_location_file_names

    target_location_file_name = nas[nas["Small Names"] == target_location_info]["File Name"].reset_index(drop=True)[0]

    all_target_location_small_names = ext_info_dict[bench_code]["All Target Location Small Names"]
    all_target_location_file_names = ext_info_dict[bench_code]["All Target Location File Names"]

    nas = pd.DataFrame()
    nas["Small Names"] = all_target_location_small_names
    nas["File Name"] = all_target_location_file_names

    bench_location_file_name = nas[nas["Small Names"] == bench_location_info]["File Name"].reset_index(drop=True)[0]

    my_path = os.path.abspath(os.path.dirname('__file__'))

    path_in_ngrams = os.path.join(my_path, "data/cpickle/")

    path_in_file = os.path.join(my_path, "input_fields.csv")

    def dicto(coy, bench, location):

        city = location

        figures_dict_c = pickle.load(open(path_in_ngrams + "figures_dict_" + coy + ".p", "rb"))
        figures_dict_b = pickle.load(open(path_in_ngrams + "figures_dict_" + bench + ".p", "rb"))

        from math import cos, asin, sqrt

        def distance(lat1, lon1, lat2, lon2):
            p = 0.017453292519943295
            a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
            return 12742 * asin(sqrt(a))


            #     def closest(data, v):
            #         return min(data, key=lambda p: distance(v['lat'], v['lon'], p['lat'], p['lon']))

        def closest(data, v):
            pas = {}
            for i in data:
                pas[i["name"]] = distance(v['lat'], v['lon'], i['lat'], i['lon'])
            return pas

        lat_list = []
        lon_list = []
        name_list = []
        for key, values in figures_dict_b.items():
            location = key[1]
            name_list.append(location)
            lat = values["Response Data"]["coordinates"]["latitude"]
            lon = values["Response Data"]["coordinates"]["longitude"]
            lat_list.append(lat)
            lon_list.append(lon)

        das = [{"lat": lat, "lon": lon, "name": name} for lat, lon, name in zip(lat_list, lon_list, name_list)]

        coy_target = figures_dict_c[coy, city]

        v = {'lat': coy_target["Response Data"]["coordinates"]["latitude"],
             'lon': coy_target["Response Data"]["coordinates"]["longitude"]}

        close = closest(das, v)
        return close

    dictoo = dicto(target_code, bench_code, target_location_file_name)
    dar = pd.DataFrame.from_dict(dictoo, orient='index')
    dar.columns = ["value"]
    dar = dar.sort_values(by="value")
    dar = dar[:5]

    dictoo_be = dicto(bench_code, target_code, dar.index[0])
    dar_be = pd.DataFrame.from_dict(dictoo_be, orient='index')
    dar_be.columns = ["value"]
    dar_be = dar_be.sort_values(by="value")
    dar_be = dar_be[:5]

    figures_dict = pickle.load(open(path_in_ngrams + "figures_dict_" + target_code + ".p", "rb"))
    fig_d = figures_dict[target_code, dar_be.index[0]]

    kar = pd.DataFrame.from_dict(fig_d, orient='index')

    kar.columns = [kar[0][0]]

    kar = kar[1:-1]

    for i in dar_be.index:
        fig_d = figures_dict[target_code, i]

        var = pd.DataFrame.from_dict(fig_d, orient='index')

        var.columns = [var[0][0]]

        var = var[1:-1]

        kar[var.columns[0]] = var

    kar.iloc[:-2, :] = kar.iloc[:-2, :].apply(pd.to_numeric).round(2)

    figures_dict_d = pickle.load(open(path_in_ngrams + "figures_dict_" + bench_code + ".p", "rb"))
    fig_b = figures_dict_d[bench_code, dar.index[0]]

    sar = pd.DataFrame.from_dict(fig_d, orient='index')

    sar.columns = [sar[0][0]]

    sar = sar[1:-1]

    for i in dar.index:
        fig_b = figures_dict_d[bench_code, i]

        var = pd.DataFrame.from_dict(fig_b, orient='index')

        var.columns = [var[0][0]]

        var = var[1:-1]

        sar[var.columns[0]] = var

    sar.iloc[:-2, :] = sar.iloc[:-2, :].apply(pd.to_numeric).round(2)

    sar = sar.iloc[:, :4]

    cols = []
    for i in sar.columns:
        cols.append(bench_short_name + ": " + i)

    sar.columns = cols

    kar = kar.iloc[:, :4]

    cols = []
    for i in kar.columns:
        cols.append(target_short_name + ": " + i)

    kar.columns = cols

    final = pd.concat((kar, sar), axis=1)
    return final