README 

Working with samples of data requires decisions, one of the most pertinent being the use of parametric or nonparametric statistical methods.

Parametric statistical methods
	- assumes that the data has a known and specific distribution (often a normal, or gaussian distribution; a bell-shaped curvature with symmetry about the mean.

Nonparametric statistical methods
	- must be used when the data is not gaussian (or normally distributed)

If methods are used that assume a normal distribution, and your data sample was from a different distribution type, then findings may be misleading or incorrect. It is important to note that the distribution can be normal enough to satisfy? the use of parametric methods, or non-normal data can be transformed into this "normal-enough" status for use with parametric methods.

So, how do we figure out if our sample data is normally distributed? We attempt to satisfy this assumption of normality through various tests. 

If data is sufficiently normal:
	use parametric statistical methods
else:
	use nonparametric statistical methods

Two common types of techniques exist for evaluating the shape of a distribution.
Graphical:
	- plot the data points graphically and interpret them to determine normality 
		- histogram
			- data is divided into a pre-specified number of groups (bins) where data is sorted into each bin and the 			number of data points in each is counted. The ordinal data for each bin is retained on the x-axis, while the 			number of data points contained within each bin is represented on the y-axis.
		- Quartile-Quartile (Q-Q) plot
			- this graphical test generates a new sample of data that is perfectly normally distributed and compares our 			data points to it. The ideal normal distribution is represented by the x-axis, while our data is on the y-			axis. A perfect match with the idea distribution will be represented by a line of dots at a 45-degree angle 			from bottom-left to top-right. There will be more variation about this 45º angle if the sample size is 				relatively small.
Statistical tests:
	- a calculation used to quantify the probability of the data in question existing within a normal distribution
	- Each of these tests assumes that the data you are testing comes from a normal distribution. Hence, the default or "null" 	hypothesis (H0) would be: "This data is normally distributed". Each test will provide a test-statistic (t) and a p-value (p), 	used to reject or accept this default hypothesis. Specifically, if p < alpha (usually 0.05), we reject the null hypothesis 	and state that the distribution is not normal. Alternatively, if p > 0.05, we fail to reject the null hypothesis that the 	data is normally distributed. 

A small disclaimer, a result above alpha = 0.05 does not confirm that the null hypothesis is true and our result is beyond reproach. It simply means that the result is very likely true given the available data points.

- Shapiro-Wilks Test
	- a reliable test of normality suitable for smaller data samples (1000 observations or less).