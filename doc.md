# Monte Carlo uncertainties simulation

According to *Harrison et al. 2016 ([DOI](https://www.example.com))*, the uncertainties are computed as described in section **4. Experimental methods and data analysis**. This section is inspired from *Wright, Petters 2013, ([DOI]( https://doi.org/10.1002/jgrd.50365))*, Table 1 (**3. Results**) and Table 2 (**Appendix A**) for simulating distribution of active sites in droplets, and simulating freezing of droplets.

## Physical Hypothesis

This uncertainties evaluation makes the *singular hypothesis* assumption (cf *Vali 2014* ([DOI](https://doi.org/10.5194/acp-14-5271-2014))) : the heterogenous freezing is time-independant, thus only depends on caracteristic temperatures associated with nucleation sites. To reformulate it, on each site the water is considered liquid at temperatures above the caracteristic temperature of the site, and once the temperatures gets lower than that temperature, the water is immediately considered frozen.

Assuming an uniform repartition of the surface area among the droplets, the poisson distribution of frozen droplets is given by :

&nbsp;&nbsp;&nbsp;&nbsp; $f = \frac{n(T)}{N_{tot}} = 1 - e^{-\mu(T)} = 1 - e^{-n_s(T) A}$

With :
- $n(T)$ the number of frozen droplets at a temperature $T$
- $N_{tot}$ the total number of droplets in the experiment
- $\mu$ the number of sites available per droplet
- $n_s$ the Ice Nucleation Active Site (INAS) density in $m^{-2}$
- $A = S_p C V$ the area available per droplet in $m^2$. $S_p$ is the specific surface of the powder in $m^2g^{-1}$, $C$ the concentration in $gL^{-1}$, and $V$ the volume of a droplet in $L$

By inverting this equation we have :

&nbsp;&nbsp;&nbsp;&nbsp; $n_s = -\frac{ln(1 - f)}{A}$

And as we can experimentally mesure $f$, we can obtain $n_s$


## Overview of the algorithm

We will generate data to figure out which values of $\mu$ can explain the $n_s$ value observed experimentally. We then have a probability density for $\mu$, we have a probability density for $A$ and we know $n_s = \frac{\mu}{A}$, we can then deduce the probability density for $n_s$.

It is important to note that the uncertainties computed are valid as long as the singular hypothesis is valid in the experiment. Whithout singular hypothesis the uncertainties don't have any meaning.

To reformulate : We know that a single value of $f$ (and thus $n_s$) can be obtained via different average active sites number per droplet $\mu$. We compute the probability for each $\mu$ to give a given $f$. We also have a probability density for the value of $A$. Knowing that $n_s = \frac{\mu}{A}$, we can deduce its probability density.

Once we have a probability density for $n_s$ we can compute the 95 % confidence interval of this distribution.

## Generating $f$- $\mu$ distribution
We run simulations with different values of $\mu$ to see what frozen fraction is the most likely to happen.

Let $\mu$ be fixed to an arbitrary value. We have a droplet array of `DROPLET_NUMBER`. We estimate the number of active site in each droplet via a poisson law of parameter $\mu$ :

&nbsp;&nbsp;&nbsp;&nbsp; $N_{site, i} = X_{\mathcal{P}}(\mu)$

Then, we consider frozen each droplet that has one or more active site in it (ie $N_{site,i} \geq 1$). The frozen fraction is then computed by $f = \frac{N_{frozen}}{N_{tot}}$.

We have one point of data : for this given $\mu$ value, the simulation yielded a frozen fraction  $f$.

We repeat the simulation `MU_REPETITION` times to see the most probable distribution of $\mu$ for each $f$ appear.

## Generating $A$ distribution

$A$ is assumed to have a gaussian distribution, being the result of uncertainties propagation.

We have $A = S_pCV$, whose uncertainties respectively equal $u(S_p)$, $u(C)$ and $u(V)$. Then propagating the uncertainties give :

&nbsp;&nbsp;&nbsp;&nbsp; $\frac{u(A)}{|A|} = \sqrt{\left( \frac{u(S_p)}{S_p} \right)^2 + \left( \frac{u(C)}{C} \right)^2 + \left( \frac{u(V)}{V} \right)^2}$

&nbsp;&nbsp;&nbsp;&nbsp; $A \sim \mathcal{N}(A, u(A))$

## Computing $n_s$ distribution
For a fixed $f$ we know the probability distribution of $\mu$ and those of $A$. We can deduce the probability distribution of $n_s = \frac{\mu}{A}$. This is a "*Ratio Distribution*" (cf [Wiki](https://en.wikipedia.org/wiki/Ratio_distribution)) and can be calculated as follows for our two independant variables :

&nbsp;&nbsp;&nbsp;&nbsp; $p_{n_s}(n_s) = \int_{-\infty}^{+\infty} |A|~p_\mu(n_sA)p_A(A)~dA$

*NB : The integral is computed between `0` and `1e-6` for the integration algorithm to converge. With `-np.inf` and `np.inf` the integration yields zero systematically.*

## Retrieving confidence interval
For each fixed $f$ we then have a probability distribution for possible $n_s$ explaining the frozen fraction (according to singular hypothesis). We must now find the 2,5-th and 97,5 quantiles; everything that lies between them belongs to the 95% confidence interval.

This is made by computing the *Cumulative Distribution Function* via trapezoïdal integration. As the resolution of $n_s$ distribution is finite, we use a linear interpolation of the CDF to yield the 2,5 and 97,5 quintiles.

## Going further
This procedure makes the strong (and false) hypothesis that the freezing process is time-independant. We need to use a stochastic approach for simulations to include this time dependance.