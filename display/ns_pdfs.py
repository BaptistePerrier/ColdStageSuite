import numpy as np
from matplotlib import pyplot as plt

raw_ns = np.load("computed_objects/ns.npz")
nss = raw_ns['nss']
ns_pdfs = raw_ns['ns_pdfs']
ns_pdfs_errors = raw_ns['ns_pdfs_errors']

for ns_pdf in ns_pdfs:
    plt.plot(nss, ns_pdf)

plt.title("$n_s$ Probability Density Function for each experimentally observed f\nBlack lines indicate 95% confidence interval")
plt.xlabel("$n_s$")
plt.ylabel("$p_{n_s}(n_s)$")
plt.show()