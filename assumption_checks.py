#!/usr/bin/env python3

import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

# custom HYPY modules
import hypy_supfunc as sup

"""
CONTINUOUS DATA HYPOTHESIS TESTER

MILESTONES
- Finish implementing all assumption checks
    x Graphical checks
    x Statistical tests

TODO
- Differentiate between independent and not t-test
- Would be cool to perform preliminary analysis on the data and suggest which test would be most suitable.
- Add descriptives output
- Make data labels more clear, remove them from list
- Create "Report Writer" that pulls everything in, all pngs and info and culminates it into one document using the statistical report formulas to do a basic write-up on it.

CURRENT WORKING

NOTES
- maybe seperate the functions that arent directly related to the hypy program into a seperate file

IMPORTANT README INFO
- This program is for measuring continuous, normally distributed, randomly sampled, and homogenous samples.
- Default dpi for output set to 150
- Bartletts should only be used on normally distributed data
- TTESTS are used to compare the means of two related or unrelated sample groups. Tests the applicability of an assumption to a population of interest. Ttests are only applicable to two data groups.
    - One-tailed t-test is DIRECTIONAL, determines the difference in sample means in a single direction (right or left tail).
    - Two-tailed is non-directional, determines if there is any relationship between sample means in either direction.
    - So when you expect a single value hypothesis, like mean1=mean2, a one-tailed test would be preferable. A two-tailed test makes more sense if your hypothesis assumes means to be greater than or less than each other.
"""

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""


def check_normality(
    data,
    data_label="",
    statistical_options=[],
    figure_options=[],
    figs_save_path="null",
    dpi=150,
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
    }
    # graphical options
    for i in figure_options:
        if i == "histogram" and figs_save_path != "null":
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
            hist_file_name = f"{data_label} - Histogram.png"
            hist_save_path = os.path.join(figs_save_path, hist_file_name)
            plt.savefig(hist_save_path, dpi=dpi)
        elif i == "qq-plot" and figs_save_path != "null":
            # create qq plot from data
            fig = sm.qqplot(data, line="s")
            plt.title(f"QQ-Plot - {data_label}")
            # save figure
            qq_file_name = f"{data_label} - QQ-Plot.png"
            qq_save_path = os.path.join(figs_save_path, qq_file_name)
            plt.savefig(qq_save_path, dpi=dpi)

    # normality statistical test options
    for j in statistical_options:
        if j == "shapiro-wilks":  # reliable for samples < 1000
            test_stat_shapiro, p_value_shapiro = stats.shapiro(data)
            normality_tests_dict[j]["t"] = test_stat_shapiro
            normality_tests_dict[j]["p"] = p_value_shapiro
            sup.test_p_value(p_value_shapiro, "shapiro-wilks", normality_tests_dict)
        elif j == "k-squared":
            test_stat_ksquare, p_value_ksquare = stats.normaltest(data)
            normality_tests_dict[j]["t"] = test_stat_ksquare
            normality_tests_dict[j]["p"] = p_value_ksquare
            sup.test_p_value(p_value_ksquare, "k-squared", normality_tests_dict)

    # return dict containing results
    return normality_tests_dict


def check_variance_equality(group_1, group_2, statistical_options=[]):
    # checks homogeneity of variances assumption and returns results dict
    variance_tests_dict = {
        "bartletts": {
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
        },
        "levenes": {
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
        },
    }
    # variance statistical test options
    for j in statistical_options:
        if j == "levenes":
            test_stat_lev, p_value_lev = stats.levene(group_1, group_2)
            variance_tests_dict[j]["t"] = test_stat_lev
            variance_tests_dict[j]["p"] = p_value_lev
            sup.test_p_value(p_value_lev, "levenes", variance_tests_dict)
        elif j == "bartletts":
            test_stat_bart, p_value_bart = stats.bartlett(group_1, group_2)
            variance_tests_dict[j]["t"] = test_stat_bart
            variance_tests_dict[j]["p"] = p_value_bart
            sup.test_p_value(p_value_bart, "bartletts", variance_tests_dict)

    # return dict containing results
    return variance_tests_dict


def main():
    data1 = np.random.normal(1, 500, 345)

    # = sup.import_csv_column(
    #    "/Users/christopher/my_programs/sample_csvs/sample1.csv", "35", float
    # )

    data2 = np.random.normal(2, 400, 350)

    # = sup.import_csv_column(
    #    "/Users/christopher/my_programs/sample_csvs/sample1.csv", "3", int
    # )

    parent_dir, figs_dir, stats_dir = sup.build_hypy_directory(
        "/Users/christopher/Desktop"
    )

    graphical_options = [
        "histogram",
        "qq-plot",
    ]
    statistical_options = [
        "shapiro-wilks",
        "k-squared",
        "kolmogorov-smirnov",
        "levenes",
        "bartletts",
    ]

    normality_dict = check_normality(
        data2,
        "Sample_1",
        statistical_options,
        graphical_options,
        figs_dir,
        300,
    )

    variance_dict = check_variance_equality(
        data2,
        data1,
        statistical_options,
    )

    # export normal stats
    sup.export_dict_png(
        normality_dict,
        "Statstical Normality Tests",
        ["Frogs"],
        stats_dir,
        300,
    )

    # export variance stats
    sup.export_dict_png(
        variance_dict,
        "Homogeneity of Variance Tests",
        ["Frogs", "Dogs"],
        stats_dir,
        300,
    )


if __name__ == "__main__":
    main()
