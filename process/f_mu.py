import numpy as np
from matplotlib import pyplot as plt

rng = np.random.default_rng()

DROPLETS_NUMBER = 200 # f resoltion
MU_REPETITION = 5000 # statistical convergence
MU_RESOLUTION = 200 # mu resolution
# )) Constructing f-µ distribution )) #

print("# Constructing f-µ distribution")

mus = np.logspace(-3,1, MU_RESOLUTION)
fs = np.array([0])
f_mu = np.zeros((mus.shape[0], fs.shape[0]))

# Not using np functions to generate MU_REPETITIONS at the same time to avoid memory overload
for repetition_i in range(MU_REPETITION):
    # Generate distribution of active sites among droplets for a given mu
    Nsites = rng.poisson(lam=mus, size=(DROPLETS_NUMBER, MU_RESOLUTION))
    # Computes the frozen fraction of the above distributions of sites
    frozenFractions = (Nsites >= 1).sum(axis=0) / DROPLETS_NUMBER

    for frozenFraction in frozenFractions:
        if not frozenFraction in fs:
            fs = np.append(fs, frozenFraction)
            fs.sort()

            f_i = np.where(fs == frozenFraction)[0]
            f_mu = np.insert(f_mu, f_i, np.zeros((mus.shape[0], 1)), axis=1)
        
    for mu_i in range(mus.shape[0]):
        frozenFraction = frozenFractions[mu_i]
        f_i = np.where(fs == frozenFraction)[0]

        f_mu[mu_i, f_i] += 1

# Normalization to yield a PDF
mu_integrations = np.trapz(f_mu, x=mus, axis=0)
f_mu = f_mu / mu_integrations

# Check if normalization went ok
#mu_integrations = np.trapz(f_mu, x=mus, axis=0)
#print(mu_integration)

print("# Saving f-µ distribution")
np.savez("computed_objects/f_mu", fs=fs, mus=mus, f_mu=f_mu) 