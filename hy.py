#!/usr/bin/env python3

# external libraries
import argparse
from pathlib import Path
import csv

# delete - only used for test data generation
import numpy as np

# hypy modules
import supfunc as sup  # suplimentary functions
import assumption_checks as assump  # statistical assumptions tests
import stats_tests as st  # statistical tests

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""


class Documentation:
    improper_csv_format = "the input .csv file is not correctly formatted for your test selection. Please see here for formatting guidelines: LINK"
    no_popmean = "you must provide a population mean if conducting a one-sample t-test"


def main():
    # TEST DATA
    # Groups with Unequal Variance
    group1 = np.random.normal(0.5, 15, 100)
    group2 = np.random.normal(0.75, 5, 100)

    # Groups with Equal Variance
    group3 = np.random.normal(1, 5, 100)
    group4 = np.random.normal(0.25, 5, 100)

    # import docs
    docs = Documentation()
    # CLI
    parser = argparse.ArgumentParser(
        prog="hypy",
        description="perform hypothesis tests from the command line.",
        epilog="Developed by Christopher Blakeney",
    )
    # basic output
    basic = parser.add_argument_group("primary input")
    basic.add_argument(
        "csvfile",
        help="csv file containing sample data. Please format .csv file according to README.md",
    )
    basic.add_argument(
        "test",
        action="store",
        default="t-one",
        choices=["assump-one", "assump-two", "t-one", "t-two"],
        help="choose between a t-test assumption check or a traditional t-test, each for either one or two samples",
    )
    # basic.add_argument("csv_column", help="column for sample 1 from spcified csv file")
    basic.add_argument("savepath", default="none", help="statistical output save path")

    # test options
    test = parser.add_argument_group("test specific")
    test.add_argument(
        "-o",
        "--onetail",
        action="store_true",
        default=False,
        help="change t-test to a one-tailed test, defaults to two-tailed if no input is presented",
        required=False,
    )
    test.add_argument(
        "-m",
        "--mean",
        action="store",
        default=0,
        type=float,
        help="if using t-one, provide population mean of which to compare sample data",
        required=False,
    )

    # auxilary options
    parser.add_argument(
        "-s",
        "--showdata",
        action="store_true",
        default=False,
        help="print the first 10 data points from each sample to the console",
    )

    args = parser.parse_args()
    csvfile = args.csvfile
    test_type = args.test
    popmean = args.mean
    one_tail = args.onetail
    save_path = Path(args.savepath)

    if one_tail:
        tail_type = "one-tailed"
    else:
        tail_type = "two-tailed"

    # get column (sample) names from input csv file
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        col_list = []
        for row in csv_reader:
            col_list.append(row)
            break

    # deal with errors and improper usage
    if save_path != "none":
        csv_pass = False
        if test_type in ["t-one", "assump-one"]:
            # set data label for sample one
            try:
                s1_label = col_list[0][0]
                # import data
                s1 = sup.import_csv_column(csvfile, s1_label, float)
                csv_pass = True
            except IndexError:
                print(docs.improper_csv_format)
            if csv_pass:
                # one sample ttest and assumption check
                assump_dict, ttest_dict, nr, vr, summary_str = st.ttest(
                    group1, None, [s1_label], 1, "one-sample", tail_type
                )
                # build directory
                parent_dir, a_dir, figs_dir, stats_dir = sup.build_hypy_directory(
                    save_path
                )
                # export assumption checks
                sup.export_dict_png(
                    assump_dict,
                    False,
                    "Assumption Checks",
                    [s1_label],
                    stats_dir,
                    300,
                    False,
                )
                # export figures
                assump.check_normality(
                    group1,
                    s1_label,
                    [],
                    ["histogram", "qq-plot"],
                    figs_dir,
                    300,
                )
                # export assumption summary
                sup.export_assump_summary(a_dir, summary_str)
            if test_type == "t-one" and popmean != 0 and nr:
                # one sample t-test
                # add ttest path
                ttest_dir = sup.build_testdir(parent_dir, "ttest")
                # export ttest as png
                sup.export_dict_png(
                    ttest_dict["one-sample"],
                    False,
                    "One Sample T Test",
                    [s1_label],
                    ttest_dir,
                    300,
                    False,
                )
            elif test_type == "t-one" and popmean == 0:
                print(docs.no_popmean)
        elif test_type in ["t-two", "assump-two"]:
            # set data labels
            try:
                s1_label = col_list[0][0]
                s2_label = col_list[0][1]
                s1 = sup.import_csv_column(csvfile, s1_label, float)
                s2 = sup.import_csv_column(csvfile, s2_label, float)
                csv_pass = True
            except IndexError:
                print(docs.improper_csv_format)
                SystemExit(1)
            if csv_pass:
                # two sample t-test and two-sample assumption check
                assump_dict, ttest_dict, nr, vr, summary_str = st.ttest(
                    group3, group4, [s1_label, s2_label], 0, "two-sample", tail_type
                )
                # build directory
                parent_dir, a_dir, figs_dir, stats_dir = sup.build_hypy_directory(
                    save_path
                )
                # export assumption checks
                sup.export_dict_png(
                    assump_dict,
                    True,
                    "Assumption Checks",
                    [s1_label, s2_label],
                    stats_dir,
                    300,
                    True,
                )
                # export figures
                assump.check_normality(
                    s1,
                    s1_label,
                    [],
                    ["histogram", "qq-plot"],
                    figs_dir,
                    300,
                )
                assump.check_normality(
                    s2,
                    s2_label,
                    [],
                    ["histogram", "qq-plot"],
                    figs_dir,
                    300,
                )
                # export assumption summary
                sup.export_assump_summary(a_dir, summary_str)
                # if ttest
                if test_type == "t-two" and nr and vr:
                    # add ttest path
                    ttest_dir = sup.build_testdir(parent_dir, "ttest")
                    # export ttest as png
                    sup.export_dict_png(
                        ttest_dict["two-sample"],
                        False,
                        "Two Sample T Test",
                        [s1_label, s2_label],
                        ttest_dir,
                        300,
                        False,
                    )


if __name__ == "__main__":
    main()
