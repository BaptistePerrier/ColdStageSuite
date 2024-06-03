import numpy as np
from matplotlib import pyplot as plt

raw_ns = np.load("computed_objects/ns.npz")
nss = raw_ns['nss']
ns_pdfs = raw_ns['ns_pdfs']
ns_pdfs_errors = raw_ns['ns_pdfs_errors']

plt.title("Relative errors during $n_s$-pdf integration")
for ns_i in range(ns_pdfs.shape[0]):
    relErr = ns_pdfs_errors[ns_i] / ns_pdfs[ns_i]
    plt.plot(nss, relErr)

plt.yscale("log")
plt.show()