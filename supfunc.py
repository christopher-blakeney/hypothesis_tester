import os
import dataframe_image as dfi
import pandas as pd
import csv
import codecs
import numpy as np

# set alpha threshold
global ALPHA
ALPHA = 0.05


def change_dict_key(dic, old_key, new_key, default=None):
    dic[new_key] = dic.pop(old_key, default)


def import_csv_column(csvfile, col, dtype):
    data = codecs.open(csvfile, "r", encoding="utf-8", errors="ignore")
    file = csv.DictReader(data)
    lst = []
    for i in file:
        lst.append(dtype(i[col]))
    array = np.array(lst)
    return array


def export_dict_png(
    dic,
    nested=False,
    df_title="Title",
    data_labels=[],
    save_path="null",
    dpi=150,
    highlight_red=False,
):
    # deal with nested garbage
    if nested:
        df = pd.DataFrame.from_dict(
            {(i, j): dic[i][j] for i in dic.keys() for j in dic[i].keys()},
            orient="index",
        )
    else:
        df = pd.DataFrame.from_dict(dic)  # .transpose()
    # save output to savepath
    stat_file_name = f"{df_title}.png"
    stat_save_path = os.path.join(save_path, stat_file_name)
    if len(data_labels) == 2:
        styled_df = df.style.set_caption(
            f"{df_title}: {data_labels[0]}, {data_labels[1]}"
        ).format(precision=3)
    else:
        styled_df = df.style.set_caption(f"{df_title}: {data_labels[0]}").format(
            precision=3
        )
    if highlight_red:
        styled_df = styled_df.applymap(highlight_fail)
    dfi.export(styled_df, stat_save_path, dpi=dpi)


def highlight_fail(cell):
    if type(cell) != str and cell < ALPHA:
        return "color: red"
    else:
        return "color: black"


def test_p_value(p, test, result_dict):
    # check whether t-test, wherein interpretation flipped
    t = False
    # set interpretations based on input dict
    if test in ["bartletts", "levenes"]:
        less_p = "likely NOT homogeneous"
        greater_p = "likely homogeneous"
    elif test in ["shapiro-wilks", "k-squared", "kolmogorov-smirnov"]:
        less_p = "likely NOT normally distributed"
        greater_p = "likely normally distributed"
    elif test in ["one-sample", "two-sample"]:
        less_p = "likely from the same population"
        greater_p = "likely NOT from the same population"
        t = True
    # test p
    if p < ALPHA and not t:
        result_dict[test]["interpretation"] = less_p
    elif p < ALPHA and t:
        result_dict[test]["interpretation"] = less_p
        result_dict[test]["conclusion"] = True
    elif p > ALPHA and t:
        result_dict[test]["conclusion"] = False
        result_dict[test]["interpretation"] = greater_p
    else:
        result_dict[test]["conclusion"] = True
        result_dict[test]["interpretation"] = greater_p


def build_hypy_directory(save_path="null", figs=True, stats=True, ttest=True):
    # file structure:
    # >/hypy_output (or hypy_output_1 etc if already exists)
    # -->/t_test # added by test dir function
    # ---->t_test.png
    # ---->report.md
    # -->/assumption_tests
    # ---->/stats
    # ------>Normality.png
    # ------>Variance.png
    # ---->/figures
    # ------>Histogram.png
    # ------>Q-Q Plot.png
    if save_path != "null":
        parent_path = uniquify_dir(os.path.join(save_path, r"hypy_output"))
        assumptions_path = os.path.join(parent_path, r"assumption_tests")
        path_structure = [parent_path, assumptions_path]
        figs_path = os.path.join(assumptions_path, r"figures")
        stats_path = os.path.join(assumptions_path, r"stats")
        if figs:
            path_structure.append(figs_path)
        if stats:
            path_structure.append(stats_path)
        for path in path_structure:
            os.mkdir(path)
    else:
        print("Please provide save path to build directory")
    return parent_path, assumptions_path, figs_path, stats_path


def build_testdir(parent_path, test):
    path_structure = []
    ttest_path = os.path.join(parent_path, r"t_test")
    if test == "ttest":
        path_structure.append(ttest_path)
    for path in path_structure:
        os.mkdir(path)
    return ttest_path


def uniquify_dir(path):
    counter = 1
    while os.path.exists(path):
        if path[-1:].isnumeric():
            counter = int(path[-1:]) + 1
            path = path.replace(path[-1:], str(counter))
        else:
            path = path + "_" + str(counter)
        counter += 1
    return path


def export_assump_summary(savepath, string):
    f = open(os.path.join(savepath, "quick_summary.txt"), "w")
    f.write(string)
    f.close()
