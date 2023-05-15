import numpy as np
from scipy import stats

# custom hypy modules
import assumption_checks as assump
import hypy_supfunc as sup


def ttest(
    group_1,
    group_2,
    data_labels=[],
    pop_mean=0,
    test_type="",
    tail_type="",
):
    ttest_dict = {
        "one-sample": {
            "tail": "two-tailed",
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
        },
        "two-sample": {
            "tail": "two-tailed",
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
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
    assumption_dict["s1 normality tests"] = norm_tests_dict

    failed_output = (
        f"input data did not meet normailty and/or homogeneity of variance assumptions."
        f"a ttest is not appropriate for this data, please consider transforming your data or using"
        f"nonparametric statistical methods"
    )

    # if assumptions are met, continue with test, if not, print failure
    for test in assumption_dict["s1 normality tests"]:
        if test[3]:
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
    elif test_type == "one-sample" and pop_mean == 0:
        print("Please provide a population mean of which to compare your sample")
    else:
        print(failed_output)
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

        for norm_test in assumption_dict["s2 normality tests"]:
            if norm_test[3]:
                s2_norm_test_counter += 1
        for var_test in assumption_dict["homogeneity of variance tests"]:
            if var_test[3]:
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
            print(failed_output)

    return assumption_dict, ttest_dict


# generate normal data
data1 = np.random.normal(1, 500, 345)
data2 = np.random.normal(2, 400, 350)

assump_dict, ttest_dict = ttest(
    data1, data2, ["frogs", "apples"], 150, "two-sample", "one-tailed"
)
