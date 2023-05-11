import numpy as np
from scipy import stats

# custom hypy modules
import assumption_checks as assump
import hypy_supfunc as sup


def ttest(group_1, group_2, assump_tests=[], test_type=[]):
    ttest_dict = {
        "two-tailed": {
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
        },
        "one-tailed": {
            "t": 0.0,
            "p": 0.0,
            "conclusion": False,
            "interpretation": "",
        },
    }
    # returns dict of all stat test results
    g_1 = assump.check_normality(group_1, "group1", assump_tests)
    g_2 = assump.check_normality(group_2, "group2", assump_tests)

    # count number of tests passed
    g1_norm_count = 0
    g2_norm_count = 0

    for test in assump_tests:
        if g_1[test]["conclusion"]:
            g1_norm_count += 1
        if g_2[test]["conclusion"]:
            g2_norm_count += 1

    if g1_norm_count == 2 and g2_norm_count == 2:
        for t in test_type:
            if t in ("two-tailed", "one-tailed"):
                print("hey")
                ttest_stat, p_value_ttest = stats.ttest_ind(group_1, group_2)
                ttest_dict[t]["t"] = ttest_stat
                if t == "two-tailed":
                    ttest_dict[t]["p"] = p_value_ttest
                    sup.test_p_value(p_value_ttest, "two-tailed", ttest_dict)
                else:
                    ttest_dict[t]["p"] = float(p_value_ttest) / 2
                    sup.test_p_value(ttest_dict[t]["p"], "one-tailed", ttest_dict)

    return ttest_dict


# generate normal data
data1 = np.random.normal(1, 500, 345)
data2 = np.random.normal(2, 400, 350)

assumptions = [
    "shapiro-wilks",
    "k-squared",
    "kolmogorov-smirnov",
    # "levenes",
    # "bartletts",
]

ttest_dict = ttest(data1, data2, assumptions, ["one-tailed"])
print(ttest_dict)
