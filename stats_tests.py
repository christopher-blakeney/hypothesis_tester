import numpy as np
from scipy import stats

# custom hypy modules
import assumption_checks as assump
import supfunc as sup


def ttest(
    group_1,
    group_2,
    data_labels=[],
    pop_mean=0,
    test_type="",
    tail_type="",
):
    # keep track of assumption pass / fail
    normal_r = True
    variance_r = True

    ttest_dict = {
        "one-sample": {
            "tail": ["two-tailed"],
            "t": [0.0],
            "p": [0.0],
            "conclusion": [False],
            "interpretation": [""],
        },
        "two-sample": {
            "tail": ["two-tailed"],
            "t": [0.0],
            "p": [0.0],
            "conclusion": [False],
            "interpretation": [""],
        },
    }

    # first, check all required assumptions to know if we can conduct T test
    normal_tests = ["shapiro-wilks", "k-squared"]
    variance_tests = ["bartletts", "levenes"]
    assumption_dict = {}

    # one-sample
    norm_tests_dict = assump.check_normality(group_1, data_labels[0], normal_tests)
    s1_norm_test_counter = 0
    s2_norm_test_counter = 0
    variance_test_counter = 0
    fail_count = 0
    assumption_dict["s1 normality tests"] = norm_tests_dict
    summary_str = ""

    failed_output = "NO T-TEST CONDUCTED: input data did not satisfy assumptions of normality/equal variance. Please consider transforming your data or using nonparametric statistical methods. Assumption test summary placed in save path."

    # if assumptions are met, continue with test, if not, print failure
    for test in assumption_dict["s1 normality tests"]:
        if assumption_dict["s1 normality tests"][test]["conclusion"]:
            s1_norm_test_counter += 1
    if s1_norm_test_counter == len(assumption_dict["s1 normality tests"]):
        # conduct one-sample t-test
        if test_type == "one-sample" and pop_mean != 0:
            o_stat, o_p_value = stats.ttest_1samp(group_1, pop_mean)
            ttest_dict["one-sample"]["t"] = o_stat
            if tail_type == "two-tailed":
                ttest_dict["one-sample"]["p"] = o_p_value
                sup.test_p_value(o_p_value, "one-sample", ttest_dict)
            else:
                ttest_dict["one-sample"]["tail"] = "one-tailed"
                ttest_dict["one-sample"]["p"] = float(o_p_value) / 2
                sup.test_p_value(
                    ttest_dict["one-sample"]["p"], "one-sample", ttest_dict
                )
            normal_r = True
            norm_str = (
                "REJECTED\n Consequently, no t-test was carried out for this data."
            )
            if normal_r:
                norm_str = (
                    f"ACCEPTED\n Consequently, a one-sample t-test was carried out on this data...\n"
                    f"The results of this one-sample t-test showed that {data_labels[0]} likely comes from\n"
                    f"the same test population, given its mean: {pop_mean}."
                )
            summary_str = (
                f"A one-sample t-test was attempted comparing {data_labels[0]} and {pop_mean}.\n"
                f"The assumption of normality was tested for {data_labels[0]} using the following statistical tests:\n"
                f"- {normal_tests}\n"
                f"Based on the results of these normality tests, the assumption of distributive normality was {norm_str}"
            )
    elif test_type == "one-sample" and pop_mean == 0:
        print("Please provide a population mean of which to compare your sample")
    else:
        print(">  Normality assumption failed")
        fail_count += 1
        normal_r = False
        SystemExit(1)

    # two-sample
    if test_type == "two-sample":
        # create second dict entry for group 2 normality tests
        assumption_dict["s2 normality tests"] = assump.check_normality(
            group_2, data_labels[1], normal_tests
        )
        variance_tests_dict = assump.check_variance_equality(
            group_1, group_2, variance_tests
        )
        assumption_dict["homogeneity of variance tests"] = variance_tests_dict

        for n_test in assumption_dict["s2 normality tests"]:
            if assumption_dict["s2 normality tests"][n_test]["conclusion"]:
                s2_norm_test_counter += 1
        for v_test in assumption_dict["homogeneity of variance tests"]:
            if assumption_dict["homogeneity of variance tests"][v_test]["conclusion"]:
                variance_test_counter += 1
        if (
            s2_norm_test_counter == len(assumption_dict["s2 normality tests"])
            and s1_norm_test_counter == len(assumption_dict["s1 normality tests"])
            and variance_test_counter
            == len(assumption_dict["homogeneity of variance tests"])
        ):
            # conduct ttest
            t_stat, t_p_value = stats.ttest_1samp(group_1, pop_mean)
            ttest_dict["two-sample"]["t"] = t_stat
            if tail_type == "two-tailed":
                ttest_dict["two-sample"]["p"] = t_p_value
                sup.test_p_value(t_p_value, "two-sample", ttest_dict)
            else:
                ttest_dict["two-sample"]["tail"] = "one-tailed"
                ttest_dict["two-sample"]["p"] = float(t_p_value) / 2
                sup.test_p_value(
                    ttest_dict["two-sample"]["p"], "two-sample", ttest_dict
                )
        else:
            print(">  Equal variances assumption failed")
            fail_count += 1
            variance_r = False
            SystemExit(1)
    # change dict names for output
    sup.change_dict_key(assumption_dict, "s1 normality tests", data_labels[0].title())
    if test_type == "two-sample":
        sup.change_dict_key(
            assumption_dict, "s2 normality tests", data_labels[1].title()
        )
    sup.change_dict_key(
        assumption_dict, "homogeneity of variance tests", "Variance Equality"
    )

    if fail_count == 2:
        print(failed_output)

    return assumption_dict, ttest_dict, normal_r, variance_r, summary_str
