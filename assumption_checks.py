#!/usr/bin/env python3

import sys
import os
import math
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd

"""
CONTINUOUS DATA HYPOTHESIS TESTER

MILESTONES
- Finish implementing all assumption checks
    x Graphical checks
    x Statistical tests
- Work out all options

TODO
- Differentiate between independent and not t-test
- Get better acquainted with the assumptions and make these satisfied within the test function
- Would be cool to perform preliminary analysis on the data and suggest which test would be most suitable.
- Just put all the main assumption checks in this file, create a new python proj for the actual tests and another for the user interface.
- Change to one loop for each statistical test, lots of repeat code; condense it.
- implement sys.stdout if option selected

CURRENT WORKING
- fix uniquify function, need to replace end numerical value if it is numerical

"""

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""


def check_normality(
    data,
    data_label="",
    statistical_options=[],
    graphical_options=[],
    graph_save_path="null",
):
    # checks normailty assumption and returns dict
    # conclusion false by default
    normality_tests_dict = {
        "shapiro-wilks": {
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
        },
        "k-squared": {
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
        },
        "kolmogorov-smirnov": {
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
        },
    }
    # alpha threshold for normality tests
    alpha = 0.05

    # pass interpretation
    pass_i = "data is likely normally distributed"
    # fail interpretation
    fail_i = "data is likely not from a normal distribution"

    # create folder to store graphs
    if graph_save_path != "null":
        folder_name = r"hypy_graphical_output"
        path = os.path.join(graph_save_path, folder_name)
        path = uniquify_dir(path)
        os.mkdir(path)

    # graphical options
    for i in graphical_options:
        if i == "histogram":
            # create histogram from data
            plt.hist(
                data, edgecolor="black", density=True, bins="auto", color="b", alpha=0.8
            )
            # create normality curve line and mean vertical
            mu, std = stats.norm.fit(data)
            xmin, xmax = plt.xlim()
            x = np.linspace(xmin, xmax, 100)
            p = stats.norm.pdf(x, mu, std)
            plt.plot(x, p, "--", color="red", linewidth=1.5)
            plt.axvline(data.mean(), color="orange", linestyle="dashed", linewidth=1)

            # histogram labels
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.title(
                f"Normalized Histogram with Normal Curve: {data_label}\nμ={round(data.mean(), 4)}, σ={round(np.std(data), 4)}"
            )
            # save histogram
            hist_file_name = f"Histogram for {data_label}.png"
            hist_save_path = os.path.join(path, hist_file_name)
            plt.savefig(hist_save_path)
        elif i == "qq-plot":
            # create qq plot from data
            fig = sm.qqplot(data, line="s")
            plt.title(f"Quartile-Quartile Plot: {data_label}")
            # save figure
            qq_file_name = f"QQ-plot for {data_label}.png"
            qq_save_path = os.path.join(path, qq_file_name)
            plt.savefig(qq_save_path)

    # statistical tests
    for j in statistical_options:
        if j == "shapiro-wilks":  # reliable for samples < 1000
            test_stat_shapiro, p_value_shapiro = stats.shapiro(data)
            normality_tests_dict[j]["t"] = test_stat_shapiro
            normality_tests_dict[j]["p"] = p_value_shapiro
            if p_value_shapiro < alpha:
                normality_tests_dict[j]["interpretation"] = fail_i
            else:
                normality_tests_dict[j]["conclusion"] = True
                normality_tests_dict[j]["interpretation"] = pass_i
        elif j == "k-squared":
            test_stat_ksquare, p_value_ksquare = stats.normaltest(data)
            normality_tests_dict[j]["t"] = test_stat_ksquare
            normality_tests_dict[j]["p"] = p_value_ksquare
            if p_value_ksquare < alpha:
                normality_tests_dict[j]["interpretation"] = fail_i
            else:
                normality_tests_dict[j]["conclusion"] = True
                normality_tests_dict[j]["interpretation"] = pass_i
        elif j == "kolmogorov-smirnov":
            test_stat_ks, p_value_ks = stats.kstest(data, "norm")
            normality_tests_dict[j]["t"] = test_stat_ks
            normality_tests_dict[j]["p"] = p_value_ks
            if p_value_ks < alpha:
                normality_tests_dict[j]["interpretation"] = fail_i
            else:
                normality_tests_dict[j]["conclusion"] = True
                normality_tests_dict[j]["interpretation"] = pass_i
    return normality_tests_dict


def check_variance_equality(group_1, group_2):
    print("\nCHECKING HOMOGENEITY OF VARIANCE...")
    # progress bar
    with alive_bar(100, bar="filling") as bar:
        for i in range(100):
            sleep(0.01)
            bar()
    # alpha threshold
    alpha = 0.05
    # levenes test for equality of variances
    test_stat_variance, p_value_variance = stats.levene(group_1, group_2)
    if p_value_variance < alpha:
        variance_result = (
            f"\n \033[1m Levenes Equality of Variances Test: (test_stat=%.3f, p=%.4f < α={alpha})"
            "\033[0m"
            "\n    Conclusion: the variances of the samples are likely different\n"
            % (test_stat_variance, p_value_variance)
        )
    else:
        variance_result = (
            f"\n \033[1m Levenes Equality of Variances Test: (test_stat=%.3f, p=%.4f < α={alpha})"
            "\033[0m"
            "\n    Conclusion: the variances of the samples are likely the same\n"
        )
    return variance_result


def uniquify_dir(path):
    counter = 1
    while os.path.isdir(path):
        print(path[-1:])
        # if path[-1:].isnumeric():
        # path = path.replace(path[:-1], "")
        path = path + "_" + str(counter)
        counter += 1
    return path


def main():
    # file structure:
    # >/HyPy
    # -->output_summary.txt
    # -->/Graphics
    # ---->Histogram.png
    # ---->Q-Q Plot

    data = np.random.normal(1, 50, 325)

    # txt_summary = "/stats_output/output.txt"
    # save_path = "/Users/christopher/Desktop"  # make this user input
    # path = os.path.join(save_path, txt_summary)
    # os.makedir(path)
    # sys.stdout = open(path, "w")

    graphical_options = [
        "histogram",
        "qq-plot",
    ]
    statistical_options = [
        "shapiro-wilks",
        "k-squared",
        "kolmogorov-smirnov",
    ]

    normality_dict = check_normality(
        data,
        "Sample_1 - Frogs",
        statistical_options,
        graphical_options,
        "/Users/christopher/Desktop",
    )
    df = pd.DataFrame.from_dict(normality_dict)
    print(df)

    # sys.stdout.close()


if __name__ == "__main__":
    main()
