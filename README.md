# HyPy
>A program to help you conduct hypothesis tests from the command line.

Working with samples of data requires decisions, one of the most pertinent being the use of parametric or nonparametric statistical methods.

### Parametric statistical methods
assumes that the data has a known and specific distribution (often a normal, or gaussian distribution; a bell-shaped curvature with symmetry about the mean.

### Nonparametric statistical methods
must be used when the data is not gaussian (or normally distributed)

If methods are used that assume a normal distribution, and your data sample was from a different distribution type, then findings may be misleading or incorrect. It is important to note that the distribution can be normal enough to satisfy the use of parametric methods, or non-normal data can be transformed into this "normal-enough" status for use with parametric methods.

So, how do we figure out if our sample data is normally distributed? We attempt to satisfy this assumption of normality through various tests. 

Two common types of techniques exist for evaluating the shape of a distribution.
**Graphical**:
	- plot the data points graphically and interpret them to determine normality 
		- histogram
		- Quartile-Quartile (Q-Q) plot
**Statistical**:
	- a calculation used to quantify the probability of the data in question existing within a normal distribution
