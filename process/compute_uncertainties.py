import numpy as np
from matplotlib import pyplot as plt

raw_ns = np.load("computed_objects/ns.npz")
nss = raw_ns['nss']
fs = raw_ns['fs']
ns_pdfs = raw_ns['ns_pdfs']
ns_pdfs_errors = raw_ns['ns_pdfs_errors']

# )) Compute the 95% uncertainties ))
print("# Constructing 95 perct. uncertainty")
def percentile_ns(xarr, yarr, percentile=0.5):
    # normalization
    norm = np.trapz(yarr, xarr)
    yarr = yarr/norm

    previous_v = 0

    for k in range(1,xarr.shape[0]):
        xx = xarr[:k]
        yy = yarr[:k]
        v = np.trapz(yy, x=xx)

        if v >= percentile:
            perc_n = (percentile - previous_v) * (xarr[k] - xarr[k-1]) / (v - previous_v) + xarr[k-1] # Linear interpolation
            return perc_n

lower_uncertainties = []
upper_uncertainties = []
for ns_pdf in ns_pdfs:
    perc_0025 = percentile_ns(nss, ns_pdf, percentile=0.025)
    perc_0975 = percentile_ns(nss, ns_pdf, percentile=0.975)

    lower_uncertainties.append(perc_0025)
    upper_uncertainties.append(perc_0975)

    # Visual check percentile position
    plt.plot(nss, ns_pdf)
    plt.xscale("log")
    #plt.scatter(nss, ns_pdf, marker="x", color="r")
    plt.vlines(perc_0025,ymin=ns_pdf.min(), ymax=ns_pdf.max(), color="k")
    plt.vlines(perc_0975,ymin=ns_pdf.min(), ymax=ns_pdf.max(), color="k")

plt.title("$n_s$ Probability Density Function\nBlack lines indicate 95% confidence interval")
plt.xlabel("$n_s$")
plt.ylabel("$p_{n_s}(n_s)$")
plt.show()

print("# Saving uncertainties")
np.savez("computed_objects/uncertainties", fs=fs, nss=nss, lower_uncertainties=lower_uncertainties, upper_uncertainties=upper_uncertainties)