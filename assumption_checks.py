#!/usr/bin/env python3

import os
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

# custom HYPY modules
import supfunc as sup

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
            "t": [0.0],
            "p": [0.0],
            "conclusion": False,
            "interpretation": "",
        },
        "k-squared": {
            "t": [0.0],
            "p": [0.0],
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
    # hi
    f = 0


if __name__ == "__main__":
    main()
