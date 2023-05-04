def ttest(group_1, group_2, parametric=True, groups=2, paired=False):
    # check all assumptions
    if (
        check_normality(group_1)
        and check_normality(group_2)
        and check_variance_equality(group_1, group_2)
    ):
        print("\n* Assumptions verified *")
    # perform ttest
    print("\nT-Test for Independent Samples")
    ttest, p_value = stats.ttest_ind(group_1, group_2)
    print("p value: %.8f" % p_value)
    print("p value one-sided: %.4f" % (float(p_value) / 2))