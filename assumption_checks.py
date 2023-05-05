#!/usr/bin/env python3

import sys
import os
import math
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
import pandas as pd
from alive_progress import alive_bar
from time import sleep

"""
CONTINUOUS DATA HYPOTHESIS TESTER

MILESTONES
- Finish implementing all assumption checks
    x Graphical checks
    - Statistical tests
- Work out all options

TODO
- Differentiate between independent and not t-test
- Get better acquainted with the assumptions and make these satisfied within the test function
- Would be cool to perform preliminary analysis on the data and suggest which test would be most suitable.
- Just put all the main assumption checks in this file, create a new python proj for the actual tests and another for the user interface.
- Change to one loop for each statistical test, lots of repeat code; condense it.
- implement sys.stdout if option selected
"""

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""


def check_normality(data, data_label="", options=[]):
    print("\nCHECKING NORMALITY...")
    # progress bar
    with alive_bar(100, bar="filling") as bar:
        for i in range(100):
            sleep(0.01)
            bar()
    print(f"\n> \033[1m {data_label}")
    print("\033[0m")
    print("\nDescriptive Statistics:")
    df = pd.DataFrame(data)
    print(df.describe())
    # counter to track how many tests have passed
    normality_checks_passed = 0
    # alpha threshold
    alpha = 0.05
    # set results to null as default
    shapiro_result = "not included in analysis"
    ksquare_result = "not included in analysis"
    ks_result = "not included in analysis"
    # loop over options
    for option in options:
        # graphical tests
        # generate histogram if option is selected
        if option == "histogram":
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
                f"Normalized Histogram with Normal Curve\nμ={round(data.mean(), 4)}, σ={round(np.std(data), 4)}"
            )
            plt.show()
            # print(data.mean(), data.std())
            # generate Q-Q plot if option is selected
        elif option == "qq-plot":
            fig = sm.qqplot(data, line="s")
            plt.title("Quartile-Quartile Plot")
            plt.show()

            # non-graphical tests
        elif option == "shapiro-wilks":  # reliable on samples < 1000
            test_stat_shapiro, p_value_shapiro = stats.shapiro(data)
            if p_value_shapiro < alpha:
                shapiro_result = (
                    f"\n \033[1m Shapiro-Wilks W Test: (test-stat=%.3f, p=%.4f < α={alpha})"
                    "\033[0m"
                    f"\n    Conclusion: data is likely NOT normally distributed\n"
                    % (test_stat_shapiro, p_value_shapiro)
                )
            else:
                shapiro_result = (
                    f"\n \033[1m Shapiro-Wilks W Test: (test-stat=%.3f, p=%.4f > α={alpha})"
                    "\033[0m"
                    "\n    Conclusion: data is likely normally distributed\n"
                    % (test_stat_shapiro, p_value_shapiro)
                )
                normality_checks_passed += 1
        elif option == "k-squared":
            test_stat_ksquare, p_value_ksquare = stats.normaltest(data)
            if p_value_ksquare < alpha:
                ksquare_result = (
                    f"\n \033[1m D'Agostino's K-Squared Test: (test-stat=%.3f, p=%.4f < α={alpha})"
                    "\033[0m"
                    f"\n    Conclusion: data is likely NOT normally distributed\n"
                    % (test_stat_ksquare, p_value_ksquare)
                )
            else:
                ksquare_result = (
                    f"\n \033[1m D'Agostino's K-Squared Test: (test-stat=%.3f, p=%.4f > α={alpha})"
                    "\033[0m"
                    "\n    Conclusion: data is likely normally distributed\n"
                    % (test_stat_ksquare, p_value_ksquare)
                )
                normality_checks_passed += 1
        elif option == "kolmogorov-smirnov":
            test_stat_ks, p_value_ks = stats.kstest(data, "norm")
            if p_value_ks < alpha:
                ks_result = (
                    f"\n \033[1m Kolomogorov-Smirnov Test for Normality: (test-stat=%.3f, p=%.4f < α={alpha})"
                    "\033[0m"
                    f"\n    Conclusion: data is likely NOT normally distributed\n"
                    % (test_stat_ks, p_value_ks)
                )
            else:
                ks_result = (
                    f"\n \033[1m Kolomogorov-Smirnov Test for Normality: (test-stat=%.3f, p=%.4f > α={alpha})"
                    "\033[0m"
                    "\n    Conclusion: data is likely normally distributed\n"
                    % (test_stat_ks, p_value_ks)
                )
                normality_checks_passed += 1
        summary = (
            f"\n* {data_label} passed {normality_checks_passed}/3 normality checks *\n"
            f"{shapiro_result}"
            f"{ksquare_result}"
            f"{ks_result}"
        )
    return summary


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
            "\n    Conclusion: the variances of the samples are sufficiently different\n"
            % (test_stat_variance, p_value_variance)
        )
    else:
        variance_result = (
            f"\n \033[1m Levenes Equality of Variances Test: (test_stat=%.3f, p=%.4f < α={alpha})"
            "\033[0m"
            "\n    Conclusion: the variances of the samples are likely the same\n"
        )
    return variance_result


def main():
    # file structure:
    # >/PROG_NAME
    # -->output_summary.txt
    # -->/Graphics
    # ---->Histogram.png
    # ---->Q-Q Plot

    data = np.random.normal(1, 50, 325)
    data_1 = np.random.normal(3, 60, 234)

    # txt_summary = "/stats_output/output.txt"
    # save_path = "/Users/christopher/Desktop"  # make this user input
    # path = os.path.join(save_path, txt_summary)
    # os.makedir(path)
    # sys.stdout = open(path, "w")

    non_graphical_options = ["shapiro-wilks", "k-squared", "kolmogorov-smirnov"]
    graphical_options = ["histogram", "qq-plot"]

    print("\nStatistical Assumption Checker - Christopher Blakeney")

    print("\nInitialising...")

    print(check_normality(data, "group 1", non_graphical_options))
    print(check_normality(data_1, "group 2", non_graphical_options))
    print(check_variance_equality(data, data_1))

    # sys.stdout.close()


if __name__ == "__main__":
    main()
