#!/usr/bin/env python3

# external libraries
import argparse
from pathlib import Path
import csv

# hypy modules
import supfunc as sup  # suplimentary functions
import assumption_checks as assump  # statistical assumptions tests
import stats_tests as st  # statistical tests

__author__ = "Christopher J. Blakeney"
__version__ = "0.1.0"
__license__ = ""


def main():
    # CLI
    parser = argparse.ArgumentParser(
        prog="hypy",
        description="perform statistical analysis and hypothesis tests from the command line.",
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
        choices=["assump", "t-one", "t-two"],
        help="choose between a t-test assumption check, one-sample or a two independent samples t-test",
    )
    # basic.add_argument("csv_column", help="column for sample 1 from spcified csv file")
    basic.add_argument("savepath", help="statistical output save path")

    # test options
    test = parser.add_argument_group("test specific")
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
    save_path = Path(args.savepath)

    # deal with errors and improper usage
    if test_type == "t-one" and popmean == 0:
        print("you must provide a population mean if conducting a one-sample t-test")

    # get column (sample) names from input csv file
    with open(csvfile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        col_list = []
        for row in csv_reader:
            col_list.append(row)
            break
    s1_label = col_list[0][0]
    s2_label = col_list[0][1]

    s1 = sup.import_csv_column(csvfile, s1_label, float)
    s2 = sup.import_csv_column(csvfile, s2_label, float)

    print(s1, s2)


if __name__ == "__main__":
    main()
